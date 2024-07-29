from pathlib import Path

import pygame as pg
import os

class Background:

    # Constantes
    ROOT_PATH = Path(__file__).parent.parent
    IMAGE_DAY = pg.transform.scale2x(pg.image.load(os.path.join(ROOT_PATH, 'assests/sprites/background-day.png')))
    IMAGE_NIGHT = pg.transform.scale2x(pg.image.load(os.path.join(ROOT_PATH, 'assests/sprites/background-night.png')))
    WIDTH = IMAGE_DAY.get_width()
    HEIGHT = IMAGE_DAY.get_height()
    VELOCITY = 1

    # Inicialização da classe
    def __init__(self, display:pg) -> None:
        self.display = display

        self.var_intX = 0
        self.var_intY = 0
        self.var_intNumItens = (self.display.get_width() // self.WIDTH) + 1
        self.var_listItens = []

    # "Criando a lista de "fundos" "
    def create(self) -> None:
        while len(self.var_listItens) <= self.var_intNumItens:
            self.var_listItens.append(pg.Surface((self.WIDTH, self.HEIGHT)).get_rect(x=self.var_intX, y=self.var_intY))
            self.var_intX += self.WIDTH

    # Atualizando a posição do "fundo" na tela
    def move(self) -> None:
        # Caso o "fundo" esteja fora da tela deleta e cria um novo ao final da tela
        if (self.var_listItens[0].x + self.WIDTH) < 0:
            self.var_listItens.pop(0)
            var_intNewX = (self.var_intX - self.WIDTH)
            self.var_listItens.append(pg.Surface((self.WIDTH, self.HEIGHT)).get_rect(x=var_intNewX, y=self.var_intY))
        
        # "Movimentando o "fundo" "
        for item in self.var_listItens:
            item.x -= self.VELOCITY
       
    # "Desenhando o fundo"
    def draw(self, day:bool=True) -> None:
        for item in self.var_listItens:
            if day: self.display.blit(self.IMAGE_DAY, item)
            else: self.display.blit(self.IMAGE_NIGHT, item)
