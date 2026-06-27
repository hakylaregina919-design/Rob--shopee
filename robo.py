import time
import requests

def obter_dolar_ao_vivo():
    try:
        resposta = requests.get("https://awesomeapi.com.br")
        return float(resposta.json()["USDBRL"]["bid"])
    except:
        return 5.50

# =============================================================
# O SEU ROBÔ AGORA RODA EM LOOP INFINITO (MODO PILOTO AUTOMÁTICO)
# =============================================================
print("🚀 [SISTEMA] ATIVANDO MODO PILOTO AUTOMÁTICO...")
time.sleep(1)

contador_execucoes = 1

while True:  # 🔄 Isso cria um loop que NUNCA para sozinho
    print(f"\n🔄 [ROTA NO AR] Executando verificação número: {contador_execucoes}")
    
    # 1. Puxa o dólar mais atualizado daquele exato minuto
    DOLAR_AGORA = obter_dolar_ao_vivo()
    print(f"📊 Dólar Atual: R$ {DOLAR_AGORA}")
    
    # 2. Dados simulados do produto
    produto_titulo = "Fone de Ouvido Original Lenovo LP40 Pro TWS"
    preco_usd = 6.99
    TAXA_SHOPEE = 0.14
    LUCRO_FIXO = 50.00
    
    # 3. Faz a matemática financeira do lucro
    custo_reais = preco_usd * DOLAR_AGORA
    preco_final_shopee = (custo_reais + LUCRO_FIXO) / (1 - TAXA_SHOPEE)
    
    print(f"💰 Preço recalculado para a Shopee: R$ {round(preco_final_shopee, 2)}")
    print("✨ [OK] Sincronização concluída. Aguardando próximo ciclo...")
    
    # Soma +1 no contador de vezes que o robô trabalhou
    contador_execucoes += 1
    
    # ⚠️ AQUI ESTÁ O SEGREDO: O robô vai dormir por 5 segundos antes de fazer tudo de novo
    # Em uma ferramenta real, mudaríamos aqui para 3600 (que seriam 60 minutos)
    time.sleep(5) 
