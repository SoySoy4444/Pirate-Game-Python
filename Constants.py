import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SEA = (59, 111, 226)

colours = {"white":WHITE, "black":BLACK, "blue":BLUE, "red":RED, "green":GREEN, "sea": SEA}
#myriadProFont = pygame.font.SysFont("Myriad Pro", 48)

class Button():
    def __init__(self, color, x, y, width, height, text='', textColour = BLACK):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColour = textColour

    def draw(self, screen, fontSize = 48, outline = None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            myriadProFont = pygame.font.SysFont("Myriad Pro", fontSize)
            text = myriadProFont.render(self.text, 1, self.textColour)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
            print("blitted")

    def isMouseHover(self, mousePos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if mousePos[0] > self.x and mousePos[0] < self.x + self.width:
            if mousePos[1] > self.y and mousePos[1] < self.y + self.height:
                return True
        return False

class Slider():
    pass
    