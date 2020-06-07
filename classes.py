#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 10:56:21 2019

@author: lord-sarcastic
"""

"""This is a Console Based Game, actually action in nature. It involves a large
amount of strategy and choice based on a given amount of cash. You will be given 
cash to select your choice of fleet"""

"""This file contains all units described as classes"""
import time
import random
import math
import os

def enforce_type_input(type_check, string=''):
    while True:
        try:
            result = type_check(input(r'{string}\n:'))
            break
        except:
            pass
    return result

def slow_print(string, wait=0.05):
    for i in string:
        print(i, end='')
        time.sleep(wait)
    print()
    
def slow_input(query, wait=0.05):
    for i in query:
        print(i, end='')
        time.sleep(wait)
    return enforce_type_input(str)


class Fighter:
    '''This class is the parent class for all military units'''
    
    def __init__(self):
        '''constructor:
            price: amount to buy unit
            health: damage unit can receive before dying
            damage: amount of damage unit can deal at once
            preferences: the order in which unit will attack various enemy units
            base: sphere of operation
        '''
        slow_print('{} Object created'.format(self.__str__()))
        self.health = 100
        self.damage = 0
        self.preferences = []
        self.base = ''
        self.alive = True

    def __str__(self):
        return 'fighter'

    def __del__(self):
        slow_print('{0} is dying...\n{0} is dead'.format(self.__str__()))

    def being_attacked(self, reduce_health_by):
        '''Computes in game stats when player is attacked'''
        if self.health <= reduce_health_by:
            self.health = 0
            self.alive = False
        else:
            self.health -= reduce_health_by
        return self.alive

class Infantry(Fighter):
    '''All infantry are land based units'''
    def __init__(self):
        super().__init__()
        self.base = 'land'

class AirSupport(Fighter):
    '''All air support are air based '''
    def __init__(self):
        super().__init__()
        self.base = 'air'

class Trooper(Infantry):
    '''ID: T'''
    def __init__(self):
        super().__init__()
        self.damage = 50
        self.preferences = ['R', 'T', 'G', 'S', 'M', 'H', 'P', 'A']

class Sniper(Infantry):
    '''ID: S'''
    def __init__(self):
        super().__init__()
        self.damage = 100
    
class Grenadier(Infantry):
    '''ID: R'''
    def __init__(self):
        super().__init__()
        self.damage = 100
        self.preferences = ['T', 'S', 'M', 'A', 'G', 'R', 'H', 'P']

class Gunner(Infantry):
    '''ID: G'''
    def __init__(self):
        super().__init__()
        self.damage = 200
        self.preferences = ['T', 'R', 'G', 'S', 'M', 'H', 'P', 'A']
        
class MotorizedUnit(Infantry):
    '''ID: M'''
    def __init__(self):
        super().__init__()
        self.damage = 250
        self.preferences = ['H', 'P', 'M', 'A', 'T', 'G', 'S', 'R']
        
class ArmouredTank(Infantry):
    '''ID: A'''
    def __init__(self):
        super().__init__()
        self.damage = 400
        self.preferences = ['A', 'M', 'H', 'P', 'S', 'G', 'R', 'T']

class Helicopter(AirSupport):
    '''ID: H'''
    def __init__(self):
        super().__init__()
        self.damage = 600
        self.preferences = ['M', 'A', 'H', 'G', 'R', 'S', 'T', 'P']
        
class Aircraft(AirSupport):
    '''ID: P'''
    def __init__(self):
        super().__init__()
        self.damage = 800
        self.preferences = ['A', 'P', 'H', 'M', 'G', 'R', 'S', 'T']
        
class Player:
    '''Individual players use this class for all operations performed for each
    player and its actions'''
    def __init__(self, name):
        self.name = name

    def clear_or_create_file(self, name='player'+str(len(os.listdir())+1)):
        '''Clears data in both user files or creates one if it doesn't exist.
        user files are of two types: 
            .scam: contains user's fighting configuration; 
            .data contains user's data and statistics
        '''
#        for .scam file
        with open(r'{name}.scam', 'w') as f:
            count = len(os.listdir())
            f.write(str(count+1), '\n')

#        for .data file
        with open(r'{name}.data', 'w') as f:
            f.write(r'{name}\n')
            f.write('played: 0\n')
            f.write('won: 0\n')
            f.write('draw: 0\n')
            f.write('lost: 0\n')
            f.write('P(win): 0\n')
            
    def check_file(self, query):
        '''Returns true if user file exists'''
        
        files = [i[:-5] for i in os.listdir()]
        return True if query in files else False
    
    def show_file_content(self, query):
        '''displays all data in .scam and .data files respectively'''
        try:
            slow_print('.scam file')
            with open(r'{query}).scam','r') as f:
                f = f.readlines()
                for i in f:
                    slow_print(i)

            slow_print('.data file')
            with open(r'{query}).data','r') as f:
                f = f.readlines()
                for i in f:
                    slow_print(i)
            return 0
        except:
            slow_print('\'scam\' file for \'{query}\' does not exist.')
            return 1
    
    def edit_name(self):
        '''interface to edit user name'''
        name = ''
        while check_file(name) is True:
            name = slow_input('Enter player name:')
            if check_file(name) is True:
                slow_print('\'{name}\' has already been taken.')
        os.rename(r'{self.name}.scam', r'{name}.scam')
            
        with open(r'{self.name}.data', 'r') as old:
            with open(r'{name}.data', 'w') as new:
                old = old.readlines()
                old[0] = name
                for i in old:
                    new.write(i)
        os.remove(r'{self.name}.data')
    
    def win(self):
        '''appends 1 for each wins a user has'''
        with open(r'{self.name}.data', 'r') as old:
            lines = old.readlines()
        mark = int(lines[2][5:-2]) + 1
        lines.pop(2)
        lines.insert(2, r'won: {mark}\n')
        with open(r'{self.name}.data', 'w') as old:
            for i in lines:
                old.write(i)
    
    def lose(self):
        '''appends 1 for each loss a player has'''
        with open(r'{self.name}.data', 'r') as old:
            lines = old.readlines()
        mark = int(lines[4][6:-2]) + 1
        lines.pop(4)
        lines.insert(4, r'lost: {mark}\n')
        with open(r'{self.name}.data', 'w') as old:
            for i in lines:
                old.write(i)
    
    def draw(self):
        '''appends 1 for each draw a player has'''
        with open(r'{self.name}.data', 'r') as old:
            lines = old.readlines()
        mark = int(lines[3][6:-2]) + 1
        lines.pop(3)
        lines.insert(3, r'draw: {mark}\n')
        with open(r'{self.name}.data', 'w') as old:
            for i in lines:
                old.write(i)
    
    def played(self):
        '''appends 1 for each played match a player has'''
        with open(r'{self.name}.data', 'r') as old:
            lines = old.readlines()
        mark = int(lines[1][8:-2]) + 1
        lines.pop(1)
        lines.insert(1, r'played: {mark}\n)
        with open(r'{self.name}.data', 'w') as old:
            for i in lines:
                old.write(i)
    
    def p_win(self):
        '''computes the probability of a player winning a match:
            probability = wins/played
        '''
        with open(r'{self.name}.data', 'r') as old:
            lines = old.readlines()
        prob = round(int(lines[1][6:-2])/int(lines[2][6:-2]), 2)
        lines.pop(5)
        lines.append(, r'p(win): {prob}\n)
        with open(r'{self.name}.data', 'w') as old:
            for i in lines:
                old.write(i)
#TTTTTTTTT  PPPPPPPPP
#SSSSSSSSS  RRRRRSSGG
#HHHPPPHHH  SSAAASSSS
