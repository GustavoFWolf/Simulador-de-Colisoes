import pygame
import random
import math
import json

# Função para carregar configurações de um arquivo JSON
def carrega_configuracao(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        return json.load(f)

# Função para inicializar esferas com posições, velocidades e cores aleatórias
def inicializar_esferas(numero_esferas, raio_esfera, velocidade_maxima, largura_janela, altura_janela):
    esferas = []
    for _ in range(numero_esferas):
        x = random.randint(raio_esfera, largura_janela - raio_esfera)
        y = random.randint(raio_esfera, altura_janela - raio_esfera)
        vx = random.uniform(-velocidade_maxima, velocidade_maxima)
        vy = random.uniform(-velocidade_maxima, velocidade_maxima)
        cor = [random.randint(0, 255) for _ in range(3)]
        esferas.append([x, y, vx, vy, cor])
    return esferas

# Função para mover as esferas e verificar colisões com as bordas da janela
def move_esferas(esferas, raio_esfera, largura_janela, altura_janela):
    for esfera in esferas:
        esfera[0] += esfera[2]
        esfera[1] += esfera[3]

        if esfera[0] - raio_esfera < 0 or esfera[0] + raio_esfera > largura_janela:
            esfera[2] *= -1
        if esfera[1] - raio_esfera < 0 or esfera[1] + raio_esfera > altura_janela:
            esfera[3] *= -1

# Função para detectar colisão entre duas esferas
def detecta_colisao(esfera1, esfera2, raio_esfera):
    dx = esfera2[0] - esfera1[0]
    dy = esfera2[1] - esfera1[1]
    distancia = math.sqrt(dx ** 2 + dy ** 2)
    return distancia < 2 * raio_esfera

# Função para resolver colisões entre esferas
def resolve_colisao(esfera1, esfera2, coeficiente_restituicao, raio_esfera):
    dx = esfera2[0] - esfera1[0]
    dy = esfera2[1] - esfera1[1]
    distancia = math.sqrt(dx ** 2 + dy ** 2)

    if distancia == 0:
        return

    nx = dx / distancia
    ny = dy / distancia
    tx = -ny
    ty = nx

    v1n = esfera1[2] * nx + esfera1[3] * ny
    v1t = esfera1[2] * tx + esfera1[3] * ty
    v2n = esfera2[2] * nx + esfera2[3] * ny
    v2t = esfera2[2] * tx + esfera2[3] * ty

    v1n_pos = (v1n * (1 - coeficiente_restituicao) + v2n * coeficiente_restituicao) / 2
    v2n_pos = (v2n * (1 - coeficiente_restituicao) + v1n * coeficiente_restituicao) / 2

    esfera1[2] = v1n_pos * nx + v1t * tx
    esfera1[3] = v1n_pos * ny + v1t * ty
    esfera2[2] = v2n_pos * nx + v2t * tx
    esfera2[3] = v2n_pos * ny + v2t * ty

    # Separar as esferas para evitar sobreposição
    overlap = 2 * raio_esfera - distancia
    esfera1[0] -= overlap / 2 * nx
    esfera1[1] -= overlap / 2 * ny
    esfera2[0] += overlap / 2 * nx
    esfera2[1] += overlap / 2 * ny

# Função principal que executa o simulador
def main(caminho_configuracao):
    configuracao = carrega_configuracao(caminho_configuracao)
    numero_esferas = configuracao['numero_esferas']
    largura_janela = configuracao['largura_janela']
    altura_janela = configuracao['altura_janela']
    raio_esfera = configuracao['raio_esfera']
    coeficiente_restituicao = configuracao['coeficiente_restituicao']
    velocidade_maxima = configuracao['velocidade_maxima']

    pygame.init()
    tela = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption("Simulador de Colisões Elásticas")

    esferas = inicializar_esferas(numero_esferas, raio_esfera, velocidade_maxima, largura_janela, altura_janela)

    relogio = pygame.time.Clock()
    executando = True

    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        move_esferas(esferas, raio_esfera, largura_janela, altura_janela)

        # Resolver colisões
        for i in range(len(esferas)):
            for j in range(i + 1, len(esferas)):
                if detecta_colisao(esferas[i], esferas[j], raio_esfera):
                    resolve_colisao(esferas[i], esferas[j], coeficiente_restituicao, raio_esfera)

        tela.fill((0, 0, 0))
        for esfera in esferas:
            pygame.draw.circle(tela, esfera[4], (int(esfera[0]), int(esfera[1])), raio_esfera)

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()

# Executa o programa com o arquivo "input simulador.json"
if __name__ == "__main__":
    main("input simulador.json")
