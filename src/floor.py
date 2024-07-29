from pathlib import Path

import pygame as pg
import os

class Floor:

    # Constantes
    ROOT_PATH = Path(__file__).parent.parent
    IMAGE = pg.transform.scale2x(pg.image.load(os.path.join(ROOT_PATH, 'assests/sprites/base.png')))
    WIDTH = IMAGE.get_width()
    HEIGHT = IMAGE.get_height()
    VELOCITY = 10

    # Inicialização da classe
    def __init__(self, display:pg) -> None:
        self.display = display

        self.var_intX = 0
        self.var_intY = (self.display.get_height() - 150)
        self.var_intNumItens = (self.display.get_width() // self.WIDTH) + 1
        self.var_listItens = []

    # "Criando a lista de "chãos" "
    def create(self) -> None:
        while len(self.var_listItens) <= self.var_intNumItens:
            self.var_listItens.append(pg.Surface((self.WIDTH, self.HEIGHT)).get_rect(x=self.var_intX, y=self.var_intY))
            self.var_intX += self.WIDTH

    # Atualizando a posição do "chão" na tela
    def move(self) -> None:
        # Caso o "chão" esteja fora da tela deleta e cria um novo ao final da tela
        if (self.var_listItens[0].x + self.WIDTH) < 0:
            self.var_listItens.pop(0)
            var_intNewX = (self.var_intX - self.WIDTH) - self.VELOCITY
            self.var_listItens.append(pg.Surface((self.WIDTH, self.HEIGHT)).get_rect(x=var_intNewX, y=self.var_intY))
        
        # "Movimentando o "chão" "
        for item in self.var_listItens:
            item.x -= self.VELOCITY
    
    # "Desenhando o chão"
    def draw(self) -> None:
        for item in self.var_listItens:
            self.display.blit(self.IMAGE, item)
