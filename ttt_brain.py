from module import TicTacToe, Utils
import networkx as nx
import operator


class PatternBrain(object):
    ## Pattern based Computer player
    def __init__(self, computer_value=0):
        print("Brain online")
        self.computer_value = computer_value
        self.other_value = 1

        if computer_value == 1:
            self.other_value = 0
        
        self.win_pattern = self.prep_pattern(self.computer_value)
        self.loss_pattern = self.prep_pattern(self.other_value)
    
    def play(self, grid):
        states, res = Utils.next_states(grid, self.computer_value)
        
        nx = {
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:0,
            7:0,
            8:0,
            9:0
        }

        grid_ref = None

        for l_pt in self.loss_pattern:
                cnt = 0
                gap = 0
            
                for i in range(0, len(grid.as_flat_list())):
                    n = grid.as_flat_list()[i]
                    l = l_pt[i]
                    
                    if l >= 0:
                        if l == n:
                            cnt += 1
                        elif  n == grid.__EMPTY__:
                            gap += 1
                            grid_ref = i+1
                            
                            
                #print(l_pt, grid.as_flat_list(), gap, cnt)        
                   
                if cnt == 2 and gap == 1:
                    
                    print("Danger: ", grid_ref)
                    break

        if grid_ref == None:
            for i in states:
                
                n_pt = i.as_flat_list()
                
                for w_pt in self.win_pattern:
            
                    for i in range(0, len(n_pt)):
                        n = n_pt[i]
                        w = w_pt[i]
                        
                        if w >= 0:
                            if w == n:
                                nx[i+1] += 1
                            elif n!=w and n < 0:
                                nx[i+1] += 2
                            elif n != w:
                                nx[i+1] -= 5

            
        
        id = 1
        for i in grid.as_flat_list():
            if i != grid.__EMPTY__:
                del nx[id]
            id +=1
        
        if not grid_ref:
            grid_ref = max(nx.items(), key=operator.itemgetter(1))[0]

        #print("Weights: ", nx)
        print("Chosen grid reference: ", grid_ref,"\n")

        if self.computer_value == 0:
            grid.set_naught(*Utils.extract_grid(grid_ref))
        else:
            grid.set_cross(*Utils.extract_grid(grid_ref))

        return grid

    def prep_pattern(self, v):
        return [[v,v,v,-3,-3,-3,-3,-3,-3],
        [-3,-3,-3,v,v,v,-3,-3,-3],
        [-3,-3,-3,-3,-3,-3,v,v,v],
        [v,-3,-3,v,-3,-3,v,-3,-3],
        [-3,v,-3,-3,v,-3,-3,v,-3],
        [-3,-3,v,-3,-3,v,-3,-3,v],
        [v,-3,-3,-3,v,-3,-3,-3,v],
        [-3,-3,v,-3,v,-3,v,-3,-3],        
        ]




class InductionBrain(object):
    ## Induction brain
    def __init__(self):
        print("Brain online")
        self.__LIMIT__ = None
        
        
    def play(self, grid):
        
        edges = self.graph.edges(hash(grid.hash()))
        wnr = 0
        nex = 0
        for e in edges:
            _d = self.graph.get_edge_data(*e)
            _from = e[0]
            _to = e[1]
            num = _d.get("win", 0)

            if num == 0:
                num = _d.get("draw",0)

                
            _wnr = num/(_d.get("loss",0)+1)
            print("Option: ",_wnr,"   ",_to,"\n",self.state[_to])  
            if _wnr > wnr:
                wnr = _wnr
                nex = _to
                
        
        return self.state[nex]
    
    def train(self, starting_value=0, computer_value=0):

            
        self.graph = nx.DiGraph()
        try:
            if open("ttt.gph", "r"):
                print("Found saved data...")
                self.graph = nx.read_gpickle("ttt.gph")
                return
        except:
            pass
        self.state = {}
        self.id_map = {}
        self.win_term_id = set()
        self.loss_term_id = set()
        self.draw_term_id = set()
        base = TicTacToe()
        
        _h = hash(base.hash())
        self.id_map[base.hash()] = _h
        self.state[_h]=base
        
        self.graph.add_node(_h)
        
        other_value = 1
        if computer_value == 1:
            other_value = 0
        
        
            
        self.build_graph(base, starting_value, computer_value, other_value, self.__LIMIT__)

        print("Wins:", len(self.win_term_id), "Loss:", len(self.loss_term_id), "Draw:",len(self.draw_term_id))
        self.back_prop_wts()

        print(f"Done  States: {len(self.id_map)}\t{len(self.state)}")
        # nx.write_gpickle(self.graph, "ttt.gph")
        # nx.draw(self.graph, with_labels=False)
        # plt.savefig("out.png")
    
    def back_prop_wts(self):
        
        for i in self.win_term_id:
            self.back_prop_wt_win(i, 1)

        for i in self.loss_term_id:
            self.back_prop_wt_loss(i, 1)

        for i in self.draw_term_id:
            self.back_prop_wt_draw(i, 1)

    def back_prop_wt_draw(self, id, draw):

        for e in self.graph.in_edges(nbunch=id):
            if draw:
                draw = draw + 1
                self.graph.get_edge_data(*e)["draw"] = draw
 

            self.back_prop_wt_draw(e[0], draw)

    def back_prop_wt_win(self, id, win):

        for e in self.graph.in_edges(nbunch=id):
            if win:
                win = win + 1
                self.graph.get_edge_data(*e)["win"] = win
 

            self.back_prop_wt_win(e[0], win)

    def back_prop_wt_loss(self, id,  lose):

        for e in self.graph.in_edges(nbunch=id):
       
            if lose:
                lose = lose+1
                self.graph.get_edge_data(*e)["loss"] = lose

            self.back_prop_wt_loss(e[0], lose)



    def build_graph(self, base, value, computer_value, other_value, limit):
        
    
        nxt, res = Utils.next_states(base, value)
        
            
        if limit and limit <= 0:
            return
            
        if value == 0:
            value = 1
        else:
            value = 0
        
        for i,n in enumerate(nxt):
            _h = hash(n.hash())
            self.id_map[n.hash()] = _h
            self.state[_h] = n
            
            wt = 0
            winner = res[i] != -1
            if res[i] == computer_value:
                wt = 100
                self.win_term_id.add(_h)
            
            elif res[i] == other_value:
                wt = -100
                self.loss_term_id.add(_h)

            elif res[i] == -1:
                wt = 0
                if n.is_complete():
                    self.draw_term_id.add(_h)

            self.graph.add_node(_h)
            self.graph.add_edge(hash(base.hash()), _h, w=wt) 
            if winner:
                
                continue
            
            if limit == None:
                self.build_graph(n, value, computer_value, other_value, None)
            else:
                self.build_graph(n, value, computer_value, other_value, limit-1)
        
            
        
    