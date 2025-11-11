// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('email-form');
  const submitButton = document.getElementById('submit-button');
  const emailTextInput = document.getElementById('email-text');
  const emailFileInput = document.getElementById('email-file');
  const fileNameSpan = document.getElementById('file-name');

  const resultsDiv = document.getElementById('results');
  const loader = document.getElementById('loader');
  const outputDiv = document.getElementById('output');
  const errorDiv = document.getElementById('error-message');

  const categoryBadge = document.getElementById('category-badge');
  const suggestedResponseP = document.getElementById('suggested-response');

  // Atualiza o nome do arquivo exibido
  emailFileInput.addEventListener('change', () => {
      if (emailFileInput.files.length > 0) {
          fileNameSpan.textContent = emailFileInput.files[0].name;
          emailTextInput.value = ''; // Limpa o textarea se um arquivo for selecionado
      } else {
          fileNameSpan.textContent = 'Nenhum arquivo selecionado';
      }
  });

  // Limpa o input de arquivo se o texto for digitado
  emailTextInput.addEventListener('input', () => {
      if (emailTextInput.value.trim() !== '') {
          emailFileInput.value = ''; // Reseta o input de arquivo
          fileNameSpan.textContent = 'Nenhum arquivo selecionado';
      }
  });

  form.addEventListener('submit', async function(event) {
      event.preventDefault();

      const formData = new FormData();
      const emailText = emailTextInput.value;
      const emailFile = emailFileInput.files[0];

      if (emailText.trim()) {
          formData.append('email_text', emailText);
      } else if (emailFile) {
          formData.append('email_file', emailFile);
      } else {
          alert('Por favor, insira um texto ou selecione um arquivo.');
          return;
      }

      // Exibe o loader e esconde resultados anteriores
      resultsDiv.classList.remove('hidden');
      loader.classList.remove('hidden');
      outputDiv.classList.add('hidden');
      errorDiv.classList.add('hidden');
      submitButton.disabled = true;
      submitButton.textContent = 'Analisando...';

      try {
          const response = await fetch('/analyze', {
              method: 'POST',
              body: formData,
          });

          const data = await response.json();

          if (!response.ok) {
              throw new Error(data.error || 'Ocorreu um erro no servidor.');
          }

          // Atualiza a categoria
          categoryBadge.textContent = data.category;
          categoryBadge.className = 'badge'; // Reseta classes
          categoryBadge.classList.add(data.category.toLowerCase());

          // Atualiza a sugestão de resposta
          suggestedResponseP.textContent = data.suggested_response;

          outputDiv.classList.remove('hidden');

      } catch (error) {
          console.error('Erro:', error);
          errorDiv.textContent = `Erro na análise: ${error.message}`;
          errorDiv.classList.remove('hidden');
      } finally {
          // Esconde o loader e reativa o botão
          loader.classList.add('hidden');
          submitButton.disabled = false;
          submitButton.textContent = 'Analisar Email';
      }
  });
});
