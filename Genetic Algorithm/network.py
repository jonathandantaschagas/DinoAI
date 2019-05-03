import numpy as np

class Network:
    def __init__(self):
        self.input_size = 3  # Distância, Altura e Velocidade
        self.hidden_size = 4 # Hidden Layers
        self.output_size = 1 # Ação
        
        self.W1 = np.random.randn(self.input_size, self.hidden_size)  # Iniciando pesos aleatóriamente com distribuição normal
        self.W2 = np.random.randn(self.hidden_size, self.output_size) # Iniciando pesos aleatóriamente. Hidden to Output
        self.fitness = 0

    def forward(self, inputs):
        self.z2 = np.dot(inputs, self.W1) #  ∑ x * w
        self.a2 = np.tanh(self.z2) # Função de ativação
        self.z3 = np.dot(self.a2, self.W2) # ∑ x * x
        y = np.tanh(self.z3) # Função de ativação
        return y # Valor Previsto

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
