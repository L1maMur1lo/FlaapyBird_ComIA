from src.bird import Bird
from pathlib import Path

import pygame as pg
import random
import os

class Pipe:

    # Constantes
    ROOT_PATH = Path(__file__).parent.parent

    PIPE_GREEN_BASE = pg.transform.scale2x(pg.image.load(os.path.join(ROOT_PATH, 'assests/sprites/pipe-green.png')))
    PIPE_GREEN_TOP = pg.transform.flip(PIPE_GREEN_BASE, False, True)

    PIPE_RED_BASE = pg.transform.scale2x(pg.image.load(os.path.join(ROOT_PATH, 'assests/sprites/pipe-red.png')))
    PIPE_RED_TOP = pg.transform.flip(PIPE_RED_BASE, False, True)

    WIDTH = PIPE_GREEN_BASE.get_width()
    HEIGHT = PIPE_GREEN_BASE.get_height()

    DISTANCE_Y = 200
    DISTANCE_X = 350
    VELOCITY = 5

    # Inicialização da classe
    def __init__(self, display:pg, var_clssBird:Bird) -> None:
        self.display = display
        self.var_clssBird = var_clssBird

        self.var_intX = self.display.get_width()
        self.var_intY = 0
        self.var_intMinY = 100
        self.var_intMaxY = (self.display.get_height() - 350)
        self.var_intNumItens = (self.display.get_width() // (self.WIDTH + self.DISTANCE_X))
        self.var_listItens = []

    # Defindo aleatoriamente a posição inicial dos "canos"
    def definy_height(self) -> tuple:
        var_intHeight = random.randrange(self.var_intMinY, self.var_intMaxY)
        var_intPos_Top = var_intHeight - self.HEIGHT
        var_intPos_Base = var_intHeight + self.DISTANCE_Y

        return (var_intPos_Top, var_intPos_Base)

    # Criando um "cano"
    def create_pipe(self, var_intX:int) -> None:
        var_intTopY, var_intBaseY = self.definy_height()
        var_intVelocity = random.randrange(0, self.VELOCITY)

        # Criando um item na lista, contendo um dicionario com as informações de cada cano
        # * As informações serão necessarias para fazer a animação individual de cada cano
        self.var_listItens.append({
            'up': True,
            'velocity' : var_intVelocity,
            'pipe_top' : pg.Surface((self.WIDTH, self.HEIGHT)).get_rect(x=var_intX, y=var_intTopY),
            'pipe_base' : pg.Surface((self.WIDTH, self.HEIGHT)).get_rect(x=var_intX, y=var_intBaseY)
        })

    # "Criando a lista de "canos" "
    def create(self) -> None:
        var_intX = self.var_intX
        while len(self.var_listItens) <= self.var_intNumItens:
            self.create_pipe(var_intX)
            var_intX += (self.WIDTH + self.DISTANCE_X)
        self.var_intX += self.DISTANCE_X

    # Atualizando a posição dos "canos" na tela
    def move(self) -> None:
        # Caso o "cano" esteja fora da tela deleta e cria um novo ao final da tela
        if (self.var_listItens[0]['pipe_top'].x + self.WIDTH) < 0:
            self.var_listItens.pop(0)
            self.create_pipe(self.var_intX)

        # "Movimentando o "cano" "
        for item in self.var_listItens:
            item['pipe_top'].x -= self.VELOCITY
            item['pipe_base'].x -= self.VELOCITY

            # Caso o cano esteja subindo e NÃO tenha atingido a posição maxima
            if item['up'] and item['pipe_base'].y > (self.var_intMinY + self.DISTANCE_Y):
                item['pipe_top'].y -= item['velocity']
                item['pipe_base'].y -= item['velocity']
            # Caso o cano esteja subindo e tenha atingido a posição maxima
            else:
                item['up'] = False
                item['up'] = False

            # Caso o cano esteja descendo e NÃO tenha atingido a posição maxima
            if not item['up'] and item['pipe_base'].y < self.var_intMaxY:
                item['pipe_top'].y += item['velocity']
                item['pipe_base'].y += item['velocity']
            # Caso o cano esteja descendo e tenha atingido a posição maxima
            else:
                item['up'] = True
                item['up'] = True

    # "Desenhando os canos"
    def draw(self, green:bool=True) -> None:
        for item in self.var_listItens:
            if green:
                self.display.blit(self.PIPE_GREEN_TOP, item['pipe_top'])
                self.display.blit(self.PIPE_GREEN_BASE, item['pipe_base'])
            else:
                self.display.blit(self.PIPE_RED_TOP, item['pipe_top'])
                self.display.blit(self.PIPE_RED_BASE, item['pipe_base'])

    # Verificando se houve "colisão do passaro com o cano"
    def collide(self, pipe, bird:Bird) -> list:
        bird_mask = self.var_clssBird.get_mask(bird)

        top_mask = pg.mask.from_surface(self.PIPE_GREEN_TOP)
        base_mask = pg.mask.from_surface(self.PIPE_GREEN_BASE)

        distance_top = (pipe['pipe_top'].x - bird['x'], pipe['pipe_top'].y - round(bird['y']))
        distance_base = (pipe['pipe_base'].x - bird['x'], pipe['pipe_base'].y - round(bird['y']))

        point_top = bird_mask.overlap(top_mask, distance_top)
        point_base = bird_mask.overlap(base_mask, distance_base)

        if point_top or point_base: return True
        else: return False
