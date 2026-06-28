import streamlit as st
import sqlite3
import time

st.set_page_config(page_title="Robô Integrador Shopee", page_icon="🤖")
st.title("🤖 Painel do Seu Robô SaaS")

aba_pagamento, aba_configuracao = st.tabs(["7c279cad-2cfe-4a4c-8296-5c4a9c4e32c2"])

# Função interna para salvar os dados do cliente no banco de dados real
def salvar_no_banco(email, pid, pkey):
    try:
        conexao = sqlite3.connect("clientes_saas.db")
        cursor = conexao.cursor()
        # Salva ou atualiza os dados se o cliente já existir
        cursor.execute("""
        INSERT INTO assinantes (email, partner_id, partner_key, status_pagamento)
        VALUES (?, ?, ?, 'pago')
        ON CONFLICT(email) DO UPDATE SET partner_id=?, partner_key=?, status_pagamento='pago'
        """, (email, pid, pkey, pid, pkey))
        conexao.commit()
        conexao.close()
        return True
    except Exception as e:
        st.error(f"Erro no banco: {e}")
        return False

with aba_pagamento:
    st.subheader("Ative sua assinatura mensal via Pix")
    st.write("Valor do Plano Profissional: **R$ 99,90 / mês**")
    st.info("🔑 **Chave Copia e Cola do Pix (Simulada):**\n00020101021126360014br.gov.bcb.pix0114seuemail@saas.com520400005303986540599.905802BR5913RoboShopeeSaaS6009SaoPaulo6207050300163047A3D")
    
    if st.button("📱 Simular Pagamento do Pix pelo Cliente"):
        with st.spinner("⏳ Aguardando confirmação do banco..."):
            time.sleep(1.5)
        st.session_state["pago"] = True
        st.success("💰 Pix de R$ 99,90 recebido com sucesso!")
        st.balloons()

with aba_configuracao:
    st.subheader("Configuração da Automação")
    
    if "pago" not in st.session_state or st.session_state["pago"] == False:
        st.error("⚠️ ACESSO BLOQUEADO: Você precisa realizar o pagamento na aba ao lado para liberar o robô.")
    else:
        st.success("🔓 ACESSO LIBERADO! Seu plano está ativo.")
        
        # Formulário que o cliente preenche
        email_cliente = st.text_input("Seu E-mail de Assinante:")
        pid_cliente = st.text_input("Shopee Partner ID:")
        pkey_cliente = st.text_input("Shopee Partner Key:", type="password")
        
        if st.button("🚀 Ligar Robô no Piloto Automático"):
            if email_cliente and pid_cliente and pkey_cliente:
                # O site grava as informações no banco de dados agora!
                sucesso = salvar_no_banco(email_cliente, pid_cliente, pkey_cliente)
                if sucesso:
                    st.success(f"🌟 PERFEITO! Dados salvos com segurança no banco de dados para o e-mail: {email_cliente}")
                    st.info("🤖 O robô central na nuvem já localizou sua conta e começou a trabalhar!")
            else:
                st.error("⚠️ Preencha todos os campos antes de ativar.")       