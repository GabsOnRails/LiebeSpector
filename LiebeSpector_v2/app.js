// 1. Obter referências aos elementos HTML (mantidas)
import { GoogleGenAI } from "https://esm.run/@google/genai";

// 1. Obter referências aos elementos HTML (mantidas)
const roteiroForm = document.getElementById("roteiroForm");
const livroNomeInput = document.getElementById("livroNome");
const partesGosteiTextarea = document.getElementById("partesGostei");
const submitBtn = document.getElementById("submitBtn");
const statusMessage = document.getElementById("statusMessage");
const roteiroOutput = document.getElementById("roteiroOutput");
const roteiroContent = document.getElementById("roteiroContent");

// --------------------------------------------------------
// CONFIGURAÇÃO DA API
// --------------------------------------------------------
const API_KEY = "";

// Inicializa a instância do Google Gen AI
// A classe GoogleGenAI agora é garantida por ter sido importada no topo
const ai = new GoogleGenAI({ apiKey: API_KEY });

roteiroForm.addEventListener("submit", handleFormSubmit);

function handleFormSubmit(event) {
  event.preventDefault();

  const livro = livroNomeInput.value.trim();
  const partes = partesGosteiTextarea.value.trim();

  if (!livro || !partes) {
    alert("Por favor, preencha o nome do livro e as partes favoritas.");
    return;
  }

  generateRoteiro(livro, partes);
}

/**
 * Função REAL que fará a chamada à API para gerar o roteiro.
 * @param {string} livro - Nome do livro.
 * @param {string} partes - Partes favoritas/temas a destacar.
 */
async function generateRoteiro(livro, partes) {
  showLoading(true);
  roteiroOutput.style.display = "none";

  // 1. Montagem do Prompt (Instrução para o Gemini)
  const promptText = `
        Você é um especialista em criação de conteúdo para Instagram/TikTok. 
        Sua tarefa é gerar um roteiro de vídeo curto (Reel/TikTok) baseado na leitura de um livro.

        Regras:
        1. O roteiro deve ter GATILHO (0-3s), DESENVOLVIMENTO (3-45s) e CHAMADA PARA AÇÃO (45-60s).
        2. O foco principal deve ser conectar as partes favoritas do usuário com a vida real.
        3. Formate a saída como um markdown limpo e fácil de ler, usando **títulos**.

        Detalhes do Usuário:
        - Livro: "${livro}"
        - Partes/Temas favoritos a destacar: "${partes}"
    `;

  try {
    // 2. Chamada à API (Usando o modelo Gemini)
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash", // Modelo rápido e eficiente para tarefas de texto
      contents: [{ role: "user", parts: [{ text: promptText }] }],
    });

    // 3. Extrair o texto do roteiro da resposta
    const roteiroGerado = response.text;

    // 4. Inserir e exibir o roteiro na tela
    roteiroContent.textContent = roteiroGerado;
    roteiroOutput.style.display = "block";
  } catch (error) {
    // Lidar com erros da API
    console.error("Erro ao gerar o roteiro com a Gemini API:", error);
    roteiroContent.textContent =
      "❌ Erro ao comunicar com a API. Verifique sua chave e a rede.";
    roteiroOutput.style.display = "block";
  } finally {
    // Ocultar feedback de carregamento, mesmo em caso de erro
    showLoading(false);
  }
}

/**
 * Função auxiliar para controlar o estado visual de carregamento. (Permanece igual)
 */
function showLoading(isLoading) {
  if (isLoading) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      Gerando...
    `;
    statusMessage.style.display = "block";
  } else {
    submitBtn.disabled = false;
    submitBtn.innerHTML = "Gerar Roteiro!";
    statusMessage.style.display = "none";
  }
}
