def salvar_jogo_completo(state_manager, campeonato, relatorios_ultima_rodada, caminho="savegame.pkl"):
    # Salva todos os objetos relevantes do jogo
    save_data = {
        "state_manager": state_manager,
        "campeonato": campeonato,
        "relatorios_ultima_rodada": relatorios_ultima_rodada
    }
    with open(caminho, "wb") as f:
        pickle.dump(save_data, f)
    print(f"Jogo salvo em {caminho} (completo).")

def carregar_jogo_completo(caminho="savegame.pkl"):
    try:
        with open(caminho, "rb") as f:
            save_data = pickle.load(f)
        print(f"Jogo carregado de {caminho} (completo).")
        return save_data
    except FileNotFoundError:
        print("Arquivo de save não encontrado.")
        return None
# Salvamento e Carregamento do Jogo
import pickle

def salvar_jogo(objeto, caminho="savegame.pkl"):
    with open(caminho, "wb") as f:
        pickle.dump(objeto, f)
    print(f"Jogo salvo em {caminho}.")

def carregar_jogo(caminho="savegame.pkl"):
    try:
        with open(caminho, "rb") as f:
            objeto = pickle.load(f)
        print(f"Jogo carregado de {caminho}.")
        return objeto
    except FileNotFoundError:
        print("Arquivo de save não encontrado.")
        return None

# Exemplo de integração com o núcleo do jogo:
# from data.save_load import salvar_jogo, carregar_jogo
# salvar_jogo(state_manager)
# state_manager = carregar_jogo()
