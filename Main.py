import pygame, sys, time
from Constants import Button, colours#, myriadProFont
from pip._vendor.colorama.ansi import Back

pygame.init()

windowSize = (800, 600)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("Pirate Game")
clock = pygame.time.Clock()

def pause(seconds = None):
    paused = True
    startTime = time.time()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: #if c pressed, Continue playing
                    paused = False
                    
        if seconds != None:
            if time.time() - startTime > seconds:
                paused = False
            
        pygame.display.update()

def continueGame():
    print("Clicked continue game button")
    try:
        with open("saved_games.txt") as file:
            return True
    except FileNotFoundError:
        return False

def loadGame():
    print("READY")

def titleScreen():
    screen.fill(colours["green"])
    
    waitingForUser = True
    
    newGameButton = Button(colours["red"], windowSize[0]//2 - 100, 300, 200, 30, text="New Game")
    continueGameButton = Button(colours["red"], windowSize[0]//2 - 150, 400, 300, 30, text="Continue Game")
    howToPlayButton = Button(colours["red"], 100, 0, 200, 24, text="How To Play")
    backToTitleScreen = Button(colours["red"], 100, windowSize[1]-100, 200, 24, text="Back")
    
    newGameButton.draw(screen)
    continueGameButton.draw(screen)
    howToPlayButton.draw(screen, fontSize=24)
    
    titleScreen = screen.copy()
    
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
                    myriadProFont = pygame.font.SysFont("Myriad Pro", 48)
                    
                    foundGame = continueGame()
                    if foundGame:
                        loadGameMessage = myriadProFont.render("Loading", 1, colours["black"], colours["white"])
                        loadGameSize = loadGameMessage.get_size()
                        startTime = time.time()
                        screen.blit(loadGameMessage, (windowSize[0]//2 - loadGameSize[0]//2, windowSize[1]//2 - loadGameSize[1]//2))
                        pause(seconds=3) #show the message for 3 seconds
                        waitingForUser = False
                        loadGame() #load the game
                    else:
                        loadGameMessage = myriadProFont.render("Could not find a game!", 1, colours["black"], colours["white"])
                        loadGameSize = loadGameMessage.get_size()
                        screen.blit(loadGameMessage, (windowSize[0]//2 - loadGameSize[0]//2, windowSize[1]//2 - loadGameSize[1]//2))
                        pause(seconds=3) #show the message for 3 seconds
                        screen.blit(titleScreen, (0, 0)) #hide the message

                if howToPlayButton.isMouseHover(mousePosition):
                    #display how to play rules
                    screen.fill(colours["blue"])
                    backToTitleScreen.draw(screen, 24)
                    
                    ruleBackground = pygame.image.load("Images/rules.png")
                    screen.blit(ruleBackground, (0, 0))
                
                if backToTitleScreen.isMouseHover(mousePosition):
                    screen.blit(titleScreen, (0, 0)) #go back to the title screen
                    
            if event.type == pygame.MOUSEMOTION: #if mouse is moving
                if newGameButton.isMouseHover(mousePosition):
                    newGameButton.color = colours["green"]
                    print("Hovering over new game button")
                else:
                    newGameButton.color = colours["red"]
        pygame.display.update()
titleScreen()