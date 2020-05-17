
import pygame
import random
import math
from pygame import mixer


# Initialzing the pygame package
pygame.init()

# Creating the gaming window
window = pygame.display.set_mode((800,600))

# Background Image
background = pygame.image.load('Space-PNG-Pic.png')

# Background music
# Adding background music 'background.wav' to the game
mixer.music.load('background.wav')
mixer.music.play(-1)                                                                                            # plays the music in the infinite loop

# Title and Icon
pygame.display.set_caption('Game 1')                                                                            # setting name to the gaming window
icon = pygame.image.load('spaceship.png')                                                                       # loading the image into the variable 'icon'
pygame.display.set_icon(icon)                                                                                   # setting the new image as icon

# Player
PlayerImg = pygame.image.load('game.png')                                                                       # loading the player image(ie, the space battleship)
Xcord = 370
Ycord = 480
Xdel = 0

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 26)
textx = 10                                                                                                      # X-coordinate of the score
texty = 10                                                                                                      # Y-coordinate of the score

# Game over
game_over = pygame.font.Font('freesansbold.ttf', 250)

# Multiple Enemies
EnemyImg = []
EnemyXcord = []
EnemyYcord = []
num_of_enemies = 6

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('halloween.png'))
    EnemyXcord.append(random.randint(0,768))                                                                              # assigning a random  x-coordinate to the enemy
    EnemyYcord.append(random.randint(32,200))                                                                             # assigning a random y- coordinate to the enemy
    Enemydel = 1


# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletXcord = 0                                                                             # assigning a random  x-coordinate to the enemy
bulletYcord = 480                                                                             # assigning a random y- coordinate to the enemy
bulletdel = 10
bullet_state = 'ready'

# Functions
# To display the score on the gaming screen
def show_score(x, y):
    sc = font.render('Score : ' + str(score), True, (255,255,255))
    window.blit(sc, (x, y))
    return

def game_over():
    text = font.render('GAME OVER !!', True, (255, 255, 255))
    window.blit(text, (300, 250))
    return

# To place the player image on the gaming window
def player(x, y):
    window.blit(PlayerImg, (x, y))                                                                                # draws/places the player image on the gaming window
    return

# To place the enemies on the gaming window
def enemy(x, y, i):
    window.blit(EnemyImg[i], (x, y))
    return

# To place the bullets on the gaming window
def bullet_fire(x, y):
    global bullet_state
    window.blit(bulletImg, (x, y))
    return

# To determine collision
def collison(x2, x1, y2, y1):
    dist = math.sqrt((math.pow((x2 - x1),2))+(math.pow((y2 - y1),2)))

    if dist <= 17:
        return True
    else:
        return False


# Main running loop of the program
running = True

while running:                                                                                                  # infinite running loop
    window.fill((32, 32, 32))                                                                                   # setting the background with (R,G,B) code

    window.blit(background, (0, 0))

    for event in pygame.event.get():                                                                            # checks for python event
        if event.type == pygame.QUIT:                                                                           # checks for the closing of window
            running = False

        # event to check if a key is pressed
        if event.type == pygame.KEYDOWN:
            # event to check if the left arrow key is pressed
            if event.key == pygame.K_LEFT:
                Xdel = -2                                                                                     # calling the key_press_left() to move the player to the left

            # event to check if the right arrow key is pressed
            if event.key == pygame.K_RIGHT:
                Xdel = 2                                                                                      # calling the key_press_right() to move the player to the right

            #event to fire the bullet
            if event.key == pygame.K_SPACE:
                # Plays the bullet firing sound
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()

                # Fires the bullet
                bullet_state = 'fire'
                bulletXcord = Xcord

            # event to check the release of keys
        if event.type == pygame.KEYUP:
            # event to check if the left or right arrow key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Xdel = 0

            # if event.key == pygame.K_SPACE:
            #     bullet_state = 'ready'

    Xcord += Xdel
    # Checking boundary conditions for the player
    # so that the player does not go outside the gaming window
    if Xcord <= 0:
        Xcord = 0

    elif Xcord >= 768:
        Xcord = 768

    # Enemy movement
    for i in range(num_of_enemies):

        if EnemyYcord[i] > 460:
            for j in range(num_of_enemies):
                EnemyYcord[j] = 2000
            game_over()
            break

        EnemyXcord[i] += Enemydel
        # when the enemy hits the left boundary, it reverses its direction
        # at the same time, it steps down in the y-axis too
        if EnemyXcord[i] <= 0:
            Enemydel = 1
            EnemyYcord[i] += 10

        elif EnemyXcord[i] >= 768:
            Enemydel = -1
            EnemyYcord[i] += 10

        # Collision
        collision = collison(EnemyXcord[i], bulletXcord, EnemyYcord[i], bulletYcord)

        if collision:
            # Plays the explosion sound
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()

            #Setting the bullet to fire again for next time
            bullet_state = 'ready'
            bulletYcord = 480
            score += 1

            # Respawning the enemy
            EnemyXcord[i] = random.randint(0, 768)                                                            # assigning a random  x-coordinate to the enemy
            EnemyYcord[i] = random.randint(32, 200)


        enemy(EnemyXcord[i], EnemyYcord[i], i)


    # Bullet movement
    if bullet_state == 'fire':
        bulletYcord -= bulletdel
        # Checking bullet boundary conditions
        # and to fire multiple bullets
        if bulletYcord <= 0:
            bullet_state = 'ready'
            bulletYcord = 480
        bullet_fire(bulletXcord, bulletYcord)




    player(Xcord, Ycord)                                                                                          # calls the player()
    show_score(textx, texty)                                                                                      # calls the function to display the score on the gaming window
    pygame.display.update()                                                                                      # updating the window so that the changes are visible