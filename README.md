---
title: Analisador de Emails com IA
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# Analisador de Emails com IA

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.0-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/Hugging_Face-Transformers-yellow.svg" alt="Hugging Face">
  <img src="https://img.shields.io/badge/Deploy-Hugging_Face_Spaces-blueviolet.svg" alt="Hugging Face Spaces">
</p>

Aplicação web que utiliza Inteligência Artificial para classificar emails em **Produtivos** ou **Improdutivos** e sugerir respostas automáticas. Desenvolvido com Python e Flask, este projeto visa otimizar a gestão de emails e aumentar a produtividade da equipe, automatizando tarefas repetitivas.

## 🔗 Link da Aplicação

A aplicação está hospedada e pode ser acessada publicamente através do Hugging Face Spaces:

**[➡️ Acessar Analisador de Emails com IA](https://huggingface.co/spaces/Valdeney/analisador-de-emails-ia)**

## ✨ Funcionalidades Principais

-   **Classificação Inteligente:** Usa um modelo de IA da Hugging Face (`facebook/bart-large-mnli`) para analisar o conteúdo do email e determinar sua categoria.
-   **Sugestão de Respostas:** Gera respostas automáticas e contextuais com base na classificação do email.
-   **Múltiplos Formatos de Entrada:** Permite colar o texto do email diretamente ou fazer o upload de arquivos nos formatos `.txt` e `.pdf`.
-   **Interface Web Simples:** Uma interface limpa e intuitiva para facilitar o uso por qualquer pessoa.

## 🛠️ Tecnologias Utilizadas

-   **Backend:** Python, Flask
-   **Inteligência Artificial:** Hugging Face Transformers
-   **Frontend:** HTML, CSS, JavaScript
-   **Leitura de PDF:** PyPDF2
-   **Servidor de Produção:** Gunicorn
-   **Deployment:** Docker, Hugging Face Spaces

## 🚀 Como Executar Localmente

Siga os passos abaixo para executar a aplicação no seu ambiente de desenvolvimento.

### Pré-requisitos

-   Python 3.8+
-   Git

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/grad-valdeney/analisador-emails-ia.git
    cd analisador-emails-ia
    ```

2.  **Crie e ative um ambiente virtual:**
    É uma boa prática isolar as dependências do projeto.
    ```bash
    # Criar o ambiente
    python -m venv venv

    # Ativar no Windows (PowerShell)
    .\venv\Scripts\Activate.ps1

    # Ativar no Linux/macOS/Git Bash
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    O arquivo `requirements.txt` contém todas as bibliotecas necessárias.
    ```bash
    pip install -r requirements.txt
    ```
    *Observação: Na primeira vez, o download das bibliotecas de IA (`torch`, `transformers`) pode levar alguns minutos.*

4.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

5.  **Acesse no navegador:**
    Abra seu navegador e acesse a URL:
    http://127.0.0.1:5000/

## ☁️ Estratégia de Deployment

A aplicação está configurada para deploy contínuo no **Hugging Face Spaces** utilizando Docker. Esta abordagem foi escolhida por oferecer um ambiente robusto e com recursos de memória adequados para aplicações de IA, garantindo estabilidade e desempenho que plataformas mais genéricas (como Vercel ou Render no plano gratuito) não suportam para este tipo de projeto.

A configuração do ambiente de produção pode ser encontrada nos arquivos `Dockerfile` e no cabeçalho deste `README.md`.

## 📂 Estrutura do Projeto
