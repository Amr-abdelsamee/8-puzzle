import pygame
from agents import *
from puzzle import Puzzle
from copy import copy
from buttons import Button
import time


NUM_BLOCKS = 9
SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH
WHITE = (255, 255, 255)
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 100
SIDES_PADDING = 10
INBTWN_SPACE = 1
PUZZLE_WIDTH = (SCREEN_WIDTH - (2*SIDES_PADDING))
BACK_GRND_COLOR = (255,255,255)
RED = (123,44,130)
bg = pygame.image.load("BG.png")
start_player = False
agent_selected = None
generate_random = False
A_star_type = None
font_size = 50
text_size = 30
padding = 4

def start_window():
    global start_player
    buttons = []
    player_button = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"Play",BACK_GRND_COLOR,font_size)
    player_button.draw(game_screen)
    buttons.append(player_button)
    AI_button = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + BUTTON_HEIGHT + padding, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"AI",BACK_GRND_COLOR,font_size)
    AI_button.draw(game_screen)
    buttons.append(AI_button)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            start_player = True
                            return
                        if i == 1:
                            return
                
            pygame.display.update()
    pygame.quit()

def AI_window():
    game_screen.blit(bg,(0,0))
    global agent_selected
    buttons = []
    BFS = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"BFS",BACK_GRND_COLOR,font_size)
    BFS.draw(game_screen)
    buttons.append(BFS)
    DFS = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + BUTTON_HEIGHT + padding, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"DFS",BACK_GRND_COLOR,font_size)
    DFS.draw(game_screen)
    buttons.append(DFS)
    a_star = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + (2*BUTTON_HEIGHT) + (2*padding), BUTTON_WIDTH,BUTTON_HEIGHT,RED,"A*",BACK_GRND_COLOR,font_size)
    a_star.draw(game_screen)
    buttons.append(a_star)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            agent_selected = 0
                            return
                        if i == 1:
                            agent_selected = 1
                            return
                        if i == 2:
                            agent_selected = 2
                            return
                
            pygame.display.update()
    pygame.quit()

def generating_window():
    game_screen.blit(bg,(0,0))
    global generate_random
    buttons = []
    text = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"Generate the puzzle random?",BACK_GRND_COLOR,text_size)
    text.draw(game_screen)
    YES = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + (BUTTON_HEIGHT)+padding, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"YES",BACK_GRND_COLOR,font_size)
    YES.draw(game_screen)
    buttons.append(YES)
    NO = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + (2*BUTTON_HEIGHT)+(2*padding), BUTTON_WIDTH,BUTTON_HEIGHT,RED,"NO",BACK_GRND_COLOR,font_size)
    NO.draw(game_screen)
    buttons.append(NO)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            generate_random = True
                            return
                        if i == 1:
                            return
                
            pygame.display.update()
    pygame.quit()

def A_Star_window():
    game_screen.blit(bg,(0,0))
    global A_star_type
    buttons = []
    mnha_type = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"Manhaten Type",BACK_GRND_COLOR,text_size)
    mnha_type.draw(game_screen)
    buttons.append(mnha_type)

    eqlid_type = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + BUTTON_HEIGHT + padding, BUTTON_WIDTH,BUTTON_HEIGHT,RED,"Ecledian Type",BACK_GRND_COLOR,text_size)
    eqlid_type.draw(game_screen)
    buttons.append(eqlid_type)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            A_star_type = 1
                            return
                        if i == 1:
                            A_star_type = 0
                            return
                
            pygame.display.update()
    pygame.quit()

pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("BG.png")
game_screen.blit(bg,(0,0))
pygame.display.set_caption("8-puzzle")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)



pygame.display.update()

# 125304678
SOLUTION = '012345678'



# running loop


start_window()

if start_player:
    # generating_window()
    game_screen.blit(bg,(0,0))
    puzzle = Puzzle(NUM_BLOCKS, game_screen)
    
    running = True
    solved = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not solved:
                x_clicked, y_clicked = pygame.mouse.get_pos()
                for i in range(NUM_BLOCKS):
                    if puzzle.blocks[i].check_clicked(x_clicked, y_clicked):
                        if not puzzle.blocks[i].get_label():
                            continue
                        # check_empty_near(i)
                        puzzle.check_empty_near(i)
                        solved = puzzle.check_solved()
                        if solved:
                            witdth = (PUZZLE_WIDTH-(2*INBTWN_SPACE))//3
                            win_text = Button(SIDES_PADDING+ witdth+INBTWN_SPACE, 10, witdth, BUTTON_HEIGHT-60, RED," Game Solved! ",BACK_GRND_COLOR,text_size)
                            win_text.draw(puzzle.screen)
                        # print(valid_moves)
            pygame.display.update()
    pygame.quit()


else:
    AI_window()
    game_screen.blit(bg,(0,0))
    puzzle = None
    
    
    
    # generating_window()game_screen.blit(bg,(0,0))
    if agent_selected != None:
        
        if agent_selected == 0:
            puzzle = Puzzle(NUM_BLOCKS, game_screen)
            labels = ''.join(map(str, puzzle.labels))
            agent = BFS(labels, puzzle.empty_block_index, SOLUTION, puzzle.valid_moves)
        elif agent_selected == 1:
            puzzle = Puzzle(NUM_BLOCKS, game_screen)
            labels = ''.join(map(str, puzzle.labels))
            agent = DFS(labels, puzzle.empty_block_index, SOLUTION, puzzle.valid_moves)
        elif agent_selected == 2:
            A_Star_window()
            game_screen.blit(bg,(0,0))
            puzzle = Puzzle(NUM_BLOCKS, game_screen)
            labels = ''.join(map(str, puzzle.labels))
            agent = AStar(labels, puzzle.empty_block_index, SOLUTION, puzzle.valid_moves, A_star_type)
    
    start = time.time()
    path, moves, depth, no_explored = agent.work()
    end = time.time()

    time_taken = end - start
    print(moves,' ', depth, ' ', time_taken)
    delay = 1

    if moves > 30:
        delay = 0.001
    puzzle.show_solution(moves, delay, path)

    time_taken = round(time_taken, 5)
    witdth = (PUZZLE_WIDTH-(2*INBTWN_SPACE))//3
    time_text = Button(SIDES_PADDING, 10, witdth, BUTTON_HEIGHT-60, RED," Time: "+str(time_taken)+ "s",BACK_GRND_COLOR,text_size-10)
    time_text.draw(puzzle.screen)
    Max_depth_text = Button(SIDES_PADDING+ witdth+INBTWN_SPACE, 10, witdth, BUTTON_HEIGHT-60, RED," Max depth: "+str(depth),BACK_GRND_COLOR,text_size-10)
    Max_depth_text.draw(puzzle.screen)
    total_no_moves_text = Button(SIDES_PADDING+(2*witdth)+(2*INBTWN_SPACE), 10, witdth, BUTTON_HEIGHT-60, RED," # of explored: " + str(no_explored),BACK_GRND_COLOR,text_size-10)
    total_no_moves_text.draw(puzzle.screen)
    total_no_moves_text = Button(SIDES_PADDING, 10+INBTWN_SPACE+BUTTON_HEIGHT-60, witdth, BUTTON_HEIGHT-60, RED," Cost of path: " + str(moves),BACK_GRND_COLOR,text_size-10)
    total_no_moves_text.draw(puzzle.screen)
    pygame.display.update()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

