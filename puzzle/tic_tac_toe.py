""" 
@author: Anuj Kumar
@email: cdac.anuj@gmail.com
@date: 
"""
import random
from copy import deepcopy


class Turn:
    def opp_turn(self, turn):
        return 2 if turn == 1 else 1


class Node:
    def __init__(self, parent, puzzle, value=0, turn=1, depth=0, visited=False):
        self.parent = parent
        self.puzzle = puzzle
        self.my_turn = turn
        self.value = value
        self.depth = depth
        self.children = []
        self.empty_indexes = [move for move, value in enumerate(self.puzzle) if value == 0]
        self.visited = visited
        self.alpha = 0
        self.beta = 0

    def __str__(self):
        return "Depth: {depth}, Value: {value}, Turn: {turn}, No. of children: {child_count}, Visited: {visited}\n{} {} {}\n{} {} {}\n{} {} {}\n".format(
            depth=self.depth,
            value=self.value, turn=self.my_turn, child_count=len(self.children), visited=self.visited, *self.puzzle)


class TicTacToe:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.win_commbinations = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        self.opp_turn = Turn()
        self.human = True

    def best_move(self):
        print "calculating..."
        root = Node(parent=None, puzzle=deepcopy(self.puzzle), value=0)
        self.depth_first_search(root, 0)
        # print [n.puzzle for n in root.children if n.value == root.value]

        return random.choice([n for n in root.children if n.value == root.value]).puzzle

    def depth_first_search(self, node, depth):
        depth += 1
        node.children = self.possible_children(node, depth)
        if len(node.children) != 0 and not (self.is_win(node.puzzle, 1) or self.is_win(node.puzzle, 2)):
            for child in node.children:
                self.depth_first_search(child, depth)
            if node.my_turn == 1:
                max = node.children[0].value
                for child in node.children:
                    if max < child.value:
                        max = child.value
                node.value = max
            else:
                min = node.children[0]
                for child in node.children:
                    if min > child.value:
                        min = child.value
                node.value = min
        else:
            # print "TERMINATION"
            node.visited = True
            if self.is_win(node.puzzle, 1):
                # print "WIN 1"
                node.value = 10 * depth

            elif self.is_win(node.puzzle, 2):
                # print "WIN 2"
                node.value = -10 * depth
            else:
                # print "DRAW"
                node.value = 0
                # print node

    def possible_children(self, node, depth):

        children = []
        for move in node.empty_indexes:
            c_puzzle = self.create_child_puzzle(move, deepcopy(node.puzzle), node.my_turn)

            child = Node(parent=node, puzzle=c_puzzle, value=0, turn=self.opp_turn.opp_turn(node.my_turn), depth=depth)
            children.append(child)
        return children

    def create_child_puzzle(self, move, puzzle, turn):
        puzzle[move] = turn
        return puzzle

    def is_win(self, puzzle, turn):
        win = False
        for combi in self.win_commbinations:
            win = False
            if puzzle[combi[0]] == turn and puzzle[combi[1]] == turn and puzzle[combi[2]] == turn:
                win = True
                break
        return win

    def play(self):
        print "### TIC TAC TOE ###"
        print self
        while 0 in self.puzzle and not self.is_win(self.puzzle, 1) and not self.is_win(self.puzzle, 2):
            if self.human:
                move = input('Your move as {X} (0-8):')
                while self.puzzle[move] != 0 and move >= 0 and move < 9:
                    print "\nInvalid move!!!\n"
                    move = input('Your move as {X} (0-8):')
                self.puzzle[move] = 2
                self.human = False
            else:
                self.puzzle = self.best_move()
                self.human = True

            print self

    def __str__(self):
        lst = []
        for i in self.puzzle:
            if i == 1:
                lst.append('O')
            elif i == 2:
                lst.append('X')
            else:
                lst.append('.')
        return "{} {} {}\n{} {} {}\n{} {} {}\n".format(*lst)
