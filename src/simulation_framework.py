import pygame as pg
import numpy as np
import random
import pandas as pd
from os import path
#import time
from enum import Enum
from math import sqrt
import copy
#random.seed(99)

# Initialize pygame.
pg.init()

# Get the current path of the python file. Used to load a font resource.
ABS_PATH = path.dirname(path.realpath(__file__))

# Window width and height
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

NUMBER_OF_PLAYERS = 10

# Shared global across Player instances to assign unique IDs
PLAYER_ID_TRACKER = 0

# How many tiles should the grid have horizontally and vertically?
# CURRENTLY ALL GRIDS MUST BE SQUARE
GAME_GRID_WIDTH = 20
GAME_GRID_HEIGHT = GAME_GRID_WIDTH

# Total number of spaces 
NUM_SPACES = GAME_GRID_WIDTH * GAME_GRID_HEIGHT

# Not currently used.
SMELL_PROPAGATION_DISTANCE = GAME_GRID_WIDTH

# How much energy is spent moving from tile to tile
DEFAULT_TERRAIN_DIFFICULTY = 1

# Should food smell stack, or take the greatest value?
# Glitches can occur if this is turned off
SCENT_STACKING = True

# Does a round's score go down to zero if the player dies?
DEATH_PENALTY = True

# Least amount of energy required at the end of each round to create a child
REPRODUCTION_ENERGY_REQ = 180

# Self explanatory
BACKGROUND_COLOR = pg.Color("#505050")
PAUSED_BACKGROUND_COLOR = pg.Color("#303030")

# Number of frames to draw per second.
FRAMES_PER_SECOND = 30

# Used to determine how many frames are skipped.
# Helps when you want the gamelogic to move faster than
# Your system can draw it.
SKIP_FRAMES = 0

# The number of food pieces that will spawn each time there is no food
# on the grid.
MAX_NUM_FOOD_ON_GRID = 20

# How much energy does the mouse get from food?
ENERGY_PER_FOOD = 20

# How much food needs to be found before a round ends?
FOOD_PER_ROUND = MAX_NUM_FOOD_ON_GRID * 5

# What is the maximum amount of energy that a player can have?
MAX_ENERGY = 200

# Maximum number of game states that can be saved per round
MAX_SAVED_GAME_STATES = MAX_ENERGY

SMELL_DIST = 10

SQUARE_SIZE = int(WINDOW_WIDTH/GAME_GRID_WIDTH*0.8)

def rand_color(min_brightness=50, max_brightness=150):
    if min_brightness < 0:
        min_brightness = 0
    if max_brightness > 255:
        max_brightness = 255
    red = random.randint(min_brightness,max_brightness)
    green = random.randint(min_brightness,max_brightness)
    blue = random.randint(min_brightness,max_brightness)

    return pg.Color(red,green,blue)

# A class that describes a occupied tile on the grid.
class GridSpace:
    def __init__(self,x,y):
        self.type = None
        self.difficulty = DEFAULT_TERRAIN_DIFFICULTY
        self.x = x
        self.y = y
        self.color = pg.Color("#000000")
        
    # Set a tile to be type 'player'
    def setPlayer(self):
        #self.color = pg.Color("#0000FF")
        self.type = "Player"
        self.img = pg.image.load(path.join(ABS_PATH,"art_assets","agent_faces","agent_faces_neutral.png"))
        self.img = pg.transform.scale(self.img,(SQUARE_SIZE,SQUARE_SIZE))
        self.img.fill(rand_color(),special_flags=pg.BLEND_ADD)
        
    # Set a tile to be type 'food'    
    def setFood(self):
        self.color = pg.Color("#FF0000")
        self.img = pg.image.load(path.join(ABS_PATH,"art_assets","plant_growth","plant_growth_7.png"))
        self.img = pg.transform.scale(self.img,(SQUARE_SIZE,SQUARE_SIZE))
        self.img.fill(rand_color(),special_flags=pg.BLEND_MIN)
        self.type = "Food"

# A class that allows for the saving and restoring of the game.
class GameState():
    def __init__(self,game_grid):
        #print(game_grid.player)
        self.player_loc_x = [current_player.tile.x for current_player in game_grid.player]
        self.player_loc_y = [current_player.tile.y for current_player in game_grid.player]
        self.player_energy = [current_player.energy for current_player in game_grid.player]
        self.player_food_eaten = [current_player.food_eaten for current_player in game_grid.player]
        self.player_score = [current_player.score for current_player in game_grid.player]
        self.food_loc = [(tile.x, tile.y) for tile in game_grid.occupied_spaces if tile.type == "Food"]
        self.number_of_food = game_grid.number_of_food
        self.round = 0
        self.curr_number_of_players = 0
        
    # Restore a player object from the game state
    def restorePlayer(self):
        player_list = []
        for current_player in range(len(self.player_loc_x)):
            new_player = Player(self.player_loc_x[current_player], 
                            self.player_loc_y[current_player])
            new_player.energy = self.player_energy[current_player]
            new_player.food_eaten = self.player_food_eaten[current_player]
            new_player.score = self.player_score[current_player]
            player_list.append(new_player)
        return player_list

class GameManager():
    """ A class that controls the logic and graphics of the game. """
    def __init__(self,width,height):
        global NUMBER_OF_PLAYERS
        
        self.game_grid = GameGrid(height, width)
        self.round = 0
        self.paused = 0
        self.game_states = []
        self.curr_game_state_index = 0
        self.round_scores = []
        self.curr_number_of_players = NUMBER_OF_PLAYERS
        
    def logicTick(self):
        """ Proceed one tick in the game logic. """
        #print((f"-----------------------------\n"
        #       f"Occupied player spaces at beginning of tick:\n"
        #       f"{self.game_grid.getPlayerPositionDict()}\n"
        #       f"-----------------------------\n"))
        # Add food if there is none on the grid
        # <key, val> = <(x, y), [(player, direction)]>
        collision_detection_game_grid_dict = {}
        
        if self.curr_game_state_index == len(self.game_states)-1:
            if self.game_grid.number_of_food == 0:
                for i in range(MAX_NUM_FOOD_ON_GRID):
                    self.game_grid.addFood()
                    self.game_grid.number_of_food += 1
    
            #self.game_grid.calcSmellMatrix()
            self.game_grid.calcPlayerSense2()
            #movement_list = []
            for current_player in range(len(self.game_grid.player)):
                decided_direction = smart_mouse(self.game_grid.player[current_player].smell_matrix)
                transient_current_player = Player(self.game_grid.player[current_player].tile.x, self.game_grid.player[current_player].tile.y)
                new_x, new_y = transient_current_player.move(decided_direction, 1)
                if (new_x, new_y) in collision_detection_game_grid_dict:
                    collision_detection_game_grid_dict[(new_x, new_y)].append((self.game_grid.player[current_player], decided_direction))
                else:
                    collision_detection_game_grid_dict[(new_x, new_y)] = [(self.game_grid.player[current_player], decided_direction)]
                #movement_list.append(decided_direction)
            
            self.game_grid.movePlayer(collision_detection_game_grid_dict)
            
            #print((f"-----------------------------\n"
            #       f"Occupied player spaces after movePlayer of tick:\n"
            #       f"{self.game_grid.getPlayerPositionDict()}\n"
            #       f"-----------------------------\n"))
            
            self.checkEndStates()
            self.saveGameState()
        else:
            self.curr_game_state_index += 1
            self.restoreGameState(self.game_states[self.curr_game_state_index])
            

    def draw(self, game_window):
        """ Draw the current gamestate to the screen """
        if self.paused:
            game_window.fill(PAUSED_BACKGROUND_COLOR)
        else:
            game_window.fill(BACKGROUND_COLOR)

        self.game_grid.draw(game_window)
        labels_y_start = self.game_grid.total_grid_x + self.game_grid.grid_padding
        
        score_list_string = ','.join([str(current_player.score) for current_player in self.game_grid.player])
        energy_list_string = ','.join([str(current_player.energy) for current_player in self.game_grid.player])
        food_eaten_string = ','.join([str(current_player.food_eaten) for current_player in self.game_grid.player])
        
        # Uneeded global keyword for read-only use of global in function
        # global NUMBER_OF_PLAYERS
        
        game_window.blit(font.render(f"SCORE:      {score_list_string}", 0, (255, 0, 0)), (10, labels_y_start))
        game_window.blit(font.render(f"ENERGY:     {energy_list_string}", 0, (255, 0, 0)), (10, labels_y_start+25))
        game_window.blit(font.render(f"FOOD_EATEN: {food_eaten_string}", 0, (255, 0, 0)), (10, labels_y_start+50))
        game_window.blit(font.render(f"POPULATION: {self.curr_number_of_players}", 0, (255, 0, 0)), (10, labels_y_start+75))
        game_window.blit(font.render(f"Game State Index: {self.curr_game_state_index}", 0, (255, 0, 0)), (10, labels_y_start+100))        
        game_window.blit(font.render(f"Round:      {self.round}", 0, (255, 0, 0)), (10, 0))        

        pg.display.flip()        

    def checkEndStates(self):
        """
        Check if something happened to end the round.
        If statements are separated in case you wanted to modify the behavior.
        """
        global NUMBER_OF_PLAYERS
        
        bHasPlayerDied = False
        bFoodLimitReached = False
        dead_players = []
        
        for current_player in self.game_grid.player:
            if not current_player.alive:
                bHasPlayerDied = True

                if DEATH_PENALTY:
                    self.game_grid.removePlayer(current_player)
                    NUMBER_OF_PLAYERS -= 1
                    dead_players.append(current_player)

            if current_player.food_eaten >= FOOD_PER_ROUND:
                bFoodLimitReached = True

        if bHasPlayerDied:
            self.endRound(dead_players)
        elif bFoodLimitReached:
            self.endRound()

    def endRound(self, dead_players=None):
        """ End the round and start a new one"""
        global NUMBER_OF_PLAYERS
        self.game_grid.roundReset()

        for i in range(NUMBER_OF_PLAYERS):
            self.round_scores.append(self.game_grid.player[i].score)

            if self.game_grid.player[i].energy > REPRODUCTION_ENERGY_REQ:
                self.game_grid.createChild(self.game_grid.player[i].id)
                NUMBER_OF_PLAYERS += 1
        
        # self.game_grid.reset()
        self.writeRoundData(dead_players) if dead_players else self.writeRoundData()
        self.game_grid.addRoundChildren()
        self.game_grid.gridPopulate()
        self.round += 1
        self.curr_number_of_players = NUMBER_OF_PLAYERS
        self.reset()

    def printScoreStats(self):
        """ Print score related statistics. """
        print(f"There have been {len(self.round_scores)} round(s).")
        print(f"The highest possible score is {MAX_ENERGY*FOOD_PER_ROUND}")
        print(f"The high score of all rounds is {max(self.round_scores)}")
        print(f"The worst of all rounds is {min(self.round_scores)}")
        print(f"The average of all rounds is {sum(self.round_scores)/len(self.round_scores)}")
        print()

    
    def reset(self):
        """ Reset self to prepare for the next round """
        #self.game_states = []

    def saveGameState(self):
        """ Save the current game state, and add it to the game state array. """
        global NUMBER_OF_PLAYERS
        if len(self.game_states) >= MAX_SAVED_GAME_STATES:
            self.game_states = self.game_states[1:]
        newGameState = GameState(self.game_grid)
        newGameState.round = self.round
        newGameState.curr_number_of_players = NUMBER_OF_PLAYERS
        self.game_states.append(newGameState)
        self.curr_game_state_index = len(self.game_states)-1
        
    # Restore a game state from a GameState object
    def restoreGameState(self,game_state):
        self.game_grid.reset()
        self.game_grid.player = game_state.restorePlayer()
        self.game_grid.number_of_food = game_state.number_of_food
        self.curr_number_of_players = game_state.curr_number_of_players
        self.round = game_state.round
        for x, y in game_state.food_loc:
            self.game_grid.addFood(x, y)
        for current_player in self.game_grid.player:
            self.game_grid.occupied_spaces.append(current_player.tile)
            
    # Rewind a given number of game states.
    def rewindGameState(self,num_to_rewind):
        if len(self.game_states) <= 1:
            return
        if num_to_rewind >= len(self.game_states):
            num_to_rewind = len(self.game_states) - 1

        #self.game_states = self.game_states[:-num_to_rewind]
        self.curr_game_state_index = 0 if self.curr_game_state_index == 0 else self.curr_game_state_index-1
        self.restoreGameState(self.game_states[self.curr_game_state_index])

    # Writes round data to .csv files in /stat_data
    def writeRoundData(self, dead_players=None):
        data_dict = {'ID' : [], 'Parent' : [], 'Food Eaten' : [], 'Energy' : [], 'Score' : [], 'Alive?' : []}
        if dead_players:
            for player in dead_players:
                data_dict['ID'].append(player.id)
                data_dict['Parent'].append(player.child_of)
                data_dict['Food Eaten'].append(player.food_eaten)
                data_dict['Energy'].append(player.energy)
                data_dict['Score'].append(player.score)
                data_dict['Alive?'].append(player.alive)
        for player in self.game_grid.player:
            data_dict['ID'].append(player.id)
            data_dict['Parent'].append(player.child_of)
            data_dict['Food Eaten'].append(player.food_eaten)
            data_dict['Energy'].append(player.energy)
            data_dict['Score'].append(player.score)
            data_dict['Alive?'].append(player.alive)

        pd.DataFrame(data_dict).to_csv(path.join(ABS_PATH, 'stat_data', f'agent_stats_round{self.round}.csv'), index=False, mode="w+")

# class SensoryMatrix:
class GameObject:
    """ TODO: ADD DOCSTRING """
    def __init__(self,x,y):
        self.type = None
        self.difficulty = DEFAULT_TERRAIN_DIFFICULTY
        self.x = x
        self.y = y
        self.alive = True

    def move_instant(self,x,y):
        """ Move to a location without using energy """
        self.x = x
        self.y = y

    def move_probabalistic(self, movement_matrix):
        """ Input a 3x3 matrix, pick a direction based on probabilities """

        movement_list = list(range(0,9))
        movement = random.choices(movement_list,weights=movement_matrix.flatten().tolist())
        return movement[0]


def dir2offset(direction):
    difficulty_multiplier = 1
    x = 0
    y = 0
    d = direction
    if d >= 0 and d <= 8:
        if d in [0,1,2]:
            y = 1
        if d in [3,4,5]:
            y = 0
        else:
            y = -1

        if d in [0,3,6]:
            x = -1
        elif d in [1,4,7]:
            x = 0
        else:
            x = 1

        # Diagonal movements are more costly than cardinal movements
        if x != 0 and y != 0:
            difficulty_multiplier = sqrt(2)
    else:
        print("Invalid direction, staying still")
    return x, y, difficulty_multiplier

# test_GO = GameObject(0,0)

# test_move_array = np.zeros((3,3))

# for x in range(0,3):
#     for y in range(0,3):
#         test_move_array[x][y] = random.random()

# move_dir = test_GO.move_probabalistic(test_move_array)
# print(move_dir)
# print(dir2offset(move_dir))

# exit()


class Agent(GameObject):
    def __init__(self,x=None,y=None,init_energy=None):
        self.stats = AgentStats()

# class Plant(GameObject):

class AgentStats:
    def __init__(self):
        self.max_energy = MAX_ENERGY
        self.energy = self.max_energy
        self.score = 0
        self.speed = 4
        self.size = 1/self.speed
        
# A class managing player actions
class Player:
    def __init__(self,x=0,y=0, child_of=-1):
        global PLAYER_ID_TRACKER
        self.id = PLAYER_ID_TRACKER
        PLAYER_ID_TRACKER += 1
        self.child_of = child_of
        self.stats = AgentStats()
        self.tile = GridSpace(x,y)
        self.tile.setPlayer()
        self.food_eaten = 0
        self.max_energy = MAX_ENERGY
        self.energy = self.max_energy
        self.alive = True
        self.smell_matrix = np.zeros((3,3))
        self.score = 0
        self.img = pg.image.load(path.join(ABS_PATH,"art_assets","agent_faces","agent_faces_neutral.png"))
        self.img = pg.transform.scale(self.img,(SQUARE_SIZE,SQUARE_SIZE))
        self.img.fill(rand_color(),special_flags=pg.BLEND_ADD)
        
    # Move to a location without using energy
    def teleport(self,x,y):
        self.tile.x = x
        self.tile.y = y

    # Move one space in a given direction. DIfficulty will be used later
    # to increase or decrease energy usage when moving onto a square.,
    def move(self,direction,difficulty):
        if self.alive:
            if direction == 0:
                if self.tile.x > 0:
                    self.tile.x -= 1
            elif direction == 1:
                if self.tile.x < GAME_GRID_HEIGHT - 1:
                    self.tile.x += 1
            elif direction == 2:
                if self.tile.y > 0:
                    self.tile.y -= 1
            elif direction == 3:
                if self.tile.y < GAME_GRID_WIDTH - 1:
                    self.tile.y += 1        
            
            self.useEnergy(difficulty)
        return self.tile.x, self.tile.y
        
    # Eat a food
    def eatFood(self):
        self.food_eaten += 1
        self.score += self.energy
        self.energy += ENERGY_PER_FOOD
        if self.energy > self.max_energy:
            self.energy = self.max_energy
            
    # Use a given amount of energy 
    def useEnergy(self, amount):
        self.energy -= amount
        if self.energy < 0:
            self.die()
    
    # Turn the player from the alive state to the not-alive state
    def die(self):
        self.alive = False
        self.tile.color = pg.Color("#00005F")

    def printStats(self):
        print(f"FOOD EATEN: {self.food_eaten}")

def fast_dist(x1,y1,x2,y2):
    return np.linalg.norm(np.array((x1,y1))-np.array((x2,y2)))

# Primary game grid actions
class GameGrid:
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.number_of_food = 0
        self.occupied_grid = np.zeros((self.width, self.height), dtype="int")
        self.occupied_spaces = []
        self.player = []
        self.new_player = []

        self.default_color = pg.Color("#FFFFFF")
        self.line_color = pg.Color("#010101")
    
        for i in range(NUMBER_OF_PLAYERS):
            x, y = self.randEmptySpace()
            new_player = Player(x, y)
            self.addTile(new_player.tile)
            self.player.append(new_player)
            #print(f"{x}, {y}.\n{self.occupied_grid}, {self.occupied_spaces}")

        #self.player[-1].tile_x = -5
        #self.player[-1].tile_y = -5
        self.padding = 2
        self.square_size = int(WINDOW_WIDTH/GAME_GRID_WIDTH*0.8)
        self.grid_padding = self.calcGridPadding()
                
    # Used to determine the size of the grid on screen.
    def calcGridPadding(self):
        self.total_grid_x = self.width*self.padding + self.width*self.square_size
        self.grid_padding = int((WINDOW_WIDTH - self.total_grid_x)/2)
        return self.grid_padding
    
    # Calculate how much food smell is on the current grid.
    def calcSmellMatrix(self):
        return
        
    # Calculate what the player can sense from the current smell matrix.
    def calcPlayerSense(self):
        for current_player in self.player:
            agent_x = current_player.tile.x
            agent_y = current_player.tile.y
            current_player.smell_matrix = np.zeros((3, 3))
            for x_offset in range(-1, 2):
                for y_offset in range(-1, 2):
                    x = agent_x + x_offset
                    y = agent_y + y_offset
                    if self.checkValidTile(x, y):
                        for tile in self.occupied_spaces:
                            if tile.x == x and tile.y == y:
                                current_player.smell_matrix[y_offset+1][x_offset+1] = 1000
                            else:
                                dist = fast_dist(x,y,tile.x,tile.y) + 1
                                if dist <= SMELL_DIST:
                                    if current_player.smell_matrix[y_offset+1][x_offset+1] < 1/dist:
                                        current_player.smell_matrix[y_offset+1][x_offset+1] = 1/dist
        #self.player.smell_matrix[[0,2]] = self.player.smell_matrix[[2,0]]

    def calcPlayerSense2(self):
        for current_player in self.player:
            agent_x = current_player.tile.x
            agent_y = current_player.tile.y
            current_player.smell_matrix = np.zeros((3, 3))
            for x_offset in range(-1, 2):
                for y_offset in range(-1, 2):
                    x = agent_x + x_offset
                    y = agent_y + y_offset
                    if self.checkValidTile(x, y):
                        for tile in self.occupied_spaces:
                            if tile.type == 'Food':
                                if tile.x == x and tile.y == y:
                                    current_player.smell_matrix[x_offset+1][y_offset+1] = 1000
                                else:
                                    dist = fast_dist(x,y,tile.x,tile.y) + 1
                                    if dist <= SMELL_DIST:
                                        if current_player.smell_matrix[x_offset+1][y_offset+1] < 1/dist:
                                            current_player.smell_matrix[x_offset+1][y_offset+1] = 1/dist

    # Get a tile by it's coordinates. If no tile matches, return None
    def getTile(self,x,y):
        if not self.checkValidTile(x,y):
            return None
        for tile in self.occupied_spaces:
            if tile.x == x and tile.y == y:
                return tile
        return None

    # Draw the grid without anything else.
    def drawGrid(self,surface):
        total_x = self.width*self.padding + self.width*self.square_size
        total_y = self.height*self.padding + self.height*self.square_size
        grid_pos_x = self.padding + self.grid_padding
        for i in range(self.height + 1):
            pg.draw.rect(
                        surface,
                        self.line_color,
                        pg.Rect(
                            grid_pos_x,
                            self.padding + self.grid_padding, 
                            self.padding, 
                            total_y)
                    )
            grid_pos_x += self.square_size + self.padding

        grid_pos_y = self.padding + self.grid_padding
        for i in range(self.width + 1):
            pg.draw.rect(
                        surface,
                        self.line_color,
                        pg.Rect(
                            self.padding + self.grid_padding,
                            grid_pos_y, 
                            total_x,
                            self.padding
                            )
                    )
            grid_pos_y += self.square_size + self.padding

    # Calculate a XY location for a given tile location
    def calcTileLocation(self,tile):
        x = tile.x * self.padding + tile.x * self.square_size + self.grid_padding
        y = tile.y * self.padding + tile.y * self.square_size + self.grid_padding
        x += self.padding*2
        y += self.padding*2

        return x, y

    def drawPlayer(self,surface):
        for current_player in self.player:
            x, y = self.calcTileLocation(current_player.tile)
            rect = current_player.img.get_rect().move((y,x))
            surface.blit(current_player.img, rect)

    # Draw a tile in the grid
    def drawTile(self,surface,tile):
        if tile.img != None:
            x, y = self.calcTileLocation(tile)
            rect = tile.img.get_rect().move((y,x))
            surface.blit(tile.img, rect)
        else:
            x, y = self.calcTileLocation(tile)
            pg.draw.rect(
                surface,
                tile.color,
                pg.Rect(
                    y, 
                    x, 
                    self.square_size, 
                    self.square_size)
            )

    # Draw the entire game grid
    def draw(self,surface):
        total_x = self.width*self.padding + self.width*self.square_size
        total_y = self.height*self.padding + self.height*self.square_size
        pg.draw.rect(
                    surface,
                    self.default_color,
                    pg.Rect(
                        self.padding + self.grid_padding,
                        self.padding + self.grid_padding, 
                        total_x, 
                        total_y)
                )

        for tile in self.occupied_spaces:
            self.drawTile(surface,tile)

        self.drawPlayer(surface)

        self.drawGrid(surface)

    # Add a tile to the game grid.
    def addTile(self,tile):
        self.occupied_spaces.append(tile)
        
        if tile.type == 'Player':
            self.occupied_grid[tile.x][tile.y] = 1
        elif tile.type == 'Food':
            self.occupied_grid[tile.x][tile.y] = 2

    # Reset the game grid
    def reset(self):
        self.number_of_food = 0
        self.occupied_grid = np.zeros((self.width, self.height), dtype="int")
        self.occupied_spaces = []
        self.player = []
        for i in range(NUMBER_OF_PLAYERS):
            self.player.append(Player())
    
    # Readies the grid for next round based on data in self.player
    def roundReset(self):
        # Reset food on board (self.addFood called by GameManager on next round)
        self.number_of_food = 0
        # Reset occupied tile tracking list
        self.occupied_spaces = []
        # Reset occupied grid tracking
        self.occupied_grid = np.zeros((self.width, self.height), dtype="int")

    def gridPopulate(self):
        # For each player
        for player_i in self.player:
            # Randomly reset position on grid
            player_i.tile.x, player_i.tile.y = self.randEmptySpace()
            # Add new position to list of occupied position tiles
            self.occupied_spaces.append(player_i.tile)
            # Set new position as occupied on grid
            self.occupied_grid[player_i.tile.x][player_i.tile.y] = 1

    # Get a random valid X coordinate.
    def randGridX(self):
        return random.randint(0,GAME_GRID_WIDTH-1)

    # Get a random valid Y coordinate.
    def randGridY(self):
        return random.randint(0,GAME_GRID_HEIGHT-1)

    # Get a random valid XY coordinate set.
    def randGridSpace(self):
        return self.randGridX(), self.randGridY()

    # Efficiently get a random XY pair that isn't already used. 
    def randEmptySpace(self):
        if len(self.occupied_spaces) < NUM_SPACES*0.5:
            found = False
            while found == False:
                x,y = self.randGridSpace()
                if self.occupied_grid[x][y] == 0:
                    found = True
            return x,y 
        else:
            empty_left = NUM_SPACES-len(self.occupied_spaces)
            choice = random.randint(0,empty_left)
            count = 0
            for i in range(self.height):
                for j in range(self.width):
                    if self.occupied_grid[i][j] == 0:
                        if count >= choice:
                            return i,j
                        count += 1
            for i in range(self.height):
                for j in range(self.width):
                    if self.occupied_grid[i][j] == 0:
                        if count >= choice:
                            return i,j
                        count += 1
            print("ERROR: No spaces available")
            exit(9)

    # Create a random tile, or one with the XY coordinate that is given.
    def genTile(self,x,y):
        if NUM_SPACES <= len(self.occupied_spaces):
            return None
        orig_x = x
        orig_y = y
        check_count = 0
        if orig_x < 0 or orig_x > GAME_GRID_WIDTH or \
            orig_y < 0 or orig_y > GAME_GRID_HEIGHT:
                x,y = self.randEmptySpace()
        return GridSpace(x,y)

    # Check to make sure a given XY set is 
    def checkValidTile(self,x,y):
        if x >= 0 and y >= 0:
            if x < GAME_GRID_WIDTH and y < GAME_GRID_HEIGHT:
                return True
        return False

    # Check to see if a given XY set is already occupied by a tile.
    def checkOccupied(self,x,y):
        if self.checkValidTile(x,y):
            if self.occupied_grid[x][y] == 1:
                return True
        return False

    # Remove a tile at a given XY set, if one exists.
    def removeTile(self,x,y):
        tile_type = None
        if self.checkOccupied(x,y):
            self.occupied_grid[x][y] = 0
            for tile in self.occupied_spaces:
                if tile.x == x and tile.y == y:
                    tile_type = tile.type
                    self.occupied_spaces.remove(tile)
        return tile_type

    def removeFoodTile(self, x, y):
        for tile in self.occupied_spaces:
            if tile.x == x and tile.y == y and tile.type == 'Food':
                tar_tile = tile
                break
        self.occupied_spaces.remove(tar_tile)

    def getPlayerPositionDict(self):
        dct = {}

        for tile in self.occupied_spaces:
            if tile.type == 'Player':
                if (tile.x, tile.y) in dct:
                    dct[(tile.x, tile.y)] += 1
                else:
                    dct[(tile.x, tile.y)] = 1

        return dct

    def debugGetTileDict(self):
        dct = {}
        for tile in self.occupied_spaces:
            if (tile.x, tile.y) in dct:
                dct[(tile.x, tile.y)] += 1
            else:
                dct[(tile.x, tile.y)] = 1
        return dct
    
    # Move the player in a direction.
    def movePlayer(self, collision_detection_grid_dict):
        global NUMBER_OF_PLAYERS
        # Dir is a number between 0 and 3:
        # 0 -> North (UP)
        # 1 -> South (DOWN)
        # 2 -> WEST (LEFT)
        # 3 -> EAST (RIGHT)

        # (x, y) = number of players on grid position
        # food and unoccupied grid positions not tracked
        position_dct = self.getPlayerPositionDict()
        #print(("--------------\nInitial debug dict\n--------------\n"
        #       f"{self.debugGetTileDict()}\n"))
        
        #print(collision_detection_grid_dict)
        for _, key_tuple in enumerate(collision_detection_grid_dict):
            player_direction_list = collision_detection_grid_dict[key_tuple]
            #print(player_direction_list)
            
            remaining_player = None
            remaining_player_direction = None
            
            if (len(player_direction_list) > 1):
                remaining_tuple = max([(player_direction_tuple[0].energy, index) for index, player_direction_tuple in enumerate(player_direction_list)])
                for index, (player, direction) in enumerate(player_direction_list):
                    if (index != remaining_tuple[1]):
                        player.die()
                        self.removePlayer(player)
                        NUMBER_OF_PLAYERS -= 1
                remaining_player, remaining_player_direction = player_direction_list[remaining_tuple[1]]
            else:
                remaining_player, remaining_player_direction = player_direction_list[0]
                
            old_x, old_y = remaining_player.tile.x, remaining_player.tile.y
            new_x, new_y = remaining_player.move(remaining_player_direction, 1)

            #print((f"--------------\nPlayer dict after player move at {index}\n--------------\n"
            #       f"{self.getPlayerPositionDict()}\n"))
            # If player moved position
            if old_x != new_x or old_y != new_y:
                position_dct[(old_x, old_y)] -= 1

                if position_dct[(old_x, old_y)] < 1:
                    self.occupied_grid[old_x][old_y] = 0

                if (new_x, new_y) in position_dct:
                    position_dct[(new_x, new_y)] += 1
                else: 
                    position_dct[(new_x, new_y)] = 1
                
                if self.occupied_grid[new_x][new_y] == 2:
                    self.removeFoodTile(new_x, new_y)
                    remaining_player.eatFood()
                    self.number_of_food -= 1
                    self.calcSmellMatrix()

                self.occupied_grid[new_x][new_y] = 1
                #print((f"--------------\nPlayer dict after index {index}\n--------------\n"
                #       f"{self.getPlayerPositionDict()}\n"))
                
            
        '''
        for index, direction in enumerate(direction_list):
            old_x, old_y = self.player[index].tile.x, self.player[index].tile.y
            new_x, new_y = self.player[index].move(direction, 1)

            #print((f"--------------\nPlayer dict after player move at {index}\n--------------\n"
            #       f"{self.getPlayerPositionDict()}\n"))
            # If player moved position
            if old_x != new_x or old_y != new_y:
                position_dct[(old_x, old_y)] -= 1

                if position_dct[(old_x, old_y)] < 1:
                    self.occupied_grid[old_x][old_y] = 0

                if (new_x, new_y) in position_dct:
                    position_dct[(new_x, new_y)] += 1
                else: 
                    position_dct[(new_x, new_y)] = 1
                
                if self.occupied_grid[new_x][new_y] == 2:
                    self.removeFoodTile(new_x, new_y)
                    self.player[index].eatFood()
                    self.number_of_food -= 1
                    self.calcSmellMatrix()

                self.occupied_grid[new_x][new_y] = 1
                #print((f"--------------\nPlayer dict after index {index}\n--------------\n"
                #       f"{self.getPlayerPositionDict()}\n"))
        '''
        
    # Add a player to the grid.
    def addPlayer(self,x=-1,y=-1):
        temp_tile = self.genTile(x,y)
        if temp_tile != None:
            temp_tile.setPlayer()
            self.addTile(temp_tile)

    # add a piece of food to the grid
    def addFood(self,x=-1,y=-1):
        temp_tile = self.genTile(x,y)
        if temp_tile != None:
            temp_tile.setFood()
            self.addTile(temp_tile)
        self.calcSmellMatrix()

    # Check if there is food at the XY set provided
    def checkForFood(self,x,y):
        if self.checkOccupied(x,y):
            tile = self.getTile(x,y)
            if tile is not None and tile.type == "Food":
                return True
        return False

    # Check to see if there is food next to the player, and
    # return the set of directions that lead to food.
    def isPlayerNext2Food(self):
        return None

    # Print a list of all occupied tiles.
    def print_occupied_tiles(self):
        for current_player in self.player:
            print(f"PLAYER AT: [{current_player.tile.x}, {current_player.tile.y}]")
            for tile in self.occupied_spaces:
                if tile.type == "Food":
                    print(f"FOOD AT: [{tile.x}, {tile.y}]")

    # Places new, child Player on grid with passed Player.id as parent ID
    def createChild(self, parent_id):
        x, y = self.randEmptySpace()
        child_player = Player(x, y, parent_id)
        self.new_player.append(child_player)

    def addRoundChildren(self):
        if self.new_player:
            self.player.extend(self.new_player)
            self.new_player = []

    # Removes Player argument from GameGrid
    def removePlayer(self, tar_player):
        self.player.remove(tar_player)
        self.occupied_spaces.remove(tar_player.tile)
        self.occupied_grid[tar_player.tile.x][tar_player.tile.y] = 0

# All simple mouse does is pick a random direction, and moves there.
# Quite senseless, if you ask me.
def simple_mouse():
    return random.choice(range(0,4))

# Decides wether or not to use the corners of the player sensory matrix
# when selecting a movement path. In its current state, the mouse can get
# stuck in a rut when this is true when multiple pieces of food are in play. 
# You can try to improve it, if you'd like.

# Do you think your RL model will make better use of the corners, or
# do you think it will rely on the cardinal directions that it can use
# for movement?

USE_DIAGONAL_SCENT = False

# The smart mouse uses its nose to find food. It does this by checking
# which path has the greatest amount of food smells, and going in that
# direction. 

def smart_mouse(scent_matrix):
    # If there are no scents, just pick a random direction.
    if not np.any(scent_matrix):
        return simple_mouse()

    if USE_DIAGONAL_SCENT:
        # Sum the top, bottom, and side rows/columns
        north = np.sum(scent_matrix,axis=1)[0]
        south = np.sum(scent_matrix,axis=1)[2]
        west = np.sum(scent_matrix,axis=0)[0]
        east = np.sum(scent_matrix,axis=0)[2]
    else:
        # Get the values of the top center, bottom center, and side centers. 
        north = scent_matrix[0][1]
        south = scent_matrix[2][1]
        west = scent_matrix[1][0]
        east = scent_matrix[1][2]

    movement_array = [north,south,west,east]

    # Get the maximum value, or values
    indexes = [i for i, x in enumerate(movement_array) if x == max(movement_array)]

    # Make a random choice from all the best options
    move_choice = random.choice(indexes)
    return move_choice
    # return movement_array.index(max(movement_array))


# initialize the game manager.
gm = GameManager(GAME_GRID_WIDTH, GAME_GRID_HEIGHT)

game_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption('ASSIGNMENT 1')
game_window.fill(BACKGROUND_COLOR)

#font = pg.font.Font(path.join(ABS_PATH,"Retron2000.ttf"), 30)
font = pg.font.SysFont("monospace", 15)

run_game_loop = True


frame_count = 0

clock = pg.time.Clock()

gm.game_states.append(GameState(gm.game_grid))

while run_game_loop:

    # Check for key presses
    # CONTROLS:
    # p -> Pause/un-pause
    # Right Arrow -> If paused, progress one tick
    # Left Arrow -> If paused, rewind one tick
    # Esc -> Exit game
    # 0 -> Toggle scent_stacking (Not useful)
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run_game_loop = False                    
            if event.key == pg.K_RIGHT:
                if gm.paused:
                    gm.logicTick()
                    gm.draw(game_window)
            if event.key == pg.K_LEFT:
                if gm.paused:
                    gm.rewindGameState(1)
                    gm.draw(game_window)
            if event.key == pg.K_p:
                gm.paused = not gm.paused
                gm.draw(game_window)
            if event.key == pg.K_0:
                SCENT_STACKING = not SCENT_STACKING
                gm.game_grid.calcSmellMatrix()
        # Check to see if the user has requested that the game end.
        if event.type == pg.QUIT:
            run_game_loop = False
    if not gm.paused:
        for i in range(SKIP_FRAMES + 1):
            gm.logicTick()

        gm.draw(game_window)
        delta_time = clock.tick(FRAMES_PER_SECOND)

    
pg.display.quit()
pg.quit()
