# --------------------
# This code has been made by Quietfart (pseudo) in July-August 2024.
# If you like my work, you can check my YouTube channel: https://www.youtube.com/@quietfart9591
# More contents will come on the channel.
# --------------------
# Ce code a été réalisé par Quietfart (pseudo) en Juillet-Aout 2024.
# Si vous aimez mon travail, vous pouvez jeter un coup d'oeil à ma chaine YouTube : https://www.youtube.com/@quietfart9591
# D'autres contenus arriveront sur la chaine.
# --------------------
import math
import random
import time

import pygame
pygame.font.init()
pygame.display.init()
pygame.mixer.init()
from utils import AnimatedCharacter, ProcessImage, get_filenames_anim_tiles, get_text_surf
from RollingText import RollingText, DialogueBoxText
from particles import ParticleSystem, get_random_speed

pygame.mixer.music.load("audio/lr_music.mp3")
pygame.mixer.music.play(-1)

dialogue_sound = pygame.mixer.Sound("audio/dialogue_sound.wav")
collision_sound = pygame.mixer.Sound("audio/collision_sound.wav")

# Load all images
filenames_char_anim = ["down1", "down2", "up1", "up2", "left1", "left2",
                           "idle_down", "idle_up", "idle_left"]
filenames_main_char_anim = ["down1", "down2", "up1", "up2", "left1", "left2", "left3",
                           "idle_down", "idle_up", "idle_left"]
filenames_flower = get_filenames_anim_tiles("flower", 4)
graphic_folder = "Graphics/"

# Creating variable with the folders_names
main_char_folder = graphic_folder + "main_character/"

npcs_folder = graphic_folder + "npcs/"
boy_folder = npcs_folder + "boy/"
girl_folder = npcs_folder + "girl/"
pinkboy_folder = npcs_folder + "pinkboy/"

anim_folder = graphic_folder + "animated_tiles/"
flower_folder = anim_folder + "flower/"


# Load and scale all images
img_processor_char = ProcessImage(2.5)
main_char_imgs = img_processor_char.load_and_scale_images(main_char_folder, filenames_main_char_anim)
boy_npc_imgs = img_processor_char.load_and_scale_images(boy_folder, filenames_char_anim)
girl_npc_imgs = img_processor_char.load_and_scale_images(girl_folder, filenames_char_anim)
pinkboy_npc_imgs = img_processor_char.load_and_scale_images(pinkboy_folder, filenames_char_anim)
flower_imgs = img_processor_char.load_images(flower_folder, filenames_flower)

# We use a different growing_factor for those images
processor_dialogue_box_img = ProcessImage(0.7, init_size=(1448, 260))
dialogue_box_img = processor_dialogue_box_img.load_and_scale_image(graphic_folder, "dialogue_box")

processor_leaf_img = ProcessImage(0.7, init_size=(32, 32))
leaf_img = processor_leaf_img.load_and_scale_image(graphic_folder, "leaf")


dialogue_pinkboy = ["Vous voulez une anecdote croustillante sur Quietfart ?", "Il est amoureux de Dora l'exploratrice."]
dialogue_girl = ["Quoicoubeh à tous !", "J'adore Mussolini et J.K. Rowling."]
dialogue_boy = ["A deux doigts d'envoyer le paquet dans mon calbute !", "Tu as senti le pet que je viens de lâcher ?"]
dilaogue_signs = {106: ["Maison de Corenti"], 107: ["Maison d'Arlithyr"], 108: ["Bourg-en-vol, la ville de la nature et du calme."],
                  109: ["Maison du Prof. Sekko"]}


# Class to load the tileset in an explicit datatype (list)
class Tileset:
    def __init__(self, file, tile_size, margin=0, spacing=(0, 0)):
        self.tile_size = tile_size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.image_dimensions = (self.image.get_width(), self.image.get_height())
        self.n_tiles_width, self.n_tiles_height = self.image_dimensions[0] // self.tile_size[0], (self.image_dimensions[1] // self.tile_size[1]) - 1  # to delete the up line of tiles
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    # Builds the list of tiles
    def load(self):

        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.tile_size[0] + self.spacing[0]
        dy = self.tile_size[1] + self.spacing[1]

        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                tile = pygame.Surface(self.tile_size, pygame.SRCALPHA)
                tile.blit(self.image, (0, 0), (x, y, *self.tile_size))
                self.tiles.append(tile)

    def blit_tileset(self):
        for i in range(self.n_tiles_height):
            for j in range(self.n_tiles_width):
                try:
                    screen.blit(self.tiles[i * self.n_tiles_width + j], (j * self.tile_size[0], i * self.tile_size[1]))
                except Exception as exc:
                    print(exc)


# An object that undergoes the scrolling
class Tile:

    def __init__(self, img, tile_rect, collider=False, below=True, npc=False):
        self.img = img
        self.rect = tile_rect
        self.collider = collider
        self.below = below
        self.npc = npc
        self.to_delete = False

    def update(self, main_char_rect, tiles):
        pass

    def draw(self, screen):
        screen.blit(self.img, self.rect.topleft)


# A tile that undergoes the scrolling but is also moving by itself (leaves)
class MovingTile(Tile):
    def __init__(self, img, rect, collider=False, below=False, npc=False):
        super().__init__(img, rect, collider, below, npc)
        """pos = [[-self.rect.width, random.randint(-self.rect.height, res[1] - self.rect.height)],
               [random.randint(0, res[0] - self.rect.width), -self.rect.height]]"""

        final_pos = [random.randint(0, res[0] - self.rect.width), -self.rect.height]#pos[random.randint(0, 1)]
        self.rect.x = final_pos[0]  # Outside left side of screen
        self.rect.y = final_pos[1]
        self.float_y = 0.0
        self.float_x = 0.0
        self.start_living_time = time.time()

    def update(self, main_char_rect, tiles):
        if time.time() - self.start_living_time > 20:
            self.to_delete = True
        self.float_y += 0.5
        self.rect.y = int(self.float_y)
        incr = 5*math.sin((self.rect.y)/10)
        self.rect.x += incr


# Tile that the player can "speak" with (Signs, NPCs, ...)
class SpeakingTile(Tile):
    def __init__(self, img, tile_rect, pos, dialogues=None):
        super().__init__(img, tile_rect, True, False, True)
        self.pos = pos
        self.dialogues = dialogues
        self.in_dialogue = False
        self.index_dialogue = 0
        self.current_text = DialogueBoxText("", font)
        self.rolling_texts = self.__create_rolling_texts()

    # Create the animated dialogues
    def __create_rolling_texts(self):
        rts = []
        for d in self.dialogues:
            rts.append(DialogueBoxText(d, font, pos=(50, res[1] - 150), rolling_speed=0.5))
        return rts

    # Dialogue logic
    def update(self, main_char_rect, tiles):
        dialogue_rect_player = pygame.Rect(0, 0, main_char_rect.width + 10, main_char_rect.height + 10)
        dialogue_rect_player.center = main_char_rect.center
        if not self.in_dialogue and dialogue_rect_player.colliderect(self.rect) and player_movements["action"]:
            self._modify_img()
            self.in_dialogue = True
            dialogue_sound.play()
            self.current_text = self.rolling_texts[self.index_dialogue]
        elif self.in_dialogue and dialogue_rect_player.colliderect(self.rect):
            if player_movements["action"]:
                if self.current_text.over:
                    dialogue_sound.play()
                    self.index_dialogue += 1
                if self.index_dialogue >= len(self.dialogues):  # End of dialogue
                    self.current_text.reset()
                    self.index_dialogue = 0
                    self.in_dialogue = False
                elif self.current_text.over:  # Change text when the previous one is over
                    prev_text = self.current_text
                    self.current_text = self.rolling_texts[self.index_dialogue]
                    prev_text.reset()
            self.current_text.update()
        else:  # Speaking tile movement, if it is not in dialogue
            if self.in_dialogue:
                self.in_dialogue = False
                self.current_text.reset()
            self._update(main_char_rect, tiles)

    def _modify_img(self):  # If we need to change the image of the tile (i.e. for NPC)
        pass

    # To move the tile
    def _update(self, main_char_rect, tiles):
        pass


# Non-Playable-Characters (NPCs)
class NPCTile(SpeakingTile):
    def __init__(self, imgs, tile_rect, pos, dialogues=None):
        super().__init__(imgs, tile_rect, pos, dialogues=dialogues)
        self.animation = AnimatedCharacter(imgs, 2)
        self.rect.width = imgs[0].get_width()
        self.rect.height = imgs[0].get_height()

    # Modify NPC image according to the direction of the player when speaking
    def _modify_img(self):
        direction = ""
        if main_char.last_img_key == "up":  # Player and NPC are facing
            direction = "down"
        if main_char.last_img_key == "down":
            direction = "up"
        if main_char.last_img_key == "left":
            direction = "right"
        if main_char.last_img_key == "right":
            direction = "left"
        self.img = self.animation.anim_imgs_dic['idle'][direction]


# For statics NPCs, e.g. signs
class NPCTileInanimated(NPCTile):
    def __init__(self, imgs, tile_rect, pos, facing="down", dialogues=None):
        super().__init__(imgs, tile_rect, pos, dialogues=dialogues)
        self.img = self.animation.anim_imgs_dic["idle"][facing]


# Same as NPCTile but a NPCTileAnimated implements "_update()" method such as it moves in random directions
class NPCTileAnimated(NPCTile):  # Moving and animated NPCs
    def __init__(self, imgs, tile_rect, pos=(0,0), anim_speed=0.04, dialogues=None):
        super().__init__(imgs, tile_rect, pos, dialogues=dialogues)
        self.rect.topleft = pos
        self.start_pos = pos
        self.position = "down"
        self.img = self.animation.anim_imgs_dic['idle'][self.position]  # Idle down
        self.current_time = time.time()
        self.moving = False
        self.start_moving_time = 0.0
        self.anim_counter = 0.0
        self.anim_speed = anim_speed

    def _update(self, main_char_rect, tiles):  # Collision, animation and movement of the NPC
        if not self.moving:
            if time.time() - self.current_time > 2 + random.random() * 3:
                if random.random() < 0.550:
                    self.position = random.choice(list(self.animation.anim_imgs_dic['idle'].keys()))
                    self.img = self.animation.anim_imgs_dic['idle'][self.position]  # Random among idle pictures
                    self.current_time = time.time()
                else:
                    self.moving = True
                    self.start_moving_time = time.time()
        else:
            if time.time() - self.start_moving_time < 0.5:
                self.anim_counter += self.anim_speed
                self.img = self.animation.anim_imgs_dic[self.position][int(self.anim_counter) % 2]
                dx = dy = 0
                if self.position == "up":
                    dy = -1
                if self.position == "down":
                    dy = 1
                if self.position == "left":
                    dx = -1
                if self.position == "right":
                    dx = 1

                self.rect.y += dy
                collider_rects = [main_char_rect] + [t.rect for t in tiles if t.collider and t.rect != self.rect and self.rect.colliderect(t.rect)]
                for rect in collider_rects:
                    if self.rect.colliderect(rect):
                        if dy == -1:
                            self.position = "down"  # go to opposite direction
                            self.img = self.animation.anim_imgs_dic["idle"][self.position]
                        else:
                            self.position = "up"  # dodge obstacle
                            self.img = self.animation.anim_imgs_dic["idle"][self.position]
                        self.rect.y -= dy

                self.rect.x += dx
                for rect in collider_rects:
                    if self.rect.colliderect(rect):
                        if dx == -1:
                            self.position = "right"  # change to opposite position
                            self.img = self.animation.anim_imgs_dic["idle"][self.position]
                        else:
                            self.position = "left"  # dodge obstacle
                            self.img = self.animation.anim_imgs_dic["idle"][self.position]
                        self.rect.x -= dx

            else:
                self.anim_counter = 0.0
                self.moving = False
                self.img = self.animation.anim_imgs_dic['idle'][self.position]
                self.current_time = time.time()  # Reset all values


# Animated tiles, e.g. flowers
class AnimatedTile(Tile):
    def __init__(self, imgs, tile_rect, anim_speed=0.0085):
        super().__init__(imgs[0], tile_rect)
        self.imgs = imgs
        self.anim_counter = 0
        self.anim_speed = anim_speed

    def update(self, main_char_rect, tiles):
        self.anim_counter += self.anim_speed
        self.anim_counter %= len(self.imgs)
        self.img = self.imgs[int(self.anim_counter)]


# All other tiles
class PassiveTile(Tile):
    def __init__(self, img, tile_rect, collider, below):
        super().__init__(img, tile_rect, collider=collider, below=below, npc=False)


# Decode a layers(.txt) and builds the map
class Tilemap:
    def __init__(self, tileset, layers, npc_tiles=None):
        self.tileset = tileset
        self.layers = layers
        self.surf = pygame.Surface((res[0], res[1]))
        self.tiles = []
        self.grow_factor = 3
        self.npc_tiles = npc_tiles
        self.create_tile_list()

    # Create the tile lists from the layers code
    def create_tile_list(self):
        for h, layer in enumerate(self.layers):
            for i, line in enumerate(layer.readlines()):
                for j, count in zip(range(len(line)), range(0, len(line)-1, 3)):
                    c = line[count:count+3]  # We take the space (or minus) and the 2 chars. e.g. ' a2' -> 102, '-60' -> -60
                    if c[1].isalpha():
                        current_char_value = 100 + int(c[2])
                    else:
                        current_char_value = int(c)
                    tile_rect = pygame.Rect(j * self.grow_factor*outside_tile_size, i * self.grow_factor*outside_tile_size, self.grow_factor*outside_tile_size, self.grow_factor*outside_tile_size)
                    if current_char_value <= 102:  # Index in the list of tiles
                        tile_to_blit = self.tileset.tiles[current_char_value]
                        if current_char_value < 0:  # If it's negative, flip the tile vertically
                            current_char_value = -current_char_value
                            tile_to_blit = pygame.transform.flip(self.tileset.tiles[current_char_value], True, False)
                        tile_to_blit = self.scale(tile_to_blit)
                        collider = True
                        below_player = True
                        if h in [1, 2]:  # Tiles of second layer are in front of player
                            below_player = False
                        if h == 0 or current_char_value in [8, 4, 5]:  # 1st layer, transparent tile and other are non-collisionable
                            collider = False
                        if current_char_value in [i for i in range(24, 29)] + [4, 5]:  # Special tiles that are in front of player and non-collisionable
                            collider = False
                            below_player = False
                        tile_to_append = PassiveTile(tile_to_blit, tile_rect, collider, below_player)
                        if current_char_value == 1:  # Animated flowers
                            tile_to_append = AnimatedTile([self.scale(img) for img in flower_imgs], tile_rect)
                    else:  # index not in the list of tiles, special tiles
                        if current_char_value == 103:
                            tile_to_append = NPCTileInanimated(girl_npc_imgs, tile_rect, tile_rect.topleft, dialogues=dialogue_girl)
                        elif current_char_value == 104:
                            tile_to_append = NPCTileAnimated(boy_npc_imgs, tile_rect, tile_rect.topleft, dialogues=dialogue_boy)
                        elif current_char_value == 105:
                            tile_to_append = NPCTileAnimated(pinkboy_npc_imgs, tile_rect, tile_rect.topleft, dialogues=dialogue_pinkboy)
                        else:  # > 105 -> City Signs
                            tile_to_blit = self.scale(self.tileset.tiles[3])
                            tile_to_append = SpeakingTile(tile_to_blit, tile_rect, tile_rect.topleft, dialogues=dilaogue_signs[current_char_value])
                    if tile_to_append is None:
                        print(current_char_value)
                    self.tiles.append(tile_to_append)

    def scale(self, img):
        return pygame.transform.scale(img,
                               (self.grow_factor * outside_tile_size, self.grow_factor * outside_tile_size))

    # Render the layers on screen
    def render(self, main_char_rect):
        for t in self.tiles:
            if not t.npc:
                screen.blit(t.surf, (t.rect.x, t.rect.y))
            if t.collider:
                if t.rect.colliderect(main_char_rect):
                    color = (0, 0, 255)
                else:
                    color = (255, 0, 0)
            else:
                color = (0, 255, 0)
            pygame.draw.rect(screen, color, t.rect, 5)


# Implemented only by the main character. With its specific update method
class MainCharacter:
    def __init__(self, imgs):
        self.current_moving_key = None
        self.last_img_key = "down"
        self.animation = AnimatedCharacter(imgs, 3)
        self.img = self.animation.anim_imgs_dic["idle"]["down"]  # Idle
        self.img_rect = self.img.get_rect()
        self.rect = pygame.Rect(32*15, 32*11, 2*self.img_rect.width/3, self.img_rect.height)
        self.vx = 1
        self.vy = 1
        self.particles = ParticleSystem()

    def update(self, player_movements):
        self.current_moving_key = None
        animation_speed = 0.0
        for k, v in player_movements.items():
            if v > 0 and k in ["down", "up", "left", "right"]:
                self.current_moving_key = k
        if player_movements["down"]:
            self.particles.x = self.rect.x + self.rect.width / 2
            self.particles.y = self.rect.y - 5
            vx, vy = get_random_speed()
            self.particles.set_v(vx, vy)
            self.current_moving_key = "down"
            animation_speed = 0.04
            self.last_img_key = "down"
        elif player_movements["up"]:
            self.particles.x = self.rect.x + self.rect.width / 2
            self.particles.y = self.rect.y + self.rect.height + 5
            vx, vy = get_random_speed(opposite2=True)
            self.particles.set_v(vx, vy)
            self.current_moving_key = "up"
            animation_speed = 0.04
            self.last_img_key = "up"
        elif player_movements["left"]:
            self.particles.x = self.rect.x + self.rect.width + 5
            self.particles.y = self.rect.y + self.rect.height - 5
            vy, vx = get_random_speed(opposite2=True)
            self.particles.set_v(vx, vy)
            self.current_moving_key = "left"
            animation_speed = 0.06
            self.last_img_key = "left"
        elif player_movements["right"]:
            self.particles.x = self.rect.x - 15
            self.particles.y = self.rect.y + self.rect.height - 5
            vy, vx = get_random_speed(opposite1=True)
            self.particles.set_v(vx, vy)
            self.current_moving_key = "right"
            animation_speed = 0.06  # We accelerate animation because there are more images in left and right animation
            self.last_img_key = "right"
        if self.current_moving_key is not None:  # Moving
            player_movements[self.current_moving_key] += animation_speed
            idx_anim = int(player_movements[self.current_moving_key]) % len(self.animation.anim_imgs_dic[self.current_moving_key])
            self.img = self.animation.anim_imgs_dic[self.current_moving_key][idx_anim]  # Change the character image for animation purpose
            self.particles.update()
        else:
            if self.current_moving_key != self.last_img_key:
                self.particles.empty()
            self.img = self.animation.anim_imgs_dic["idle"][self.last_img_key]  # Idle images

    def draw(self, screen):
        screen.blit(self.img, (self.rect.x - self.rect.width/3, self.rect.y - 1))
        if self.current_moving_key is not None:  # If main char is moving
            self.particles.draw(screen)
        if player_movements["debug"]:
            pygame.draw.rect(screen, (0, 0, 255), self.rect, 5)


# Main class that articulates everything together
class Game:
    def __init__(self, main_char, tilemap):
        self.main_char = main_char
        self.tilemap = tilemap
        self.tiles = tilemap.tiles
        self.collision_sound_timer = 0
        self.new_leaf_timer = 0
        self.text_surf = None

    # Scroll all the tiles
    def __scroll(self):
        self.collision_sound_timer += 1
        collide = {'y': False, 'x': False}
        dx = dy = 0
        if player_movements["down"]:
            dy = -3
        elif player_movements["up"]:
            dy = 3
        elif player_movements["left"]:
            dx = 3
        elif player_movements["right"]:
            dx = -3

        # Move and then check for collisions
        for t in self.tiles:
            t.rect.y += dy
        for t in self.tiles:
            if t.collider:
                if t.rect.colliderect(self.main_char.rect):
                    if player_movements["down"] or player_movements["up"]:
                        collide['y'] = True
        # If there is a collision, play a sound and cancels movement
        if collide['y']:
            for t in self.tiles:
                if self.collision_sound_timer > 100:  # So that collision sound does not play too rapidly
                    collision_sound.play()
                    self.collision_sound_timer = 0
                t.rect.y -= dy
        # Same for x
        for t in self.tiles:
            t.rect.x += dx
        for t in self.tiles:
            if t.collider:
                if t.rect.colliderect(self.main_char.rect):
                    if player_movements["right"] or player_movements["left"]:
                        collide['x'] = True
        if collide['x']:
            if self.collision_sound_timer > 100:
                collision_sound.play()
                self.collision_sound_timer = 0
            for t in self.tiles:
                t.rect.x -= dx

    def __update_tiles(self):
        self.__scroll()
        tiles_to_delete = []
        for t in self.tiles:
            t.update(self.main_char.rect, self.tiles)
            # Code below is used only for the leaves
            """if t.to_delete:
                tiles_to_delete.append(t)  # Only used for deleting outscreen's leaves
        for t in tiles_to_delete:
            self.tiles.remove(t)
        self.new_leaf_timer += 1
        if self.new_leaf_timer > 150:  # We add leaves separately from other tiles
            self.tiles.append(MovingTile(leaf_img, leaf_img.get_rect()))
            self.new_leaf_timer = 0"""

    def update(self):
        self.main_char.update(player_movements)
        self.__update_tiles()

    # Renders all the tiles' rect, to debug
    def __draw_debug(self, t):
        if t.collider:
            if t.rect.colliderect(self.main_char.rect):
                color = (0, 0, 255)
            else:
                color = (255, 0, 0)
        else:
            color = (0, 255, 0)
        pygame.draw.rect(screen, color, t.rect, 5)

    def __draw_char_tilemap(self, screen):  # draw tilemap and main char such that some tiles are below main char and others in front
        for t in self.tilemap.tiles:
            if not t.npc and t.below:  # Tiles below main char
                t.draw(screen)
            if player_movements['debug']:
                self.__draw_debug(t)
        main_char.draw(screen)
        for t in self.tilemap.tiles:  # Tiles in front of main char
            if not t.below:
                t.draw(screen)
            if player_movements['debug']:
                self.__draw_debug(t)

    def __draw_dialogue(self, npc, screen):
        screen.blit(dialogue_box_img, (0, res[1] - dialogue_box_img.get_height()))
        npc.current_text.draw(screen)

    # Draws everything
    def draw(self, screen):
        self.__draw_char_tilemap(screen)
        for t in self.tiles:
            if isinstance(t, SpeakingTile) and t.in_dialogue:
                self.__draw_dialogue(t, screen)


n_tiles_width, n_tiles_height = 30, 23
outside_tile_size = 32
res = (n_tiles_width * outside_tile_size, n_tiles_height * outside_tile_size)
font = pygame.font.Font("emerald_font.ttf", 60)
if __name__ == '__main__':
    path_to_tileset = "Graphics/Tilesets/"
    filename_tileset_outside = "LR_tileset_transparent.png"
    filename_tileset_main_character = "main_character.png"
    basename_tileset_outside = path_to_tileset + filename_tileset_outside
    basename_tileset_main_character = path_to_tileset + filename_tileset_main_character
    tileset_outside = Tileset(basename_tileset_outside, (32, 32))
    tileset_main_character = Tileset(basename_tileset_main_character, (14, 21), spacing=(1, 1))

    tileset_outside.tiles = [e for i, e in enumerate(tileset_outside.tiles) if  # Keeping the ones of interest (deleting the upper line of tiles)
                        i not in [k for k in range(8)]]

    size_tileset = len(tileset_outside.tiles)

    main_char = MainCharacter(main_char_imgs)
    player_movements = {"up": 0.0, "down": 0.0, "left": 0.0, "right": 0.0, "debug": False, "action": False}

    layer0, layer1, layer2 = open("layer0", 'r'), open("layer1", 'r'), open("layer2", 'r')
    tilemap = Tilemap(tileset_outside, [layer0, layer1, layer2])  # creating the tile list
    for tile in tilemap.tiles:
        tile.rect.x -= 800  # Centers the map approximately
        tile.rect.y -= 500

    game = Game(main_char, tilemap)

    screen = pygame.display.set_mode(res, pygame.FULLSCREEN)
    play = True
    while play:
        dx = dy = 0
        player_movements["action"] = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_movements["up"] = 0.1  # This value is used as the animation counter
                if event.key == pygame.K_DOWN:
                    player_movements["down"] = 0.1
                if event.key == pygame.K_LEFT:
                    player_movements["left"] = 0.1
                if event.key == pygame.K_RIGHT:
                    player_movements["right"] = 0.1
                if event.key == pygame.K_RETURN:
                    player_movements["action"] = True
                if event.key == pygame.K_d:
                    player_movements["debug"] = not player_movements["debug"]
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_movements["up"] = 0.0
                if event.key == pygame.K_DOWN:
                    player_movements["down"] = 0.0
                if event.key == pygame.K_LEFT:
                    player_movements["left"] = 0.0
                if event.key == pygame.K_RIGHT:
                    player_movements["right"] = 0.0
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                x_idx = mouse_pos[0] // outside_tile_size
                y_idx = mouse_pos[1] // outside_tile_size
                print(x_idx, y_idx)
                print(f"final idx: {y_idx * tileset_outside.n_tiles_width + x_idx}")


        #tileset_outside.blit_tileset()  # To debug
        # tileset_main_character.blit_tileset()
        screen.fill((0, 0, 0))
        game.update()
        game.draw(screen)

        pygame.display.update()
        pygame.display.flip()
