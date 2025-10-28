import streamlit as st
import pandas as pd
import numpy as np
import time

# --- Configurações Iniciais e Estado da Aplicação ---
st.set_page_config(page_title="BioMine Nexus - Digital Twin", layout="wide")

# Inicialização de dados e estado na sessão
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        'Tempo (h)', 'Toneladas Processadas', 'Contaminacao (%)', 
        'Minerais Recuperados (kg)', 'Bioplasticos Produzidos (kg)', 
        'Biofertilizantes Produzidos (kg)', 'Compositos Produzidos (kg)',
        'Energia Gerada (kWh)', 'Parametro IA', 'Status Reator', 'Status Energia',
        'pH', 'Temperatura (°C)', 'Turbidez (NTU)', 'Condutividade (mS/cm)',
        'Oxigênio Dissolvido (mg/L)', 'Metais Pesados (ppm)'
    ])
    st.session_state.contaminacao_atual = 100.0
    st.session_state.total_toneladas = 0
    st.session_state.tempo_simulado_h = 0
    st.session_state.is_running = False

# --- Título e Controles no Topo da Página ---
st.title("👨‍🔬 BioMine Nexus: Painel de Controle de Operações")
st.markdown("### Monitoramento do Processo Biorregenerativo em Tempo Real")

col_start, col_stop, col_reset = st.columns([1, 1, 6])
with col_start:
    start_btn = st.button("▶️ Iniciar Operação", type="primary")
with col_stop:
    stop_btn = st.button("⏸️ Parar Operação")
with col_reset:
    reset_btn = st.button("🔄 Resetar Simulação")

st.markdown("---")

# Lógica dos botões
if start_btn:
    st.session_state.is_running = True
if stop_btn:
    st.session_state.is_running = False
if reset_btn:
    st.session_state.session_state = None # Limpa todo o estado para reset completo
    st.rerun()

# --- Placeholder para o Dashboard Principal (KPIs e Gráficos) ---
main_kpis = st.empty()
reactor_details = st.empty()
energy_details = st.empty()
rejeitos_details = st.empty()
comparison_details = st.empty()

# --- Funções de Simulação (O Coração do Gêmeo Digital) ---
def simulate_step(hora_simulada):
    toneladas_processadas = 2 # 2 toneladas por hora
    contaminacao_anterior = st.session_state.contaminacao_atual
    
    # Módulo 1: Biofiltração + IA (Otimização do processo)
    # A IA otimiza a eficiência com o tempo, simulando aprendizado contínuo
    fator_otimizacao_ia = 1.0 + (hora_simulada / 100.0) * 0.2
    reducao_total = np.random.uniform(0.04, 0.08) * fator_otimizacao_ia
    contaminacao_nova = max(0, contaminacao_anterior * (1 - reducao_total))
    
    # Módulo 2: Reator - Simulação de Parâmetros
    parametros_reator = {
        "pH": np.random.uniform(6.5, 7.5) + (fator_otimizacao_ia - 1),
        "Temperatura (°C)": np.random.uniform(25, 30),
        "Turbidez (NTU)": np.random.uniform(10, 20) * (1 - reducao_total),
        "Condutividade (mS/cm)": np.random.uniform(1.5, 2.5),
        "Oxigênio Dissolvido (mg/L)": np.random.uniform(6.0, 8.0),
        "Metais Pesados (ppm)": np.random.uniform(100, 200) * (1 - reducao_total),
        "Status de Operação": "OK" if np.random.random() > 0.95 else "Anomalia Detectada"
    }

    # Módulo 3: Energia Autossustentável
    energia_gerada = toneladas_processadas * np.random.uniform(0.1, 0.2)
    status_energia = "OK" if np.random.random() > 0.98 else "Atenção: Queda de Geração"

    # Módulo 4: Reaproveitamento de Rejeitos 4.0
    minerais_recuperados = toneladas_processadas * np.random.uniform(0.5, 0.8)
    bioplasticos = toneladas_processadas * np.random.uniform(0.1, 0.15)
    biofertilizantes = toneladas_processadas * np.random.uniform(0.2, 0.25)
    compositos = toneladas_processadas * np.random.uniform(0.05, 0.1)

    # Atualiza o estado da aplicação
    st.session_state.contaminacao_atual = contaminacao_nova
    st.session_state.total_toneladas += toneladas_processadas
    
    return {
        'Tempo (h)': hora_simulada,
        'Toneladas Processadas': st.session_state.total_toneladas,
        'Contaminacao (%)': contaminacao_nova,
        'Minerais Recuperados (kg)': minerais_recuperados,
        'Bioplasticos Produzidos (kg)': bioplasticos,
        'Biofertilizantes Produzidos (kg)': biofertilizantes,
        'Compositos Produzidos (kg)': compositos,
        'Energia Gerada (kWh)': energia_gerada,
        'Parametro IA': parametros_reator["pH"],
        'Status Reator': parametros_reator["Status de Operação"],
        'Status Energia': status_energia,
        **parametros_reator
    }

# --- Loop Principal da Simulação ---
if st.session_state.is_running:
    # O loop `while` rodará indefinidamente enquanto is_running for True
    while st.session_state.is_running:
        st.session_state.tempo_simulado_h += 1
        
        novo_registro = simulate_step(st.session_state.tempo_simulado_h)
        
        novo_registro_df = pd.DataFrame([novo_registro])
        st.session_state.data = pd.concat([st.session_state.data, novo_registro_df], ignore_index=True)

        # --- Atualização do Dashboard em Tempo Real ---
        with main_kpis.container():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Tempo de Operação", f"{st.session_state.tempo_simulado_h} h")
            with col2:
                st.metric("Toneladas Processadas", f"{st.session_state.total_toneladas} t")
            with col3:
                st.metric("Contaminação Atual", f"{st.session_state.contaminacao_atual:.2f}%", delta=f"{-novo_registro['Contaminacao (%)']:.2f}%")
            with col4:
                st.metric("Minerais Recuperados", f"{st.session_state.data['Minerais Recuperados (kg)'].sum():.2f} kg")

        with reactor_details.container():
            st.markdown("### 🔬 Reator Autônomo - Monitoramento de Parâmetros")
            col_reactor = st.columns(4)
            with col_reactor[0]: st.metric("pH", f"{novo_registro['pH']:.2f}")
            with col_reactor[1]: st.metric("Temperatura (°C)", f"{novo_registro['Temperatura (°C)']:.2f}")
            with col_reactor[2]: st.metric("Turbidez (NTU)", f"{novo_registro['Turbidez (NTU)']:.2f}")
            with col_reactor[3]: st.metric("Condutividade (mS/cm)", f"{novo_registro['Condutividade (mS/cm)']:.2f}")
            
            col_reactor2 = st.columns(4)
            with col_reactor2[0]: st.metric("Oxigênio Dissolvido", f"{novo_registro['Oxigênio Dissolvido (mg/L)']:.2f}")
            with col_reactor2[1]: st.metric("Metais Pesados (ppm)", f"{novo_registro['Metais Pesados (ppm)']:.2f}")
            with col_reactor2[2]: st.metric("Status Operacional", novo_registro['Status de Operação'])
            with col_reactor2[3]: st.metric("Ajuste IA", f"{novo_registro['Parametro IA']:.2f}")

        # --- Seção de Gráficos ---
        with energy_details.container():
            st.markdown("### ⚡ Módulo de Energia Autossustentável")
            col_energy = st.columns(2)
            with col_energy[0]:
                st.metric("Status do Equipamento", novo_registro['Status Energia'])
                st.bar_chart(pd.DataFrame({'Energia Gerada (kWh)': [novo_registro['Energia Gerada (kWh)']]}), use_container_width=True)
            with col_energy[1]:
                st.markdown("##### Geração de Energia por Hora")
                st.line_chart(st.session_state.data.set_index('Tempo (h)')['Energia Gerada (kWh)'])

        with rejeitos_details.container():
            st.markdown("### ♻️ Módulo Rejeitos 4.0")
            st.bar_chart(st.session_state.data[['Minerais Recuperados (kg)', 'Bioplasticos Produzidos (kg)', 'Biofertilizantes Produzidos (kg)', 'Compositos Produzidos (kg)']])

        with comparison_details.container():
            st.markdown("### 🆚 Comparativo: BioMine Nexus vs. Mineração Tradicional")
            comparativo_df = pd.DataFrame({
                'Tempo (h)': st.session_state.data['Tempo (h)'],
                'Contaminação Tradicional': [100 * (0.95 ** t) for t in st.session_state.data['Tempo (h)']],
                'Contaminação BioMine Nexus': st.session_state.data['Contaminacao (%)']
            }).set_index('Tempo (h)')
            st.line_chart(comparativo_df)
        
        # Simula o tempo de uma hora, essencial para o "real-time"
        time.sleep(1) 

if not st.session_state.is_running and st.session_state.tempo_simulado_h > 0:
    st.success("Operação concluída. O sistema está parado. ✅")
