# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:42:00 2020

@author: Jirka
"""

import math
import random
import time

import pygame
from pygame import mixer

# Otevření knihovny Pygame
pygame.init()

# Vytvoření displeje
screen = pygame.display.set_mode((800, 600))

# Zvuk
mixer.music.load("game_music.wav")
mixer.music.play(-1)

# Název a ikona okna
pygame.display.set_caption("Pizza vs Burger")
icon = pygame.image.load('icon_burger.png')
pygame.display.set_icon(icon)

#Hodiny
clock = pygame.time.Clock()

#Barvy
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

#Délka a šířka displeje
display_width = 800
display_height  = 600

#Směr
direction = "right"

#Fonty
smallfont = pygame.font.SysFont("freesansbold.ttf'", 25)
medfont = pygame.font.SysFont("freesansbold.ttf'", 50)
largefont = pygame.font.SysFont("freesansbold.ttf'", 80)



def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    
    return textSurface, textSurface.get_rect()
    
def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    screen.blit(textSurf, textRect)
    

def game_intro():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
   
        screen.fill(white)
        message_to_screen("Pizza vs Burger",
                          green,
                          -100,
                          "large")
        message_to_screen("Cil hry je vydrzet co nejdele nazivu a strilet burgery",
                          black,
                          -30)
        message_to_screen("Stiskni C pro start nebo Q pro ukonceni.",
                          black,
                          180)
    
        pygame.display.update()
        clock.tick(15)

def pause():

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        screen.fill(white)
        message_to_screen("Paused",
                          black,
                          -100,
                          size="large")

        message_to_screen("Stiskni C pro pokracovani nebo Q pro ukonceni.",
                          black,
                          25)
        pygame.display.update()
        clock.tick(5)

def gameLoop():
    
    gameExit = False
    gameOver = False

        
    # Hráč
    playerImg = pygame.image.load('pizza.png')
    playerX = 370
    playerY = 480
    playerX_change = 0
            
    # Nepřítel
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 1

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('hamburger.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

    # Bullet

    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving

    bulletImg = pygame.image.load('ananas.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    # Skóre

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    textX = 10
    testY = 10
          
    # Pozadí hry
    background = pygame.image.load('kuchyne.jpg')
    screen.fill(white) 
        
    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (0, 0, 0))
        screen.blit(score, (x, y))


    def player(x, y):
        screen.blit(playerImg, (x, y))


    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))


    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))


    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False    
     
        
    while not gameExit:
        
        while gameOver == True:
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
                        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                if event.key == pygame.K_p:
                    pause()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
            
    

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Pohyb nepřátel
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                        enemyY[j] = 2000
                gameOver == False
                
                    

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            # Kolize
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
           
            if collision:
                explosionSound = mixer.Sound("uff.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

            # Pohyb ananasů
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)
        pygame.display.update()
               
    
    pygame.quit()
    quit()

game_intro()
gameLoop()     
       
