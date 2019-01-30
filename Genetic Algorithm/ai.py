from generation import Generation

def main():
    # Instancia a geração
    generation = Generation()
    geracao = 1
    while True:
        print('Generation: {}'.format(geracao))
        # Inicia a geração
        generation.execute()

        # Seleciona os melhores genomas da geação
        generation.keep_best_genomes()

        # Adiciona mutações na geração
        generation.mutations()

        geracao +=1

if __name__ == '__main__':
    main()
