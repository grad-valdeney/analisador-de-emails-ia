# ai_processor.py
from transformers import pipeline

# Carregue os modelos uma única vez para otimizar o desempenho.
# O modelo de classificação pode determinar a categoria sem treinamento prévio.
print("Carregando modelo de classificação...")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
print("Modelo de classificação carregado.")


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

    # Rótulos mais simples e diretos para melhorar a precisão da IA.
    candidate_labels = [
        "email de trabalho que precisa de uma resposta",
        "email pessoal ou de felicitações"
    ]
    hypothesis_template = "O conteúdo deste email é sobre {}."

    result = classifier(text, candidate_labels, hypothesis_template=hypothesis_template)

    # Mapeamos o resultado do rótulo descritivo de volta para a categoria simples.
    top_label = result['labels'][0]
    if "trabalho" in top_label:
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
