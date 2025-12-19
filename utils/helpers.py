def mostrar_ranking_artilheiros(ranking, modo_grafico=False):
    """Exibe o ranking de artilheiros em texto ou Pygame."""
    if not ranking:
        msg = "Nenhum gol marcado ainda."
        if not modo_grafico:
            print(msg)
        else:
            from scenes.match_scene import mostrar_relatorio_partida
            mostrar_relatorio_partida(msg, modo_grafico=True)
        return
    if not modo_grafico:
        print("\nRanking de Artilheiros:")
        print("Pos  Jogador              Clube           Gols")
        for i, ((nome, clube), gols) in enumerate(ranking, 1):
            print(f"{i:>2}   {nome:<18} {clube:<14} {gols}")
    else:
        from scenes.match_scene import mostrar_relatorio_partida
        rel = "Ranking de Artilheiros:\n\n"
        rel += "Pos  Jogador              Clube           Gols\n"
        for i, ((nome, clube), gols) in enumerate(ranking, 1):
            rel += f"{i:>2}   {nome:<18} {clube:<14} {gols}\n"
        mostrar_relatorio_partida(rel, modo_grafico=True)

def get_artilheiros_geral(campeonato, copa=None):
    """Retorna ranking combinado de artilheiros do campeonato e copa."""
    gols_totais = {}
    
    # Adiciona gols do campeonato
    for (jogador, clube), gols in campeonato.gols_jogadores.items():
        chave = (jogador, clube)
        gols_totais[chave] = gols_totais.get(chave, 0) + gols
    
    # Adiciona gols da copa
    if copa:
        for (jogador, clube), gols in copa.gols_jogadores.items():
            chave = (jogador, clube)
            gols_totais[chave] = gols_totais.get(chave, 0) + gols
    
    return sorted(gols_totais.items(), key=lambda x: -x[1])

def mostrar_ranking_artilheiros_geral(campeonato, copa=None, modo_grafico=False):
    """Mostra o ranking combinado de artilheiros."""
    ranking = get_artilheiros_geral(campeonato, copa)
    print("\nArtilheiros Geral (Campeonato + Copa):")
    mostrar_ranking_artilheiros(ranking, modo_grafico=modo_grafico)
