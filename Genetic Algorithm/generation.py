from scanner import Scanner
from network import Network
from time import sleep
import numpy as np
import pykeyboard
import keyboard
import random
import copy
import pyautogui

class Generation:
    def __init__(self):
        self.__genomes = [Network() for i in range(12)]
        self.__best_genomes = []

    def execute(self):
        # Pegar comandos do teclado
        k = pykeyboard.PyKeyboard()
        # Instancia Scanner
        scanner = Scanner()

        # Encontra o jogo na tela
        scanner.find_game()

        print('start')

        for n_genome, genome in enumerate(self.__genomes):
            print('Genoma: {}'.format(n_genome + 1))
            scanner.reset()
            while True:

                try:
                    obs = scanner.find_next_obstacle()
                    inputs = [obs['distance'] / 1000, obs['length'], obs['speed'] / 10]
                    outputs = genome.forward(np.array(inputs, dtype=float))
                    # print(outputs)
                    if outputs[0] > 0.55:
                        k.press_key(k.up_key)
                except:
                    #print('Morreu')
                    pyautogui.click()
                    break

            genome.fitness = scanner.get_fitness()
            print('Genome fitness: {}'.format(genome.fitness))

    # Executado a cada geração
    def keep_best_genomes(self):
        # Ordena os genomas pelo fitness, de forma descendente (Do maior para o menor)
        self.__genomes.sort(key=lambda x: x.fitness, reverse=True)
        # Seleciona os 4 melhores genomas
        self.__genomes = self.__genomes[:4]
        # Passa os melhores genomas para a variavel __next_obstacle_dist
        self.__best_genomes = self.__genomes[:]


    def mutations(self):
        # Enquanto quantidade de genoma menor que 10
        while len(self.__genomes) < 10:
            # Seleciona de forma aleatórioa os dois genomas entre os 4 melhores
            genome1 = random.choice(self.__best_genomes)
            genome2 = random.choice(self.__best_genomes)

            self.__genomes.append(self.mutate(self.cross_over(genome1, genome2)))

        while len(self.__genomes) < 12:
            genome = random.choice(self.__best_genomes)
            self.__genomes.append(self.mutate(genome))

    # Efetua a troca de pesos entre os dois genomas e retorna um novo genoma
    def cross_over(self, genome1, genome2):
        # Faz cópia dos dois genomas
        new_genome = copy.deepcopy(genome1)
        other_genome = copy.deepcopy(genome2)

        cut_location = int(len(new_genome.W1) * random.uniform(0, 1))
        for i in range(cut_location):
            new_genome.W1[i], other_genome.W1[i] = other_genome.W1[i], new_genome.W1[i]

        cut_location = int(len(new_genome.W2) * random.uniform(0, 1))
        for i in range(cut_location):
            new_genome.W2[i], other_genome.W2[i] = other_genome.W2[i], new_genome.W2[i]

        return new_genome
    # Atualiza os pesos do  genoma após o cross_over.
    def __mutate_weights(self, weights):
        if random.uniform(0, 1) < 0.2:
            return weights * (random.uniform(0, 1) - 0.5) * 3 + (random.uniform(0, 1) - 0.5)
        else:
            return 0

    def mutate(self, genome):
        new_genome = copy.deepcopy(genome)
        new_genome.W1 += self.__mutate_weights(new_genome.W1)
        new_genome.W2 += self.__mutate_weights(new_genome.W2)
        return new_genome
