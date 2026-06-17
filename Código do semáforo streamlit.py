# app.py
import streamlit as st
import pandas as pd
from random import randint

st.set_page_config(
    page_title="Centro Nacional de Controle de Trânsito",
    page_icon="🚦",
    layout="wide"
)

# TOPOLOGIA DA REDE
rede = {
    "Brasil": {
        "Sudeste": {
            "São Paulo": {
                "Campinas": ["CAMP-001", "CAMP-002"],
                "Santos": ["SANTOS-001", "SANTOS-002"]
            },
            "Rio de Janeiro": {
                "Rio de Janeiro": ["RIO-001", "RIO-002"]
            }
        },
        "Sul": {
            "Paraná": {
                "Curitiba": ["CUR-001", "CUR-002"]
            }
        }
    }
}


# FUNÇÕES
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
    return randint(1, 100) <= 5


def verificar_configuracao(rede):
    if not isinstance(rede, dict):
        return False

    if "Brasil" not in rede:
        return False

    for estados in rede["Brasil"].values():
        if not isinstance(estados, dict):
            return False

        for municipios in estados.values():
            if not isinstance(municipios, dict):
                return False

            for semaforos in municipios.values():
                if not isinstance(semaforos, list):
                    return False

    return True


def executar_semaforo(id_semaforo):
    fluxo = randint(5, 150)

    if detectar_emergencia():
        modo = "EMERGÊNCIA"
        tempo_verde = 120
    else:
        modo = "NORMAL"
        tempo_verde = calcular_tempo_verde(fluxo)

    return {
        "Semáforo": id_semaforo,
        "Fluxo": fluxo,
        "Modo": modo,
        "Verde (s)": tempo_verde,
        "Amarelo (s)": 5,
        "Vermelho (s)": 30
    }


# INTERFACE
st.title("🚦 Centro Nacional de Controle de Trânsito")
st.write("Sistema Inteligente de Gerenciamento de Semáforos")

# Verificação da rede
if not verificar_configuracao(rede):
    st.error("Configuração da rede inválida.")
    st.stop()

# Sidebar
st.sidebar.header("Controle")
executar = st.sidebar.button("▶ Executar Simulação")

# Exibe a topologia
with st.expander("Topologia da Rede"):
    st.json(rede)

if executar:
    for regiao, estados in rede["Brasil"].items():

        st.header(f"Região: {regiao}")

        for estado, municipios in estados.items():

            fluxo_estado = 0

            st.subheader(f"Estado: {estado}")

            dados_semaforos = []

            for municipio, semaforos in municipios.items():

                fluxo_municipio = randint(100, 1000)
                fluxo_estado += fluxo_municipio

                st.markdown(f"### Município: {municipio}")
                st.write(f"Fluxo Municipal: **{fluxo_municipio} veículos**")

                if fluxo_municipio > 700:
                    st.warning(
                        "Congestionamento detectado. "
                        "Aumentar tempo verde nas vias principais."
                    )

                for semaforo in semaforos:
                    dados_semaforos.append(
                        executar_semaforo(semaforo)
                    )

            st.dataframe(
                pd.DataFrame(dados_semaforos),
                use_container_width=True
            )

            st.success(
                f"Fluxo Total do Estado: {fluxo_estado} veículos"
            )

            if fluxo_estado > 1500:
                st.error(
                    "DECISÃO ESTADUAL:\n\n"
                    "- Sincronizar semáforos\n"
                    "- Priorizar corredores de ônibus\n"
                    "- Gerar alerta ao centro regional"
                )

else:
    st.info("Clique em 'Executar Simulação' para iniciar o monitoramento.")