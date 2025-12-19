# Banco de Dados Inicial do PyFoot25
# Definições de divisões, clubes e jogadores


# Geração de 4 divisões com 16 clubes cada
DIVISOES = []
CLUBES = {}
nomes_divisoes = ["Série A", "Série B", "Série C", "Série D"]
for idx_div, nome_div in enumerate(nomes_divisoes):
    clubes_div = []
    for i in range(16):
        nome_clube = f"Clube{idx_div*16+i+1}"
        clubes_div.append(nome_clube)
        # Geração de jogadores
        jogadores = []
        for j in range(16):
            posicoes = ["Goleiro", "Zagueiro", "Lateral", "Meia", "Atacante"]
            pos = posicoes[j%5]
            nome_jog = f"Jogador{j+1}"
            forca = 90-idx_div*10-j//2  # Série A mais forte, D mais fraca
            jogadores.append({"nome": nome_jog, "posicao": pos, "forca": forca})
        CLUBES[nome_clube] = {
            "cidade": f"Cidade{idx_div*16+i+1}",
            "jogadores": jogadores
        }
    DIVISOES.append({"nome": nome_div, "clubes": clubes_div})

# Exemplo de clubes reais (mantém para testes e integração)
CLUBES.update({
    "Flamengo": {
        "cidade": "Rio de Janeiro",
        "jogadores": [
            {"nome": "Pedro", "posicao": "Atacante", "forca": 85},
            {"nome": "Arrascaeta", "posicao": "Meia", "forca": 87},
            {"nome": "Everton Ribeiro", "posicao": "Meia", "forca": 83},
            {"nome": "Fabrício Bruno", "posicao": "Zagueiro", "forca": 80}
        ]
    },
    "Palmeiras": {
        "cidade": "São Paulo",
        "jogadores": [
            {"nome": "Endrick", "posicao": "Atacante", "forca": 82},
            {"nome": "Raphael Veiga", "posicao": "Meia", "forca": 85},
            {"nome": "Gustavo Gómez", "posicao": "Zagueiro", "forca": 86},
            {"nome": "Weverton", "posicao": "Goleiro", "forca": 84}
        ]
    },
    "Corinthians": {
        "cidade": "São Paulo",
        "jogadores": [
            {"nome": "Fagner", "posicao": "Lateral", "forca": 80},
            {"nome": "Renato Augusto", "posicao": "Meia", "forca": 84},
            {"nome": "Cássio", "posicao": "Goleiro", "forca": 83},
            {"nome": "Yuri Alberto", "posicao": "Atacante", "forca": 81}
        ]
    },
    "Atlético-MG": {
        "cidade": "Belo Horizonte",
        "jogadores": [
            {"nome": "Hulk", "posicao": "Atacante", "forca": 86},
            {"nome": "Paulinho", "posicao": "Atacante", "forca": 82},
            {"nome": "Everson", "posicao": "Goleiro", "forca": 82},
            {"nome": "Arana", "posicao": "Lateral", "forca": 80}
        ]
    }
})


def get_divisoes():
    return DIVISOES

def get_clubes():
    return CLUBES

def get_clube(nome):
    return CLUBES.get(nome)

def get_jogadores(clube_nome):
    clube = CLUBES.get(clube_nome)
    if clube:
        return clube["jogadores"]
    return []

def get_clubes_data():
    clubes_data = {}
    for nome, dados in CLUBES.items():
        clubes_data[nome] = {"jogadores": dados["jogadores"]}
    return clubes_data
