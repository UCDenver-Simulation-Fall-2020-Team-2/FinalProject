from simulation_framework import *
import pygame as pg


pg.init()


# initialize the game manager.
gm = GameManager(GAME_GRID_WIDTH, GAME_GRID_HEIGHT)
game_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_window.fill(BACKGROUND_COLOR)
pg.display.set_caption('Simulation')

def GameLoop(game_manager):

    clock = pg.time.Clock()
    run_game_loop = True
    while run_game_loop:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run_game_loop = False
            # Check to see if the user has requested that the game end.
            if event.type == pg.QUIT:
                run_game_loop = False

        for i in range(SKIP_FRAMES + 1):
            game_manager.logicTick()
        game_window.fill(BACKGROUND_COLOR)
        game_manager.draw(game_window)
        pg.display.flip()        

        delta_time = clock.tick(FRAMES_PER_SECOND)

    pg.display.quit()
    pg.quit()


GameLoop(gm)

# game_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pg.display.set_caption('ASSIGNMENT 1')
# game_window.fill(BACKGROUND_COLOR)

# #font = pg.font.Font(path.join(ABS_PATH,"Retron2000.ttf"), 30)
# font = pg.font.SysFont("monospace", 30)

# run_game_loop = True


# frame_count = 0

# clock = pg.time.Clock()

# while run_game_loop:

#     # Check for key presses
#     # CONTROLS:
#     # p -> Pause/un-pause
#     # Right Arrow -> If paused, progress one tick
#     # Left Arrow -> If paused, rewind one tick
#     # Esc -> Exit game
#     # 0 -> Toggle scent_stacking (Not useful)
#     for event in pg.event.get():
#         if event.type == pg.KEYDOWN:
#             if event.key == pg.K_ESCAPE:
#                 run_game_loop = False                    
#             if event.key == pg.K_RIGHT:
#                 if gm.paused:
#                     gm.logicTick()
#                     gm.draw(game_window)
#             if event.key == pg.K_LEFT:
#                 if gm.paused:
#                     gm.rewindGameState(1)
#                     gm.draw(game_window)
#             if event.key == pg.K_p:
#                 gm.paused = not gm.paused
#                 gm.draw(game_window)
#             if event.key == pg.K_0:
#                 SCENT_STACKING = not SCENT_STACKING
#                 gm.game_grid.calcSmellMatrix()
#         # Check to see if the user has requested that the game end.
#         if event.type == pg.QUIT:
#             run_game_loop = False

#     if not gm.paused:
#         for i in range(SKIP_FRAMES + 1):
#             gm.logicTick()

#         gm.draw(game_window)
#         delta_time = clock.tick(FRAMES_PER_SECOND)

    
# pg.display.quit()
# pg.quit()
