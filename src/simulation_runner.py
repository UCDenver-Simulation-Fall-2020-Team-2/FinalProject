from simulation_framework import *
import pygame as pg


# Used to determine how many frames are skipped.
# Helps when you want the gamelogic to move faster than
# Your system can draw it.
SKIP_FRAMES = 0

# Number of frames to draw per second.
FRAMES_PER_SECOND = 5

MAX_GAME_STATES = 200

ARR_GAME_STATES = []

GAME_STATE_INDEX = -1 # Needs to execute one logic tick to create a legitimate game state for the initial GameManager

GLOBAL_TICK = 0

pg.init()


game_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_window.fill(BACKGROUND_COLOR)
pg.display.set_caption('Simulation')


def GameLoop():
    global ARR_GAME_STATES
    global GLOBAL_TICK
    global GAME_STATE_INDEX
    
    paused = False
    restore = True
    
    clock = pg.time.Clock()
    run_game_loop = True
    
    game_manager = GameManager(GAME_GRID_WIDTH, GAME_GRID_HEIGHT)
    
    while run_game_loop:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run_game_loop = False
                if event.key == pg.K_p:
                    restore = True
                    paused = not paused
                if event.key == pg.K_RIGHT and paused:
                    if (GAME_STATE_INDEX < len(ARR_GAME_STATES)-1):
                        GAME_STATE_INDEX += 1
                        restore = True
                    elif (GAME_STATE_INDEX > len(ARR_GAME_STATES)-1):
                        print("ERROR: GAME_STATE_INDEX OOB WITH K_RIGHT")
                        exit(9)
                if event.key == pg.K_LEFT and paused:
                    if (GAME_STATE_INDEX > 0):
                        GAME_STATE_INDEX -= 1
                        restore = True
            # Check to see if the user has requested that the game end.
            if event.type == pg.QUIT:
                run_game_loop = False
                
        if not paused:
            for i in range(SKIP_FRAMES + 1):
                # CALL YOUR CODE HERE!
                player_move = None
                # CALL YOUR CODE HERE!
                if (GAME_STATE_INDEX < len(ARR_GAME_STATES)-1):
                    restored_state = ARR_GAME_STATES[GAME_STATE_INDEX][1]
                    game_manager = restored_state.restore()
                    GAME_STATE_INDEX += 1
                else:
                    game_manager.logicTick(player_move)
                    if (len(ARR_GAME_STATES) < MAX_GAME_STATES):
                        GAME_STATE_INDEX += 1
                    GLOBAL_TICK += 1     
                    if (len(ARR_GAME_STATES) == MAX_GAME_STATES):
                        ARR_GAME_STATES.pop(0)
                    ARR_GAME_STATES.append((GLOBAL_TICK, GameState(game_manager)))
        else:
            if restore and GAME_STATE_INDEX <= len(ARR_GAME_STATES)-1:
                restore = False
                restored_state = ARR_GAME_STATES[GAME_STATE_INDEX][1]
                game_manager = restored_state.restore()
            #print(f"Restoring state: {restored_state}")
            #print(f"Game manager: {game_manager}")
            
        print(f"Index: {GAME_STATE_INDEX}")
        game_window.fill(BACKGROUND_COLOR)
        game_manager.draw(game_window)
        pg.display.flip()        
        
        delta_time = clock.tick(FRAMES_PER_SECOND)
    
            
    pg.display.quit()
    pg.quit()


GameLoop()
