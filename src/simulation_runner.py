from simulation_framework import *
from variable_config import *

# Used to determine how many frames are skipped.
# Helps when you want the gamelogic to move faster than
# Your system can draw it.
SKIP_FRAMES = 0

# Number of frames to draw per second.
# FRAMES_PER_SECOND = 0

MAX_GAME_STATES = 200

ARR_GAME_STATES = []

GAME_STATE_INDEX = -1 # Needs to execute one logic tick to create a legitimate game state for the initial GameManager

GLOBAL_TICK = 0

SAVE_STATES = True

TURN_VIEW = True

pg.init()
game_manager = None

selected_id = None
current_agent_id = None

game_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_window.fill(BACKGROUND_COLOR)
pg.display.set_caption('Simulation')

run_game_loop = True
restore = True

def incFPS():
    global FPS_SELECTION
    global FPS_LIST
    
    FPS_SELECTION += 1
    if FPS_SELECTION >= len(FPS_LIST):
        FPS_SELECTION = 0

def globalDraw():
    global game_window
    global game_manager
    global clock
    global SIMULATION_RUNNER_PAUSED
    global SIMULATION_RUNNER_PAUSE_LOCK
    global SIMULATION_RUNNER_SIGNAL_REDRAW
    global delta_time
    
    check_events()
    
    game_window.fill(BACKGROUND_COLOR)
    desired_id = game_manager.selectByID(selected_id)
    if desired_id is None:
        latest_selected_id = game_manager.selectByID(current_agent_id)
        if latest_selected_id is None:
            game_manager.selectByID(None)
            
    game_manager.draw(game_window,paused=SIMULATION_RUNNER_PAUSED,pause_lock=SIMULATION_RUNNER_PAUSE_LOCK,terminating=SIMULATION_RUNNER_TERMINATING)
    pg.display.flip()
    
    diff = pg.time.get_ticks() - delta_time
    #print(f"Initial diff: {diff}")
    while (diff < 1000/FPS_LIST[FPS_SELECTION]):
        check_events()
        if (SIMULATION_RUNNER_PAUSED and not SIMULATION_RUNNER_PAUSE_LOCK) or SIMULATION_RUNNER_SIGNAL_REDRAW:
            SIMULATION_RUNNER_SIGNAL_REDRAW = False
            game_window.fill(BACKGROUND_COLOR)
            desired_id = game_manager.selectByID(selected_id)
            if desired_id is None:
                latest_selected_id = game_manager.selectByID(current_agent_id)
                if latest_selected_id is None:
                    game_manager.selectByID(None)
            game_manager.draw(game_window,paused=SIMULATION_RUNNER_PAUSED,pause_lock=SIMULATION_RUNNER_PAUSE_LOCK,terminating=SIMULATION_RUNNER_TERMINATING)
            pg.display.flip()
            
        diff = pg.time.get_ticks() - delta_time
        #print(f"Diff: {diff}")
        
    delta_time = pg.time.get_ticks()
        
def progressState():
    global ARR_GAME_STATES
    global GLOBAL_TICK
    global GAME_STATE_INDEX
    global SIMULATION_RUNNER_PAUSE_LOCK
    global game_manager
    global delta_time
    
    delta_time = pg.time.get_ticks()
    if GLOBAL_TICK > 0 and TURN_VIEW:
        current_agent_id = game_manager.logicTick(draw_func=globalDraw)
    else:
        current_agent_id = game_manager.logicTick()
    
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
    global SIMULATION_RUNNER_PAUSED
    global SIMULATION_RUNNER_PAUSE_LOCK
    global restore
    global run_game_loop
    global GAME_STATE_INDEX
    global selected_id
    global SIMULATION_RUNNER_SIGNAL_REDRAW
    global clock
    global FPS_SELECTION
    global FPS_LIST
    global SIMULATION_RUNNER_TERMINATING
    
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run_game_loop = False
            if event.key == pg.K_f:
                incFPS()
            if event.key == pg.K_p and not SIMULATION_RUNNER_PAUSE_LOCK:
                if not SIMULATION_RUNNER_PAUSED:
                    SIMULATION_RUNNER_PAUSE_LOCK = True
                    SIMULATION_RUNNER_SIGNAL_REDRAW = True
                    print("Waiting for agents' actions to end before pausing...")
                if SAVE_STATES:
                    restore = True
                SIMULATION_RUNNER_PAUSED = not SIMULATION_RUNNER_PAUSED
            if event.key == pg.K_RIGHT and SIMULATION_RUNNER_PAUSED and not SIMULATION_RUNNER_PAUSE_LOCK:
                if SAVE_STATES:
                    if (GAME_STATE_INDEX < len(ARR_GAME_STATES)-1):
                        GAME_STATE_INDEX += 1
                        restore = True
                    elif (GAME_STATE_INDEX > len(ARR_GAME_STATES)-1):
                        print("ERROR: GAME_STATE_INDEX OOB WITH K_RIGHT")
                        exit(9)
                else:
                    progressState()
    
            if event.key == pg.K_LEFT and SIMULATION_RUNNER_PAUSED and not SIMULATION_RUNNER_PAUSE_LOCK:
                if (GAME_STATE_INDEX == len(ARR_GAME_STATES)):
                    GAME_STATE_INDEX -= 2
                    restore = True
                elif (GAME_STATE_INDEX > 0):
                    GAME_STATE_INDEX -= 1
                    restore = True
        # Check to see if the user has requested that the game end.
        if event.type == pg.QUIT:
            run_game_loop = False
            SIMULATION_RUNNER_TERMINATING = True
            SIMULATION_RUNNER_SIGNAL_REDRAW = True
            print("Waiting for tick to finish before closing...")
        if event.type == pg.MOUSEBUTTONUP:
            #print("Received MBUTTONUP event!")
            mpos = pg.mouse.get_pos()
            selected_id = game_manager.selectFromXY(mpos[0], mpos[1])
            SIMULATION_RUNNER_SIGNAL_REDRAW = True
        
def GameLoop():
    global ARR_GAME_STATES
    global GLOBAL_TICK
    global GAME_STATE_INDEX
    global game_manager
    global run_game_loop
    global SIMULATION_RUNNER_PAUSED 
    global SIMULATION_RUNNER_PAUSE_LOCK
    global restore 

    game_manager = GameManager(GAME_GRID_WIDTH, GAME_GRID_HEIGHT)
    
    while run_game_loop:
        check_events()
        if not SIMULATION_RUNNER_PAUSED:
            for i in range(SKIP_FRAMES + 1):
                if (GAME_STATE_INDEX >= 0 and GAME_STATE_INDEX <= len(ARR_GAME_STATES)-1):
                    rewindState()
                else:
                    progressState()
        else:
            if SAVE_STATES:
                if restore and GAME_STATE_INDEX >= 0 and GAME_STATE_INDEX <= len(ARR_GAME_STATES)-1:
                    restore = False
                    restored_state = ARR_GAME_STATES[GAME_STATE_INDEX][1]
                    game_manager = restored_state.restore()
            #print(f"Restoring state: {restored_state}")
            #print(f"Game manager: {game_manager}")
            
        # print(f"Index: {GAME_STATE_INDEX}")
        globalDraw()
        if SIMULATION_RUNNER_PAUSED and SIMULATION_RUNNER_PAUSE_LOCK:
            SIMULATION_RUNNER_PAUSE_LOCK = False
            print("Paused the simulation!")
    print("Simulation ending. Goodbye!")
    pg.display.quit()
    pg.quit()
    


GameLoop()
