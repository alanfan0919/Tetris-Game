
#definition of global variables
WINDOWWIDTH=640
WINDOWHEIGHT=480
BOARDWIDTH=10
BOARDHEIGHT=20
BOXSIZE=20
XMARGIN=int((WINDOWWIDTH-BOARDWIDTH*BOXSIZE)/2)
TOPMARGIN=WINDOWHEIGHT-BOARDHEIGHT*BOXSIZE-5
TEMPLATEWIDTH=5
FPS=25
FALLFREQ=0.27
MOVESIDEWAYFREQ = 0.15
MOVEDOWNFREQ = 0.1

WHITE=(255,255,255)
GRAY=(185, 185, 185)
BLACK=(0,0,0)
RED=(155,0,0)
LIGHTRED=(175,20,20)
GREEN=(0,155,0)
LIGHTGREEN=(20,175,20)
BLUE=(0,0,155)
YELLOW=(230,230,0)
LIGHTYELLOW=(250,250,20)
PURPLE=(60,0,80)
LIGHTPURPLE=(80,20,100)

DARKCOLORS=[RED,GREEN,YELLOW,PURPLE]
LIGHTCOLORS=[LIGHTRED,LIGHTGREEN,LIGHTYELLOW,LIGHTPURPLE]

Z_TEMP=[
		['.....',
		 '.....',
		 '.OO..',
		 '..OO.',
		 '.....'],

		['.....',
		 '..O..',
		 '.OO..',
		 '.O...',
		 '.....']
	   ]

S_TEMP=[
		['.....',
		 '.....',
		 '..OO.',
		 '.OO..',
		 '.....'],

		['.....',
		 '.O...',
		 '.OO..',
		 '..O..',
		 '.....']
	   ]

J_TEMP=[
		['.....',
		 '...O.',
		 '...O.',
		 '..OO.',
		 '.....'],

		['.....',
		 '.O...',
		 '.OOO.',
		 '.....',
		 '.....'],

		['.....',
		 '.OO..',
		 '.O...',
		 '.O...',
		 '.....'],

		['.....',
		 '.....',
		 '.OOO.',
		 '...O.',
		 '.....']
	   ]

L_TEMP=[
		['.....',
		 '..O..',
		 '..O..',
		 '..OO.',
		 '.....'],

		['.....',
		 '.....',
		 '.OOO.',
		 '.O...',
		 '.....'],

		['.....',
		 '.OO..',
		 '..O..',
		 '..O..',
		 '.....'],

		['.....',
		 '...O.',
		 '.OOO.',
		 '.....',
		 '.....'],
	   ]

I_TEMP=[
		['..O..',
		 '..O..',
		 '..O..',
		 '..O..',
		 '.....'],

		['.....',
		 '.....',
		 'OOOO.',
		 '.....',
		 '.....']
	   ]

O_TEMP=[
		['.....',
		 '..OO.',
		 '..OO.',
		 '.....',
		 '.....']
	   ]

T_TEMP=[
		['.....',
		 '.....',
		 '.OOO.',
		 '..O..',
		 '.....'],

		['.....',
		 '..O..',
		 '.OO..',
		 '..O..',
		 '.....'],

		['.....',
		 '..O..',
		 '.OOO.',
		 '.....',
		 '.....'],

		['.....',
		 '..O..',
		 '..OO.',
		 '..O..',
		 '.....'],
	   ]

PIECES={'J':J_TEMP,
		'L':L_TEMP,
		'S':S_TEMP,
		'Z':Z_TEMP,
		'O':O_TEMP,
		'I':I_TEMP,
		'T':T_TEMP}