import pygame
import sys, os, random

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    print(os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)

#initializing window
WIDTH = 350
HEIGHT = 450
FPS = 12

pygame.init()
pygame.display.set_caption("Assignment Game")
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# Define color
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
brown = (100,40,0)
background = pygame.image.load(resource_path('white.jpg'))
background = pygame.transform.scale(background, (350, 450))
font = pygame.font.Font(resource_path('comic.ttf'), 70)

def makeText(text, color, bgcolor, top, left):
    textSurf = font.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)    
# Generic method to draw fonts on the screen   
font_name = pygame.font.match_font('comic.ttf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, brown)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)
	
class Generate_Puzzle:                     
    def __init__(self, size, tilesize, margin,n = 0):
        gridsize = (size, size)
        self.gridsize,self.tilesize,self.margin, self.n = gridsize, tilesize, margin, n
        self.begin = False
        self.tiles_no = gridsize[0]*gridsize[1]-1          # no of tiles
        self.orig = [(x,y) for y in range(gridsize[1]) for x in range(gridsize[0])]
        if self.n < 4:
            self.tiles = [(x,y) for y in range(gridsize[1]) for x in range(gridsize[0])]  #coordinate of tiles 
        else:
            self.tiles = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2), (3, 2), (0, 3), (2, 3),(1, 3), (3, 3)]
        self.tilepos = {(x,y):(x*(tilesize+margin)+margin,y*(tilesize+margin)+margin) for y in range(gridsize[1]) for x in range(gridsize[0])}  #tile position
        self.prev = None
        self.tile_images =[]
        font = pygame.font.Font(None, 80)           
        for i in range(self.tiles_no):
            image = pygame.Surface((tilesize,tilesize))    #display tiles 
            image.fill(brown)
            text = font.render(str(i+1),2,(255,255,255))  ##text on tiles
            width,height = text.get_size()  #text size
            image.blit(text,((tilesize-width)/2 , (tilesize-height)/2))   #####display text in the middle of tile
            self.tile_images += [image]
           
    def Blank_pos(self):
        return self.tiles[-1]
    
    
    def set_Blank_pos(self,pos):
        self.tiles[-1] = pos
        
    opentile = property(Blank_pos, set_Blank_pos)   #get and set the pos of blank
    
    def switch_tile(self, tile):
        self.tiles[self.tiles.index(tile)]=self.opentile
        self.opentile = tile
        self.prev= self.opentile
        
    def check_in_grid(self, tile):
        return tile[0]>=0 and tile[0]<self.gridsize[0] and tile[1]>=0 and tile[1]<self.gridsize[1]
        
    def close_to(self):              #adjacent tile postion to blank (which tiles can move to blank position)
        x, y = self.opentile
        return (x-1,y),(x+1,y),(x,y-1),(x,y+1)
        
    def set_tile_randomly(self):
        adj = self.close_to()
        adj = [pos for pos in adj if self.check_in_grid(pos)and pos!= self.prev ]
        tile = random.choice(adj)
        self.switch_tile(tile)
        #print(self.prev)
            
    def update_tile_pos(self,dt):        #update tile position
        if self.tiles == self.orig and self.begin:
            levelup(self.n+1)
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        if mouse[0]:
            x,y = mpos[0]%(self.tilesize+self.margin),mpos[1]%(self.tilesize+self.margin)
            if x>self.margin and y>self.margin:
                tile = mpos[0]//self.tilesize,mpos[1]//self.tilesize
                if self.check_in_grid(tile) and tile in self.close_to():
                    self.switch_tile(tile)
       
            
    def draw_tile(self,gameDisplay):                             #####draw tiles in particular positioned
        for i in range(self.tiles_no):
            x,y = self.tilepos[self.tiles[i]]
            gameDisplay.blit(self.tile_images[i],(x,y))
                    
    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:    #press space to random the tiles
                for i in range(100):
                    self.begin = True
                    if self.n < 4: 
                        self.set_tile_randomly()
                    else:
                        level(4)


def game_front_screen():
    gameDisplay.blit(background, (0,0))
    draw_text(gameDisplay, "Assignment Puzzle", 30, WIDTH / 2, HEIGHT / 4)
    draw_text(gameDisplay, "Send a screenshot after you finish all levels!", 20, WIDTH / 2, HEIGHT / 2)
    draw_text(gameDisplay, "Press a key to begin!", 40, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False             
	
def levelup(n):
    if n == 5:
        gameDisplay.blit(background, (0,0))
        draw_text(gameDisplay, "Awesome! Take a screenshot!", 30, WIDTH / 2, HEIGHT / 4)
        draw_text(gameDisplay, "And send it to me for marks!", 30, WIDTH / 2, HEIGHT * 3 / 4)
        draw_text(gameDisplay, "Press any key to quit.", 30, WIDTH / 2, HEIGHT * 4 / 5)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    pygame.quit()
    else:
        gameDisplay.blit(background, (0,0))
        draw_text(gameDisplay, "Level Cleared", 30, WIDTH / 2, HEIGHT / 4)
        draw_text(gameDisplay, "Press a key to continue!", 40, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False
                    level(n)
def level(n):
    size = n + 1 if n!= 4 else n
    program=Generate_Puzzle(size,80,5, n)
    while True:
        dt = clock.tick()/1000
        gameDisplay.blit(background, (0,0))
        draw_text(gameDisplay,'Press Space to Start/Reset', 20, WIDTH / 2, HEIGHT * 4 / 5)
        draw_text(gameDisplay,'Click on tile next to blank space to move it.', 20, WIDTH / 2, HEIGHT * 6 / 7)
        draw_text(gameDisplay,('Aim: Arrange numbers in the order'), 20, WIDTH / 2, HEIGHT * 8 / 9)
        draw_text(gameDisplay,('1,2,..,'+(str((n+1)*(n+1)-1) if n!=4 else str(16))+' with blank at the end'), 20, WIDTH / 2, HEIGHT * 13 / 14)
        program.draw_tile(gameDisplay)
        pygame.display.flip()        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit();sys.exit()
            program.events(event)
        program.update_tile_pos(dt)
		
		
game_over = True        
game_running = True 
while game_running :
    if game_over :
        game_front_screen()       
    game_over = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:          
            game_running = False
    gameDisplay.blit(background, (0,0))  
    level(1)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
