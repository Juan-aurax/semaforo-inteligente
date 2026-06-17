# app.py
import streamlit as st
import pandas as pd
from random import randint

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Centro Nacional de Controle de Trânsito",
    page_icon="🚦",
    layout="wide"
)

# ==========================
# ESTILOS (CSS)
# ==========================
st.markdown("""
<style>
.brasil {
    background-color: #0B3D91;
    color: white;
    padding: 12px;
    border-radius: 10px;
    font-size: 28px;
    font-weight: bold;
    text-align: center;
}

.regiao {
    background-color: #2E8B57;
    color: white;
    padding: 10px;
    border-radius: 10px;
    font-size: 24px;
    font-weight: bold;
    margin-top: 20px;
}

.estado {
    background-color: #FF8C00;
    color: white;
    padding: 10px;
    border-radius: 10px;
    font-size: 20px;
    font-weight: bold;
    margin-top: 15px;
}

.card-municipio {
    border: 2px solid #8A2BE2;
    border-radius: 15px;
    padding: 15px;
    margin-top: 20px;
    margin-bottom: 20px;
    background-color: rgba(138, 43, 226, 0.05);
}

.municipio {
    color: #8A2BE2;
    font-size: 22px;
    font-weight: bold;
}

.small-text {
    color: gray;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# TOPOLOGIA DA REDE
# ==========================
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

# ==========================
# FUNÇÕES
# ==========================
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

    emergencia = detectar_emergencia()

    if emergencia:
        modo = "🚑 Emergência"
        tempo_verde = 120
    else:
        modo = "🟢 Normal"
        tempo_verde = calcular_tempo_verde(fluxo)

    return {
        "Semáforo": id_semaforo,
        "Fluxo": fluxo,
        "Modo": modo,
        "Verde (s)": tempo_verde,
        "Amarelo (s)": 5,
        "Vermelho (s)": 30,
        "Emergência": emergencia
    }


# ==========================
# INTERFACE
# ==========================
st.title("🚦 Centro Nacional de Controle de Trânsito")
st.write("Sistema Inteligente de Gerenciamento de Semáforos")

# Sidebar
st.sidebar.header("⚙️ Controle")

executar = st.sidebar.button("▶ Executar Simulação")

with st.sidebar.expander("🌎 Topologia da Rede"):
    st.json(rede)

# Verificação
if not verificar_configuracao(rede):
    st.error("❌ Configuração da rede inválida.")
    st.stop()

if not executar:
    st.info("Clique em **Executar Simulação** para iniciar o monitoramento.")
    st.stop()

# ==========================
# BRASIL
# ==========================
st.markdown(
    '<div class="brasil">🇧🇷 BRASIL</div>',
    unsafe_allow_html=True
)

# ==========================
# PROCESSAMENTO
# ==========================
for regiao, estados in rede["Brasil"].items():

    st.markdown(
        f'<div class="regiao">🌎 REGIÃO: {regiao}</div>',
        unsafe_allow_html=True
    )

    for estado, municipios in estados.items():

        fluxo_estado = 0
        total_emergencias_estado = 0
        total_semaforos_estado = 0

        st.markdown(
            f'<div class="estado">🏛️ ESTADO: {estado}</div>',
            unsafe_allow_html=True
        )

        # MUNICÍPIOS
        for municipio, semaforos in municipios.items():

            dados_semaforos = []

            fluxo_municipio = 0
            emergencias_municipio = 0

            for semaforo in semaforos:

                dados = executar_semaforo(semaforo)

                dados_semaforos.append({
                    "Semáforo": dados["Semáforo"],
                    "Fluxo": dados["Fluxo"],
                    "Modo": dados["Modo"],
                    "Verde (s)": dados["Verde (s)"],
                    "Amarelo (s)": dados["Amarelo (s)"],
                    "Vermelho (s)": dados["Vermelho (s)"]
                })

                fluxo_municipio += dados["Fluxo"]

                if dados["Emergência"]:
                    emergencias_municipio += 1

            fluxo_estado += fluxo_municipio
            total_emergencias_estado += emergencias_municipio
            total_semaforos_estado += len(semaforos)

            # CARD DO MUNICÍPIO
            with st.container():

                st.markdown(
                    '<div class="card-municipio">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="municipio">🏙️ MUNICÍPIO: {municipio}</div>',
                    unsafe_allow_html=True
                )

                # MÉTRICAS
                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "🚗 Fluxo Municipal",
                    f"{fluxo_municipio} veículos"
                )

                col2.metric(
                    "🚦 Semáforos",
                    len(semaforos)
                )

                col3.metric(
                    "🚑 Emergências",
                    emergencias_municipio
                )

                # ALERTA DE CONGESTIONAMENTO
                if fluxo_municipio > 200:
                    st.warning(
                        "⚠️ Congestionamento detectado.\n"
                        "Aumentar tempo verde nas vias principais."
                    )
                else:
                    st.success(
                        "✅ Fluxo dentro da normalidade."
                    )

                # TABELA DO MUNICÍPIO
                st.dataframe(
                    pd.DataFrame(dados_semaforos),
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

        # MÉTRICAS DO ESTADO
        st.markdown("### 📊 Resumo Estadual")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "🚗 Fluxo Total",
            f"{fluxo_estado} veículos"
        )

        c2.metric(
            "🚦 Total de Semáforos",
            total_semaforos_estado
        )

        c3.metric(
            "🚑 Emergências",
            total_emergencias_estado
        )

        # DECISÕES ESTADUAIS
        if fluxo_estado > 500:
            st.error(
                "🚨 DECISÃO ESTADUAL\n\n"
                "- Sincronizar semáforos dos municípios\n"
                "- Priorizar corredores de ônibus\n"
                "- Gerar alerta para o centro regional"
            )
        else:
            st.info(
                "ℹ️ Operação estadual dentro dos parâmetros normais."
            )

        st.divider()
