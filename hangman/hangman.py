import pygame, sys, random
from time import sleep
from pygame.locals import *
from timeit import default_timer as timer
from pygame import mixer

fps = 30
pygame.init()
width = 1080
height = 605
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hangman!")
#background
bg = pygame.image.load('bgP.jpeg')
bg = pygame.transform.scale(bg,(width,height))
bg2 = pygame.image.load('bg2.jpg')
bg2 = pygame.transform.scale(bg2,(width,height))
bg3 = pygame.image.load('losebg.jpg')
bg3 = pygame.transform.scale(bg3,(1000,500))
bg4 = pygame.image.load('winbg.jpg')
bg4 = pygame.transform.scale(bg4,(1000,500))
#title
title = pygame.image.load('title.png')
title.convert()
title =pygame.transform.scale(title, (400, 400))
#gameover
gameover = pygame.image.load('gameover.png')
gameover.convert()
gameover =pygame.transform.scale(gameover, (400, 100))
#gamewin
correct = pygame.image.load('correct.png')
correct.convert()
correct =pygame.transform.scale(correct, (400, 400))
#load images
vtitle = pygame.image.load('videotitle.png')
vtitle.convert()
vtitle =pygame.transform.scale(vtitle, (300, 90))

gtitle = pygame.image.load('graphictitle.png')
gtitle.convert()
gtitle =pygame.transform.scale(gtitle, (300, 90))

stitle = pygame.image.load('soundtitle.png')
stitle.convert()
stitle =pygame.transform.scale(stitle, (300, 90))

ttitle = pygame.image.load('texttitle.png')
ttitle.convert()
ttitle =pygame.transform.scale(ttitle, (300, 90))

#add background music
mixer.init()
mixer.music.load('bgmusic.mp3')
mixer.music.play(-1) #-1 to loop audio
mixer.music.set_volume(0.5) #set volume for audio (0.0-1.0)

#colors
black = (0,0,0)
lightpurple = (238,210,238)
lightred = (255, 165, 145)
darklightred = (255, 97, 81)
lightblue = (126,178,255)
darklightblue = (42, 129, 255)
lightgrey = (192, 192, 192)

textBoxSpace = 5
textBoxNumber = 0

#Button
#load button images
vidimg = pygame.image.load('video.png').convert_alpha()
soundimg = pygame.image.load('sound.png').convert_alpha()
textimg = pygame.image.load('text.png').convert_alpha()
gpimg = pygame.image.load('graphic.png').convert_alpha()
quitimg = pygame.image.load('quit.png').convert_alpha()
yesimg = pygame.image.load('yes.png').convert_alpha()
noimg = pygame.image.load('no.png').convert_alpha()
contimg = pygame.image.load('continue.png').convert_alpha()
backimg = pygame.image.load('back.png').convert_alpha()
#button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        action = False
        
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #0 for right click
                self.clicked = True
                action = True
        
        #so that the button can be click again
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

#create button instances
#(x, y, img)
videobt = Button(80, 400, vidimg)
soundbt = Button(830, 400, soundimg)
textbt = Button(830, 100, textimg)
gpbt = Button(80, 100, gpimg)
quitbt = Button(450, 500, quitimg)
yesbt = Button(300, 400, yesimg)
nobt = Button(600, 405, noimg)
contbt = Button(450, 500, contimg)
backbt = Button(830, 500, backimg)

def endGame():
    global textBoxSpace, textBoxNumber, end, start
    end = timer()
    #gameover
    screen.blit(bg3,(40, 50))
    screen.blit(gameover,(350, 250))

    print("Time it took: ",end - start)
    timeTaken = (end - start)
    textBoxSpace = 5
    textBoxNumber = 0
    message = "Time taken: " + str(round(timeTaken)) + "s"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if quitbt.draw():        
            quitGame()
        if backbt.draw():        
            hangman()

        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf = largeText.render(message,True,darklightred)
        textRect = TextSurf.get_rect()
        textRect.center = (width/2,200)
        screen.blit(TextSurf, textRect)

        message2 = "The word was " + pick
        TextSurf = largeText.render(message2,True,darklightred)
        TextRect = TextSurf.get_rect()
        TextRect.center = (width / 2,400)
        screen.blit(TextSurf, TextRect)
        
        pygame.display.update()
        clock.tick(fps)

def winGame(category,title):
    global textBoxSpace, textBoxNumber, end, start
    end = timer()
    #gameover
    screen.blit(bg4,(40, 50))
    screen.blit(correct,(350, 100))

    print("Time it took: ",end - start)
    timeTaken = (end - start)
    textBoxSpace = 5
    textBoxNumber = 0
    message = "Time taken: " + str(round(timeTaken)) + "s"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if contbt.draw():        
            hangmanGame(category,title)
        if backbt.draw():        
            hangman()

        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf = largeText.render(message,True,darklightred)
        textRect = TextSurf.get_rect()
        textRect.center = (width/2,200)
        screen.blit(TextSurf, textRect)

        message2 = "The word is " + " ' " + pick + " ' "
        TextSurf = largeText.render(message2,True,darklightred)
        TextRect = TextSurf.get_rect()
        TextRect.center = (width / 2,400)
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(fps)

def quitGame():
    pygame.quit()
    sys.exit()


def textObjects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
    
def main():
    global clock, screen, play
    play = True
    clock = pygame.time.Clock()

    while True:
        hangman()

def placeLetter(letter):
    global pick, pickSplit
    space = 10
    wordSpace = 0
    while wordSpace < len(pick):
        text = pygame.font.Font('freesansbold.ttf',40)
        if letter in pickSplit[wordSpace]:
            textSurf = text.render(letter,True,black)
            textRect = textSurf.get_rect()
            textRect.center = (((150)+space),(200))
            screen.blit(textSurf, textRect)
        wordSpace += 1
        space += 60

    pygame.display.update()
    clock.tick(fps)
        
def textBoxLetter(letter):
    global textBoxSpace, textBoxNumber
    if textBoxNumber <= 5:
        text = pygame.font.Font("freesansbold.ttf",40)
        textSurf = text.render(letter,True,black)
        textRect = textSurf.get_rect()
        textRect.center = (((105)+textBoxSpace),(350))
        screen.blit(textSurf, textRect)

    elif textBoxNumber <= 10:
        text = pygame.font.Font("freesansbold.ttf",40)
        textSurf = text.render(letter,True,black)
        textRect = textSurf.get_rect()
        textRect.center = (((105)+textBoxSpace),(400))
        screen.blit(textSurf, textRect)

    elif textBoxNumber <= 15:
        text = pygame.font.Font("freesansbold.ttf",40)
        textSurf = text.render(letter,True,black)
        textRect = textSurf.get_rect()
        textRect.center = (((105)+textBoxSpace),(450))
        screen.blit(textSurf, textRect)

    elif textBoxNumber <= 20:
        text = pygame.font.Font("freesansbold.ttf",40)
        textSurf = text.render(letter,True,black)
        textRect = textSurf.get_rect()
        textRect.center = (((105)+textBoxSpace),(500))
        screen.blit(textSurf, textRect)  
        
    pygame.display.update()
    clock.tick(fps)

#start screen
def hangman():
    i=0
    while play == True:
        clock.tick(fps)
        #background
        screen.fill((0,0,0))
        screen.blit(bg,(i,0))
        screen.blit(bg,(width+i,0))

        if (i == -width):
            screen.blit(bg,(width+i,0))
            i=0
        i-=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #title
        screen.blit(title,(350, 100))

        if videobt.draw():        
            Video()
        if soundbt.draw():
            Sound()
        if gpbt.draw():
            Graphic()
        if textbt.draw():
            Text()
        if quitbt.draw():
            quitGame()
   
        pygame.display.update()

def hangmanGame(category,title):
    global puase, pick, pickSplit, textBoxSpace, textBoxNumber, start
    start = timer()
    chances = 20
    pick = random.choice(category)
    pickSplit = [pick[i:i+1] for i in range(0, len(pick), 1)]
    
    screen.fill((0,0,0))
    screen.blit(bg2,(0,0))
    
    wordSpace = 0
    space = 10
    while wordSpace < len(pick):
        text = pygame.font.Font("freesansbold.ttf",40)
        textSurf1 = text.render("_",True,black)
        textRect1 = textSurf1.get_rect()
        textRect1.center = (((150)+space),(200))
        screen.blit(textSurf1, textRect1)
        space = space + 60
        wordSpace += 1
            
    guesses = ''
    gamePlay = True
    while gamePlay == True:
        guessLett = ''

        if textBoxNumber == 5:
            textBoxSpace = 5
        if textBoxNumber == 10:
            textBoxSpace = 5
        if textBoxNumber == 15:
            textBoxSpace = 5

        pygame.draw.rect(screen, lightpurple, [750,20,200,20]) #chance box
        text = pygame.font.Font("freesansbold.ttf",20)
        textSurf = text.render(("Chances: %s" % chances),False,black)
        textRect = textSurf.get_rect()
        textRect.topright = (900,20) #word coordinate
        screen.blit(textSurf, textRect)

        message = "Tried Alphabets"
        text = pygame.font.SysFont("comicsansms",25)
        TextSurf = text.render(message,True,black)
        textRect = TextSurf.get_rect()
        textRect.center = (220,270)
        screen.blit(TextSurf, textRect)

        #man mesagge
        message7 = "Man:"
        text = pygame.font.SysFont("comicsansms",25)
        TextSurf = text.render(message7,True,black)
        textRect = TextSurf.get_rect()
        textRect.center = (770,120)
        screen.blit(TextSurf, textRect)
        message3 = "Please save me!!"
        text = pygame.font.SysFont("comicsansms",25)
        TextSurf = text.render(message3,True,black)
        textRect = TextSurf.get_rect()
        textRect.center = (850,145)
        screen.blit(TextSurf, textRect)
        message4 = "Use the keyboard to"
        text = pygame.font.SysFont("comicsansms",25)
        TextSurf = text.render(message4,True,black)
        textRect = TextSurf.get_rect()
        textRect.center = (875,195)
        screen.blit(TextSurf, textRect)
        message5 ="keyin the correct word."
        text = pygame.font.SysFont("comicsansms",25)
        TextSurf = text.render(message5,True,black)
        textRect = TextSurf.get_rect()
        textRect.center = (895,220)
        screen.blit(TextSurf, textRect)
        message6 = " You only have 20 chances."
        text = pygame.font.SysFont("comicsansms",25)
        TextSurf = text.render(message6,True,black)
        textRect = TextSurf.get_rect()
        textRect.center = (900,270)
        screen.blit(TextSurf, textRect)
        message8 = "Try to avoid pressing "
        text = pygame.font.SysFont("comicsansms",25)
        TextSurf = text.render(message8,True,black)
        textRect = TextSurf.get_rect()
        textRect.center = (880,320)
        screen.blit(TextSurf, textRect)
        message9 = "the same alphabet."
        text = pygame.font.SysFont("comicsansms",25)
        TextSurf = text.render(message9,True,black)
        textRect = TextSurf.get_rect()
        textRect.center = (870,345)
        screen.blit(TextSurf, textRect)
        

        if title == 'Video':
            screen.blit(vtitle,(400, 10))
        if title == 'Sound':
            screen.blit(stitle,(400, 10))
        if title == 'Graphic':
            screen.blit(gtitle,(400, 10))
        if title == 'Text':
            screen.blit(ttitle,(400, 10))

        pygame.draw.rect(screen, black, [100,300,250,250],2)

        if chances == 19:
            pygame.draw.rect(screen,black,[450,550,100,10])
        elif chances == 18:
            pygame.draw.rect(screen,black,[550,550,100,10])
        elif chances == 17:
            pygame.draw.rect(screen,black,[650,550,100,10])
        elif chances == 16:
            pygame.draw.rect(screen,black,[500,450,10,100])
        elif chances == 15:
            pygame.draw.rect(screen,black,[500,350,10,100])
        elif chances == 14:
            pygame.draw.rect(screen,black,[500,250,10,100])
        elif chances == 13:
            pygame.draw.rect(screen,black,[500,250,150,10])
        elif chances == 12:
            pygame.draw.rect(screen,black,[600,250,100,10])
        elif chances == 11:
            pygame.draw.rect(screen,black,[600,250,10,50])
        elif chances == 10:
            pygame.draw.line(screen,black,[505,505],[550,550],10)
        elif chances == 9:
            pygame.draw.line(screen,black,[550,250],[505,295],10)
        elif chances == 8:
            pygame.draw.line(screen,black,[505,505],[460,550],10)
        elif chances == 7:
            pygame.draw.circle(screen,black,[605,325],30)
        elif chances == 6:
            pygame.draw.rect(screen,black,[600,350,10,60])
        elif chances == 5:
            pygame.draw.rect(screen,black,[600,410,10,60])
        elif chances == 4:
            pygame.draw.line(screen,black,[605,375],[550,395],10)
        elif chances == 3:
            pygame.draw.line(screen,black,[605,375],[650,395],10)
        elif chances == 2:
            pygame.draw.line(screen,black,[605,465],[550,485],10)
        elif chances == 1:
            pygame.draw.line(screen,black,[605,465],[650,485],10)

        if backbt.draw():        
            hangman()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                failed = 0
                print("Failed",failed)
                print("Chance", chances)
                    
                if event.key == pygame.K_ESCAPE:
                    gamePlay = False
                    
                if event.key == pygame.K_a:
#letter a
                    guessLett = guessLett + 'a'
                    guesses += guessLett
                    print("letter a guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('a')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('a')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_b:
#letter b
                    guessLett = guessLett + 'b'
                    guesses += guessLett
                    print("letter b guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('b')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('b')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_c:
#letter c
                    guessLett = guessLett + 'c'
                    guesses += guessLett
                    print("letter c guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('c')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('c')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_d:
#letter d
                    guessLett = guessLett + 'd'
                    guesses += guessLett
                    print("letter d guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('d')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('d')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_e:
#letter e
                    guessLett = guessLett + 'e'
                    guesses += guessLett
                    print("letter e guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('e')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('e')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_f:
#letter f
                    guessLett = guessLett + 'f'
                    guesses += guessLett
                    print("letter f guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('f')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('f')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_g:
#letter g
                    guessLett = guessLett + 'g'
                    guesses += guessLett
                    print("letter g guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('g')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('g')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_h:
#letter h
                    guessLett = guessLett + 'h'
                    guesses += guessLett
                    print("letter h guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('h')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('h')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_i:
#letter i
                    guessLett = guessLett + 'i'
                    guesses += guessLett
                    print("letter i guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('i')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('i')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_j:
#letter j
                    guessLett = guessLett + 'j'
                    guesses += guessLett
                    print("letter j guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('j')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        #gamePlay = False
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('j')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        #gamePlay = False
                        endGame()
                            
                if event.key == pygame.K_k:
#letter k
                    guessLett = guessLett + 'k'
                    guesses += guessLett
                    print("letter k guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('k')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('k')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_l:
#letter l
                    guessLett = guessLett + 'l'
                    guesses += guessLett
                    print("letter l guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('l')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('l')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_m:
#letter m
                    guessLett = guessLett + 'm'
                    guesses += guessLett
                    print("letter m guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('m')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('m')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_n:
#letter n
                    guessLett = guessLett + 'n'
                    guesses += guessLett
                    print("letter n guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('n')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        #gamePlay = False
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('n')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        #gamePlay = False
                        endGame()
                            
                if event.key == pygame.K_o:
#letter o
                    guessLett = guessLett + 'o'
                    guesses += guessLett
                    print("letter o guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('o')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('o')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_p:
#letter p
                    guessLett = guessLett + 'p'
                    guesses += guessLett
                    print("letter p guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('p')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('p')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_q:
#letter q
                    guessLett = guessLett + 'q'
                    guesses += guessLett
                    print("letter q guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('a')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('q')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_r:
#letter r
                    guessLett = guessLett + 'r'
                    guesses += guessLett
                    print("letter r guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('r')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('r')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_s:
#letter s
                    guessLett = guessLett + 's'
                    guesses += guessLett
                    print("letter s guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('s')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('s')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_t:
#letter t
                    guessLett = guessLett + 't'
                    guesses += guessLett
                    print("letter t guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('t')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('t')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_u:
#letter u
                    guessLett = guessLett + 'u'
                    guesses += guessLett
                    print("letter u guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1
                    if guessLett in pick:
                        placeLetter('u')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('u')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_v:
#letter v
                    guessLett = guessLett + 'v'
                    guesses += guessLett
                    print("letter v guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('v')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('v')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_w:
#letter w
                    guessLett = guessLett + 'w'
                    guesses += guessLett
                    print("letter w guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('w')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('w')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                            
                if event.key == pygame.K_x:
#letter x
                    guessLett = guessLett + 'x'
                    guesses += guessLett
                    print("letter x guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1
                    if guessLett in pick:
                        placeLetter('x')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('x')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                    
                if event.key == pygame.K_y:
#letter y
                    guessLett = guessLett + 'y'
                    guesses += guessLett
                    print("letter y guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('y')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)
                    

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('y')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()
                    
                if event.key == pygame.K_z:
#letter z
                    guessLett = guessLett + 'z'
                    guesses += guessLett
                    print("letter z guessed")
                    print("")
                    for char in pick:
                        if char in guesses:
                            print(char)
                        else:
                            print("_")
                            failed += 1

                    if guessLett in pick:
                        placeLetter('z')
            
                    if failed == 0:
                        print("You got the word")
                        print(pick)
                        winGame(category,title)

                    if guessLett not in pick:
                        textBoxSpace += 40
                        textBoxNumber += 1
                        chances = chances - 1
                        print("")
                        print(textBoxNumber)
                        print("")
                        print("That letter is not in the word")
                        textBoxLetter('z')

                    if chances == 0:
                        print("Sorry you have lost")
                        print("The word was",pick)
                        endGame()

        pygame.display.update()
        clock.tick(fps)

def Video():
    video = ['mov','swf','flv','avi','mpeg']
    print("video")
    title = "Video"
    hangmanGame(video,title)

def Sound():
    sound = ['wav','acc','ogg','midi','aif']
    print("sound")
    title = "Sound"
    hangmanGame(sound,title)
    
def Graphic():
    graphic = ['jpeg','gif','png','jpg','psd']
    print("graphic")
    title = "Graphic"
    hangmanGame(graphic,title)
    
def Text():
    text = ['html','txt','docx','rtf','wpd']
    print("text")
    title = "Text"
    hangmanGame(text,title)

    
if __name__ == '__main__':
    main()