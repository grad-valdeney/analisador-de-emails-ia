# ai_processor.py
from transformers import pipeline

# Dicionário para armazenar os modelos após o primeiro carregamento (Lazy Loading).
MODELS = {}

def get_classifier():
    """Carrega ou retorna o modelo de classificação já carregado."""
    if "classifier" not in MODELS:
        print("Carregando modelo de classificação pela primeira vez...")
        # Usando um modelo especialista em análise de sentimento e intenção,
        # que é mais preciso para classificar emails do que um modelo genérico.
        # Este modelo classifica o texto em 'positive', 'neutral', ou 'negative'.
        # Vamos mapear 'neutral' e 'positive' para Produtivo, e 'negative' para Improdutivo.
        MODELS["classifier"] = pipeline(
            "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        print("Modelo de classificação carregado.")
    return MODELS["classifier"]

def classify_email(text):
    """
    Classifica o texto do email em 'Produtivo' ou 'Improdutivo'.

    - Produtivo: Emails que requerem uma ação ou resposta específica
      (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
    - Improdutivo: Emails que não necessitam de uma ação imediata
      (ex.: mensagens de felicitações, agradecimentos).
    """
    if not text or not text.strip():
        return "Indeterminado"

    # 1. Abordagem Híbrida: Filtro rápido por palavras-chave para spam/propaganda.
    # Isso resolve casos óbvios de forma rápida e precisa antes de usar a IA.
    text_lower = text.lower()
    spam_keywords = [
        "desconto", "oferta", "promoção", "clique aqui", "imperdível",
        "grátis", "oportunidade única", "compre agora", "vagas limitadas"
    ]

    if any(keyword in text_lower for keyword in spam_keywords):
        return "Improdutivo"

    # 2. Se não for spam óbvio, usamos o modelo especialista em sentimento/intenção.
    classifier = get_classifier()
    # Truncamos o texto para focar na parte principal do email, melhorando a precisão.
    result = classifier(text[:512]) # O modelo tem um limite de 512 tokens.

    # Mapeamos o resultado do modelo para nossas categorias.
    # Emails de trabalho (dúvidas, pedidos) são geralmente 'neutral' ou 'positive'.
    # Emails improdutivos (reclamações vagas, desabafos) tendem a ser 'negative'.
    sentiment = result[0]['label']

    if sentiment == 'neutral' or sentiment == 'positive':
        return "Produtivo"
    else:
        return "Improdutivo"

def suggest_response(text, category):
    """Gera uma sugestão de resposta com base na categoria do email."""
    if not text or not text.strip():
        return "Nenhum texto fornecido para gerar resposta."

    if category == "Improdutivo":
        # Resposta amigável para emails que não necessitam ação imediata
        # (felicitações, agradecimentos, etc.)
        response = "Olá,\n\n"
        response += "Obrigado pela sua mensagem. Agradecemos o contato e o carinho.\n\n"
        response += "Atenciosamente,\nEquipe"

    elif category == "Produtivo":
        # Resposta profissional para emails que requerem ação ou resposta específica
        # (solicitações de suporte, atualizações sobre casos, dúvidas sobre o sistema)
        response = "Prezado(a),\n\n"
        response += "Agradecemos o seu contato. Recebemos a sua mensagem e nossa equipe irá analisar a solicitação.\n\n"
        response += "Retornaremos em breve com mais informações ou com a resolução do seu caso.\n\n"
        response += "Atenciosamente,\nEquipe"

    else:
        return "Não foi possível gerar uma sugestão de resposta para esta categoria."

    return response
