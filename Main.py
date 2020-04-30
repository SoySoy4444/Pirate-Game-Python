import pygame, sys
from Constants import Button, colours#, myriadProFont

pygame.init()

windowSize = (800, 600)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Pirate Game")

def titleScreen():
    screen.fill(colours["green"])
    
    waitingForUser = True
    
    newGameButton = Button(colours["red"], windowSize[0]//2 - 100, 300, 200, 30, text="New Game")
    continueGameButton = Button(colours["red"], windowSize[0]//2 - 150, 400, 300, 30, text="Continue Game")
    howToPlayButton = Button(colours["red"], 100, 0, 200, 24, text="How To Play")
    
    newGameButton.draw(screen)
    continueGameButton.draw(screen)
    howToPlayButton.draw(screen, fontSize=24)
    
    while waitingForUser:
        for event in pygame.event.get():
            mousePosition = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.MOUSEBUTTONDOWN: #if mouse is clicked
                if newGameButton.isMouseHover(mousePosition):
                    newGameButton.color = colours["blue"]
                    print("Clicked new game button")
                if continueGameButton.isMouseHover(mousePosition):
                    print("Clicked continue game button")
            
            if event.type == pygame.MOUSEMOTION: #if mouse is moving
                if newGameButton.isMouseHover(mousePosition):
                    newGameButton.color = colours["green"]
                    print("Hovering over new game button")
                else:
                    newGameButton.color = colours["red"]
            pygame.display.update()
titleScreen()