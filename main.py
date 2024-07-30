from src.background import Background
from src.floor import Floor
from src.pipe import Pipe
from src.bird import Bird
from pathlib import Path

import neat.config
import pygame
import neat
import time
import os

# Variaveis "global"
var_boolPlayerIA = False
var_intGeneration = 0
var_intRecord = 0

class Main:

    # Constantes
    DISPLAY_WIDTH = 1910
    DISPLAY_HEIGHT = 995
    FRAMERATE = 30

    # Inicialização da fonte
    pygame.font.init()
    FONTE_PONTOS = pygame.font.SysFont('arial', 50)

    def __init__(self) -> None:
        # Inicialização pygame
        pygame.init()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(5, 35)
        self.display = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))

    def reset(self) -> None:
        # Inicialização/"reset" das classes do jogo
        self.var_clssBackground = Background(self.display)
        self.var_clssBird = Bird(self.display)
        self.var_clssPipe = Pipe(self.display, self.var_clssBird)
        self.var_clssFloor = Floor(self.display)

        # Reset das variaveis
        self.var_intPoints = 0
        self.var_intPipeIndex = 0
        self.clock = pygame.time.Clock()

        # Criando as listas responsaveis pelos "objetos em tela"
        self.var_clssBackground.create()
        self.var_clssPipe.create()
        self.var_clssFloor.create()

    def draw_display(self) -> None:
        # Variaveis "global"
        global var_intGeneration
        global var_intRecord

        # Cada 50 pontos muda o cenario
        # Cenario Dia
        if (self.var_intPoints // 50) % 2 == 0:
            # "Desenhando o(s) fundo dia"
            self.var_clssBackground.draw()
            # "Desenhando o(s) canos verdes"
            self.var_clssPipe.draw()
        # Cenario Noite
        else: 
            # "Desenhando o(s) "fundo noite"
            self.var_clssBackground.draw(day=False)
            # "Desenhando os canos vermelhos"
            self.var_clssPipe.draw(False)

        # "Desenhando" a "pontuação" em tela
        text_points = self.FONTE_PONTOS.render(f"Pontuação: {self.var_intPoints}", 1, (255, 255, 255))
        text_points_size = (10, 10)
        self.display.blit(text_points, text_points_size)

        # "Desenhando" o "record" em tela
        text_record = self.FONTE_PONTOS.render(f"Recorde: {var_intRecord}", 1, (255, 255, 255))
        text_record_size = (10, text_points_size[0] + text_record.get_height())
        self.display.blit(text_record, text_record_size)

        if var_boolPlayerIA:
            # "Desenhando" a "geração atual" em tela
            text_generation = self.FONTE_PONTOS.render(f"Geração: {var_intGeneration}", 1, (255, 255, 255))
            text_generation_size = (10, text_points_size[0] + text_generation.get_height() *2 )
            self.display.blit(text_generation, text_generation_size)

            # "Desenhando" o numero de "individuos" em tela
            text_individuals = self.FONTE_PONTOS.render(f"indivíduos: {len(self.var_clssBird.var_listItens)}", 1, (255, 255, 255))
            text_individuals_size = (10, text_generation_size[0] + text_individuals.get_height() * 3)
            self.display.blit(text_individuals, text_individuals_size)

        # "Desenhando o(s) passaros" em tela
        self.var_clssBird.draw()
        # "Desenhando o(s) Chão"
        self.var_clssFloor.draw()

        # Atualizando a tela
        pygame.display.update()

    def run(self, genomes, config) -> None:
        global var_boolPlayerIA
        global var_intGeneration
        global var_intRecord

        # Iniciando/resetando (as classes) "o jogo"
        self.reset()

        if var_boolPlayerIA:
            # Variaveis IA
            var_intGeneration += 1
            networks = []
            var_listGenomes = []

            # Criando "os passaros"
            for _, genome in genomes:
                network = neat.nn.FeedForwardNetwork.create(genome, config)
                networks.append(network)
                genome.fitness = 0
                var_listGenomes.append(genome)
                self.var_clssBird.create_bird()

        # Criando "o passaro"
        else: self.var_clssBird.create_bird()

        var_boolGameInit = False
        var_boolRunning = True
        # Loop para rodar o game
        while var_boolRunning:
            self.clock.tick(self.FRAMERATE)

            if var_boolPlayerIA: var_boolGameInit = True

            # Verificando os eventos do jogo
            for event in pygame.event.get():
                # Caso o click em fechar a janela tenha acionado
                if event.type == pygame.QUIT:
                    var_boolRunning = False
                    pygame.quit()
                    break
                
                if event.type == pygame.KEYDOWN:

                    # Caso NÃO seja a IA jogando 
                    if not var_boolPlayerIA:
                        # Caso o "space" tenha acionado "o(s) passaros pulam"
                        if event.key == pygame.K_ESCAPE:
                            # Reseta o jogo
                            self.reset()
                            self.var_clssBird.create_bird()
                            var_boolGameInit = False

                        # Caso o "space" tenha acionado "o(s) passaros pulam"
                        if event.key == pygame.K_SPACE:
                            for bird in self.var_clssBird.var_listItens:
                                self.var_clssBird.jump(bird)
                                var_boolGameInit = True

            # "Desenhando" os " objetos" na tela 
            self.draw_display()

            if var_boolGameInit:
                # Verificando se ainda existe "passaro"/"passaros" "vivos"
                if len(self.var_clssBird.var_listItens) > 0:
                    for index, pipe in enumerate(self.var_clssPipe.var_listItens):
                        # Verificando se "o passaro" passou do cano
                        if self.var_clssBird.var_listItens[0]['x'] > (pipe['pipe_base'].x + self.var_clssPipe.WIDTH):
                            # Definindo qual o "proximo cano"
                            self.var_intPipeIndex = index+1
                # Caso não haja mais "passaro vivo"
                else:
                    if var_boolPlayerIA:
                        var_boolRunning = False
                        break
                    
                    # Caso Player jogando
                    else:
                        # Reseta o jogo
                        self.reset()
                        self.var_clssBird.create_bird()

                if var_boolPlayerIA:
                    # Pontuando cada "passaro" por "continuar vivo" e passando parametros de entrada para IA decidir se pula ou não
                    for index, bird in enumerate(self.var_clssBird.var_listItens):
                        # Pontuando "o passaro" por "ainda estar vivo"
                        var_listGenomes[index].fitness += 0.1
                        output = networks[index].activate(
                            (
                                bird['y'] - (self.var_clssPipe.var_listItens[self.var_intPipeIndex]['pipe_base'].y -(self.var_clssPipe.DISTANCE_Y // 2)),
                                bird['x'] - (self.var_clssPipe.var_listItens[self.var_intPipeIndex]['pipe_base'].x + (self.var_clssPipe.WIDTH // 2)),
                                int(self.var_clssPipe.var_listItens[self.var_intPipeIndex]['up']),
                                self.var_clssPipe.var_listItens[self.var_intPipeIndex]['velocity']
                            )
                        )
                        
                        if output[0] > 0.5:
                            # IA "decidiu" pular
                            self.var_clssBird.jump(bird)
                
                var_boolPointed = False
                # Analisando cada passaro
                for index, bird in enumerate(self.var_clssBird.var_listItens):
                    # Verificando se o "passaro colidiu com o cano"
                    var_boolPassed = self.var_clssPipe.collide(self.var_clssPipe.var_listItens[self.var_intPipeIndex], bird)

                    # Caso o "passaro tenha colidido com o cano"
                    if var_boolPassed:
                        # "Apagando o passaro"
                        self.var_clssBird.var_listItens.pop(index)
                        if var_boolPlayerIA:
                            # Reduzindo a "pontuação do individuo"
                            var_listGenomes[index].fitness -= 1
                            var_listGenomes.pop(index)
                            networks.pop(index)
                        
                        if not var_boolPlayerIA:
                            time.sleep(0.5)

                    # Caso o "passaro NÃO tenha colidido com o cano" e ela tenha ultrapassado o cano
                    if not var_boolPassed and bird['x'] > (
                        self.var_clssPipe.var_listItens[self.var_intPipeIndex]['pipe_base'].x + (
                            self.var_clssPipe.WIDTH - self.var_clssPipe.VELOCITY
                        )):
                        # Pontuando "o passaro" por "ter passado pelo cano"
                        if var_boolPlayerIA:
                            for genome in var_listGenomes:
                                genome.fitness += 5
                        # Aumentando a pontuação
                        var_boolPointed = True

                # Aumentando a pontuação, Caso "algum passaro tenha passado pelo cano"
                if var_boolPointed:
                    self.var_intPoints += 1
                    
                    # Verificando se a pontuação é maior que o record atual
                    if var_intRecord < self.var_intPoints:
                    # Definindo um "novo" record
                        var_intRecord = self.var_intPoints

                # Verificando se "algum passaro colidiu com o chão"
                for index, bird in enumerate(self.var_clssBird.var_listItens):
                    if (bird['y'] + bird['img'].get_height()) > self.var_clssFloor.var_intY or bird['y'] < 0:
                        self.var_clssBird.var_listItens.pop(index)
                        if var_boolPlayerIA:
                            var_listGenomes.pop(index)
                            networks.pop(index)
                        
                        if not var_boolPlayerIA:
                            time.sleep(0.5)

                # Atualizando a posição dos "objetos na tela"
                self.var_clssBackground.move()
                self.var_clssPipe.move()
                self.var_clssBird.move()
                self.var_clssFloor.move()

if __name__ == '__main__':
    # Variaveis de caminho
    ROOT_PATH = Path(__file__).parent
    CONFIG_PATH = os.path.join(ROOT_PATH, 'assests/config/config.txt')

    # Variavel inicialização config neat
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        CONFIG_PATH
    )

    # Variavel IA 
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    try:
        # Caso IA jogando
        if var_boolPlayerIA: population.run(Main().run, 100)
        # Caso Player jogando
        else: Main().run(None, None)

    except Exception as error:
        # Caso a exceção especifica
        if error.__str__() == "display Surface quit": pass
        # Caso exceção não mapeada
        else: raise error
