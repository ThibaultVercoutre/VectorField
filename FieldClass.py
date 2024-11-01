import numpy as np
import pygame as pg
from PIL import ImageDraw

RED = (255, 0, 0)
DIRECTION = [
    {'y': -1, 'x': 0},
    {'y': -1, 'x': 1},
    {'y': 0, 'x': 1},
    {'y': 1, 'x': 1},
    {'y': 1, 'x': 0},
    {'y': 1, 'x': -1},
    {'y': 0, 'x': -1},
    {'y': -1, 'x': -1}]

class FieldClass:
    def __init__(self, resolution: int, larg: int, haut: int):
        self.balls = []
        self.larg = larg
        self.haut = haut
        self.resolution = resolution
        self.field = np.zeros((resolution, resolution, 2), dtype=int)

    def remplir_matrice_alea(self) -> None:
        for i in range(self.field.shape[0]):
            for j in range(self.field.shape[1]):
                self.field[i, j, 0] = np.random.randint(0, len(DIRECTION))
                self.field[i, j, 1] = np.random.randint(1, 2)

    def draw_field(self, image):
        draw = ImageDraw.Draw(image)
        margin = (self.larg/self.resolution) / 5
        for i in range(self.field.shape[0]):
            for j in range(self.field.shape[1]):
                x = i * (self.larg / self.resolution) + self.larg / (2 * self.resolution)
                y = j * (self.haut / self.resolution) + self.haut / (2 * self.resolution)
                draw.line((x - DIRECTION[self.field[i, j, 0]]['x']*(self.larg/(2*self.resolution) - margin), 
                        y - DIRECTION[self.field[i, j, 0]]['y']*(self.haut/(2*self.resolution) - margin),
                        x + DIRECTION[self.field[i, j, 0]]['x']*(self.larg/(2*self.resolution) - margin), 
                        y + DIRECTION[self.field[i, j, 0]]['y']*(self.haut/(2*self.resolution) - margin)), 
                        fill='black', width=1)
                
                if DIRECTION[self.field[i, j, 0]]['x'] != 0 or DIRECTION[self.field[i, j, 0]]['y'] != 0:
                    x = x + DIRECTION[self.field[i, j, 0]]['x']*(self.larg/(2*self.resolution) - margin)
                    y = y + DIRECTION[self.field[i, j, 0]]['y']*(self.haut/(2*self.resolution) - margin)
                    draw.rectangle((x - margin/2, y - margin/2, x + margin/2, y + margin/2), fill='black')

    def draw_field_2(self, image):
        draw = ImageDraw.Draw(image)
        margin = (self.larg / self.resolution) / 5

        x_coords = np.arange(self.resolution) * (self.larg / self.resolution) + self.larg / (2 * self.resolution)
        y_coords = np.arange(self.resolution) * (self.haut / self.resolution) + self.haut / (2 * self.resolution)
        x_grid, y_grid = np.meshgrid(x_coords, y_coords)

        vectors = np.array([[DIRECTION[idx] for idx in row] for row in self.field[:, :, 0]])

        start_x = x_grid - np.array([[vec['x'] for vec in row] for row in vectors]) * (self.larg / (2 * self.resolution) - margin)
        start_y = y_grid - np.array([[vec['y'] for vec in row] for row in vectors]) * (self.haut / (2 * self.resolution) - margin)
        end_x = x_grid + np.array([[vec['x'] for vec in row] for row in vectors]) * (self.larg / (2 * self.resolution) - margin)
        end_y = y_grid + np.array([[vec['y'] for vec in row] for row in vectors]) * (self.haut / (2 * self.resolution) - margin)

        for i in range(self.resolution):
            for j in range(self.resolution):
                draw.line((start_x[i, j], start_y[i, j], end_x[i, j], end_y[i, j]), fill='black', width=1)

                if vectors[i, j]['x'] != 0 or vectors[i, j]['y'] != 0:
                    x = x_grid[i, j] + vectors[i, j]['x'] * (self.larg / (2 * self.resolution) - margin)
                    y = y_grid[i, j] + vectors[i, j]['y'] * (self.haut / (2 * self.resolution) - margin)
                    draw.rectangle((x - margin / 2, y - margin / 2, x + margin / 2, y + margin / 2), fill='black')
    
    def changeVector(self, i: int, j: int) -> None:
        print(f"({i}, {j}) = ({DIRECTION[self.field[i, j, 0]]}")
        # self.field[i, j, 0] = (self.field[i, j, 0] + 1) % len(DIRECTION)


class BallClass:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.color = np.random.randint(0, 256, size=3)

    def move(self, field: FieldClass) -> None:
        self.old_x = self.x
        self.old_y = self.y
        self.x = (self.x + DIRECTION[field.field[int(self.old_x), int(self.old_y), 0]]['x'] * field.field[int(self.old_x), int(self.old_y), 1]) % field.resolution
        self.y = (self.y + DIRECTION[field.field[int(self.old_x), int(self.old_y), 0]]['y'] * field.field[int(self.old_x), int(self.old_y), 1]) % field.resolution

    def draw(self, surface, field: FieldClass, larg: int, haut: int) -> None:
        x_draw = self.old_x * (larg / field.resolution) + larg / (2 * field.resolution)
        y_draw = self.old_y * (haut / field.resolution) + haut / (2 * field.resolution)
        pg.draw.circle(surface, self.color, (int(x_draw), int(y_draw)), larg / (2 * field.resolution))
