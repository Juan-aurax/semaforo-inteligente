# ==========================================================
# app.py - PARTE 1
# ==========================================================
# Centro Nacional de Controle de Trânsito
# Sistema Inteligente de Gerenciamento de Semáforos

import streamlit as st
import pandas as pd
from random import randint
import time

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
# Define:
# - Título exibido na aba do navegador;
# - Ícone da aplicação;
# - Layout amplo para aproveitar melhor a tela.
# ==========================================================

st.set_page_config(
    page_title="Centro Nacional de Controle de Trânsito",
    page_icon="🚦",
    layout="wide"
)

# ==========================================================
# ESTILOS (CSS)
# ==========================================================
# Personalização visual do sistema.
#
# Cada classe representa um nível hierárquico:
#
# brasil     → Centro Nacional
# regiao     → Região do país
# estado     → Estado
# municipio  → Município
#
# ==========================================================

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

# ==========================================================
# TOPOLOGIA DA REDE
# ==========================================================
# Estrutura hierárquica do sistema.
#
# Brasil
# └── Região
#     └── Estado
#         └── Município
#             └── Semáforos
#
# Cada semáforo possui um identificador único.
# ==========================================================

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

# ==========================================================
# FUNÇÃO: calcular_tempo_verde
# ==========================================================
# Responsável por definir automaticamente o
# tempo do sinal verde com base no fluxo detectado.
#
# Quanto maior o fluxo,
# maior será o tempo do sinal verde.
#
# Fluxo < 20     → 20 segundos
# Fluxo < 50     → 40 segundos
# Fluxo < 100    → 60 segundos
# Fluxo ≥ 100    → 90 segundos
# ==========================================================

def calcular_tempo_verde(fluxo):

    if fluxo < 20:
        return 20

    elif fluxo < 50:
        return 40

    elif fluxo < 100:
        return 60

    else:
        return 90


# ==========================================================
# FUNÇÃO: detectar_emergencia
# ==========================================================
# Simula a detecção de veículos prioritários,
# como ambulâncias, bombeiros ou polícia.
#
# Foi adotada uma probabilidade de 5%.
#
# Retorna:
# True  → emergência detectada
# False → situação normal
# ==========================================================

def detectar_emergencia():

    return randint(1, 100) <= 5


# ==========================================================
# FUNÇÃO: verificar_configuracao
# ==========================================================
# Verifica se a estrutura da rede está correta.
#
# O objetivo é evitar que o sistema execute
# utilizando uma topologia inválida.
#
# Retorna:
# True  → configuração válida
# False → configuração inválida
# ==========================================================

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


# ==========================================================
# FUNÇÃO: executar_semaforo
# ==========================================================
# Simula o funcionamento de um semáforo.
#
# Etapas:
# 1. Gera o fluxo de veículos;
# 2. Verifica se há emergência;
# 3. Ajusta automaticamente o tempo verde;
# 4. Retorna os dados para o painel.
#
# Retorna um dicionário contendo:
# - Identificação do semáforo;
# - Fluxo detectado;
# - Modo de operação;
# - Tempos dos sinais;
# - Informação sobre emergência.
# ==========================================================

def executar_semaforo(id_semaforo):

    # Simula o fluxo detectado pelo sensor.
    fluxo = randint(5, 150)

    # Verifica emergência.
    emergencia = detectar_emergencia()

    # Caso exista emergência,
    # o tempo verde é ampliado.
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


# Título principal da aplicação
st.title("🚦 Centro Nacional de Controle de Trânsito")

# Descrição do sistema
st.write("Sistema Inteligente de Gerenciamento de Semáforos")

# ==========================================================
# SIDEBAR (MENU LATERAL)
# ==========================================================
# Contém os controles principais do sistema.
# ==========================================================

st.sidebar.header("⚙️ Controle")

# Botão responsável por executar uma nova simulação.
# Cada clique gera novos fluxos e novos resultados.
executar = st.sidebar.button("▶ Executar Simulação")

# ==========================================================
# ATUALIZAÇÃO AUTOMÁTICA
# ==========================================================
# O painel permanecerá executando continuamente,
# recarregando os dados a cada 20 segundos.
# ==========================================================

st.sidebar.success("🟢 Monitoramento em tempo real")

st.sidebar.write("Atualização automática: 20 segundos")

# Exibe a topologia da rede na barra lateral.
with st.sidebar.expander("🌎 Topologia da Rede"):
    st.json(rede)

# Aguarda 20 segundos e recarrega a página automaticamente.
time.sleep(20)
st.rerun()

# ==========================================================
# NÍVEL NACIONAL
# ==========================================================
# Representa o Centro Nacional de Controle.
# ==========================================================

st.markdown(
    '<div class="brasil">🇧🇷 BRASIL</div>',
    unsafe_allow_html=True
)

# ==========================================================
# PROCESSAMENTO DA HIERARQUIA
# ==========================================================
# Brasil
# └── Região
#     └── Estado
#         └── Município
#             └── Semáforo
# ==========================================================

for regiao, estados in rede["Brasil"].items():

    # ======================================================
    # REGIÃO
    # ======================================================

    st.markdown(
        f'<div class="regiao">🌎 REGIÃO: {regiao}</div>',
        unsafe_allow_html=True
    )

    for estado, municipios in estados.items():

        # ==================================================
        # ESTADO
        # ==================================================
        # Variáveis acumuladoras estaduais.
        # ==================================================

        fluxo_estado = 0
        total_emergencias_estado = 0
        total_semaforos_estado = 0

        st.markdown(
            f'<div class="estado">🏛️ ESTADO: {estado}</div>',
            unsafe_allow_html=True
        )

        # ==================================================
        # MUNICÍPIOS
        # ==================================================

        for municipio, semaforos in municipios.items():

            # Lista que armazenará os dados da tabela.
            dados_semaforos = []

            # Variáveis acumuladoras municipais.
            fluxo_municipio = 0
            emergencias_municipio = 0

            # ==============================================
            # SEMÁFOROS
            # ==============================================

            for semaforo in semaforos:

                # Executa a lógica inteligente do semáforo.
                dados = executar_semaforo(semaforo)

                # Adiciona os dados na tabela.
                dados_semaforos.append({
                    "Semáforo": dados["Semáforo"],
                    "Fluxo": dados["Fluxo"],
                    "Modo": dados["Modo"],
                    "Verde (s)": dados["Verde (s)"],
                    "Amarelo (s)": dados["Amarelo (s)"],
                    "Vermelho (s)": dados["Vermelho (s)"]
                })

                # ==========================================
                # FLUXO MUNICIPAL
                # ==========================================
                # O fluxo municipal é calculado pela soma
                # dos fluxos dos semáforos.
                # ==========================================

                fluxo_municipio += dados["Fluxo"]

                # Contabiliza emergências municipais.
                if dados["Emergência"]:
                    emergencias_municipio += 1

            # ==============================================
            # FLUXO ESTADUAL
            # ==============================================
            # O fluxo estadual é obtido pela soma dos
            # fluxos municipais.
            # ==============================================

            fluxo_estado += fluxo_municipio

            total_emergencias_estado += emergencias_municipio

            total_semaforos_estado += len(semaforos)

            # ==============================================
            # CARD DO MUNICÍPIO (CORRIGIDO)
            # ==============================================
            # Utiliza border=True para garantir que
            # métricas, alertas e tabela permaneçam
            # dentro do mesmo bloco visual.
            # ==============================================

            with st.container(border=True):

                # Nome do município
                st.markdown(
                    f"""
                    <div class="municipio">
                        🏙️ MUNICÍPIO: {municipio}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ==========================================
                # MÉTRICAS MUNICIPAIS
                # ==========================================

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

                # ==========================================
                # ALERTA DE CONGESTIONAMENTO
                # ==========================================

                if fluxo_municipio > 200:

                    st.warning(
                        "⚠️ Congestionamento detectado.\n"
                        "Aumentar tempo verde nas vias principais."
                    )

                else:

                    st.success(
                        "✅ Fluxo dentro da normalidade."
                    )

                # ==========================================
                # TABELA DOS SEMÁFOROS
                # ==========================================
                # Cada município possui sua própria tabela.
                # ==========================================

                st.dataframe(
                    pd.DataFrame(dados_semaforos),
                    use_container_width=True,
                    hide_index=True
                )

        # ==================================================
        # RESUMO ESTADUAL
        # ==================================================
        # Exibe os indicadores consolidados do estado.
        # ==================================================

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

        # ==================================================
        # DECISÕES ESTADUAIS
        # ==================================================
        # Caso o fluxo estadual seja elevado,
        # o sistema sugere ações de gerenciamento.
        # ==================================================

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

        # Linha divisória entre estados.
        st.divider()

# ==========================================================
# FIM DO SISTEMA
# ==========================================================
# Ao final da execução, o painel apresenta uma visão
# completa do funcionamento da rede nacional de
# semáforos inteligentes, auxiliando gestores na
# tomada de decisão em diferentes níveis hierárquicos.
# ==========================================================
