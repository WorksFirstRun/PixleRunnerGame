import sys

import pygame
from random import randint
from sys import exit

"""
Author : Mohamed Adel
Version : version 2
Requirements : pygame library 

"""


SCREEN_HIGHT = 600
SCREEN_WIDTH = 1200

pygame.init()

WIN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT)) # init the screen
COLOR = 'Gray' # White color

pygame.display.set_caption("Pixel Runner") # display caption for the game

Score_Variable = 0

text_font = pygame.font.Font(None,size = 50) # Any text font

#Score_Text = text_font.render(f" Score : {Score_Variable} ",False,'Black') # Text
#Score_Text_Rect = Score_Text.get_rect(topright = (1200,5)) # text Rect

Game_Over_text = text_font.render("Game Over to start again press E",False,'Black')
Game_over_Rect = Game_Over_text.get_rect(center = (600,300))


Surface2 = pygame.transform.scale(pygame.image.load('Images/ground.png').convert() , (1600,169)) # render Ground
Ground_Rect = Surface2.get_rect(midbottom = (400,666)) # Ground Rect

back_ground = pygame.transform.scale(pygame.image.load('Images/Sky.png'),(1200,600))

Surface1 = pygame.image.load('Images/snail1.png').convert_alpha() # obstacles
Fly = pygame.image.load('Images/Fly1.png').convert_alpha() # fly


Player_jumping = pygame.transform.scale(pygame.image.load('Images/Kareem_Maged_jumping.png') , (100,100))
Player_Standing = pygame.transform.scale(pygame.image.load('Images/Kareem_Maged_standing.png') , (100,100))

Player_1 = Player_Standing # Player


Player_1_Rect = Player_1.get_rect(midbottom = (70,500)) # Player Rect


# physics
Gravity = 1
Velocity = 0

# Timer

Enimes_Spawn_Timer = pygame.USEREVENT + 1
pygame.time.set_timer(Enimes_Spawn_Timer,850)
Clock = pygame.time.Clock() # Clock obj

# Enimes
Enimes_list = []

def moving(Box_Rect): # Moving BoX function
    Flag_Remove = False
    Box_Rect.x -= 10
    global Score_Variable
    if Box_Rect.x < -100:
        Score_Variable +=1
        Flag_Remove = True
    if Flag_Remove:
        return Box_Rect , Flag_Remove
    return Box_Rect , None

def player_moving(Player_Rect):
    global Gravity
    global  Velocity
    if Player_Rect.bottom >= 500:
        Player_Rect.bottom = 500
        Velocity = 0
    keys = pygame.key.get_pressed()
    Mouse = pygame.mouse.get_pressed()

    if keys[pygame.K_SPACE] and Player_Rect.bottom == 500:
        Velocity -=21

    Velocity += Gravity
    Player_Rect.y +=Velocity


def Spawning_Enimes(Enimes_list):
    updated_list = []
    removing_indexes = []
    if len(Enimes_list) == 0:
        return updated_list
    for i in range(0,len(Enimes_list)):
        result_of_moving = moving(Enimes_list[i])
        if result_of_moving[1]:
            removing_indexes.append(i)
            continue
        updated_list.append(result_of_moving[0])

    for i in range(0,len(removing_indexes)):
        Enimes_list.pop(removing_indexes[i])
    return updated_list

def interactions(Enimes_list ,resetbox = False , resetplayer = False):
    global Score_Variable
    if len(Enimes_list) == 0 :
        return True
    if resetbox and resetplayer :
        Player_1_Rect.y = 500
        Enimes_list.clear()
        Score_Variable = 0
    for i in range (0,len(Enimes_list)):
        if Player_1_Rect.colliderect(Enimes_list[i]):
            return False
    else:
        return True


def update(Enimes_list):
        global Player_1
        WIN.blit(back_ground,(0,0))
        for i in range (0,len(Enimes_list)):
            if Enimes_list[i].y >= 450:
                WIN.blit(Surface1,Enimes_list[i])
            else:
                WIN.blit(Fly,Enimes_list[i])
        WIN.blit(Surface2,Ground_Rect) # Ground
        if Player_1_Rect.bottom < 500:
            Player_1 = Player_jumping
        if Player_1_Rect.bottom >= 500:
            Player_1 = Player_Standing
        WIN.blit(Player_1,Player_1_Rect)
        Score_Text = text_font.render(f" Score : {Score_Variable} ", False, 'Black')  # Text
        Score_Text_Rect = Score_Text.get_rect(topright=(1200, 5))
        pygame.draw.rect(WIN, 'Yellow', Score_Text_Rect)
        WIN.blit(Score_Text, Score_Text_Rect)
        pygame.display.update()





def main():
    Game_stat = True
    global Enimes_list
    while True:
        keys = pygame.key.get_pressed()
        Clock.tick(60) # delay the while loop to run at 60 fps

        Game_stat = interactions(Enimes_list)
        if Game_stat:
            player_moving(Player_1_Rect)
            Enimes_list = Spawning_Enimes(Enimes_list)

            update(Enimes_list) # update screen


        elif not Game_stat:
            pygame.draw.rect(WIN,"Red",Game_over_Rect)
            WIN.blit(Game_Over_text,Game_over_Rect)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                interactions(Enimes_list,True,True)
            if  event.type == Enimes_Spawn_Timer:
                pygame.time.set_timer(Enimes_Spawn_Timer, randint(850, 1300))
                alternate = randint(0,2)
                if alternate:
                    Enimes_list.append(Surface1.get_rect(midbottom = (randint(1300,1350), 500)))
                else:
                    Enimes_list.append(Fly.get_rect(midbottom = (randint(1300,1350), 400 )))





if __name__ == "__main__":
    main()