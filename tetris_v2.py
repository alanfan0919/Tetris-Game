import random, time, pygame, sys, pdb
from pygame.locals import *
from global_variables import *


def main():

	pygame.init()
	MAINSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),0,32)
	FPSCLOCK=pygame.time.Clock()
	BIGFONT=pygame.font.SysFont('arial',100)
	BASICFONT=pygame.font.SysFont('arial',16)
	pygame.display.set_caption('Funny Tetris')

	MAINSURF.fill(BLACK)
	displaySurface('Funny Tetris',BIGFONT,BASICFONT,MAINSURF,FPSCLOCK)

	while True:
		restart=run_game(BIGFONT,BASICFONT,FPSCLOCK,MAINSURF)
		if not restart:
			displaySurface('Game over',BIGFONT,BASICFONT,MAINSURF,FPSCLOCK)#enter game over page

def run_game(BIGFONT,BASICFONT,FPSCLOCK,MAINSURF):

	board=clean_board()

	lastMoveDownTime=time.time()
	lastMoveSidewayTime=time.time()
	lastFallTime=time.time()

	move_left=False
	move_right=False
	move_down=False
	score=0
	fallPiece=Piece()#.IPiece()
	nextPiece=Piece()#.IPiece()

	while True:
		if not isValidPosition(board,fallPiece):
			return False# can't fit a new piece on the board, so game over, return False
		
		landed=False
		for event in pygame.event.get([QUIT,KEYDOWN,KEYUP]):
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				exit()#check for quit

			if event.type==KEYUP:
				if event.key==K_LEFT:
					move_left=False
				elif event.key==K_RIGHT:
					move_right=False
				elif event.key==K_DOWN:
					move_down=False
				elif event.key==K_r:
					return True #press 'r', restart the game

			if event.type==KEYDOWN:
				#get key been pressed
				if event.key==K_p:
					displaySurface("Pause",BIGFONT,BASICFONT,MAINSURF,FPSCLOCK)
					#lastMoveDownTime=time.time()
					#lastMoveSidewayTime=time.time()
					#lastFallTime=time.time()
				elif event.key==K_LEFT:
					move_left=True
					move_right=False
					move_down=False
					if isValidPosition(board,fallPiece,-1,0):
						fallPiece.x-=1
					lastMoveSidewayTime=time.time()
				elif event.key==K_RIGHT :
					move_right=True
					move_left=False
					move_down=False
					if isValidPosition(board,fallPiece,1,0):
						fallPiece.x+=1
					lastMoveSidewayTime=time.time()
				elif event.key==K_DOWN :
					move_down=True
					move_left=False
					move_right=False
					if isValidPosition(board,fallPiece,0,1):
						fallPiece.y+=1
					lastMoveDownTime=time.time()
				elif event.key==K_UP:
					tmpInd=fallPiece.rotationInd
					fallPiece.rotationInd=(fallPiece.rotationInd+1)%len(PIECES[fallPiece.shape])
					if not isValidPosition(board,fallPiece):
						fallPiece.rotationInd=tmpInd
				
				
		#handle long press of K_left, K_right, K_down
		if (move_right or move_left) and MOVESIDEWAYFREQ < time.time()-lastMoveSidewayTime:
			if move_right and isValidPosition(board,fallPiece,1,0):
				fallPiece.x+=1
			elif move_left and isValidPosition(board,fallPiece,-1,0):
				fallPiece.x-=1
			lastMoveSidewayTime=time.time()
		if move_down and isValidPosition(board,fallPiece,0,1) and MOVEDOWNFREQ < time.time()-lastMoveDownTime:
			fallPiece.y+=1
			lastMoveDownTime=time.time()

		if FALLFREQ < time.time()-lastFallTime:
			#judge whether falling piece has landed, if not fall down one unit
			if not isValidPosition(board,fallPiece,0,1):
				# falling piece has landed
				landed=True
				addToBoard(board,fallPiece)
				score+=evaluate(board)
			else:
				fallPiece.y+=1
				lastFallTime=time.time()
				landed=False

		MAINSURF.fill(BLACK)
		drawBoard(board,MAINSURF)
		if not landed:
			drawPiece(fallPiece,MAINSURF)
		drawNextPiece(nextPiece,MAINSURF,BASICFONT)
		drawScore(score,MAINSURF,BASICFONT)
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		if landed:
			fallPiece=nextPiece
			nextPiece=Piece()#IPiece()


def displaySurface(title,BIGFONT,BASICFONT,MAINSURF,FPSCLOCK):
	#draw title
	titleSurf=BIGFONT.render(title,True,WHITE)
	titleRect=titleSurf.get_rect()
	titleRect.center=(int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2))
	MAINSURF.blit(titleSurf,titleRect)	
	#draw text
	textSurf=BASICFONT.render("Press any key to play",True,WHITE)
	textRect=textSurf.get_rect()
	textRect.center=(int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)+150)
	MAINSURF.blit(textSurf,textRect)
	pygame.display.update()
	#waiting for key pressed or quit
	while True:
		for event in pygame.event.get([KEYDOWN,QUIT]):
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				exit()
			else:
				FPSCLOCK.tick() #tick for frame per second
				return

def clean_board():
	board=[]
	for i in range(BOARDHEIGHT):
		board.append(['.']*BOARDWIDTH)
	return board

class Piece:
	# return a random new piece in a random rotation and color
	def __init__(self):
		self.x=int(BOARDWIDTH/2)-int(TEMPLATEWIDTH/2)
		self.y=-2
		self.shape=random.choice(list(PIECES.keys()))
		self.rotationInd=random.randint(0, len(PIECES[self.shape]) - 1)
		self.colorInd=random.randint(0,len(DARKCOLORS)-1)
	@classmethod
	def IPiece(cls):
		newPiece=cls()
		newPiece.shape='I'
		newPiece.rotationInd=0
		return newPiece


def isValidPosition(board,piece,x_offset=0,y_offset=0):
	pieceTemp=PIECES[piece.shape][piece.rotationInd]
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEWIDTH):
			if pieceTemp[y][x]!='.':
				aboveBoard=(piece.y+y+y_offset<0)
				onBoard= (0<=piece.y+y+y_offset<BOARDHEIGHT) and (0<=piece.x+x+x_offset<BOARDWIDTH)
				if aboveBoard:
					continue
				if not onBoard or board[piece.y+y+y_offset][piece.x+x+x_offset]!='.':
					return False
	return True

def convertToPixelCoord(x,y):
	return (XMARGIN + (x * BOXSIZE)), (TOPMARGIN + (y * BOXSIZE))

def drawBox(x,y,colorInd,MAINSURF,pixelx=None,pixely=None):
	if colorInd=='.':
		return
	if pixelx==None:
		pixelx,pixely=convertToPixelCoord(x,y)
	pygame.draw.rect(MAINSURF,DARKCOLORS[int(colorInd)],(pixelx+1,pixely+1,BOXSIZE-1,BOXSIZE-1))
	pygame.draw.rect(MAINSURF,LIGHTCOLORS[int(colorInd)],(pixelx+4,pixely+4,BOXSIZE-4,BOXSIZE-4))

def drawBoard(board,MAINSURF):
	# draw the border around the board
	pygame.draw.rect(MAINSURF, BLUE, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)
    # fill the background of the board
	pygame.draw.rect(MAINSURF, BLACK, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))

	for y in range(BOARDHEIGHT):
		for x in range(BOARDWIDTH):
			drawBox(x,y,board[y][x],MAINSURF)

def drawPiece(fallPiece,MAINSURF,x_offset=None,y_offset=None):
	pieceTemp=PIECES[fallPiece.shape][fallPiece.rotationInd]
	if x_offset == None and y_offset == None:
        # if x_offset & y_offset hasn't been specified, use the location stored in the piece data structure
		x_offset, y_offset = convertToPixelCoord(fallPiece.x, fallPiece.y)
	for y in range(TEMPLATEWIDTH):
		for x in range(TEMPLATEWIDTH):
			if pieceTemp[y][x]!='.':
				drawBox(None,None,fallPiece.colorInd,MAINSURF,x_offset+x*BOXSIZE,y_offset+y*BOXSIZE)

def drawNextPiece(nextPiece,MAINSURF,BASICFONT):
	# draw the "next" text
	nextPieceSurf=BASICFONT.render('Next piece:',True,WHITE)
	nextPieceRect=nextPieceSurf.get_rect()
	nextPieceRect.topleft=(WINDOWWIDTH-150,80)
	MAINSURF.blit(nextPieceSurf,nextPieceRect)
	# draw the "next" piece
	drawPiece(nextPiece,MAINSURF,WINDOWWIDTH-120,95)

def drawScore(score,MAINSURF,BASICFONT):
	#display score currently got
	scoreSurf=BASICFONT.render("Score: %s" %score,True,WHITE)
	scoreRect=scoreSurf.get_rect()
	scoreRect.topleft=(WINDOWWIDTH-150,20)
	MAINSURF.blit(scoreSurf,scoreRect)

def addToBoard(board,fallPiece):
	piece=PIECES[fallPiece.shape][fallPiece.rotationInd]
	for y in range(TEMPLATEWIDTH):
		for x in range(TEMPLATEWIDTH):
			if piece[y][x]!='.':
				board[fallPiece.y+y][fallPiece.x+x]=str(fallPiece.colorInd)

def evaluate(board):
	score=0
	#pdb.set_trace()
	y=BOARDHEIGHT-1
	while y >=score:
		nonDot=0
		for x in range(BOARDWIDTH):
			if board[y][x]!='.':
				nonDot+=1
		if nonDot==BOARDWIDTH:
			score+=1
			board[y]=board[y-score]
		else:
			board[y]=board[y-score]
			y-=1
	for row in range(score):
		board[row]=['.']*BOARDWIDTH
	return score

main()	
