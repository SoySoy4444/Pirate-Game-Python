import pygame, sys, time, datetime
from Constants import Button, colours, Image, UserInput, Message
from GameItems import *

pygame.init()

monitorSize = [pygame.display.Info().current_w, pygame.display.Info().current_h] #Get's the monitor size of the user's computer
#For mine, Macbook Air 2015, it's 13.3-inch, 1440 x 900 pixel display (128 ppi) so it'll be [1440, 900]

windowSize = (800, 600) #TODO: Make the default size relative to the screen size
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
pygame.display.set_caption("Pirate Game")
clock = pygame.time.Clock()

def log(listLines, filename, cash):
    with open(filename, "a") as file:
        now = datetime.datetime.now()
        dateAndTime = now.strftime("%d/%m/%y %H:%M")
        
        #for each string in the list of strings given, log the current time, cash and the message 
        for line in listLines:
            file.write(dateAndTime + "\t" + str(cash) + "\t" + line + "\n")

def fade(width, height, alpha=95, colour="white"):
    fade = pygame.Surface((width, height))
    fade.fill(colours[colour])
    fade.set_alpha(alpha)
    screen.blit(fade, (0, 0))

def pause(seconds = None):
    paused = True
    startTime = time.time()
    currentScreen = screen.copy()
    
    if seconds == None: #display "Paused" message indefinitely until the user presses c.
        fade(windowSize[0], windowSize[1]) #make the screen look whitish
        pauseMessage = Message("Paused", 48)
        pauseMessage.blit(screen, (windowSize[0]//2 - pauseMessage.width//2, windowSize[1]//2 - pauseMessage.height//2))

    while paused:
        clock.tick(2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: #if c pressed, continue playing
                    screen.blit(currentScreen, (0, 0))
                    paused = False
                    
        if seconds != None and time.time() - startTime > seconds:
            paused = False
            
        pygame.display.update()

def checkFileExists(filename):
    try:
        with open(filename):
            return True
    except FileNotFoundError:
        return False

def loadGame(): #Transition from continue game -> main screen
    states = []
    with open("saved_game.txt") as file:
        for line in file.readlines():
            line = line.replace("\n", "")
            states.append(line)
    
    cash = int(states[0])
    
    shield = True if states[1] == "True" else False
    mirror = True if states[2] == "True" else False
    bankAmount = int(states[3])
    #enteredCoordinates = states[4].replace("[", "").replace("]", "").replace("'", "").split(", ")     does the same as below, both work. 
    enteredCoordinates = states[4][1:len(states[4])-1].replace("'", "").split(", ")
    
    #convert from 1 huge 1D array called items to a 7 by 7 2D array of Strings called gridString
    items = states[5][:len(states[5])-2].replace("[", "").replace("]", "").replace(" ", "").replace("'", "").split(",")
    gridString = []
    currentRow = -1
    for i in range(49):
        if i % 7 == 0: #every 7 elements, create a new row
            gridString.append([])
            currentRow += 1
        gridString[currentRow].append(items[i]) #in the current row, add the current element

    grid = []
    itemDict = {
        "Present": Present(), "ChooseNextSquare": ChooseNextSquare(), "LostAtSea": LostAtSea(),
        "SwapScore": SwapScore(), "Rob": Rob(), "Mirror": Mirror(), "DoubleScore": DoubleScore(),
        "Shield": Shield(), "SinkShip": SinkShip(), "Backstab": Backstab(), "SneakPeek": SneakPeak(),
        "Bank": Bank(), "$200": Cash(200), "$1000": Cash(1000), "$3000": Cash(3000), "$5000": Cash(5000)
    }
    
    #turn the grid into a grid of game item objects instead of grid of strings
    for rowNum, row in enumerate(gridString):
        grid.append([])
        for element in row:
            grid[rowNum].append(itemDict[element])
            
    mainScreen(grid, enteredCoordinates, cash, bankAmount, shield, mirror, False)

def titleScreen():
    screen.fill(colours["sea"])
    
    waitingForUser = True #TODO: Define the logic for this.
    
    newGameButton = Button(colours["red"], windowSize[0]//2 - 100, 300, text="New Game")
    continueGameButton = Button(colours["red"], windowSize[0]//2 - 150, 400, text="Continue Game")
    howToPlayButton = Button(colours["red"], 100, 0, text="How To Play", fontSize=24)
    backToTitleScreen = Button(colours["red"], 100, windowSize[1]-100, text="Back")
    
    newGameButton.draw(screen)
    continueGameButton.draw(screen)
    howToPlayButton.draw(screen)
    
    title = Message("The Pirate Game", 64)
    title.blit(screen, (windowSize[0]//2 - title.width//2, 200))
    
    titleScreen = screen.copy()
    
    while waitingForUser:
        clock.tick(5)
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
                    if checkFileExists("saved_game.txt"):
                        loadingMessage = Message("Loading...", 48)
                        loadingMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                        pause(seconds=3) #show the message for 3 seconds
                        waitingForUser = False
                        loadGame() #load the game
                    else:
                        loadingMessage = Message("Could not find a game!", 48)
                        loadingMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
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
                else:
                    newGameButton.color = colours["red"]
        pygame.display.update()

def saveGame(grid, enteredCoordinates, cash, bankAmount, shield, mirror):
    with open("saved_game.txt", "w") as file:
        file.write(str(cash) + "\n")
        file.write(str(shield) + "\n")
        file.write(str(mirror) + "\n")
        file.write(str(bankAmount) + "\n")
        file.write(str(enteredCoordinates) + "\n")

        temp = [map(lambda item: item.itemName, row) for row in grid]
        s = str(list(map(list, temp)))
        file.write(s)

#Converts from something like 4, 2 to D3
def intCoordinateToStrCoordinate(rowCoordinate, colCoordinate):
    rows = "ABCDEFG"
    return rows[rowCoordinate] + str(colCoordinate+1)

#item is a GameItem class
def makeChanges(item, cash, bankAmount, shield, mirror):
    itemName = item.itemName
    
    currentScreen = screen.copy()
    itemMessage = Message(item.itemDescription, 24)
    itemMessage.blit(screen, (windowSize[0]//2 - itemMessage.width//2, windowSize[1]//2 - itemMessage.height//2))
    pause(seconds=1)
    screen.blit(currentScreen, (0, 0))
    
    log([item.itemDescription], "currentGame.txt", cash)
    
    if itemName[0] == "$": #this means the item is either $5000, $3000, $1000 or $200
        value = int(itemName[1:]) #the part after the $, so 5000, 3000, 1000 or 200
        return cash+value, bankAmount, shield, mirror
    elif itemName == "Rob":
        screenBeforeUserInput = screen.copy()
        requestMessage = Message("Please type how much you robbed", 24)
        requestMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
        newField = UserInput(300, 400, numeric=True) #x, y
        amountRobbed = int(newField.takeUserInput(screen))
        screen.blit(screenBeforeUserInput, (0, 0))
        return cash+amountRobbed, bankAmount, shield, mirror
    
    elif itemName == "SwapScore":
        screenBeforeUserInput = screen.copy()
        requestMessage = Message("Please type your opponent's cash", 24)
        requestMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
        newField = UserInput(300, 400, numeric=True) #x, y
        opponentCash = int(newField.takeUserInput(screen))
        screen.blit(screenBeforeUserInput, (0, 0))
        return opponentCash, bankAmount, shield, mirror

    elif itemName == "Bank":
        return 0, cash, shield, mirror
    elif itemName == "Mirror":
        return cash, bankAmount, shield, True
    elif itemName == "Shield":
        return cash, bankAmount, True, mirror
    elif itemName == "LostAtSea":
        #TODO: if user has shield == True or mirror == True, ask user if they would like to use it, 
        return 0, bankAmount, shield, mirror
    elif itemName == "DoubleScore":
        return 2*cash, bankAmount, shield, mirror
    
    #default case - present (which does nothing), sneak peek (again, nothing), choose next square, sink ship, back stab (?)
    return cash, bankAmount, shield, mirror

def updateUI(cash, bankAmount, shield, mirror):
    #TODO: Not working ↓
    region = pygame.Rect((500, 20), (300, 30)) #the square to cover with blue
    screen.fill(colours["sea"], rect=region)
    
    cashButton = Button(colours["green"], 650, 20, text="Cash: %d" % cash, fontSize=24)
    cashButton.draw(screen)
    
    #if bank is not 0, then this game is being continued and not a new game
    if bankAmount != 0: 
        bankButton = Button(colours["green"], 650, 60, text="Bank: %d" % bankAmount, fontSize=24)
        bankButton.draw(screen)

    #Add the shield and mirror icons if they are initialised as True
    shieldButton = Button(colours["green"], 650, 100, image="Images/GameItems/Shield.png", width=80, height=80)
    if shield:
        shieldButton.draw(screen)
    else:
        buttonRegion = pygame.Rect((650, 100), (int(80), int(80))) #TODO: remove hardcoding
        screen.fill(colours["sea"], rect=buttonRegion)
        
    mirrorButton = Button(colours["green"], 650, 190, image="Images/GameItems/Mirror.png", width=80, height=80)
    if mirror:
        mirrorButton.draw(screen)
    else:
        buttonRegion = pygame.Rect((650, 190), (int(80), int(80))) #TODO: remove hardcoding
        screen.fill(colours["sea"], rect=buttonRegion)
    return shieldButton, mirrorButton

def confirm(message):
    currentScreen = screen.copy()
    
    screen.fill(colours["white"])
    confirmMessage = Message(message, 24)
    confirmMessage.blit(screen, (windowSize[0]//2 - confirmMessage.width//2, 200))
    
    yesButton = Button(colours["green"], 'horizontalCentre', 300, text="Yes", widthScale=2, windowSize=windowSize)
    yesButton.draw(screen)
    
    noButton = Button(colours["red"], 'horizontalCentre', 400, text="No", widthScale=2, windowSize=windowSize)
    noButton.draw(screen)
    
    waitingForReply = True
    while waitingForReply:
        clock.tick(5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                if yesButton.isMouseHover(mousePosition):
                    waitingForReply = False
                    screen.blit(currentScreen, (0, 0))
                    return True
                if noButton.isMouseHover(mousePosition):
                    waitingForReply = False
                    screen.blit(currentScreen, (0, 0))
                    return False
        pygame.display.update()
    

#Triggered either by titleScreen -> loadGame or setUpScreen()
def mainScreen(grid, enteredCoordinates, cash, bankAmount, shield, mirror, newGame):        
    if not newGame: #if continuing game, we need to setup
        screen.fill(colours["sea"]) #background blue colour
        
        gridImage = Image("Images/grid.png", size=(460, 460))
        gridImage.blit(screen, pos = (windowSize[0]//2 - gridImage.width//2, windowSize[1]//2 - gridImage.height//2))
    

        xLeft, xRight = 228, 628
        yTop, yBottom = 129, 529
        squareSize = gridImage.width / 8 #the grid has 8 squares, so / 8 will produce the size of each grid.
        
        #Add the game item images to the grid ONLY NECESSARY IF playing via CONTINUE GAME and not setup
        fill = 0.85 #the image will fill 85% of the square
        inset = 1 + ((squareSize * (1-fill)/2))/2/100 #for a square size of 57 and fill of 85%, is 2.15625%%.
        for rowCoordinate, row in enumerate(grid):
            for colCoordinate, element in enumerate(row):
                if intCoordinateToStrCoordinate(rowCoordinate, colCoordinate) not in enteredCoordinates:
                    filename = "Images/GameItems/" + element.itemName + ".png"
                    image = Image(filename, size=(int(squareSize * fill), int(squareSize * fill)))
                    image.blit(screen, pos=(rowCoordinate * squareSize + (inset * xLeft), colCoordinate * squareSize + (inset * yTop)))
        
    # ---------------- Clickable Buttons With Text ---------------
    whatHappenedButton = Button(colours["green"], windowSize[0]//2 - 150, 550, text="What Happened?", fontSize=24)
    whatHappenedButton.draw(screen)
    
    saveGameButton = Button(colours["green"], 20, 20, text="Save Game", fontSize=24)
    saveGameButton.draw(screen)
    
    undoButton = Button(colours["green"], 20, 60, text="Undo Square", fontSize=24)
    undoButton.draw(screen)
    
    #TODO: Display log button
    #If clicked, showLog()
    # ------------------------------------------------------------
    
    shieldButton, mirrorButton = updateUI(cash, bankAmount, shield, mirror)
    oldCash, oldBankAmount, oldShield, oldMirror = cash, bankAmount, shield, mirror
    oldMainScreen = screen.copy()
    saved = False #initially, the game is unsaved
    clickable = False #initially, the user may not enter a square
    undoAllowed = False
    while len(enteredCoordinates) != 49:
        clock.tick(30)

        for event in pygame.event.get():
            mousePosition = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                if not saved and confirm("Would you like to save your game?"):
                    saveGame(grid, enteredCoordinates, cash, bankAmount, shield, mirror)
                    confirmationMessage = Message("Your game was saved!", 24)
                    confirmationMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
                    pause(seconds=2)
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    currentScreen = screen.copy()
                    clickable = True #the user may now click on the grid to remove a square
                     
                    clickMessage = Message("Click on the coordinate that the teacher called out", 24) #TODO: Very annoying? Fix.
                    clickMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
                    pause(seconds=1)
                    screen.blit(currentScreen, (0, 0))
                    
                if event.key == pygame.K_p:
                    pause()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(mousePosition)
                if shieldButton.isMouseHover(mousePosition) and shield == True:
                    if confirm("Use shield?"):
                        shield = False
                        shieldButton, mirrorButton = updateUI(cash, bankAmount, shield, mirror)
                        saved = False
                if mirrorButton.isMouseHover(mousePosition) and mirror == True:
                    if confirm("Use mirror?"):
                        mirror = False
                        shieldButton, mirrorButton = updateUI(cash, bankAmount, shield, mirror)
                        saved = False
                
                if saveGameButton.isMouseHover(mousePosition):
                    saveGame(grid, enteredCoordinates, cash, bankAmount, shield, mirror)
                    screenBeforeSaving = screen.copy()
                    confirmationMessage = Message("Your game was saved!", 24)
                    confirmationMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)
                    pause(seconds=2)
                    screen.blit(screenBeforeSaving, (0, 0))
                    saved = True
                
                if len(enteredCoordinates) != 0 and undoAllowed and undoButton.isMouseHover(mousePosition):
                    screen.blit(oldMainScreen, (0, 0))
                    shieldButton, mirrorButton = updateUI(oldCash, oldBankAmount, oldShield, oldMirror)
                    cash, bankAmount, shield, mirror = oldCash, oldBankAmount, oldShield, oldMirror
                    previousSquare = enteredCoordinates.pop()
                    
                    screenBeforeUndoMessage = screen.copy()
                    undoMessage = Message("{} was reverted!".format(previousSquare), 24)
                    undoMessage.blit(screen, ("horizontalCentre", 200), windowSize=windowSize)   
                    pause(seconds=2)
                    screen.blit(screenBeforeUndoMessage, (0, 0))     
                    undoAllowed = False
                
                #this entire if block is for entering coordinates onto the grid
                if clickable:
                    #TODO: Game logic - don't hard code
                    #244, 126 - - - - - 610, 126
                    #    -    - - - - -     -
                    #    -    - - - - -     -
                    #    -    - - - - -     -
                    #    -    - - - - -     -
                    #    -    - - - - -     -
                    #244, 534 - - - - - 610, 534
                    
                    #if the user presses within the boundaries of the grid
                    if mousePosition[0] > xLeft and mousePosition[0] < xRight and mousePosition[1] > yTop and mousePosition[1] < yBottom:
                        row = int( (mousePosition[0] - xLeft) // ((xRight - xLeft)/7) ) #calculate the row number from 0 - 6
                        col = int( (mousePosition[1] - yTop) // ((yBottom - yTop)/7) ) #calculate the col number from 0 - 6
                        
                        if intCoordinateToStrCoordinate(row, col) not in enteredCoordinates:    
                            undoAllowed = True  
                            oldMainScreen = screen.copy()
                            oldCash, oldBankAmount, oldShield, oldMirror = cash, bankAmount, shield, mirror
                                                  
                            #topLeft corner of the square has the least x and y value
                            top = int(yTop + (col * squareSize))
                            left = int(xLeft + (row * squareSize))
                            region = pygame.Rect((left, top), (int(squareSize), int(squareSize))) #the square to cover with blue
                            screen.fill(colours["sea"], rect=region)
                            
                            cash, bankAmount, shield, mirror = makeChanges(grid[row][col], cash, bankAmount, shield, mirror) #if user lands on cash, increase cash, if user lands on double, double score, etc.
                            shieldButton, mirrorButton = updateUI(cash, bankAmount, shield, mirror)
                            
                            enteredCoordinates.append(intCoordinateToStrCoordinate(row, col))
                            saved = False
                        else: #This square was already played.
                            #Remind the user to click on an empty square
                            currentScreen = screen.copy()
                            
                            warningMessage = Message("Please enter available square", 24, textColour=colours["black"], backgroundColour=colours["red"])
                            warningMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                            pause(seconds=1)
                            screen.blit(currentScreen, (0, 0))
                    else:
                        #Remind the user to click inside the grid only
                        currentScreen = screen.copy()
                        
                        warningMessage = Message("Please click inside the grid", 24, textColour=colours["black"], backgroundColour=colours["red"])
                        warningMessage.blit(screen, ("horizontalCentre", "verticalCentre"), windowSize=windowSize)
                        pause(seconds=1)
                        screen.blit(currentScreen, (0, 0))
                    
                    clickable = False #The user entered a square now, so they are now not allowed to enter again.
        pygame.display.update()
    
    gameOverScreen(cash+bankAmount)
    
def gameOverScreen(score):

    #a+ mode - append AND read file
    with open("recent_scores.txt", "a+") as file:
        #TODO: read in the last 5 lines
        
        today = datetime.date.today()
        formattedDate = today.strftime("%d/%m/%y")
        file.write(formattedDate + "\t" + str(score) + "\n")

if __name__ == "__main__":
    titleScreen()
    #gameOverScreen(6000) 