import pygame as pg
from random import randint
import sys
pg.init()
screen = pg.display.set_mode((720,720))
difficulty = 1
playMusic = False
if playMusic:
	pg.mixer.init()
	music = pg.mixer.Sound('music.mp3')
	music.play()
if difficulty == 1:
	width = 666
	n = 9
	minecount = 10
elif difficulty == 2:
	width = 688
	n = 16
	minecount = 40

elif difficulty == 3:
	width = 696
	n = 24
	minecount = 99
sOffset = (720-width)/2
fsize = int(0.7 * width)// n
font = pg.font.SysFont('Monospace',fsize)
mines = []
c=0
length = width/n
cOffset = length/2 +sOffset
clickedL = clickedR = True
started = False
bgcolor = '#000030'
gameOver = False


class Cells():
	def __init__(self,x,y):
		self.showmines = False
		self.x = x
		self.y = y
		self.coord = (x,y)
		self.num = 0
		self.iscovered = True
		self.isflagged = False
		self.ismine = False
		self.isstarting = False
		self.isempty = False
		self.color = 'white'
		self.color2 = 'white'
		if self.x % 2 == self.y % 2:
			self.color = '#ab6a20'
			self.color2 ='#d9aa75'
		else:
			self.color = '#cf893a'
			self.color2 = '#f2c48f'
        
	def setup(self,mines):
		self.num = 0
    
		if self.coord not in mines and self.isstarting == False :
			if(self.coord[0]-1,self.coord[1]-1) in mines:
				self.num += 1
			if(self.coord[0]-1,self.coord[1]) in mines:
				self.num += 1
			if(self.coord[0]-1,self.coord[1]+1) in mines:
				self.num += 1
			if(self.coord[0]+1,self.coord[1]-1) in mines:
				self.num += 1
			if(self.coord[0]+1,self.coord[1]) in mines:
				self.num += 1
			if(self.coord[0]+1,self.coord[1]+1) in mines:
				self.num += 1
			if(self.coord[0],self.coord[1]-1) in mines:
				self.num += 1
			if(self.coord[0],self.coord[1]+1) in mines:
				self.num += 1
		else:
			if self.coord in mines:
				self.ismine = True
		if self.num == 0 and self.ismine == False:
					self.isempty = True

	def update(self,List,n):
		N    =  List[self.x][self.y-1] if self.y != 0 else None
		S    =  None if self.y >= n-1 else List[self.x][self.y+1] 
		W    =  List[self.x-1][self.y] if self.x != 0 else None
		E    =  None if self.x >= n-1 else List[self.x+1][self.y]
		NW   =  List[self.x-1][self.y-1] if self.y != 0 and self.x != 0 else None
		NE   = None if self.x >= n-1 or self.y == 0 else List[self.x+1][self.y-1] 
		SW   =None if self.y >= n-1 or self.x == 0 else List[self.x-1][self.y+1] 
		SE   =None if self.x >= n-1 or self.y >= n-1 else List[self.x+1][self.y+1]
		p=False
		if p == False:
			try: p = (N.isempty) and (N.iscovered == False)
			except:pass
		if p == False:
			try: p = (S.isempty) and (S.iscovered == False)
			except:pass
		if p == False:
			try: p = (NW.isempty) and (NW.iscovered == False)
			except:pass
		if p == False:
			try: p = (NE.isempty) and (NE.iscovered == False)
			except:pass
		if p == False:
			try: p = (W.isempty) and (W.iscovered == False)
			except:pass
		if p == False:
			try: p = (E.isempty) and (E.iscovered == False)
			except:pass
		if p == False:
			try: p = (SE.isempty) and (SE.iscovered == False)
			except:pass
		if p == False:
			try: p = (SW.isempty) and (SW.iscovered == False)
			except:pass
		if p and self.ismine == False:
				self.iscovered = False
		if self.showmines:
			if self.ismine:
				self.iscovered = False
	def draw(self):
		self.update(CellsList,n)
		if self.iscovered:
			pg.draw.rect(screen,self.color,(self.x * length +sOffset,self.y *  length +sOffset,length,length))
			if self.isflagged:
				r = pg.Rect(self.x * length +sOffset,self.y *  length +sOffset,length/2,length/2)
				r.center = ((self.x*length+cOffset),(self.y*length+cOffset))
				pg.draw.rect(screen,'red',r)
		else:
			pg.draw.rect(screen,self.color2,(self.x * length +sOffset,self.y *  length +sOffset,length,length))
			if self.num != 0 and self.ismine == False:
				label = font.render(str(self.num),1,'#874e0e')
				rect = label.get_rect(center = ((self.x*length+cOffset),(self.y*length+cOffset)))
				screen.blit(label,rect)
			if self.ismine:
				pg.draw.circle(screen,'red',((self.x*length+cOffset),(self.y*length+cOffset)),length*0.3)


CellsList = []
for I in range(n):
	l =[]
	for j in range(n):
		l.append(0)
	CellsList.append(l)
for x in range(n):
	for y in range(n):
		CellsList[x][y] = Cells(x,y)


while True:

	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			sys.exit()
	
	screen.fill('black')
	pg.draw.rect(screen,bgcolor,(0,0,720,720))
	if started != True:
		if pg.mouse.get_pressed()[0] and clickedL == False:
			pos = pg.mouse.get_pos()
			pos = (int((pos[0]-20)/length),int((pos[1]-20)/length))
			if pos[0]+pos[1] <= 2*(n-1):
				CellsList[pos[0]][pos[1]].iscovered = False
				CellsList[pos[0]][pos[1]].isstarting = True
				started = True
				while c <= minecount-1:
					x = randint(0,n-1)
					y = randint(0,n-1)
					if (x,y) not in mines and (CellsList[x][y].isstarting == False) :
						mines.append((x,y))
						c+=1
				for row in CellsList:
					for cell in row:
						cell.setup(mines)
				if CellsList[pos[0]][pos[1]].num == 0:
					CellsList[pos[0]][pos[1]].isempty = True
			clickedL = True
		elif pg.mouse.get_pressed()[0] == 0:
			clickedL = False
	elif gameOver == False:
		if pg.mouse.get_pressed()[0] and clickedL == False:
			pos = pg.mouse.get_pos()
			pos = (int((pos[0]-20)/length),int((pos[1]-20)/length))
			if pos[0]+pos[1] <= 2*(n-1):
				if CellsList[pos[0]][pos[1]].isflagged == False:
					CellsList[pos[0]][pos[1]].iscovered = False
					if CellsList[pos[0]][pos[1]].ismine:
						for row in CellsList:
							for cell in row:
								cell.showmines = True
								bgcolor = 'red'
								gameOver = True
			clickedL = True
		elif pg.mouse.get_pressed()[0] == 0:
			clickedL = False

		if pg.mouse.get_pressed()[2] and clickedR == False:
			pos = pg.mouse.get_pos()
			pos = (int((pos[0]-20)/length),int((pos[1]-20)/length))
			if pos[0]+pos[1] <= 2*(n-1):
				if CellsList[pos[0]][pos[1]].isflagged:
					CellsList[pos[0]][pos[1]].isflagged = False
				elif CellsList[pos[0]][pos[1]].isflagged == False:
					CellsList[pos[0]][pos[1]].isflagged = True
			clickedR = True
		elif pg.mouse.get_pressed()[2] == 0:
			clickedR = False
			
	count = 0
	for row in CellsList:
		for cell in row:
			cell.draw()
			if cell.iscovered == False and cell.ismine == False:
				count += 1
			if count == n*n-minecount:
				bgcolor = 'green'
				gameOver = True
	pg.display.update()