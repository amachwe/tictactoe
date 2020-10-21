import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

class Utils(object):
    
    @staticmethod
    def extract_grid(id):
        id = int(id)
        x = 0
        y = 0
        if id in (1,2,3):
            x = 1
            y = id
        elif id in (4,5,6):
            x = 2
            y = id - 3
        elif id in (7,8,9):
            x = 3
            y = id - 6
        
        return x,y

    @staticmethod
    def next_states(current_state, value):
        next_st = []
        results = []
        row_c = 0
        new_sts = 0
        for i in current_state.as_list():
            row_c += 1
            col_c = 0
            for j in i:
                col_c += 1

                if j < 0:
                    new_sts += 1
                    cp = current_state.clone()
                    if value == 0:
                        cp.set_naught(row_c, col_c)
                    elif value == 1:
                        cp.set_cross(row_c, col_c)
                    
                    next_st.append(cp)
                    results.append(cp.check_result())
        
        if new_sts == 0:
            return [], -1
        
        return next_st, results
    
class TicTacToe(object):
    
    
    def __init__(self, np_arr=None):
        self.__EMPTY__ = -3
        if np_arr is not None:
            self.grid = np_arr
        else:
            self.grid = np.full((3,3),self.__EMPTY__)
        
    def clone(self):
        cp = TicTacToe()
        
        cp.grid = np.array(self.grid, copy=True)
        return cp
    
    def hash(self):
        hash=""
        for r in self.grid.tolist():
            for c in r:
                if c == 0:
                    hash = hash + "O"
                elif c == 1:
                    hash = hash + "X"
                elif c == self.__EMPTY__:
                    hash = hash + "_"
            
        return hash
                
        
    def as_list(self):
        return self.grid.tolist()
    
    def as_flat_list(self):
        return self.grid.flatten()
    
    def is_complete(self):
      
        for r in self.grid.tolist():
            for c in r:
                if c == self.__EMPTY__:
                    return False
            
        return True
    
    def set_naught(self,x,y):
        # index starts from 1
        if self.grid[x-1][y-1] == self.__EMPTY__:
            self.grid[x-1][y-1] = 0
        else:
            raise Exception(f"Grid position: {x},{y} already set to {self.grid[x-1][y-1]}")
    
    def set_cross(self,x,y):
        # index starts from 1
        if self.grid[x-1][y-1] == self.__EMPTY__: 
            self.grid[x-1][y-1] = 1
        else:
            raise Exception(f"Grid position: {x},{y} already set to {self.grid[x-1][y-1]}")

    def check_result(self):
        result = -1
        
        def check_sum(sum):
            if sum == 0:
                return True, 0
            elif sum == 3:
                return True, 1
            else:
                return False, -1
            
            
        for i in range(0,3):
            sum = self.grid[i].sum()
            
            result, winner = check_sum(sum)
            
            if result:
                return winner
                
            sum = self.grid[:,i].sum()
            
            result, winner = check_sum(sum)
            
            if result:
                return winner
        sum = 0
        for i in range(0, 3):
            sum += self.grid[i][i]
            
        result, winner = check_sum(sum)
        
        if result:
            return winner
        
        sum = self.grid[0][2]+self.grid[1][1]+self.grid[2][0]
        
        result, winner = check_sum(sum)
        
        if result:
            return winner
        
        return -1
    
    def __test__(self, np_arr):
        self.grid = np_arr
  
    def __str__(self):
        grid = ""
        for r in self.grid:
            for c in r:
                if c == self.__EMPTY__:
                    grid = grid + "  | "
                elif c == 1:
                    grid = grid + "X | "
                elif c == 0:
                    grid = grid + "O | "
            
            grid = grid[:-2]
            grid = grid + "\n----------\n"
        grid = grid[:-len("\n----------")]
        
        return grid

    def draw_with_grid(self):
        grid = ""
        id = 1
        for r in self.grid:
            for c in r:
                if c == self.__EMPTY__:
                    grid = grid + f"{id} | "
                else:
                    grid = grid + "* | "
                
                id += 1
            grid = grid[:-2]
            grid = grid + "\n----------\n"
        grid = grid[:-len("\n----------")]
        
        return grid
        