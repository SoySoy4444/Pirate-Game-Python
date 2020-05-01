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
    def __init__(self, color, x, y, width, height, text='', textColour = BLACK, image = None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColour = textColour
        self.image = image

    def draw(self, screen, fontSize = 48, outline = None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        
        if self.image != None: #We want an image button
            img = pygame.image.load(self.image)
            img = pygame.transform.scale(img, (self.width, self.height))
            screen.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '': #We want text displayed on our button
            myriadProFont = pygame.font.SysFont("Myriad Pro", fontSize)
            text = myriadProFont.render(self.text, 1, self.textColour)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isMouseHover(self, mousePos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if mousePos[0] > self.x and mousePos[0] < self.x + self.width:
            if mousePos[1] > self.y and mousePos[1] < self.y + self.height:
                return True
        return False


class Image():
    def __init__(self, filename, size = None):
        #We cannot initialise position yet because it may depend on the size of the image
        self.image = pygame.image.load(filename)
        
        #User has ordered manual scaling
        if size == None: #if the size was not specified, then use the default values for size
            self.width, self.height = self.image.get_rect().size
        else: #the file size was specified, so scale the image to the correct size
            self.width = size[0]
            self.height = size[1]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
    def blit(self, screen, pos):
        self.x = pos[0]
        self.y = pos[1]
        screen.blit(self.image, (self.x, self.y))

"""
class Message():
    def __init__(self, pause = None, fontSize, font = "MyriadProFont"):
        pass

    
class UserInput():
    def __init__(self, x, y, height, fontSize = 24, numeric = False):
        self.x = x
        self.y = y
        self.height = height
        self.fontSize = fontSize
        self.numeric = numeric
    
    def takeUserInput(self):
        pass
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
"""