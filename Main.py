import pygame, sys, time, numpy
from Constants import Button, colours#, myriadProFont
from GameItems import *

pygame.init()

monitorSize = [pygame.display.Info().current_w, pygame.display.Info().current_h] #Get's the monitor size of the user's computer
#For mine, Macbook Air 2015, it's 13.3-inch, 1440 x 900 pixel display (128 ppi) so it'll be [1440, 900]

print(monitorSize)
windowSize = (800, 600) #TODO: Make the default size relative to the screen size
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
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

def checkFileExists(filename):
    try:
        with open(filename) as file:
            return True
    except FileNotFoundError:
        return False

def loadGame():
    states = []
    with open("saved_game.txt") as file:
        for line in file.readlines():
            line = line.replace("\n", "")
            states.append(line)
    
    cash = int(states[0])
    shield = bool(states[1])
    mirror = bool(states[2])
    bankAmount = int(states[3])
    #enteredCoordinates = states[4].replace("[", "").replace("]", "").split(", ")     does the same as below, easier to read 
    enteredCoordinates = states[4][1:len(states[4])-1].split(", ")
    
    items = states[5][:len(states[5])-2].replace("[", "").replace("]", "").replace(" ", "").split(",")
    gridString = []
    itemNumber = 0
    for i in range(7):
        gridString.append([])
        for j in range(7):
            gridString[i].append(items[itemNumber])
            itemNumber += 1

    grid = []
    itemDict = {
        "present": Present(), "choosenextsquare": ChooseNextSquare(), "lostatsea": LostAtSea(),
        "swapscore": SwapScore(), "rob": Rob(), "mirror": Mirror(), "doublescore": DoubleScore(),
        "shield": Shield(), "sinkship": SinkShip(), "backstab": Backstab(), "sneakpeek": SneakPeak(),
        "bank": Bank(), "$200": Cash(200), "$1000": Cash(1000), "$3000": Cash(3000), "$5000": Cash(5000)
        }
    for rowNum, row in enumerate(gridString):
        grid.append([])
        for element in row:
            grid[rowNum].append(itemDict[element])
    
    mainScreen(grid, enteredCoordinates, cash, bankAmount, shield, mirror)

def titleScreen():
    screen.fill(colours["sea"])
    
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
                
            #TODO: Make the screen resizable.
            #if event.type == pygame.VIDEORESIZE:
            #   screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    
            if event.type == pygame.MOUSEBUTTONDOWN: #if mouse is clicked
                if newGameButton.isMouseHover(mousePosition):
                    newGameButton.color = colours["blue"]
                    print("Clicked new game button")
                    
                if continueGameButton.isMouseHover(mousePosition):
                    myriadProFont = pygame.font.SysFont("Myriad Pro", 48)
                    
                    foundGame = checkFileExists("saved_game.txt")
                    if foundGame:
                        loadGameMessage = myriadProFont.render("Loading", 1, colours["black"], colours["white"])
                        loadGameSize = loadGameMessage.get_size()
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
                    
            #TODO: Change button colour upon hover is not working
            if event.type == pygame.MOUSEMOTION: #if mouse is moving
                if newGameButton.isMouseHover(mousePosition):
                    newGameButton.color = colours["green"]
                    print("Hovering over new game button")
                else:
                    newGameButton.color = colours["red"]
        pygame.display.update()

#TODO: Open (or create if necessary) saved_game file and then just write. Don't append, write.
def saveGame(grid, enteredCoordinates, cash, bankAmount, shield, mirror):
    pass

#Converts from something like 4, 2 to D3
def intCoordinateToStrCoordinate(rowCoordinate, colCoordinate):
    rows = "ABCDEFG"
    return rows[rowCoordinate] + str(colCoordinate+1)

def mainScreen(grid, enteredCoordinates, cash, bankAmount, shield, mirror):
    print("Main screen!")
    screen.fill(colours["sea"])
    
    whatHappenedButton = Button(colours["green"], windowSize[0]//2 - 150, 550, 300, 30, text="What Happened?")
    whatHappenedButton.draw(screen)
    
    saveGameButton = Button(colours["green"], 20, 20, 200, 30, text="Save Game")
    saveGameButton.draw(screen)
    
    gridImage = pygame.image.load("Images/grid.png")
    gridImageSize = gridImage.get_rect().size
    screen.blit(gridImage, (windowSize[0]//2 - gridImageSize[0]//2, windowSize[1]//2 - gridImageSize[1]//2))
    
    cashButton = Button(colours["green"], 620, 20, 180, 30, text="Cash: %d" % cash)
    cashButton.draw(screen)
    
    if bankAmount != 0: #if bank is not 0, then this game is being continued and not a new game
        bankButton = Button(colours["green"], 620, 60, 180, 30, text="Bank: %d" % bankAmount)
        bankButton.draw(screen)
    
    #TODO: Add the shield and mirror icons if they are initialised as True
    shieldButton = Button(colours["green"], 620, 100, 80, 80, image="Images/GameItems/Shield.png")
    if shield:
        shieldButton.draw(screen)
    mirrorButton = Button(colours["green"], 620, 190, 80, 80, image="Images/GameItems/Mirror.png")
    if mirror:
        mirrorButton.draw(screen)
    
    mainScreen = screen.copy()
    
    print(grid)
    
    #Add the game item images to the grid
    for rowCoordinate, row in enumerate(grid):
        for colCoordinate, element in enumerate(row):
            if intCoordinateToStrCoordinate(rowCoordinate, colCoordinate) not in enteredCoordinates:
                filename = "Images/GameItems/" + element.itemName + ".png"
                image = pygame.image.load(filename)
                image = pygame.transform.scale(image, (48, 48))
                screen.blit(image, (rowCoordinate * 53 + 245, colCoordinate * 58 + 130)) #TODO: Don't hard code the numbers
    
    while True: #TODO: While there are still squares to be picked
        for event in pygame.event.get():
            mousePosition = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                #TODO: Ask user if they would like to save game. Display two buttons - yes and no. If yes, call saveGame().
                pygame.quit()
                sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    titleScreen()