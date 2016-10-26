#!user/bin/env python
# -*- coding: utf-8 -*-
"""
This module shows update of a simple game called Pig using Factory and Proxy patterns.
"""

import random
import datetime
import argparse

class Die(object):
    """the die which has 6 sides"""
    def __init__(self, seed):
        if seed is not None:
            random.seed(seed)

    def roll(self):
        return random.randint(1, 6)

def PlayerFactory(player):
    if player == 'human':
        return HumanPlayer(player)
    if player == 'computer':
        return ComputerPlayer(player)
    else :
    	print "invalid input"
    	exit()    

class Player(object):
    """constructor for the players"""
    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.turns_score = 0

class ComputerPlayer(Player):
    """constructor for the players"""
    def __init__(self, name):
        Player.__init__(self, name)
        self.strategy = True

class HumanPlayer(Player):
    """constructor for the players"""
    def __init__(self, name):
        Player.__init__(self, name)
        self.strategy = False

def GameFactory(player1, player2, timed=False, seed=None):
    if timed:
        return TimedGame(player1, player2, seed)
    else:
        return Game(player1, player2, seed)


class Game(object):
    """Constructor for Pig Game"""
    def __init__(self, player1, player2, seed= None):  
        self.player1 = player1
        self.player2 = player2
        self.die = Die(seed)
    
    def turn(self, player):
        """A players turn"""
        print '\nit is Player {}\'s turn'.format(player.name)
        r = self.die.roll()
        print '\nyou rolled a {}\n'.format(r)
        if r == 1:
            player.turns_score = 0
            print ('oops! you rolled a 1, '
                   'next player.\n').format(player.name, player.total_score)
            print '-' * 60, '\n'
            self.next_player(player)
        else:
            player.turns_score += r
            player.total_score += r
            print 'your total this turn is {}\n'.format(player.turns_score)
            if player.total_score >= 100:
                print ('{} is the winner '
                       'with a score of {}!').format(player.name, player.total_score)
                exit()
            if player.strategy:
                self.strategy(player)
            else:
                self.player_ans(player)
  
    def strategy(self, player):
        if player.turns_score < 25:
            self.turn(player)
        else:
            print '\nyour turn is now over.\n'
            player.turns_score = 0
            print ('{}\'s total score is'
                   ' now {}.\n\n').format(player.name, player.total_score)
            print '-' * 60, '\n'
            self.next_player(player)

    def player_ans(self, player):
        print('The total for this player is ' + str(player.total_score))
        """players answer to his roll"""
        ans = raw_input('would you like to roll again? '
                        'r = roll h = hold ').lower()
        if ans == 'h':
            print '\nyour turn is now over.\n'
            player.turns_score = 0
            print ('{}\'s total score is'
                   ' now {}.\n\n').format(player.name, player.total_score)
            print '-' * 60, '\n'
            self.next_player(player)
        elif ans == 'r':
            self.turn(player)
        else:
            print 'Invalid option, r = roll h = hold '
            self.player_ans(player)     
                
    def next_player(self, current_player):
        """initiates next players turn"""
        if self.player1 == current_player:
            self.turn(self.player2)
        else:
            self.turn(self.player1)

class TimedGame(Game):
    def __init__(self, player1, player2, seed):
        Game.__init__(self, player1, player2, seed)
        self.startTime = datetime.datetime.now()

    def determineWinner(self):
        if self.player1.total_score > self.player2.total_score:
            print ('{} is the winner '
                   'with a score of {}!').format(self.player1.name, self.player1.total_score)
            exit()        
        else:            
            print ('{} is the winner '
                   'with a score of {}!').format(self.player2.name, self.player2.total_score)
            exit()    

    def timeOut(self):
        stopTime = datetime.datetime.now()
        elapsedTime = stopTime - self.startTime
        if elapsedTime > datetime.timedelta(minutes=1):
            return True
        else:
            return False

    def turn(self, player):
        """A players turn"""
        if self.timeOut():
            self.determineWinner()
        super(TimedGame, self).turn(player)

def main():
    """initiates the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--player1', help='Enter the player type for player 1 (human or computer).')
    parser.add_argument('--player2', help='Enter the player type for player 2 (human or computer).')
    parser.add_argument('--timed', help='Specify if the game is timed')
    args = parser.parse_args()
    player1 = PlayerFactory(args.player1)
    player2 = PlayerFactory(args.player2)
    game = GameFactory(player1, player2, args.timed, 0)
    print 'Welcome to pig'
    game.turn(game.player1)

if __name__ == '__main__':
    main()
    

