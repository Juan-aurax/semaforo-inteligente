# -*- coding: utf-8 -*-
from random import randint
from time import sleep

# TOPOLOGIA DA REDE - ESTRUTURA HIERÁRQUICA DOS GERENCIADORES DE TRÂNSITO E SEMÁFOROS EM:
# Nível Nacional
# Nível Regional
# Nível Estadual
# Nível Municipal

rede = {
    "Brasil": {
        "Sudeste": {
            "São Paulo": {
                "Campinas": [
                    "CAMP-001",
                    "CAMP-002"
                ],
                "Santos": [
                    "SANTOS-001",
                    "SANTOS-002"
                ]
            },
            "Rio de Janeiro": {
                "Rio de Janeiro": [
                    "RIO-001",
                    "RIO-002"
                ]
            }
        },
        "Sul": {
            "Paraná": {
                "Curitiba": [
                    "CUR-001",
                    "CUR-002"
                ]
            }
        }
    }
}

# FUNÇÕES DE IA DO SEMÁFORO

def calcular_tempo_verde(fluxo): # Ajusta o tempo verde com base no fluxo de veículos
    if fluxo < 20:
        return 20
    elif fluxo < 50:
        return 40
    elif fluxo < 100:
        return 60
    else:
        return 90

def detectar_emergencia(): # Simula a detecção de uma emergência com uma chance de 5%
    return randint(1, 100) <= 5  # 5% de chance


def verificar_configuracao(rede): # Verifica as configurações de rede para garantir que estão corretas
    if not isinstance(rede, dict):
        return False
    if "Brasil" not in rede or not isinstance(rede["Brasil"], dict):
        return False
    for regiao, estados in rede["Brasil"].items():
        if not isinstance(estados, dict):
            return False
        for estado, municipios in estados.items():
            if not isinstance(municipios, dict):
                return False
            for semaforos in municipios.values():
                if not isinstance(semaforos, list):
                    return False
    return True


def menu_erro_gerenciador(): # Caso haja um erro na configuração do gerenciador, apresenta um menu para o usuário escolher entre reiniciar ou parar o programa
    print("\nERRO: configuração de gerenciador inválida ou faltando.")
    print("Escolha uma opção:")
    print("1. Reiniciar o programa")
    print("2. Parar o programa")
    while True: # Loop para caso a opção sejáo inválida, o usuário possa tentar novamente
        opcao = input("Digite 1 ou 2: ").strip()
        if opcao == "1":
            print("Reiniciando o programa...\n")
            return True
        elif opcao == "2":
            print("Parando o programa.")
            return False
        else:
            print("Opção inválida. Tente novamente.")


def executar_semaforo(id_semaforo): # Executa o semáfaro e detecta emergências para ajustar o tempo verde
    fluxo = randint(5, 150)

    if detectar_emergencia():
        estado = "EMERGÊNCIA"
        tempo_verde = 120
    else:
        estado = "NORMAL"
        tempo_verde = calcular_tempo_verde(fluxo)

    print(f"\nSemáforo: {id_semaforo}")
    print(f"Fluxo detectado: {fluxo} veículos")
    print(f"Modo: {estado}")

    print(f"🟢 VERDE   ({tempo_verde}s)")
    print("🟡 AMARELO (5s)")
    print("🔴 VERMELHO (30s)")

# CENTRO NACIONAL

while True: # Loop principal do programa para simular o funcionamento contínuo do sistema de semáforos inteligentes
    if not verificar_configuracao(rede):
        if not menu_erro_gerenciador():
            break
        continue

    print("="*60)
    print("CENTRO NACIONAL DE CONTROLE DE TRÂNSITO")
    print("="*60)

    for regiao, estados in rede["Brasil"].items(): # Verifica cada região e estados para monitorar o fluxo de veículos e ajustar os semáforos

        print(f"\nREGIÃO: {regiao}")

        for estado, municipios in estados.items(): # Verfica cada estado e municípios para monitorar o fluxo de veículos e ajustar os semáforos

            fluxo_estado = 0

            print(f"  ESTADO: {estado}")

            for municipio, semaforos in municipios.items(): # Verifica cada município e semáforos para monitorar o fluxo de veículos e ajustar os semáforos

                fluxo_municipio = randint(100, 1000)
                fluxo_estado += fluxo_municipio

                print(f"\n    MUNICÍPIO: {municipio}")
                print(f"    Fluxo Municipal: {fluxo_municipio}")

                if fluxo_municipio > 700:
                    print("    ALERTA: congestionamento detectado")
                    print("    Ação: aumentar tempo verde em vias principais")

                for semaforo in semaforos: # Verifica cada semáforo para monitorar o fluxo de veículos e ajustar os semáforos
                    executar_semaforo(semaforo)

            print(f"\n  Fluxo Total do Estado: {fluxo_estado}")

            if fluxo_estado > 1500:
                print("  DECISÃO ESTADUAL:")
                print("  -> Sincronizar semáforos dos municípios")
                print("  -> Priorizar corredores de ônibus")
                print("  -> Gerar alerta para centro regional")

    sleep(5)  # pausa antes da próxima rodada
