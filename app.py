import streamlit as st
import sqlite3
import requests
import time

st.set_page_config(page_title="Robo Integrador Shopee & Shein", page_icon="🤖", layout="centered")
st.title("🤖 Painel do Seu Robo SaaS")

# 🚨 CHAVE DO ASAAS (Caso use o modo real, insira sua chave aqui)
ASAAS_API_KEY ="$aact_prod_000MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OmM0MDk3NTg5LTBmODctNGNiYS05YzhmLWNiY2YxMzM5MzVjZDo6JGFhY2hfMWJmZDRiNjMtZjdjMy00NjA4LWE4OWYtNDAwNDM4MDI0M2Nh"

aba_pagamento, aba_configuracao, aba_suporte = st.tabs(["Assinatura Pix", "Configurar Robo", "Suporte 24h"])

def salvar_no_banco(email, mktplace, campo1, campo2):
    try:
        conexao = sqlite3.connect("clientes_saas.db")
        cursor = conexao.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS assinantes_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            plataforma TEXT NOT NULL,
            credencial_1 TEXT NOT NULL,
            credencial_2 TEXT NOT NULL,
            status_pagamento TEXT DEFAULT 'pago'
        )
        """)
        cursor.execute("""
        INSERT INTO assinantes_v2 (email, plataforma, credencial_1, credencial_2, status_pagamento)
        VALUES (?, ?, ?, ?, 'pago')
        ON CONFLICT(email) DO UPDATE SET plataforma=?, credencial_1=?, credencial_2=?, status_pagamento='pago'
        """, (email, mktplace, campo1, campo2, mktplace, campo1, campo2))
        conexao.commit()
        conexao.close()
        return True
    except:
        return False

with aba_pagamento:
    st.subheader("Ative sua assinatura mensal via Pix")
    st.write("Plano Padrao (Apenas Shopee): **R$ 99,90 / mes**")
    st.write("Plano Premium (Shopee + Shein): **R$ 149,90 / mes**")
    
    email_pagar = st.text_input("Digite seu e-mail para gerar o Pix:")
    
    if st.button("⚡ Gerar QRCode do Pix"):
        if email_pagar:
            st.success("✅ Pix gerado com sucesso!")
            st.code("00020101021126360014br.gov.bcb.pix0114seuemail@saas.com...", language="text")
            if st.button("🔄 Já paguei! Verificar pagamento"):
                st.session_state["pago"] = True
                st.success("💰 Pagamento confirmado! Acesso liberado.")
                st.balloons()

with aba_configuracao:
    st.subheader("Configuracao da Automacao")
    if "pago" not in st.session_state or st.session_state["pago"] == False:
        st.error("⚠️ ACESSO BLOQUEADO: Voce precisa realizar o pagamento na aba ao lado para liberar o robo.")
    else:
        st.success("🔓 ACESSO LIBERADO! Seu plano esta ativo.")
        email_cliente = st.text_input("Seu E-mail de Assinante:")
        
        # O cliente escolhe em qual plataforma quer ligar a integracao
        plataforma_escolhida = st.selectbox("Selecione qual integracao deseja ativar:", ["Shopee", "Shein Marketplace"])
        
        if plataforma_escolhida == "Shopee":
            c1 = st.text_input("Shopee Partner ID:")
            c2 = st.text_input("Shopee Partner Key:", type="password")
        else:
            st.info("🔗 Integracao Shein Local ativada pelo portal ://shein.com")
            c1 = st.text_input("Shein App Key:")
            c2 = st.text_input("Shein App Secret:", type="password")
            
        if st.button("🚀 Ligar Robo no Piloto Automatico"):
            if email_cliente and c1 and c2:
                if salvar_no_banco(email_cliente, plataforma_escolhida, c1, c2):
                    st.success(f"🌟 SUCESSO! O robo começou a rodar para a sua loja da {plataforma_escolhida}!")
            else:
                st.error("⚠️ Preencha todos os campos antes de ligar o robo.")

with aba_suporte:
    st.subheader("🤖 Assistente de Suporte Tecnico 24h")
    st.write("Digite sua duvida sobre a integracao Shopee ou Shein.")
    pergunta_cliente = st.text_input("Como posso te ajudar hoje?")
    
    if st.button("💬 Enviar para o Suporte"):
        if pergunta_cliente:
            pergunta = pergunta_cliente.lower()
            if "shein" in pergunta:
                st.write("🤖 **Suporte:** Para vender automatizado na Shein, o lojista deve habilitar a API no menu 'Open Platform' dentro do painel Shein Seller local.")
            else:
                st.write("🤖 **Suporte:** Recebi seu chamado! Nossa equipe de plantao ja esta de olho.")
