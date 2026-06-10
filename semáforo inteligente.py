# -*- coding: utf-8 -*-
from random import randint
from time import sleep

# TOPOLOGIA DA REDE

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

def calcular_tempo_verde(fluxo):
    if fluxo < 20:
        return 20
    elif fluxo < 50:
        return 40
    elif fluxo < 100:
        return 60
    else:
        return 90

def detectar_emergencia():
    return randint(1, 100) <= 5  # 5% de chance

def executar_semaforo(id_semaforo):
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

# ==========================
# CENTRO NACIONAL
# ==========================

print("="*60)
print("CENTRO NACIONAL DE CONTROLE DE TRÂNSITO")
print("="*60)

for regiao, estados in rede["Brasil"].items():

    print(f"\nREGIÃO: {regiao}")

    for estado, municipios in estados.items():

        fluxo_estado = 0

        print(f"  ESTADO: {estado}")

        for municipio, semaforos in municipios.items():

            fluxo_municipio = randint(100, 1000)
            fluxo_estado += fluxo_municipio

            print(f"\n    MUNICÍPIO: {municipio}")
            print(f"    Fluxo Municipal: {fluxo_municipio}")

            if fluxo_municipio > 700:
                print("    ALERTA: congestionamento detectado")
                print("    Ação: aumentar tempo verde em vias principais")

            for semaforo in semaforos:
                executar_semaforo(semaforo)

        print(f"\n  Fluxo Total do Estado: {fluxo_estado}")

        if fluxo_estado > 1500:
            print("  DECISÃO ESTADUAL:")
            print("  -> Sincronizar semáforos dos municípios")
            print("  -> Priorizar corredores de ônibus")
            print("  -> Gerar alerta para centro regional")
