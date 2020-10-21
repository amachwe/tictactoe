#!/usr/bin/env python
# coding: utf-8

# In[65]:


import tensorflow as tf
import numpy as np


# In[104]:


class TicTacToe(object):
    
    def __init__(self):
        self.grid = np.full((3,3),-3)
        
    def clone(self):
        cp = TicTacToe()
        
        cp.grid = np.array(self.grid, copy=True)
        return cp
        
    def as_list(self):
        return self.grid.tolist()
    
    def as_flat_list(self):
        return self.grid.flatten()
    
    def set_naught(self,x,y):
        # index starts from 1
        self.grid[x-1][y-1] = 0
    
    def set_cross(self,x,y):
        # index starts from 1
        self.grid[x-1][y-1] = 1
    
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
                
            sum = self.grid[:][i].sum()
            
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
  
    def __str__(self):
        return self.grid.__str__()
        


# In[105]:


def next_states(current_state, value):
    next_st = []
    results = []
    row_c = 0
    for i in current_state.as_list():
        row_c += 1
        col_c = 0
        for j in i:
            col_c += 1
            
            if j < 0:
                cp = current_state.clone()
                if value == 0:
                    cp.set_naught(row_c, col_c)
                elif value == 1:
                    cp.set_cross(row_c, col_c)
               
                next_st.append(cp)
                results.append(cp.check_result())
                
    return next_st, results
    


# In[107]:

CROSS = 1
NAUGHT = 0

COMPUTER = CROSS
ttt = TicTacToe()
print(ttt)
print(next_states(ttt,1))


# In[ ]:

# In[]





