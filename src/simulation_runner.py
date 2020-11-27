from simulation_framework import *
import pygame as pg


# Used to determine how many frames are skipped.
# Helps when you want the gamelogic to move faster than
# Your system can draw it.
SKIP_FRAMES = 0

# Number of frames to draw per second.
FRAMES_PER_SECOND = 20

pg.init()


# initialize the game manager.
gm = GameManager(GAME_GRID_WIDTH, GAME_GRID_HEIGHT)
game_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
game_window.fill(BACKGROUND_COLOR)
pg.display.set_caption('Simulation')


def GameLoop(game_manager):
    paused = False

    clock = pg.time.Clock()
    run_game_loop = True
    while run_game_loop:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run_game_loop = False
                if event.key == pg.K_p:
                    paused = not paused
            # Check to see if the user has requested that the game end.
            if event.type == pg.QUIT:
                run_game_loop = False
        if not paused:
            for i in range(SKIP_FRAMES + 1):
                # CALL YOUR CODE HERE!
                player_move = None
                # CALL YOUR CODE HERE!

                game_manager.logicTick(player_move)

            game_window.fill(BACKGROUND_COLOR)
            game_manager.draw(game_window)
            pg.display.flip()        

            delta_time = clock.tick(FRAMES_PER_SECOND)

    pg.display.quit()
    pg.quit()


GameLoop(gm)
