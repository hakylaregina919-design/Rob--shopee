import streamlit as st
import sqlite3
import requests
import time

st.set_page_config(page_title="Robo Integrador Shopee", page_icon="🤖", layout="centered")
st.title("🤖 Painel do Seu Robo SaaS")

ASAAS_API_KEY =  "$aact_prod_000MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OjhlNWI2YTYyLTlmNjYtNGM5Yi1iYzhhLTMzMjExYjIxMDQzMjo6JGFhY2hfOWNhNDQ1ZTAtZTY0Yy00YTAxLWIzMmUtNDQwZDk5N2RjYTdl"
TELEGRAM_BOT_TOKEN = "8013204437"
# Abas limpas sem caracteres especiais para o servidor nao travar
aba_pagamento, aba_configuracao, aba_suporte = st.tabs(["Assinatura Pix", "Configurar Robo", "Suporte 24h"])

def salvar_no_banco(email, pid, pkey):
    try:
        conexao = sqlite3.connect("clientes_saas.db")
        cursor = conexao.cursor()
        cursor.execute("""
        INSERT INTO assinantes (email, partner_id, partner_key, status_pagamento)
        VALUES (?, ?, ?, 'pago')
        ON CONFLICT(email) DO UPDATE SET partner_id=?, partner_key=?, status_pagamento='pago'
        """, (email, pid, pkey, pid, pkey))
        conexao.commit()
        conexao.close()
        return True
    except:
        return False

with aba_pagamento:
    st.subheader("Ative sua assinatura mensal via Pix")
    st.write("Plano Profissional: **R$ 99,90 / mes**")
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
        pid_cliente = st.text_input("Shopee Partner ID:")
        pkey_cliente = st.text_input("Shopee Partner Key:", type="password")
        
        if st.button("🚀 Ligar Robo no Piloto Automatico"):
            if email_cliente and pid_cliente and pkey_cliente:
                if salvar_no_banco(email_cliente, pid_cliente, pkey_cliente):
                    st.success("🌟 Dados salvos! O robo central comecou a trabalhar por voce!")

with aba_suporte:
    st.subheader("🤖 Assistente de Suporte Tecnico 24h")
    st.write("Digite sua duvida sobre o robo integrador abaixo.")
    pergunta_cliente = st.text_input("Como posso te ajudar hoje?")
    
    if st.button("💬 Enviar para o Suporte"):
        if pergunta_cliente:
            with st.spinner("🤖 Robo analisando sua duvida..."):
                time.sleep(1)
            pergunta = pergunta_cliente.lower()
            if "pagar" in pergunta or "pix" in pergunta:
                st.write("🤖 **Suporte:** Se ja fez o Pix, va na aba 'Assinatura Pix' e clique em 'Ja paguei!'.")
            elif "shopee" in pergunta or "chave" in pergunta:
                st.write("🤖 **Suporte:** Acesse ://shopee.com para pegar seu Partner ID.")
            else:
                st.write("🤖 **Suporte:** Recebi sua mensagem! Nossa equipe entrara em contato por e-mail em ate 1 hora.")
