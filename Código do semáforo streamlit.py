# ==========================================================

# IMPORTAÇÃO DAS BIBLIOTECAS

# ==========================================================

# streamlit: cria a interface web do sistema.

# pandas: organiza os dados em tabelas.

# randint: gera valores aleatórios para simular o trânsito.

# time: tempo para automatizar o código

import streamlit as st

import pandas as pd

from random import randint

import time



# ==========================================================

# CONFIGURAÇÃO DA PÁGINA

# ==========================================================

# Define o título exibido na aba do navegador,

# o ícone e o tipo de layout utilizado.

st.set_page_config(

    page_title="Centro Nacional de Controle de Trânsito",

    page_icon="🚦",

    layout="wide"

)



# Controle automático da simulação

if "executando" not in st.session_state:

    st.session_state.executando = False



# ==========================================================

# ESTILOS DA INTERFACE (CSS)

# ==========================================================

# Utiliza CSS para personalizar a aparência do sistema.

# Cada classe será aplicada em diferentes partes do painel.

st.markdown("""

<style>



/* Cabeçalho principal do Brasil */

.brasil {

    background-color: #0B3D91;

    color: white;

    padding: 12px;

    border-radius: 10px;

    font-size: 28px;

    font-weight: bold;

    text-align: center;

}



/* Título das regiões */

.regiao {

    background-color: #2E8B57;

    color: white;

    padding: 10px;

    border-radius: 10px;

    font-size: 24px;

    font-weight: bold;

    margin-top: 20px;

}



/* Título dos estados */

.estado {

    background-color: #FF8C00;

    color: white;

    padding: 10px;

    border-radius: 10px;

    font-size: 20px;

    font-weight: bold;

    margin-top: 15px;

}



/* Cartão de informações do município */

.card-municipio {

    border: 2px solid #8A2BE2;

    border-radius: 15px;

    padding: 15px;

    margin-top: 20px;

    margin-bottom: 20px;

    background-color: rgba(138, 43, 226, 0.05);

}



/* Nome do município */

.municipio {

    color: #8A2BE2;

    font-size: 22px;

    font-weight: bold;

}



/* Texto auxiliar */

.small-text {

    color: gray;

    font-size: 14px;

}



</style>

""", unsafe_allow_html=True)



# ==========================================================

# TOPOLOGIA DA REDE

# ==========================================================

# Estrutura hierárquica do sistema:

#

# Brasil

# └─ Região

#    └─ Estado

#       └─ Município

#          └─ Semáforos

#

# Essa organização representa como os dados

# seriam distribuídos em um sistema nacional.

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



# ==========================================================

# FUNÇÃO: CALCULAR TEMPO VERDE

# ==========================================================

# Define o tempo do sinal verde de acordo

# com o fluxo de veículos detectado.

#

# Quanto maior o fluxo, maior o tempo verde.

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

# FUNÇÃO: DETECTAR EMERGÊNCIA

# ==========================================================

# Simula a passagem de veículos prioritários.

#

# Existe aproximadamente 5% de chance de ocorrer

# uma situação de emergência.

def detectar_emergencia():



    return randint(1, 100) <= 5





# ==========================================================

# FUNÇÃO: VERIFICAR CONFIGURAÇÃO DA REDE

# ==========================================================

# Garante que a estrutura da topologia

# esteja corretamente organizada.

#

# Retorna True se estiver correta

# e False caso exista algum erro.

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

# FUNÇÃO: EXECUTAR SEMÁFORO

# ==========================================================

# Simula o funcionamento individual

# de cada semáforo do sistema.

#

# Etapas:

# 1. Gera um fluxo aleatório;

# 2. Verifica emergência;

# 3. Define o modo de operação;

# 4. Retorna os dados do ciclo.

def executar_semaforo(id_semaforo):



    # Quantidade simulada de veículos

    fluxo = randint(5, 150)



    # Verifica emergência

    emergencia = detectar_emergencia()



    # Define o comportamento do semáforo

    if emergencia:



        modo = "🚑 Emergência"



        # Prioridade máxima

        tempo_verde = 120



    else:



        modo = "🟢 Normal"



        tempo_verde = calcular_tempo_verde(fluxo)



    # Retorna todos os dados

    return {

        "Semáforo": id_semaforo,

        "Fluxo": fluxo,

        "Modo": modo,

        "Verde (s)": tempo_verde,

        "Amarelo (s)": 5,

        "Vermelho (s)": 30,

        "Emergência": emergencia

    }





# ==========================================================

# INTERFACE PRINCIPAL

# ==========================================================

# Exibe o título e descrição do sistema.

st.title("🚦 Centro Nacional de Controle de Trânsito")



st.write(

    "Sistema Inteligente de Gerenciamento de Semáforos"

)



# ==========================================================

# MENU LATERAL

# ==========================================================

# Área destinada aos controles do operador.

st.sidebar.header("⚙️ Controle")



# Botão para iniciar a simulação.

if st.sidebar.button("▶ Iniciar Simulação"):

    st.session_state.executando = True



if st.sidebar.button("⏹ Parar Simulação"):

    st.session_state.executando = False



# Exibe a estrutura da rede.

with st.sidebar.expander("🌎 Topologia da Rede"):



    st.json(rede)





# ==========================================================

# VALIDAÇÃO DA REDE

# ==========================================================

# Interrompe o sistema caso a topologia

# esteja configurada incorretamente.

if not verificar_configuracao(rede):



    st.error("❌ Configuração da rede inválida.")



    st.stop()





# ==========================================================

# AGUARDA O INÍCIO DA SIMULAÇÃO

# ==========================================================

# O programa só continua após o clique.

if not st.session_state.executando:

    

    st.info(

        "Clique em **Executar Simulação** "

        "para iniciar o monitoramento."

    )



    st.stop()





# ==========================================================

# CABEÇALHO NACIONAL

# ==========================================================

st.markdown(

    '<div class="brasil">🇧🇷 BRASIL</div>',

    unsafe_allow_html=True

)





# ==========================================================

# PROCESSAMENTO DOS DADOS

# ==========================================================

# Percorre toda a estrutura da rede,

# simulando cada semáforo.

for regiao, estados in rede["Brasil"].items():



    # Exibe a região atual

    st.markdown(

        f'<div class="regiao">🌎 REGIÃO: {regiao}</div>',

        unsafe_allow_html=True

    )



    for estado, municipios in estados.items():



        # Acumuladores estaduais

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



            dados_semaforos = []



            fluxo_municipio = 0

            emergencias_municipio = 0



            # Simula cada semáforo

            for semaforo in semaforos:



                dados = executar_semaforo(semaforo)



                # Guarda os dados para a tabela

                dados_semaforos.append({

                    "Semáforo": dados["Semáforo"],

                    "Fluxo": dados["Fluxo"],

                    "Modo": dados["Modo"],

                    "Verde (s)": dados["Verde (s)"],

                    "Amarelo (s)": dados["Amarelo (s)"],

                    "Vermelho (s)": dados["Vermelho (s)"]

                })



                # Soma fluxo municipal

                fluxo_municipio += dados["Fluxo"]



                # Conta emergências

                if dados["Emergência"]:

                    emergencias_municipio += 1



            # Atualiza dados estaduais

            fluxo_estado += fluxo_municipio



            total_emergencias_estado += (

                emergencias_municipio

            )



            total_semaforos_estado += len(semaforos)



            # ==============================================

            # CARD DO MUNICÍPIO

            # ==============================================

            with st.container(border=True):



                st.markdown(

                    f'🏙️ MUNICÍPIO: {municipio}'

                )



                # Métricas do município

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



                # Identifica congestionamento

                if fluxo_municipio > 200:



                    st.warning(

                        "⚠️ Congestionamento detectado.\n"

                        "Aumentar tempo verde nas "

                        "vias principais."

                    )



                else:



                    st.success(

                        "✅ Fluxo dentro da normalidade."

                    )



                # Exibe a tabela

                st.dataframe(

                    pd.DataFrame(dados_semaforos),

                    use_container_width=True,

                    hide_index=True

                )



                st.markdown(

                    '</div>',

                    unsafe_allow_html=True

                )



        # ==================================================

        # RESUMO DO ESTADO

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

        # TOMADA DE DECISÃO ESTADUAL

        # ==================================================

        # Caso o fluxo seja elevado,

        # o sistema sugere ações estratégicas.

        if fluxo_estado > 500:



            st.error(

                "🚨 DECISÃO ESTADUAL\n\n"

                "- Sincronizar semáforos "

                "dos municípios\n"

                "- Priorizar corredores "

                "de ônibus\n"

                "- Gerar alerta para o "

                "centro regional"

            )



        else:



            st.info(

                "ℹ️ Operação estadual dentro "

                "dos parâmetros normais."

            )



        # Linha divisória entre estados

        st.divider()

        

# Atualização automática a cada 20 segundos

if st.session_state.executando:

    time.sleep(20)

    st.rerun()



