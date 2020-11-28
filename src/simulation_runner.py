from simulation_framework import *
import pygame as pg


# Used to determine how many frames are skipped.
# Helps when you want the gamelogic to move faster than
# Your system can draw it.
SKIP_FRAMES = 0

# Number of frames to draw per second.
FRAMES_PER_SECOND = 50

FPS_LIST = [5,10,50,100,150]

FPS_SELECTION = 4
MAX_GAME_STATES = 200

ARR_GAME_STATES = []

GAME_STATE_INDEX = -1 # Needs to execute one logic tick to create a legitimate game state for the initial GameManager

GLOBAL_TICK = 0

SAVE_STATES = False

TURN_VIEW = True

pg.init()
game_manager = None

game_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_window.fill(BACKGROUND_COLOR)
pg.display.set_caption('Simulation')

clock = pg.time.Clock()

run_game_loop = True
paused = False
restore = True

def incFPS():
    global FPS_SELECTION
    FPS_SELECTION += 1
    if FPS_SELECTION >= len(FPS_LIST):
        FPS_SELECTION = 0

def globalDraw():
    global game_window
    global game_manager
    global clock
    
    game_window.fill(BACKGROUND_COLOR)
    game_manager.draw(game_window)
    pg.display.flip()
    
    delta_time = clock.tick(FPS_LIST[FPS_SELECTION])
    check_events()

def progressState():
    global ARR_GAME_STATES
    global GLOBAL_TICK
    global GAME_STATE_INDEX
    global game_manager

    if GLOBAL_TICK > 1 and TURN_VIEW:
        game_manager.logicTick(draw_func=globalDraw)
    else:
        game_manager.logicTick()
    
    GLOBAL_TICK += 1     
    
    if SAVE_STATES:
        if (len(ARR_GAME_STATES) < MAX_GAME_STATES):
            GAME_STATE_INDEX += 1
        
        if (len(ARR_GAME_STATES) == MAX_GAME_STATES):
            ARR_GAME_STATES.pop(0)
        ARR_GAME_STATES.append((GLOBAL_TICK, GameState(game_manager)))

def rewindState():
    global ARR_GAME_STATES
    global GLOBAL_TICK
    global GAME_STATE_INDEX
    global game_manager
    if SAVE_STATES:
        restored_state = ARR_GAME_STATES[GAME_STATE_INDEX][1]
        game_manager = restored_state.restore()
        GAME_STATE_INDEX += 1

def check_events():
    global run_game_loop
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run_game_loop = False
            if event.key == pg.K_f:
                incFPS()
            if event.key == pg.K_p:
                if SAVE_STATES:
                    restore = True
                paused = not paused
            if event.key == pg.K_RIGHT and paused:
                if SAVE_STATES:
                    if (GAME_STATE_INDEX < len(ARR_GAME_STATES)-1):
                        GAME_STATE_INDEX += 1
                        restore = True
                    elif (GAME_STATE_INDEX > len(ARR_GAME_STATES)-1):
                        print("ERROR: GAME_STATE_INDEX OOB WITH K_RIGHT")
                        exit(9)
                else:
                    progressState()
    
            if event.key == pg.K_LEFT and paused:
                if (GAME_STATE_INDEX > 0):
                    GAME_STATE_INDEX -= 1
                    restore = True
        # Check to see if the user has requested that the game end.
        if event.type == pg.QUIT:
            run_game_loop = False
        if event.type == pg.MOUSEBUTTONUP:
            mpos = pg.mouse.get_pos()
            game_manager.selectFromXY(mpos[0], mpos[1])

def GameLoop():
    global ARR_GAME_STATES
    global GLOBAL_TICK
    global GAME_STATE_INDEX
    global game_manager
    global run_game_loop
    global paused 
    global restore 

    
    game_manager = GameManager(GAME_GRID_WIDTH, GAME_GRID_HEIGHT)
    
    while run_game_loop:
        check_events()
        if not paused:
            for i in range(SKIP_FRAMES + 1):
                if (GAME_STATE_INDEX < len(ARR_GAME_STATES)-1):
                    rewindState()
                else:
                    progressState()
        else:
            if SAVE_STATES:
                if restore and GAME_STATE_INDEX <= len(ARR_GAME_STATES)-1:
                    restore = False
                    restored_state = ARR_GAME_STATES[GAME_STATE_INDEX][1]
                    game_manager = restored_state.restore()
            #print(f"Restoring state: {restored_state}")
            #print(f"Game manager: {game_manager}")
            
        # print(f"Index: {GAME_STATE_INDEX}")
        globalDraw()

    pg.display.quit()
    pg.quit()


GameLoop()
