#!/usr/bin/env python
# coding: utf-8


import numpy as np
from module import Utils, TicTacToe
import ttt_brain
import sys
import argparse

        
    
def check_and_apply(ttt, value, grid_x, grid_y):
    if (grid_x < 1 or grid_x > 3) or (grid_y < 1 or grid_y > 3):
        print("Grid must be within [1, 3]")
        return
    
    if value == 0:
        ttt.set_naught(grid_x, grid_y)
    elif value == 1:
        ttt.set_cross(grid_x, grid_y)
    else:
        print(f"Unknown value {value}, select from 0 or 1")
   


# Tests
def check_stack(i):
    check_win([[i,i,i],[-3,-3,-3],[-3,-3,-3]],i)
    check_win([[-3,-3,-3],[i,i,i],[-3,-3,-3]],i)
    check_win([[-3,-3,-3],[-3,-3,-3],[i,i,i]],i)
    check_win([[i,-3,-3],[i,-3,-3],[i,-3,-3]],i)
    check_win([[-3,i,-3],[-3,i,-3],[-3,i,-3]],i)
    check_win([[-3,-3,i],[-3,-3,i],[-3,-3,i]],i)
    check_win([[i,-3,-3],[-3,i,-3],[-3,-3,i]],i)
    check_win([[-3,-3,i],[-3,i,-3],[i,-3,-3]],i)

def check_win(test_arr, winner):
    ttt = TicTacToe(np_arr=np.array(test_arr))
    
    if ttt.check_result() != winner:
        raise Exception(f"Test Failed, winner expect {winner}, result actual: {ttt.check_result()}")
# Blank: [[-3,-3,-3],[-3,-3,-3],[-3,-3,-3]]
check_stack(0)
check_stack(1)

tick_tock = 0

AGAINST_COMPUTER = True
COMPUTER_VALUE = 0

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("--pvp", action="store_true", help="play against another player, default play against the computer.")
    parser.add_argument("--start_first", action="store_true", help="start first (play as O) otherwise go second and play as X.")

    args = parser.parse_args()
    if args.pvp:
        AGAINST_COMPUTER = False
    if args.start_first:
        COMPUTER_VALUE = 1

    ttt = TicTacToe()
    brain = ttt_brain.PatternBrain(computer_value=COMPUTER_VALUE)

    print("Welcome to Tic Tac Toe, q to quit at any time.")
    print(f"Against computer: {AGAINST_COMPUTER}")
    if args.start_first:
        print("Player starts first...")
    print("\n-- Choose from grid --")
    print(ttt.draw_with_grid())

    while ttt.check_result() == -1:
        
            
            if AGAINST_COMPUTER and tick_tock == COMPUTER_VALUE:
                print("Thinking...")
                
                ttt = brain.play(ttt)
                
            else: 
                ttt.as_flat_list()
                print(f"\nSelect {tick_tock}: ")
                inp = input()

                if inp == "q":
                    print("Bye bye!")
                    break

                grid_x,grid_y = Utils.extract_grid(inp)


                check_and_apply(ttt, tick_tock, grid_x, grid_y)

            if tick_tock == 0:
                tick_tock = 1
            else:
                tick_tock = 0


            print(f"Result: {ttt.check_result()}\n")
            print(ttt)
            print("\n-- Choose from grid --")
            print(ttt.draw_with_grid())

            if ttt.is_complete() and ttt.check_result() == -1:
                print("Its a Draw!")
                break
        
    if ttt.check_result() >= 0:
        print(f"Game Over. Game won by {ttt.check_result()}")





