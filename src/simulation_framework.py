import pygame as pg
from pygame.font import Font
import numpy as np
import random
<<<<<<< HEAD
import pandas as pd
=======
import sys
>>>>>>> master
from os import path
from PIL import Image, ImageFilter
from variable_config import *
#import time
from enum import Enum
from math import sqrt
import traceback
import pickle
#import dill

#random.seed(99)

# Initialize pygame.
#pg.init()

# Get the current path of the python file. Used to load a font resource.
ABS_PATH = path.dirname(path.realpath(__file__))

<<<<<<< HEAD
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
=======
EXCEPTION_CAUGHT = False
>>>>>>> master

AGENT_ID = 0

<<<<<<< HEAD
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
=======
class ObjectType(Enum):
    PLANT = 0
    EVIL = 1
    NEUTRAL = 2
    PREGNANT = 3
    BABY = 4
    
def fast_dist(x1,y1,x2,y2):
    return np.linalg.norm(np.array((x1,y1))-np.array((x2,y2)))
>>>>>>> master

def dir2offset(direction):
    difficulty_multiplier = 1
    x = 0
    y = 0
    d = direction
    if d >= 0 and d <= 8:
        if d in [0,1,2]:
            y = -1
        elif d in [3,4,5]:
            y = 0
        else:
            y = 1

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

# Draw the grid without anything else.
def drawGenericGrid(self,surface,rect,num_x,num_y):

    total_x = rect.width
    total_y = rect.height
    grid_pos_x = rect.x
    grid_pos_y = rect.y
    
    line_width = 1
    square_size = int(rect.width/num_x)
    line_color = pg.Color("#000000")

    for i in range(num_y + 1):
        pg.draw.rect(
                    surface,
                    line_color,
                    pg.Rect(
                        grid_pos_x,
                        grid_pos_y, 
                        1, 
                        total_y)
                )
        grid_pos_x += square_size
        if num_x == 3 and i == 2:
            grid_pos_x += 1

<<<<<<< HEAD
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
=======
    grid_pos_x = rect.x
>>>>>>> master

    for i in range(num_x + 1):
        pg.draw.rect(
                    surface,
                    line_color,
                    pg.Rect(
                        grid_pos_x,
                        grid_pos_y, 
                        total_x, 
                        1)
                )
        grid_pos_y += square_size
        if num_y == 3 and i == 2:
            grid_pos_y += 1

# A class that allows for the saving and restoring of the game.
class GameState():
<<<<<<< HEAD
    def __init__(self,game_grid):
        #print(game_grid.player)
        self.player_loc_x = [current_player.tile.x for current_player in game_grid.player]
        self.player_loc_y = [current_player.tile.y for current_player in game_grid.player]
        self.player_energy = [current_player.energy for current_player in game_grid.player]
        self.player_food_eaten = [current_player.food_eaten for current_player in game_grid.player]
        self.player_score = [current_player.score for current_player in game_grid.player]

        self.foods_loc = []
        for tile in game_grid.occupied_spaces:
            if tile.type == "Food":
                self.foods_loc.append([tile.x,tile.y])
                    
    # Restore a player object from the game state
    def restorePlayer(self):
        player_list = []
        for current_player in range(NUMBER_OF_PLAYERS):
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
        self.game_grid = GameGrid(height, width)
        self.round = 0
        self.paused = 0
        self.game_states = []
        self.round_scores = []

    def logicTick(self):
        """ Proceed one tick in the game logic. """

        # Add food if there is none on the grid
        if self.game_grid.number_of_food == 0:
            for i in range(MAX_NUM_FOOD_ON_GRID):
                self.game_grid.addFood()
                self.game_grid.number_of_food += 1

        #self.game_grid.calcSmellMatrix()
        self.game_grid.calcPlayerSense2()
        movement_list = []
        for current_player in range(NUMBER_OF_PLAYERS):
            movement_list.append(smart_mouse(self.game_grid.player[current_player].smell_matrix))
        
        self.game_grid.movePlayer(movement_list)
        self.checkEndStates()
        self.saveGameState()

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
        game_window.blit(font.render(f"POPULATION: {NUMBER_OF_PLAYERS}", 0, (255, 0, 0)), (10, labels_y_start+75))        
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
        self.game_states = []

    def saveGameState(self):
        """ Save the current game state, and add it to the game state array. """
        if len(self.game_states) >= MAX_SAVED_GAME_STATES:
            self.game_states = self.game_states[1:]
        self.game_states.append(GameState(self.game_grid))

    # Restore a game state from a GameState object
    def restoreGameState(self,game_state):
        self.game_grid.reset()
        self.game_grid.player = game_state.restorePlayer()
        for food in game_state.foods_loc:
            self.game_grid.addFood(food[0], food[1])

    # Rewind a given number of game states.
    def rewindGameState(self,num_to_rewind):
        if len(self.game_states) <= 1:
            return
        if num_to_rewind >= len(self.game_states):
            num_to_rewind = len(self.game_states) - 1

        self.game_states = self.game_states[:-num_to_rewind]
        self.restoreGameState(self.game_states[-1])
=======
    def __init__(self, in_game_manager):
        self.pickled_game_manager = None
        try:
            #dill.detect.trace(False)
            self.pickled_game_manager = pickle.dumps(in_game_manager)
        except Exception as e:
            traceback.print_exc()
            sys.exit(9)

    def restore(self):
        game_manager = None
        try:
           game_manager = pickle.loads(self.pickled_game_manager)
        except Exception as e:
            traceback.print_exc()
            sys.exit(9)
        return game_manager
>>>>>>> master

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

        pd.DataFrame(data_dict).to_csv(path.join(ABS_PATH, 'stat_data', f'agent_stats_round{self.round}.csv'), index=False)

# class SensoryMatrix:
class GameObject:
    """ TODO: ADD DOCSTRING """
    def __init__(self,x,y,raw_img_path=None,stage=None):
        if raw_img_path == None:
            raw_img_path = path.join(ABS_PATH, "art_assets","ERROR")
        self.type = None
        self.difficulty = DEFAULT_TERRAIN_DIFFICULTY
        self.x = x
        self.y = y
        self.stage = stage
        self.alive = True
        self.raw_img_path = raw_img_path
        self.calc_img_path(raw_img_path)
        self.loadImg(self.img_path)
        self.energy = 0    
        self.max_energy = 100

    def __getstate__(self):
        attributes = self.__dict__.copy()
        del attributes['img']
        del attributes['img_rect']
        return attributes
    
    def __setstate__(self, state):
        #print("Within setstate of GameObject")
        self.__dict__ = state
        self.calc_img_path(self.raw_img_path)
        self.loadImg(self.img_path)
    
    def consume(self,energy):
        self.energy += energy
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def deplete(self,energy):
        self.energy -= energy
        if self.energy <= 0:
            self.die()
    
    def die(self):
        self.alive = False
    
    def loadImg(self, img_path):
        self.img = pg.image.load(img_path)
        self.img = pg.transform.scale(self.img,(SQUARE_SIZE,SQUARE_SIZE))
        self.img_rect = self.img.get_rect()

    def calc_img_path(self, raw_img_path):
        if self.stage is not None:
            img_path = f"{raw_img_path}{self.stage}.png"
        else:
            img_path = f"{raw_img_path}.png"
        if path.exists(img_path):
            self.img_path = img_path
        else:
            print(f"ERROR: FILE NOT FOUND ({img_path})")
            sys.exit(101)

    def move_instant(self,x,y):
        """ Move to a location without using energy """
        self.x = x
        self.y = y

    def move_probabalistic(self, movement_matrix):
        """ Input a 3x3 matrix, pick a direction based on probabilities """

        movement_list = list(range(0,9))
        movement = random.choices(movement_list,weights=movement_matrix.flatten().tolist())
        return movement[0]

    def draw(self,x,y,surface):
        surface.blit(self.img, self.img_rect.move(x,y))

class Plant(GameObject):
    def __init__(self,x=None, y=None):
        self.stage = 1
        self.raw_img_path = path.join(ABS_PATH, "art_assets","plant_growth","plant")
        super().__init__(x,y,self.raw_img_path,stage=self.stage)
        # Probability of growth per round
        self.growth_rate = 0.9
        self.num_stages = 5
        self.max_energy = 100
        self.energy = 10
        self.energy_steps = int(self.max_energy / self.num_stages)

    def tick(self):
        if random.random() < self.growth_rate:
            self.grow()

        new_stage = self.energy2stage()
        if new_stage != self.stage:
            self.stage = new_stage
            self.calc_img_path(self.raw_img_path)
            self.loadImg(self.img_path)

    def grow(self):
        self.energy += 1
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    # Calculate stage based on energy level:
    def energy2stage(self):
        for i in range(self.num_stages+1):
            if self.energy <= i * self.energy_steps:
                return i
        return i

class Agent(GameObject):
    def __init__(self,x=None,y=None,raw_img_path=None,parent_1=None,parent_2=None):
        global AGENT_ID
        self.sprite_path = path.join(ABS_PATH, "art_assets","agent_faces","neutral")
        if raw_img_path is None:
            self.raw_img_path = path.join(self.sprite_path,"agent_faces")
        else:
            self.raw_img_path = raw_img_path

        super().__init__(x,y,self.raw_img_path)
        self.stats = AgentStats(parent_1=parent_1,parent_2=parent_2)
        self.sense = AgentSense()
        self.movement_choice = 4
        self.max_energy = MAX_ENERGY
        self.energy = self.max_energy
        self.health = MAX_HEALTH
        self.score = 0
        self.alive = True
        self.type = ObjectType.NEUTRAL
        self.pregnant = -1
        self.id = AGENT_ID
        AGENT_ID += 1
        self.sense.id = self.id
        self.good_choice_chance = DEFAULT_INTELLIGENCE
        self.score = 0
        self.age = 0
        self.mate = None
        self.last_pregnant_age = -PREGNANCY_COOLDOWN
        self.selected = False
        self.is_pregnant = False
        self.mating_cooldown = 0
        self.mating_cooldown_max = 5
    def __setstate__(self, state):
        self.__dict__ = state
        self.calc_color()
        
    def choose_sprite(self):
        def finalize_sprite(old_path):    
            if old_path != self.raw_img_path:
                self.calc_img_path(self.raw_img_path)
                self.loadImg(self.img_path)
      
        if self.raw_img_path:
            old_raw_path = self.raw_img_path
        else:
            old_raw_path = None

        is_baby = self.age < AGE_OF_CONSENT
        self.is_pregnant = self.pregnant > 0
        
        sprite_file_name = "agent_faces"

        if is_baby:
            sprite_file_name += "_baby"
        elif self.is_pregnant:
            sprite_file_name += "_procreation"
        if not self.alive:
            sprite_file_name += "_dead"
            self.raw_img_path = path.join(self.sprite_path,sprite_file_name)
            finalize_sprite(old_raw_path)
            return

        if self.selected:
            sprite_file_name += "_main"
        #elif self.type == ObjectType.EVIL:
            #sprite_file_name += "_evil"
        self.raw_img_path = path.join(self.sprite_path,sprite_file_name)
        finalize_sprite(old_raw_path)
        return

    def consume(self,energy):
        self.energy += energy
        if self.energy > self.max_energy:
            self.energy = self.max_energy
        if self.pregnant >= 0:
            self.pregnant += energy
        
        health_score = self.health/MAX_HEALTH
        if health_score < 0.001:
            health_score = 0.001
        energy_score = self.energy/MAX_ENERGY
        if energy_score < 0.001:
            energy_score = 0.001

        self.score += energy * health_score * energy_score

    def tick(self):
        if self.mating_cooldown > 0:
            self.mating_cooldown -= 1
        if self.energy <= 0 or self.health <= 0:
            self.die()

        if self.selected and self.alive:
            self.heal()
        # if self.type == ObjectType.EVIL:
        #     print(f"EVIL: {self.age}")
        # else:
        #     print(f"GOOD: {self.age}")

    def choose_movement(self):
        move = random.randint(0,8)

        if random.random() <= self.good_choice_chance:
            smell_list = list(self.sense.food_smell.flatten())
            move = smell_list.index(max(smell_list))
            if sum(smell_list) < 100:
                move = random.randint(0,8)

        return move

    def move(self,x,y,difficulty):
        self.x = x
        self.y = y
        self.energy -= difficulty

    def heal(self):
        if self.health < MAX_HEALTH:
            self.health += 1
            self.deplete(1)
            self.calc_color()

<<<<<<< HEAD
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
=======
    def die(self):
        # self.raw_img_path = path.join(ABS_PATH, "art_assets","agent_faces","agent_faces_dead")
        # self.calc_img_path(self.raw_img_path)
        # self.loadImg(self.img_path)
        blue = 0
        if self.type == ObjectType.EVIL:
            blue = 255
        self.img.fill(pg.Color(255,0,blue,1),special_flags=pg.BLEND_MIN)
        self.alive = 0

    def select(self):
        self.selected = True

    def calc_color(self):
        self.loadImg(self.img_path)
        red_color =  int(255-(255 * (self.health/MAX_HEALTH)))
        if red_color < 0:
            red_color = 0

        self.img.fill(pg.Color(255,255-red_color,255-red_color,1),special_flags=pg.BLEND_MIN)

    def take_damage(self, damage):
        hit = damage*(self.stats.stats["endurance"]/self.stats.gene_cap)
        self.health -= hit
        if self.health >= 0:
            self.calc_color()
        else:
            self.die()

        return hit
    
    def draw(self,x,y,surface):
        self.choose_sprite()
        if self.type == ObjectType.EVIL:
            self.img.fill(pg.Color("#AAAAFF"),special_flags=pg.BLEND_MIN)
        surface.blit(self.img, self.img_rect.move(x,y))
        if self.selected:
            self.sense.draw(surface)

    def attempt_mate(self,mate):
        if self.age >= AGE_OF_CONSENT and self.pregnant == -1 and self.mating_cooldown <= 0:
            if mate.id != self.id and mate.type == self.type and mate.is_pregnant == False and mate.alive and mate.age >= AGE_OF_CONSENT:
                #if (target_agent.age - target_agent.last_pregnant_age >= PREGNANCY_COOLDOWN):
                if self.x == mate.x and self.y == mate.y:
                    fertility_score = mate.stats.stats["fertility"] + self.stats.stats["fertility"]  
                    needed = random.randint(0,self.stats.gene_cap*2)
                    if fertility_score >= needed:
                        if VERBOSE:
                            print(f"{self.id} has impregnated {mate.id}!")
                        mate.is_pregnant = True
                        mate.pregnant = 0
                        mate.current_mate = self
                        self.mating_cooldown = self.mating_cooldown_max
    
    def give_birth(self,x,y):
        self.is_pregnant = False
        self.pregnant = -1
        self.last_pregnant_age = self.age
        
        
        if (self.type != ObjectType.EVIL):
            if self.mate != None:
                baby = Agent(x, y,parent_1=self,parent_2=self.mate)
            else:
                baby = Agent(x, y,parent_1=self,parent_2=self)

        else:
            if self.mate != None:
                baby = EvilAgent(x, y,parent_1=self,parent_2=self.mate)
            else:
                baby = EvilAgent(x, y,parent_1=self,parent_2=self)
        
        self.mate = None
        baby.energy = PREGNANCY_FOOD_GOAL
        self.deplete(PREGNANCY_FOOD_GOAL)
        return baby

class EvilAgent(Agent):
    def __init__(self,x=None,y=None,parent_1=None,parent_2=None):
        self.raw_img_path = None
        super().__init__(x,y,parent_1=parent_1,parent_2=parent_2)
        self.sprite_path = path.join(ABS_PATH, "art_assets","agent_faces","evil")
        self.choose_sprite()
        self.type = ObjectType.EVIL
        self.good_choice_chance = DEFAULT_EVIL_INTELLIGENCE
        self.sense.type = ObjectType.EVIL
        self.max_energy = MAX_ENERGY * 2
        self.energy = self.max_energy
>>>>>>> master
    
    def choose_movement(self):
        move = random.randint(0,8)
        if random.random() <= self.good_choice_chance:
            smell_list = list(self.sense.creature_smell.flatten())
            move = smell_list.index(max(smell_list))
            if sum(smell_list) < 100:
                move = random.randint(0,8)

        return move

class AgentSense:
    def __init__(self):
        self.sm_font = Font(path.join(ABS_PATH,"Retron2000.ttf"), 11)

        self.sight_dist_from_agent = 2
        self.smell_dist_from_agent = 1

<<<<<<< HEAD
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
            print(f"{x}, {y}.\n{self.occupied_grid}, {self.occupied_spaces}")

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
=======
        self.sight_range = self.sight_dist_from_agent * 2 + 1
        self.smell_range = self.smell_dist_from_agent * 2 + 1

        self.reset_sight()
        self.reset_smell()
        
        self.sight_rects = []
        self.smell_rects = []
>>>>>>> master


        self.type = ObjectType.NEUTRAL
        
        for i in range(4):
            sight_rect = pg.Rect(
                            10 + 60 * i,
                            WINDOW_HEIGHT - 60,
                            50,
                            50
                            )
            self.sight_rects.append(sight_rect)


        for i in range(2):
            smell_rect = pg.Rect(
                            10 + 60 * 4 + 60 * i,
                            WINDOW_HEIGHT - 60,
                            50,
                            50
                            )
            self.smell_rects.append(smell_rect)

    # Reference: https://realpython.com/python-pickle-module/
    def __getstate__(self):
        #print("Within getState of AgentSense")
        attributes = self.__dict__.copy()
        del attributes['sight_rects']
        del attributes['smell_rects']
        del attributes['sm_font']
        return attributes
    
    def __setstate__(self, state):
        #print("Within setstate of AgentSense")
        self.__dict__ = state
        self.sm_font = Font(path.join(ABS_PATH,"Retron2000.ttf"), 11)
        self.sight_rects = []
        for i in range(4):
            sight_rect = pg.Rect(
                            10 + 60 * i,
                            WINDOW_HEIGHT - 60,
                            50,
                            50
                            )
            self.sight_rects.append(sight_rect)
        self.smell_rects = []
        for i in range(2):
            smell_rect = pg.Rect(
                            10 + 60 * 4 + 60 * i,
                            WINDOW_HEIGHT - 60,
                            50,
                            50
                            )
            self.smell_rects.append(smell_rect)
    
    def reset_sight(self):
        self.elevation_sight = np.zeros((self.sight_range,self.sight_range))
        self.food_sight = np.zeros((self.sight_range,self.sight_range))
        self.creature_sight = np.zeros((self.sight_range,self.sight_range))
        self.danger_sight = np.zeros((self.sight_range,self.sight_range))

    def apply_sight_to_array(self):
        self.sight_senses = []

        self.sight_senses.append(self.elevation_sight)
        self.sight_senses.append(self.food_sight)
        self.sight_senses.append(self.creature_sight)
        self.sight_senses.append(self.danger_sight)

<<<<<<< HEAD
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
=======
    def apply_smell_to_array(self):
        self.smell_senses = []
>>>>>>> master

        self.smell_senses.append(self.food_smell)
        self.smell_senses.append(self.creature_smell)

    def reset_smell(self):
        self.food_smell = np.zeros((self.smell_range,self.smell_range))
        self.creature_smell = np.zeros((self.smell_range,self.smell_range))

    def draw(self, surface):

        surface.blit(self.sm_font.render(f"Terrain", 0, (255, 0, 0)), (10, WINDOW_HEIGHT - 80))
        surface.blit(self.sm_font.render(f"Food", 0, (255, 0, 0)), (80, WINDOW_HEIGHT - 80))
        surface.blit(self.sm_font.render(f"Agent", 0, (255, 0, 0)), (135, WINDOW_HEIGHT - 80))
        surface.blit(self.sm_font.render(f"Danger", 0, (255, 0, 0)), (190, WINDOW_HEIGHT - 80))

        surface.blit(self.sm_font.render(f"Food", 0, (255, 0, 0)), (260, WINDOW_HEIGHT - 80))
        surface.blit(self.sm_font.render(f"Agent", 0, (255, 0, 0)), (320, WINDOW_HEIGHT - 80))

<<<<<<< HEAD
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
=======

        for i in range(4):
            img = Image.fromarray(self.sight_senses[i]).convert('RGB')
            sense_img = pg.image.fromstring(img.tobytes("raw","RGB"), img.size, img.mode)                
            sense_img = pg.transform.scale(sense_img,(50,50))
            surface.blit(sense_img, self.sight_rects[i])
            drawGenericGrid(self,surface,self.sight_rects[i],5,5)

        for i in range(2):
            img = Image.fromarray(self.smell_senses[i]).convert('RGB')
            sense_img = pg.image.fromstring(img.tobytes("raw","RGB"), img.size, img.mode)                
            sense_img = pg.transform.scale(sense_img,(50,50))
            surface.blit(sense_img, self.smell_rects[i])
            drawGenericGrid(self,surface,self.smell_rects[i],3,3)


    def flip_matrices(self):
        for i in range(4):
            self.sight_senses[i] = np.rot90(self.sight_senses[i],2) 
            #self.sight_senses[i] = np.fliplr(self.sight_senses[i])
            #self.sight_senses[i] = np.flipud(self.sight_senses[i])
        
    def update(self,x,y,grid,agents,plants):
        self.update_sight(x,y,grid,agents,plants)
        self.update_smell(x,y,grid,agents,plants)
        grid_loc_x = 0
        for x_offset in range(-self.smell_dist_from_agent, self.smell_dist_from_agent+1):
            grid_loc_y = 0
            for y_offset in range(-self.smell_dist_from_agent, self.smell_dist_from_agent+1):
                x_new = x + x_offset
                y_new = y + y_offset
                if grid.checkValidTile(x_new,y_new):
                    for agent in agents:
                        if agent.id != self.id:
                            if not (self.type == ObjectType.EVIL and agent.type == ObjectType.EVIL):
                                self.creature_smell[grid_loc_y,grid_loc_x] += (0.5/(fast_dist(x_new,y_new,agent.x,agent.y)+1))*255

                    for plant in plants:
                        self.food_smell[grid_loc_y,grid_loc_x] += (0.5/(fast_dist(x_new,y_new,plant.x,plant.y)+1))*(plant.energy/plant.max_energy)*255

                        
                else:
                    self.creature_smell[grid_loc_y,grid_loc_x] = 0
                    self.food_smell[grid_loc_y,grid_loc_x] = 0
                grid_loc_y += 1
            grid_loc_x += 1
        self.apply_smell_to_array()

    def update_sight(self,x,y,grid,agents,plants):
        self.reset_sight()
        self.reset_smell()

        grid_loc_x = 0
        for x_offset in range(-self.sight_dist_from_agent, self.sight_dist_from_agent+1):
            grid_loc_y = 0
            for y_offset in range(-self.sight_dist_from_agent, self.sight_dist_from_agent+1):
                x_new = x + x_offset
                y_new = y + y_offset
                if grid.checkValidTile(x_new,y_new):
                    self.elevation_sight[grid_loc_y,grid_loc_x] = grid.elevation_map[x_new,y_new]
                    self.creature_sight[grid_loc_y,grid_loc_x] = 128
                    self.danger_sight[grid_loc_y,grid_loc_x] = 128
                    self.food_sight[grid_loc_y,grid_loc_x] = 128

                    for agent in agents:
                        if agent.x == x_new and agent.y == y_new:
                            self.creature_sight[grid_loc_y,grid_loc_x] = 255
                            if agent.type == ObjectType.EVIL:
                                self.danger_sight[grid_loc_y,grid_loc_x] = 255

                    for plant in plants:
                        if plant.x == x_new and plant.y == y_new:
                            self.food_sight[grid_loc_y,grid_loc_x] = 255

                else:
                    self.elevation_sight[grid_loc_y,grid_loc_x] = 255
                    self.creature_sight[grid_loc_y,grid_loc_x] = 0
                    self.danger_sight[grid_loc_y,grid_loc_x] = 0
                    self.food_sight[grid_loc_y,grid_loc_x] = 0

                grid_loc_y += 1
            grid_loc_x += 1
        #TODO: Cleanup this math
        self.apply_sight_to_array()
        #self.flip_matrices()

    def update_smell(self,x,y,grid,agents,plants):
        self.apply_smell_to_array()

class AgentStats:
    def __init__(self,parent_1=None,parent_2=None):
        # All Stats range from 1 to 10
        
        self.gene_avg = 4
        self.gene_cap = 10
        self.gene_min = 1

        self.stats = {}
        self.stats["speed"] = self.gene_min
        self.stats["agility"] = self.gene_min
        self.stats["intelligence"] = self.gene_min
        self.stats["endurance"] = self.gene_min
        self.stats["strength"] = self.gene_min
        self.stats["fertility"] = self.gene_min
        self.stats["bite_size"] = self.gene_min
        self.stats["gene_stability"] = self.gene_min
        
        # If GS == 10, only mod by gene_avg
        # If GS == 1, mod gene_avg * 5
        
        self.gene_limit = self.gene_avg*len(self.stats)*self.gene_min
        if parent_1 != None and parent_2 != None:
            self.assignFromParents(parent_1,parent_2)
        else:
            self.scramble_genetics()

        self.cleanGenes()
        print(self.stats)

    def getNumMoves(self):
        speed = self.stats["speed"]
        if speed <= 3:
            return 1
        elif speed <= 6:
            return 2
        elif speed <= 9:
            return 3
        return 1
    def assignFromParents(self,parent_1, parent_2):
        for key in self.stats:
            self.stats[key] = (parent_1.stats.stats[key] + parent_2.stats.stats[key])/2
        # genes_to_mod = self.gene_cap/self.stats["gene_stability"]/2 + 1
        genes_to_mod = 10
        amount_to_mod = (self.gene_cap/self.stats["gene_stability"])/self.gene_avg

        for i in range(int(genes_to_mod)):
            self.addToRandGene(amount_to_mod)
            self.subFromRandGene(amount_to_mod)

    def addToRandGene(self,amount):
        assigned = False
        while not assigned:
            key = random.choice(list(self.stats.keys()))
            if self.stats[key] < self.gene_cap:
                self.stats[key] += amount
                assigned = True

    def subFromRandGene(self,amount):
        assigned = False
        while not assigned:
            key = random.choice(list(self.stats.keys()))
            if self.stats[key] - amount >= self.gene_min:
                self.stats[key] -= 1
                assigned = True

    def cleanGenes(self):
        for key in self.stats:
            self.stats[key] = round(self.stats[key],3)
            if self.stats[key] < self.gene_min:
                self.stats[key] = self.gene_min
            if self.stats[key] > self.gene_cap:
                self.stats[key] = self.gene_cap

    def scramble_genetics(self):
        for i in range(self.gene_limit - len(self.stats)):
            assigned = False
            while not assigned:
                key = random.choice(list(self.stats.keys()))
                if self.stats[key] < self.gene_cap:
                    self.stats[key] += 1
                    assigned = True
class Grid:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.padding = 1
        self.square_size = int(WINDOW_WIDTH/GAME_GRID_WIDTH*0.8)
        self.grid_padding = self.calcGridPadding()
        self.calcGridSize()

        self.occupied_grid = np.zeros((GAME_GRID_WIDTH,GAME_GRID_HEIGHT))
        
        self.default_color = pg.Color("#FFFFFF")
        self.line_color = pg.Color("#010101")
        self.calcHeightMap()

    def __getstate__(self):
        #print("Within getState of Grid")
        attributes = self.__dict__.copy()
        del attributes['default_color']
        del attributes['line_color']
        del attributes['elevation_map_img']
        return attributes
    
    def __setstate__(self, state):
        #print("Within setstate of Grid")
        self.__dict__ = state
        self.default_color = pg.Color("#FFFFFF")
        self.line_color = pg.Color("#010101")
        
        # Redraw elevation map image
        img_path = path.join(ABS_PATH,"height.png")
        elevation_map_img = pg.image.load(img_path)
        
        self.elevation_map_img = pg.transform.scale(elevation_map_img,(self.total_x,self.total_y))
        self.elevation_map_img = pg.transform.rotate(self.elevation_map_img,90)
        self.elevation_map_img = pg.transform.flip(self.elevation_map_img,0,1)

    def calcRandNearby(self,x,y,rand_range):
        rand_range = rand_range * 2
        found = False
        empty_range = self.checkEmptyInRange(x,y,rand_range)
        if empty_range == []:
            return None, None
        tuple = random.choice(empty_range)
        return tuple[0], tuple[1]

    def checkEmptyInRange(self,x,y,rand_range):
        empties = []
        for i in range(-rand_range, rand_range + 1):
            for j in range(-rand_range, rand_range + 1):
                if self.checkValidTile(x+i,y+j):
                    if self.occupied_grid[x+i][y+j] == 0:
                        empties.append([x+i,y+j])
        return empties

    # Check to make sure a given XY set is 
    def checkValidTile(self,x,y):
        if x >= 0 and y >= 0:
            if x < GAME_GRID_WIDTH and y < GAME_GRID_HEIGHT:
                return True
        return False

    def calcHeightMap(self):
        self.elevation_map = np.random.randint(0,high=250, size=(GAME_GRID_WIDTH,GAME_GRID_HEIGHT))
        img_path = path.join(ABS_PATH,"height.png")
        img = Image.fromarray(self.elevation_map).convert('L').filter(ImageFilter.GaussianBlur(1))
        img.save(img_path)
        self.elevation_map = np.asarray(Image.open(img_path)).copy()
        arr_max = self.elevation_map.max()
        arr_min = self.elevation_map.min()

        for x in range(GAME_GRID_WIDTH):
            for y in range(GAME_GRID_HEIGHT):
                val = np.interp(self.elevation_map[x][y],[arr_min,arr_max],[20,255])
                self.elevation_map[x,y] = val

        img = Image.fromarray(self.elevation_map).convert('L')
        img.save(img_path)
        
        elevation_map_img = pg.image.load(img_path)
        
        self.elevation_map_img = pg.transform.scale(elevation_map_img,(self.total_x,self.total_y))
        self.elevation_map_img = pg.transform.rotate(self.elevation_map_img,90)
        self.elevation_map_img = pg.transform.flip(self.elevation_map_img,0,1)
>>>>>>> master

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
        if np.count_nonzero(self.occupied_grid) < NUM_SPACES*0.5:
            found = False
            while found == False:
                x,y = self.randGridSpace()
                if self.occupied_grid[x][y] == 0:
                    found = True
            return x,y 
        else:
            empty_left = NUM_SPACES-len(occupied_spaces)
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
            sys.exit(9)

    # Calculate the amount of padding needed for the current grid.
    def calcGridPadding(self):
        self.total_grid_x = self.width*self.padding + self.width*self.square_size
        self.grid_padding = int((WINDOW_WIDTH - self.total_grid_x)/2)
        return self.grid_padding

    # Calculate a XY location for a given tile location
    def calcTileLocation(self,tile):
        x = tile.x * self.padding + tile.x * self.square_size + self.grid_padding
        y = tile.y * self.padding + tile.y * self.square_size + self.grid_padding
        x += self.padding*2
        y += self.padding*2
        return x, y
    
    def calcXYLocation(self,x,y):
        world_x = x * self.padding + x * self.square_size + self.grid_padding
        world_y = y * self.padding + y * self.square_size + self.grid_padding
        world_x += self.padding*2
        world_y += self.padding*2
        return world_x, world_y
        
    def calcTileFromXY(self,x,y):

        if x <= self.grid_padding or y <= self.grid_padding:
            return None, None
        if x >= self.grid_padding + GAME_GRID_WIDTH * (self.padding + self.square_size):
            return None, None
        if y >= self.grid_padding + GAME_GRID_HEIGHT * (self.padding + self.square_size):
            return None, None

        tile_x = None
        tile_y = None

        for i in range(GAME_GRID_WIDTH):
            j = i + 1
            low = i * self.padding + i * self.square_size + self.grid_padding
            high = j * self.padding + j * self.square_size + self.grid_padding
            if low <= x <= high:
                tile_x = i 

        for i in range(GAME_GRID_HEIGHT):
            j = i + 1
            low = i * self.padding + i * self.square_size + self.grid_padding
            high = j * self.padding + j * self.square_size + self.grid_padding
            if low <= y <= high:
                tile_y = i

        return tile_x, tile_y
        

    # Get a tile by it's coordinates. If no tile matches, return None
    def getTile(self,x,y):
        if not self.checkValidTile(x,y):
            return None
        for tile in self.occupied_spaces:
            if tile.x == x and tile.y == y:
                return tile
        return None

    def calcGridSize(self):
        self.total_x = self.width * self.padding + self.width * self.square_size
        self.total_y = self.height * self.padding + self.height * self.square_size

    # Draw the grid without anything else.
    def drawGrid(self,surface):
        grid_pos_x = self.padding + self.grid_padding
        for i in range(self.height + 1):
            pg.draw.rect(
                        surface,
                        self.line_color,
                        pg.Rect(
                            grid_pos_x,
                            self.padding + self.grid_padding, 
                            self.padding, 
                            self.total_y)
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
                            self.total_x,
                            self.padding
                            )
                    )
            grid_pos_y += self.square_size + self.padding

<<<<<<< HEAD
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

    # Move the player in a direction.
    def movePlayer(self,direction_list):
        # Dir is a number between 0 and 3:
        # 0 -> North (UP)
        # 1 -> South (DOWN)
        # 2 -> WEST (LEFT)
        # 3 -> EAST (RIGHT)

        # (x, y) = number of players on grid position
        # food and unoccupied grid positions not tracked
        position_dct = self.getPlayerPositionDict()

        for index, direction in enumerate(direction_list):
            old_x, old_y = self.player[index].tile.x, self.player[index].tile.y
            new_x, new_y = self.player[index].move(direction, 1)

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
=======
    def draw(self, surface):
        x = self.padding + self.grid_padding
        y = self.padding + self.grid_padding
        
        rect = self.elevation_map_img.get_rect().move((x,y))
        surface.blit(self.elevation_map_img, rect)
>>>>>>> master


<<<<<<< HEAD
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
=======
        self.drawGrid(surface)
>>>>>>> master

class GameManager:
    """ A class that controls the logic and graphics of the game. """
    def __init__(self,width,height):
        self.grid = Grid(height, width)
        self.agents = []
        self.plants = []
        
        self.addAgent()
        self.font = Font(path.join(ABS_PATH,"Retron2000.ttf"), 12)
        
        self.agents[0].select()
        self.main_agent = self.agents[0]
        for i in range(NUM_EVIL):
            self.addEvilAgent()
        for i in range(NUM_AGENTS-1):
            self.addAgent()
    
        for curr in self.agents:
            curr.age = AGE_OF_CONSENT
            
        #self.addAgent(ObjectType.PROCREATION, path.join(ABS_PATH, "art_assets","agent_faces","agent_faces_procreation"))
        
        for i in range(MAX_NUM_FOOD_ON_GRID):
            self.addPlant()
    
    def __getstate__(self):
        #print("Within getState of GameManager")
        attributes = self.__dict__.copy()
        del attributes['font']
        return attributes
    
    def __setstate__(self, state):
        #print("Within setstate of GameManager")
        self.__dict__ = state
        self.font = Font(path.join(ABS_PATH,"Retron2000.ttf"), 25)
    
    def selectFromXY(self,x,y):
        calc_x, calc_y = self.grid.calcTileFromXY(x,y)
        selected_id = None
        if calc_x != None and calc_y != None:
            for agent in self.agents:
                if agent.x == calc_x and agent.y == calc_y:
                    selected_id = agent.id
        if selected_id != None:
            self.selectByID(selected_id)

    def selectByID(self,sel_id):
        for agent in self.agents:
            if agent.id == sel_id:
                agent.select()
            else:
                agent.selected = False

    def draw(self,game_window):
        self.grid.draw(game_window)
        # Draw plants
        for plant in self.plants:
            world_x, world_y = self.grid.calcXYLocation(plant.x,plant.y)
            plant.draw(world_x, world_y, game_window)

        for agent in self.agents:
                world_x, world_y = self.grid.calcXYLocation(agent.x,agent.y)
                agent.draw(world_x, world_y, game_window)
        


        for agent in self.agents:
            if agent.selected:
                self.main_agent = agent
        labels_y_start = 470
        game_window.blit(self.font.render(f"ID: {self.main_agent.id}", 0, (255, 0, 0)), (self.grid.grid_padding, labels_y_start))
        game_window.blit(self.font.render(f"HEALTH: {round(self.main_agent.health,2)}", 0, (255, 0, 0)), (self.grid.grid_padding, labels_y_start+20))

        game_window.blit(self.font.render(f"ENERGY: {round(self.main_agent.energy,2)}", 0, (255, 0, 0)), (self.grid.grid_padding, labels_y_start+40))
        game_window.blit(self.font.render(f"SCORE:   {round(self.main_agent.score,2)}", 0, (255, 0, 0)), (self.grid.grid_padding, labels_y_start+60))
        stats1 = {}
        stats2 = {}
        index = 0
        for key in self.main_agent.stats.stats:
            if index < 4:
                stats1[key] = self.main_agent.stats.stats[key]
            else:
                stats2[key] = self.main_agent.stats.stats[key]
            index += 1
        
        game_window.blit(self.font.render(f"{stats1}", 0, (255, 0, 0)), (self.grid.grid_padding, labels_y_start+80))
        game_window.blit(self.font.render(f"{stats2}", 0, (255, 0, 0)), (self.grid.grid_padding, labels_y_start+100))

    def plantTick(self):
        for plant in self.plants:
            plant.tick()

    def agentTick(self,agent,move=None):
        if agent.alive == 0:
            return
        agent.tick()
        if move == None:
            move = agent.choose_movement()

        offset_x, offset_y, difficulty = dir2offset(move)
        old_x = agent.x
        old_y = agent.y
        new_x = agent.x + offset_x
        new_y = agent.y + offset_y
        
        if self.grid.checkValidTile(new_x, new_y):
            curr_height = self.grid.elevation_map[agent.x][agent.y]
            new_height = self.grid.elevation_map[new_x][new_y]
            difficulty = 1
            diff_add = (int(new_height) - int(curr_height))/255

            difficulty = DEFAULT_TERRAIN_DIFFICULTY + diff_add
            #TODO Finish this

            agent.move(new_x,new_y,difficulty)

        if agent.type != ObjectType.EVIL:
            for plant in self.plants:
                if agent.x == plant.x and agent.y == plant.y:
                    if EAT_PLANT_INSTANT:
                        agent.consume(plant.energy)
                        self.plants.remove(plant)
                        self.addPlant()
                    else:
                        #if agent.pregnant >= 0:
                        #    agent.pregnant += 1
                        if plant.energy > 10:
                            agent.consume(10)
                            plant.deplete(10)
                        else:
                            agent.consume(plant.energy)
                            self.plants.remove(plant)
                            self.addPlant()

                for target_agent in self.agents:
                    if agent.x == target_agent.x and agent.y == target_agent.y:    
                        agent.attempt_mate(target_agent)

                # if agent.age >= AGE_OF_CONSENT and agent.pregnant == -1:
                #     for target_agent in self.agents:
                #         if target_agent.id != agent.id and target_agent.type == agent.type and target_agent.pregnant == -1 and target_agent.alive and target_agent.age >= AGE_OF_CONSENT and (target_agent.age - target_agent.last_pregnant_age >= PREGNANCY_COOLDOWN):
                #             if agent.x == target_agent.x and agent.y == target_agent.y:
                #                 target_agent.pregnant = 0
                                #if (target_agent.type == ObjectType.EVIL):
                                    #target_agent.img.fill(pg.Color("#AAAAFF"),special_flags=pg.BLEND_MIN)
        else:
            for target_agent in self.agents:
                if target_agent.type != ObjectType.EVIL or not target_agent.alive or agent.energy < 30:
                    if target_agent.alive:
                        if agent.id != target_agent.id and agent.x == target_agent.x and agent.y == target_agent.y:
                            hit_strength = agent.stats.stats["strength"]
                            damage = target_agent.take_damage(hit_strength)
                            agent.consume(damage)
                    else:
                        bite = agent.stats.stats["bite_size"]
                        if target_agent.energy > bite:
                            agent.consume(bite)
                            #if agent.pregnant >= 0:
                            #    agent.pregnant += 10
                            target_agent.deplete(bite)
                        else:
                            agent.consume(target_agent.energy)
                            #if agent.pregnant >= 0:
                            #    agent.pregnant += target_agent.energy
                            if (target_agent.selected):
                                for candidate in self.agents:
                                    if (candidate.type != ObjectType.EVIL and candidate.alive):
                                        candidate.select()
                                        break
                            target_agent.selected = False
                            self.agents.remove(target_agent)
            
            for target_agent in self.agents:
                if agent.x == target_agent.x and agent.y == target_agent.y:    
                    agent.attempt_mate(target_agent)
            # if agent.age >= AGE_OF_CONSENT and agent.pregnant == -1:
            #     for target_agent in self.agents:
            #         if target_agent.id != agent.id and target_agent.type == agent.type and target_agent.is_pregnant == False and target_agent.alive and target_agent.age >= AGE_OF_CONSENT:
            #             #if (target_agent.age - target_agent.last_pregnant_age >= PREGNANCY_COOLDOWN):
            #             if agent.x == target_agent.x and agent.y == target_agent.y:
            #                 fertility_score = target_agent.stats.stats["fertility"] + agent.stats.stats["fertility"]  
            #                 needed = random.randint(0,agent.stats.gene_cap*2)
            #                 if fertility_score >= needed:
            #                     if VERBOSE:
            #                         print(f"{agent.id} has impregnated {target_agent.id}!")
            #                     target_agent.is_pregnant = True
            #                     target_agent.pregnant = 0
                            #target_agent.raw_img_path = path.join(ABS_PATH,"art_assets","agent_faces","agent_faces_procreation_evil")
                            #target_agent.calc_img_path(target_agent.raw_img_path)
                            #target_agent.loadImg(target_agent.img_path)
                            #target_agent.img.fill(pg.Color("#AAAAFF"),special_flags=pg.BLEND_MIN)

        if agent.alive and agent.pregnant >= PREGNANCY_FOOD_GOAL:
            baby_x, baby_y = self.grid.calcRandNearby(agent.x, agent.y, 1)
            baby = agent.give_birth(baby_x, baby_y)
            
            self.agents.append(baby)
            baby.sense.update(baby.x, baby.y, self.grid, self.agents,self.plants)
            if VERBOSE:
                print(f"{agent.id} has given birth to {baby.id}!")
        
        agent.sense.update(agent.x,agent.y,self.grid,self.agents,self.plants)
        agent.age += 1


    def logicTick(self,player_move=None,draw_func=None):
        random.shuffle(self.plants)
        self.plantTick()

        #TODO Prove this won't skip anyone if someone is killed or is born
        run_ids = []

        remaining_ids = []
        for agent in self.agents:
            remaining_ids.append(agent.id)

        while len(run_ids) < len(self.agents):
            random.shuffle(self.agents)
            for agent in self.agents:
                if agent.id not in run_ids:
                    rand = random.randint(0,10)
                    if rand <= agent.stats.stats["agility"]:
                        for i in range(agent.stats.getNumMoves()):
                            self.agentTick(agent)
                            if draw_func != None:
                                draw_func()
                        run_ids.append(agent.id)


    def addPlant(self):
        x, y = self.grid.randEmptySpace()
        plant = Plant(x,y)
        self.plants.append(plant)

    def addAgent(self,agent_type=None,image_path=None):
        x, y = self.grid.randEmptySpace()
        agent = Agent(x,y,image_path)
        if agent_type is not None:
            agent.type = agent_type
        self.agents.append(agent)

    def addEvilAgent(self):
        x, y = self.grid.randEmptySpace()
        agent = EvilAgent(x,y)
        self.agents.append(agent)

    def setOccupiedGrid():
        self.grid.occupied_grid = np.zeros((GAME_GRID_WIDTH,GAME_GRID_HEIGHT))
        for plant in self.plants:
            self.grid.occupied_grid[plant.x][plant.y] = ObjectType.PLANT
        for agent in self.agents:
            self.grid.occupied_grid[agent.x][agent.y] = agent.type

<<<<<<< HEAD
=======
# All simple mouse does is pick a random direction, and moves there.
# Quite senseless, if you ask me.
def simple_mouse():
    return random.choice(range(0,4))

>>>>>>> master
# The smart mouse uses its nose to find food. It does this by checking
# which path has the greatest amount of food smells, and going in that
# direction. 

def smart_mouse(scent_matrix):
<<<<<<< HEAD
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

=======

    # If there are no scents, just pick a random direction.
    if not np.any(scent_matrix):
        return simple_mouse()
    
>>>>>>> master
    # Get the maximum value, or values
    indexes = [i for i, x in enumerate(scent_matrix) if x == max(scent_matrix)]

    # Make a random choice from all the best options
    move_choice = random.choice(indexes)
    return move_choice
    # return movement_array.index(max(movement_array))
<<<<<<< HEAD


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
=======
>>>>>>> master
