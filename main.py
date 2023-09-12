import pygame
from sys import exit
from random import randint

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -=5

            if obstacle_rect.bottom == 300: screen.blit(fire_surf, obstacle_rect)
            else : screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else : return []

def collisions(player,obstacles):
    if obstacles :
        for obstacle_rect in obstacles :
            if player.colliderect(obstacle_rect): return False
    return True

#score
def display_score():

    time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score : {time}',False,('Black'))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return time
#animation
def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.08
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]

#Game window
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Warrior')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0
music = pygame.mixer.Sound('Audio/Music.wav')
music.set_volume(0.2)
music.play(loops = -1)

#Graphics

sky = pygame.image.load('Graphics/Skyy.jpg').convert()
ground = pygame.image.load('Graphics/Ground.jpg').convert()

#Fire
fire_enemy_frame_1 = pygame.image.load('Graphics/Enemies/Enemy_1.png').convert_alpha()
fire_enemy_frame_2 = pygame.image.load('Graphics/Enemies/Enemy_1_Walk.png').convert_alpha()
fire_frames = [fire_enemy_frame_1,fire_enemy_frame_2]
fire_frame_index = 0
fire_surf = fire_frames[fire_frame_index]

#Fireball
fly_frame_1 = pygame.image.load('Graphics/Enemies/Enemy_2.png').convert_alpha()
fly_frame_2 = pygame.image.load('Graphics/Enemies/Enemy_2_Walk.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]
obstacle_rect_list = []

#Player

player_walk_1 = pygame.image.load('Graphics/Player/Player_Walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Graphics/Player/Player_Walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load('Graphics/Player/Player_Walk_2.png').convert_alpha()
player_index = 0

player_surf = player_walk[player_index]

player_rect = player_walk_1.get_rect(topleft = (80,237))
player_gravity = 0

jump_sound = pygame.mixer.Sound('Audio/Jump.mp3')
jump_sound.set_volume(0.3)

#Intro

player_stand = pygame.image.load('Graphics/Player/Player_Walk_1.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Warrior', False, 'Orange')
game_name_rect = game_name.get_rect(center =(400,80))

game_message = test_font.render('Press SPACE for start ', False, 'Red')
game_message_rect = game_message.get_rect(center= (400, 320))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

fire_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fire_animation_timer,250)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,100)

#Game running cycle
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -21.5
                    jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(fire_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

            if event.type == fire_animation_timer:
                if fire_frame_index == 0 : fire_frame_index = 1
                else : fire_frame_index = 0
                fire_surf = fire_frames[fire_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0 : fly_frame_index = 1
                else : fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        # Update display
        screen.blit(sky,(0,-330))
        screen.blit(ground, (0, 300))
        score_surf = display_score()

    #Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300

        player_animation()
        screen.blit(player_surf, player_rect)

    #Enemy movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

    #Collision
        game_active = collisions(player_rect,obstacle_rect_list)

    else :
        screen.fill('Black')
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        score_message = test_font.render(f'Your Score : {score}',False,'Red')
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)

        if score == 0 : screen.blit(game_message,game_message_rect)
        else : screen.blit(score_message,score_message_rect)

#Frame per second
    pygame.display.update()
    clock.tick(60)