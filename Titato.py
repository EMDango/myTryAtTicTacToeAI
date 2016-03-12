# -*- coding: utf-8 -*-
import os
import sys
import copy


"""
NOTES:
-Inside the AlphaBeta prune method the ev variable crashes because it's not set when it returns

"""

def printBoard(board):
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == 1:
				print "|O|",
			elif board[i][j] == 2:
				print "|X|",
			else:
				print "| |",
		print "\n"

def updateBoard(board, row, column, play):
	temp = copy.deepcopy(board)
	value = 0
	if(play == 'max'):
		value = 1
	elif(play == 'min'):
		value = 2
	temp[row][column] = value
	return copy.deepcopy(temp)

def inverse(player):
	if player == 'max':
		return 'min'
	elif player == 'min':
		return 'max'

def heuristic(board):
	h=0
	for i in range(3):
		if ((board[i][0] != 2) and (board[i][1] != 2) and (board[i][2] != 2)):
			h+=1
		if ((board[i][0] != 1) and (board[i][1] != 1) and (board[i][2] != 1)):
			h-=1
		if ((board[0][i] != 2) and (board[1][i] != 2) and (board[2][i] != 2)):
			h+=1
		if ((board[0][i] != 1) and (board[1][i] != 1) and (board[2][i] != 1)):
			h-=1
	if ((board[0][0] != 1) and (board[1][1] != 1) and (board[2][2] != 1)):
		h-=1
	if ((board[0][0] != 2) and (board[1][1] != 2) and (board[2][2] != 2)):
		h+=1
	if ((board[0][2] != 1) and (board[1][1] != 1) and (board[2][0] != 1)):
		h-=1
	if ((board[0][2] != 2) and (board[1][1] != 2) and (board[2][0] != 2)):
		h+=1

	return h

def expand(board, turn):
	e = []
	#print board
	for i in range(len(board)):
		#print(board[i])
		for j in range(len(board[i])):
			if (board[i][j] == 0):
				e.append(updateBoard(board,i,j,turn))
				#print e[i+j]
	return e

def AlphaBeta(board, alpha, beta, player, profMax):

	if(profMax == 0):
		return [heuristic(board), copy.deepcopy(board)]
	else:
		e = expand(board, player)
		#print profMax
		#print e
		print len(e)
		print "a: "+str(alpha)+" b: "+str(beta)
		if (player == 'min'):
			while ((len(e) != 0) and (alpha < beta)):
				v = AlphaBeta(e[0], alpha, beta, inverse(player), profMax-1)
				if(v[0]<beta):
					beta = v[0]
					ev=copy.deepcopy(e[0])
				#if(len(e)!=1):
				e=e[1:]
			return [beta, ev]
		else: #player = max
			while ((len(e) != 0) and (alpha < beta)):
				v = AlphaBeta(e[0], alpha, beta, inverse(player), profMax-1)
				if(v[0]>alpha):
					alpha = v[0]
					ev=copy.deepcopy(e[0])
				#if(len(e)!=1):
				e=e[1:]
			return [alpha, ev]

def checkWin(board):
	for i in range(3):
		if ((board[i][0] == 2) and (board[i][1] == 2) and (board[i][2] == 2)):
			return True
		if ((board[i][0] == 1) and (board[i][1] == 1) and (board[i][2] == 1)):
			return True
		if ((board[0][i] == 2) and (board[1][i] == 2) and (board[2][i] == 2)):
			return True
		if ((board[0][i] == 1) and (board[1][i] == 1) and (board[2][i] == 1)):
			return True
	if ((board[0][0] == 1) and (board[1][1] == 1) and (board[2][2] == 1)):
		return True
	if ((board[0][0] == 2) and (board[1][1] == 2) and (board[2][2] == 2)):
		return True
	if ((board[0][2] == 1) and (board[1][1] == 1) and (board[2][0] == 1)):
		return True
	if ((board[0][2] == 2) and (board[1][1] == 2) and (board[2][0] == 2)):
		return True
	return False



def main():
	rows = 3
	columns = 3
	prof = 6
	alpha = -999
	beta = 999
	win = 0
	playCount = 0
	board = [[0 for x in range(3)] for y in range(3)]
	# 0: null: 1: O(max) 2: X(min)
	
	os.system('cls')

	print "================="
	print "Welcome to Titato"
	print "=================\n\n"

	menuIn = raw_input("Choose a side to play:\n1: O\n2: X\n3: Quit\n")
	menuIn = int(menuIn)
	while(menuIn not in [1,2,3]):
		os.system('cls')
		menuIn = None
		menuIn = raw_input("Choose a side to play:\n1: O\n2: X\n3: Quit\n")
		menuIn = int(menuIn)
	if(menuIn == 1):
			player = 'max'
	elif(menuIn == 2):
			player = 'min'
	while (menuIn != 3):

			end = False
			while (end is False):
					os.system('cls')	
					printBoard(board)

					if(player == 'max'):
						playRow = raw_input("Row to play:")
						playCol = raw_input("Column to play:")
						playRow = int(playRow)
						playCol = int(playCol)
						while((playRow not in [1,2,3]) or (playCol not in [1,2,3])):
							os.system('cls')
							printBoard(board)
							playRow = None
							playCol = None
							print("Row or column wasn't a number")
							playRow = raw_input("Row to play:")
							playCol = raw_input("Column to play:")
							playRow = int(playRow)
							playCol = int(playCol)
						board = updateBoard(board, playRow-1, playCol-1, player)
						playCount+=1
						if(playCount == 9):
							end = True
						os.system('cls')		
						printBoard(board)
						end = checkWin(board)

						pcPlay = AlphaBeta(board, alpha, beta, inverse(player), prof)
						#print("Found a play")
						board = copy.deepcopy(pcPlay[1])
						playCount+=1
						if(playCount == 9):
							end = True
						os.system('cls')	
						printBoard(board)                    	
						end = checkWin(board)

					elif(player == 'min'):
						pcPlay = AlphaBeta(board, alpha, beta, inverse(player), prof)
						board = pcPlay[1]
						playCount+=1
						if(playCount == 9):
							end = True
						os.system('cls')	
						printBoard(board)                    	
						end = checkWin(board)

						playRow = raw_input("Row to play:")
						playCol = raw_input("Column to play:")
						playRow = int(playRow)
						playCol = int(playCol)
						while((playRow not in [1,2,3]) or (playCol not in [1,2,3])):
							os.system('cls')
							printBoard(board)
							playRow = None
							playCol = None
							print("Row or column wasn't a number")
							playRow = raw_input("Row to play:")
							playCol = raw_input("Column to play:")
							playRow = int(playRow)
							playCol = int(playCol)
						board = updateBoard(board, playRow-1, playCol-1, player)
						playCount+=1
						if(playCount == 9):
							end = True
						os.system('cls')	
						printBoard(board)
						end = checkWin(board)
			if(win == 1):
				print "WINNER: O"
			elif(win == 2):
				print "WINNER: X"
			else:
				print "DRAW"
			menuIn = raw_input("Choose a side to play:\n1: O\n2: X\n3: Quit\n")
			menuIn = int(menuIn)
			while(menuIn not in [1,2,3]):
				os.system('cls')
				menuIn = None
				menuIn = raw_input("Choose a side to play:\n1: O\n2: X\n3: Quit\n")
				menuIn = int(menuIn)
			if(menuIn == 1):
					player = 'max'
			elif(menuIn == 2):
					player = 'min'


main()
