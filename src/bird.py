from pathlib import Path

import pygame
import random
import os

class Bird:

    # Constantes
    ROOT_PATH = Path(__file__).parent.parent
    BIRDS = [
        [
            pygame.transform.scale2x(pygame.image.load(os.path.join(ROOT_PATH, 'assests/sprites/bluebird-upflap.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join(ROOT_PATH, 'assests/sprites/bluebird-midflap.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join(ROOT_PATH, 'assests/sprites/bluebird-downflap.png')))
        ],
        [
            pygame.transform.scale2x(pygame.image.load(os.path.join(ROOT_PATH, 'assests/sprites/redbird-upflap.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join(ROOT_PATH, 'assests/sprites/redbird-midflap.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join(ROOT_PATH, 'assests/sprites/redbird-downflap.png')))
            
        ],
        [
            pygame.transform.scale2x(pygame.image.load(os.path.join(ROOT_PATH, 'assests/sprites/yellowbird-upflap.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join(ROOT_PATH, 'assests/sprites/yellowbird-midflap.png'))),
            pygame.transform.scale2x(pygame.image.load(os.path.join(ROOT_PATH, 'assests/sprites/yellowbird-downflap.png')))
        ]
    ]
    MAX_ROTATION = 25
    SPEED_ROTATION = 20
    ANIMATION_TIME = 5

        # Inicialização da classe
    def __init__(self, display) -> None:
        self.display = display

        self.var_floatX = self.display.get_width() // 2
        self.var_floatY = self.display.get_height() // 2
        self.var_listItens = []

    # "Criando a lista de "passaros" "
    def create_bird(self) -> None:
        var_listImgs = self.BIRDS[random.randrange(0,3)]
        # Criando um item na lista, contendo um dicionario com as informações de cada passaro
        # * As informações serão necessarias para fazer a animação individual de cada passaro
        self.var_listItens.append({
            'x' : self.var_floatX,
            'y' : self.var_floatY,
            'angle' : 0,
            'speed' : 0,
            'height' : self.var_floatY,
            'time' : 0,
            'countImg' : 0,
            'imgs' : var_listImgs,
            'img' : var_listImgs[0]
        })

    # Atualizando a posição do "passaro" na tela
    # * Criando a animação de "pulo"
    def jump(self, bird) -> None:
        bird['speed'] = -10.5
        bird['time'] = 0
        bird['height'] = bird['y']

    # Atualizando a posição dos "passaros" na tela
    # * Criando a animação de "queda"
    def move(self) -> None:
        for item in self.var_listItens:
            item['time'] += 1
            displacement = 1.5 * (item['time']**2) + item['speed'] * item['time']

            if displacement > 16: displacement = 16
            elif displacement < 0: displacement -= 2

            item['y'] += displacement

            if displacement < 0 or item['y'] < (item['height'] + 50):
                if item['angle'] < self.MAX_ROTATION:
                    item['angle'] = self.MAX_ROTATION
            else:
                if item['angle'] > -90:
                    item['angle'] -= self.SPEED_ROTATION

    # "Desenhando os passaros" na tela
    def draw(self) -> None:
        for item in self.var_listItens:
            item['countImg'] += 1

            if item['countImg'] < self.ANIMATION_TIME:
                item['img'] = item['imgs'][0]
            elif item['countImg'] < self.ANIMATION_TIME*2:
                item['img'] = item['imgs'][1]
            elif item['countImg'] < self.ANIMATION_TIME*3:
                item['img'] = item['imgs'][2]
            elif item['countImg'] < self.ANIMATION_TIME*4:
                item['img'] = item['imgs'][1]
            elif item['countImg'] >= self.ANIMATION_TIME*4 + 1:
                item['img'] = item['imgs'][0]
                item['countImg'] = 0
            
            if item['angle'] <= -80:
                item['img'] = item['imgs'][1]
                item['countImg'] = self.ANIMATION_TIME*2

            rotated_image = pygame.transform.rotate(item['img'], item['angle'])
            pos_center_image = item['img'].get_rect(topleft=(item['x'], item['y'])).center
            rectangle = rotated_image.get_rect(center=pos_center_image)
            self.display.blit(rotated_image, rectangle.topleft)

    # "Criando uma mascara para o passaro"
    def get_mask(self, bird) -> None:
        return pygame.mask.from_surface(bird['img'])
