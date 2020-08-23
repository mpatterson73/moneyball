#!/usr/bin/env python
# coding: utf-8

# ## Moneyball Rosters
# 
# Using the 'moneyball_stats' (specifically the 'On Base Percentage' to salary ratio) create
# a roster for each year that the proper stats were available). 
# 
# #### The Roster
# 
# A roster shall consist of the following players:
# * Pitcher
# * Catcher
# * First Baseman
# * Second Baseman
# * Third Baseman
# * Shortstop
# * Left Fielder
# * Center Fielder
# * Right Fielder
# * Designated Hitter
# 
# *NOTE: pitchers are probably not selected this way. As a matter of fact, pitchers don't even hit in the American League. In the National League, the pitchers actual pitching stats must weigh heavily in the selection process and I did not venture into that for this project. For these reasons I have included a DH along with the 9 defensive postitions.*
# 
# #### The Rules
# 1. One roster for each year.
# 2. One player per postition.
# 3. Players that play multiple positions in a season, connot occupy multiple spots on a roster.
# 4. A player must have at least 20 appearances at a position to be considered for a roster spot.



import numpy as np
import pandas as pd


df = pd.read_csv('MB-Data/moneyball_stats.csv')
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', None)
mb_df = df.copy()

positions = ['G_p', 'G_c', 'G_1b', 'G_2b', 'G_3b', 'G_ss','G_lf', 'G_cf',
             'G_rf', 'G_dh']

# Create a list for a specific position and year ordered by obp to salary.
def top_ten_position(position, year):
    '''
    Returns a dataframe(orig index, playerID) consisting of the top ten
    players at a position in a given year ordered by OBP/salary ratio.
    '''
    df = mb_df.copy()
    yr_df = df.loc[(df.yearID == year) & (df[position] >= 20)]
    top_ten_df = yr_df.sort_values(by='OBP_to_salary', ascending=False)
    # reset the index of the dataframe and keep the original index ifor use later. 
    return top_ten_df.iloc[:10].reset_index()[['index','playerID']]
 


def get_indexes(year):
    '''
    Return a list indexes (correlating to master moneyball_stats
    dataframe) for the player at each position with the best 
    moneyball value (OBP/salary). RULE: a player can not be 
    aelected for multiple postitions.
    '''
    id_df = pd.DataFrame(columns=['index', 'playerID'])
    selected = []
    for p in positions:
        ten_best_df = top_ten_position(p, year)
        best_list = ten_best_df['index'].to_list()
        available = True
        while available:
            idx = best_list.pop(0)
            if idx not in selected:
                selected.append(idx)
                available = False
            else:
                idx = best_list.pop(0)
        #print(p, best_player)        
    return selected


def mb_roster_df(year):
    '''Return a roster based on OBP/salary ratio for a given year'''
    df = mb_df.copy()
    index_list = get_indexes(year)
    roster_df = df.loc[index_list][['nameFirst', 'nameLast', 'nameGiven',
       'teamID', 'AB', 'H', 'BB', 'HBP', 'SF', 'OBP', 'salary',
       'OBP_to_salary']]
    roster_df.insert(0, 'position', ['Pitcher', 'Catcher', '1st Base', '2nd Base',
                                     '3rd Base', 'Shortstop', 'Left Field',
                                     'Center Field', 'Right Feld', 'Designated Hitter'])
    return roster_df
    
if __name__ == "__main__":

    print("Choose a year between 1985 and 2016 to create a Moneyball roster from.")
    print("examples: 1985 or 2011 or 1999")
    yr = int(input())
    if yr in range(1985, 2017):
        print(mb_roster_df(yr))
    else:
        print('Selected must be between 1985-2016 \n Please try again')