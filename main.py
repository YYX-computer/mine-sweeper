from tkinter.messagebox import showinfo
from pygame.locals import *
import tkinter as tk
import random
import pygame
base = tk.Tk()
base.withdraw()
pygame.init()
WIDTH = 10
HEIGHT = 10
def generate(w,h):
	res = []
	for i in range(h):
		ls = []
		for j in range(w):
			ls.append(False)
		res.append(ls)
	bomb_total = random.randint(1,w * h // 4)
	for i in range(bomb_total):
		x = random.randint(0,w - 1)
		y = random.randint(0,h - 1)
		res[x][y] = True
	return res
def show(surf,vals):
	font = pygame.font.Font('songti SC.TTF',100)
	for i in range(len(vals)):
		for j in range(len(vals[i])):
			x1,y1,x2,y2 = i * 50,j * 50,i * 50 + 50,j * 50 + 50
			rect = pygame.Rect((x1,y1,x2,y2))
			if(vals[i][j] == None):
				t = font.render(' ',True,(0,0,0),(255,255,255))
			else:
				t = font.render(str(vals[i][j]),True,(0,0,0),(255,255,255))
				t = pygame.transform.scale(t,(50,50))
				surf.blit(t,(50 * i,50 * j))
			pygame.draw.rect(surf,(0,0,0),rect,2)
def judge(vals,puzzle):
	for i in range(len(vals)):
		for j in range(len(vals[i])):
			if(vals[i][j] == None or (vals[i][j] == '!' and (not puzzle[j][i]))):
				return False
	return True
def sweep(display,puzzle,x,y,w,h):
	dir = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
	def _sweep(display,puzzle,x,y,w,h):
		dir = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
		display[x][y] = 0
		for dx,dy in dir:
			tx,ty = x + dx,y + dy
			if(tx in range(h) and ty in range(w) and \
			   puzzle[ty][tx]):
				display[x][y] += 1
		return display
	if(display[x][y] not in (None,'!') or puzzle[y][x]):
		return display
	display = _sweep(display,puzzle,x,y,w,h)
	if(display[x][y] == 0):
		for dx,dy in dir:
			tx,ty = x + dx,y + dy
			if(tx in range(h) and ty in range(w)):
				display = sweep(display,puzzle,tx,ty,w,h)
	return display
def main():
	src = pygame.display.set_mode((50 * WIDTH,50 * HEIGHT))
	puzzle = generate(WIDTH,HEIGHT)
	display = []
	for i in range(HEIGHT):
		ls = []
		for j in range(WIDTH):
			ls.append(None)
		display.append(ls)
	while(1):
		pygame.display.update()
		src.fill((255,255,255))
		show(src,display)
		if(judge(display,puzzle)):
			pygame.display.update()
			showinfo('Congratulations!','Congratulations!You\'ve done it!')
			exit()
		for ev in pygame.event.get():
			if(ev.type == QUIT):
				exit()
			elif(ev.type == MOUSEBUTTONDOWN):
				x = ev.pos[0] // 50
				y = ev.pos[1] // 50
				if(ev.button == 3):
					if(display[x][y] == '!'):
						display[x][y] = None
					else:
						display[x][y] = '!'
				else:
					if(puzzle[y][x]):
						showinfo('Failed','You click a BOMB!')
						exit()
					else:
						display = sweep(display,puzzle,x,y,WIDTH,HEIGHT)
if(__name__ == '__main__'):
	main()
