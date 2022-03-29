import pygame
from agents import *
from puzzle import Puzzle
from buttons import Button
import time

NUM_BLOCKS = 9

PRINT_DELAY = 1

# size constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = SCREEN_WIDTH
SIDES_PADDING = 10
INBTWN_SPACE = 1
PUZZLE_WIDTH = (SCREEN_WIDTH - (2*SIDES_PADDING))

# properties of buttons
# TEXT_COLOR = (150,150,150)
TEXT_COLOR = (255,255,255)
BUTTONS_COLOR = (12,44,130)
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 100
FONT_SIZE1 = 50
FONT_SIZE2 = 30

# back ground color constant
BGROUND_IMG = pygame.image.load("BG.png")

# windows variables
# start_player checks if player or AI
start_player = False
# agent_selected store the selected agent  
agent_selected = None
# A_star_type store the heurestic type
A_star_type = None

# start window contains two buttons play and AI
def start_window():
    global start_player
    buttons = []
    player_button = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," Play",TEXT_COLOR,FONT_SIZE1)
    player_button.draw(game_screen)
    buttons.append(player_button)
    AI_button = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + 50 + BUTTON_HEIGHT + SIDES_PADDING, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," AI",TEXT_COLOR,FONT_SIZE1)
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

# AI window contains three buttons BFS DFS A*
def AI_window():
    game_screen.blit(BGROUND_IMG,(0,0))
    global agent_selected
    buttons = []
    BFS = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," BFS",TEXT_COLOR,FONT_SIZE1)
    BFS.draw(game_screen)
    buttons.append(BFS)
    DFS = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + BUTTON_HEIGHT + SIDES_PADDING, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," DFS",TEXT_COLOR,FONT_SIZE1)
    DFS.draw(game_screen)
    buttons.append(DFS)
    a_star = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + (2*BUTTON_HEIGHT) + (2*SIDES_PADDING), BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," A*",TEXT_COLOR,FONT_SIZE1)
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

# A* winodw contains two buttons  Manhaten Type Ecledian Type
def A_Star_window():
    game_screen.blit(BGROUND_IMG,(0,0))
    global A_star_type
    buttons = []
    mnha_type = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," Manhaten Type",TEXT_COLOR,FONT_SIZE2+5)
    mnha_type.draw(game_screen)
    buttons.append(mnha_type)

    eqlid_type = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + 50 + BUTTON_HEIGHT + SIDES_PADDING, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," Ecledian Type",TEXT_COLOR,FONT_SIZE2+5)
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

# starting the pygame screen
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# draw the background 
game_screen.blit(BGROUND_IMG,(0,0))
# set the title
pygame.display.set_caption("8-puzzle")
# set the logo
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)


start_window()
if start_player:
    # draw the background again for the new window
    game_screen.blit(BGROUND_IMG,(0,0))
    # create a ppuzzle object
    puzzle = Puzzle(NUM_BLOCKS, game_screen)
    
    running = True # running condition
    solved = False # solved condition
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # check if user clicked
            if event.type == pygame.MOUSEBUTTONDOWN and not solved:
                # store the coordinates of the clicked position
                x_clicked, y_clicked = pygame.mouse.get_pos()
                for i in range(NUM_BLOCKS):
                    # get the index of the clicked block in the puzzle
                    if puzzle.blocks[i].check_clicked(x_clicked, y_clicked):
                        # skip if the clicked block is the blank block 
                        if not puzzle.blocks[i].get_label():
                            continue
                        # check is the blank block is near the clicked block
                        puzzle.check_empty_near(i)
                        # check if the puzzle is solved
                        solved = puzzle.check_solved()
                        if solved:
                            # draw winning button 
                            witdth = (PUZZLE_WIDTH-(2*INBTWN_SPACE))//3
                            win_text = Button(SIDES_PADDING + witdth + INBTWN_SPACE, 10, witdth, BUTTON_HEIGHT-60, BUTTONS_COLOR," Game Solved! ",TEXT_COLOR,FONT_SIZE2)
                            win_text.draw(puzzle.screen)
            pygame.display.update()
    pygame.quit()


else:
    AI_window()
    # draw the background again for the new window
    game_screen.blit(BGROUND_IMG,(0,0))
    puzzle = None
    
    if agent_selected != None:
        # create object of the agent depending on the user selection
        if agent_selected == 0:
            puzzle = Puzzle(NUM_BLOCKS, game_screen)
            labels = ''.join(map(str, puzzle.labels))
            SOLUTION = ''.join(puzzle.solution)
            agent = BFS(labels, puzzle.empty_block_index, SOLUTION, puzzle.valid_moves)
        elif agent_selected == 1:
            puzzle = Puzzle(NUM_BLOCKS, game_screen)
            labels = ''.join(map(str, puzzle.labels))
            SOLUTION = ''.join(puzzle.solution)
            agent = DFS(labels, puzzle.empty_block_index, SOLUTION, puzzle.valid_moves)
        elif agent_selected == 2:
            A_Star_window()
            game_screen.blit(BGROUND_IMG,(0,0))
            puzzle = Puzzle(NUM_BLOCKS, game_screen)
            labels = ''.join(map(str, puzzle.labels))
            SOLUTION = ''.join(puzzle.solution)
            agent = AStar(labels, puzzle.empty_block_index, SOLUTION, puzzle.valid_moves, A_star_type)
    
    # start the agent by calling the work method
    start = time.time()
    path, moves, depth, no_explored = agent.work()
    end = time.time()

    time_taken = end - start
    print(moves ,' ', depth, ' ', time_taken)
    
    # handling the print speed depending on the number of moves
    if moves > 20:
        PRINT_DELAY = 10/moves
    if moves > 100:
        PRINT_DELAY = 0
    # show solution method play the agent solution
    puzzle.show_solution(moves, PRINT_DELAY, path)

    # info labels creation
    time_taken = round(time_taken, 5)
    witdth = (PUZZLE_WIDTH-(2*INBTWN_SPACE))//3
    time_text = Button(SIDES_PADDING, 10, witdth, BUTTON_HEIGHT-60, BUTTONS_COLOR," Time: "+str(time_taken)+ "s",TEXT_COLOR,FONT_SIZE2-10)
    time_text.draw(puzzle.screen)
    Max_depth_text = Button(SIDES_PADDING+ witdth+INBTWN_SPACE, 10, witdth, BUTTON_HEIGHT-60, BUTTONS_COLOR," Max depth: "+str(depth),TEXT_COLOR,FONT_SIZE2-10)
    Max_depth_text.draw(puzzle.screen)
    total_no_moves_text = Button(SIDES_PADDING+(2*witdth)+(2*INBTWN_SPACE), 10, witdth, BUTTON_HEIGHT-60, BUTTONS_COLOR," # of explored: " + str(no_explored),TEXT_COLOR,FONT_SIZE2-10)
    total_no_moves_text.draw(puzzle.screen)
    total_no_moves_text = Button(SIDES_PADDING, 10+INBTWN_SPACE+BUTTON_HEIGHT-60, witdth, BUTTON_HEIGHT-60, BUTTONS_COLOR," Cost of path: " + str(moves),TEXT_COLOR,FONT_SIZE2-10)
    total_no_moves_text.draw(puzzle.screen)
    pygame.display.update()

    # wait for user to close the game
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

