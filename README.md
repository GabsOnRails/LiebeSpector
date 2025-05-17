✨📚 **LiebeSpector: Seu Assistente Literário com Alma de Clarice** ✍️💭

Mergulhe no universo da literatura com LiebeSpector, uma ferramenta inovadora que combina a busca inteligente com a sensibilidade da escrita de Clarice Lispector. Explore tópicos literários, descubra obras inspiradoras e deixe a magia das palavras fluir\!

**🌟 O Que é LiebeSpector?**

LiebeSpector é um projeto encantador que atua como seu assistente literário pessoal. Ao inserir um tópico de seu interesse, LiebeSpector vasculha a web em busca de informações relevantes, incluindo resultados do YouTube e insights do Google. Em seguida, com uma pitada da profundidade e estilo característicos de Clarice Lispector, ele gera um conteúdo original para inspirar sua jornada literária.

**🚀 Funcionalidades Incríveis:**

* 🔍 **Busca Inteligente:** Encontra rapidamente informações relevantes sobre seus tópicos literários favoritos na web.
* 📺 **Vídeos Inspiradores:** Descubra análises, discussões e conteúdos relacionados no YouTube.
* 💡 **Conteúdo Criativo:** Receba textos originais com a essência da escrita introspectiva e envolvente de Clarice Lispector.
* 💾 **Opção de Download:** Salve o conteúdo gerado para revisitar suas ideias a qualquer momento.
* 🎨 **Interface Charmosa:** Uma experiência de usuário intuitiva e visualmente agradável com Streamlit.


**🛠️ Como Usar?**

1.  **Clone o Repositório:**
    ```bash
    git clone <link_do_seu_repositório>
    cd LiebeSpector
    ```
2.  **Configure as Variáveis de Ambiente:**
    * Crie um diretório `backend/config`.
    * Dentro, crie um arquivo `.env` e adicione suas chaves de API do Google e do YouTube:
        ```
        GOOGLE_API_KEY=SUA_CHAVE_AQUI
        YOUTUBE_API_KEY=SUA_CHAVE_AQUI
        ```
    * Certifique-se de ajustar o caminho no arquivo `main.py` se necessário.
3.  **Instale as Dependências:**
    No diretório raiz do projeto, execute:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o Backend FastAPI:**
    Navegue até o diretório `backend` e execute:
    ```bash
    uvicorn main:app --reload
    ```
5.  **Execute a Interface Streamlit:**
    No diretório raiz do projeto, execute:
    ```bash
    streamlit run app.py
    ```
6.  **Explore e Crie\!** Abra o link que o Streamlit fornecerá no seu navegador e comece a digitar seus tópicos literários.

**⚙️ Tecnologias Utilizadas:**

* 🐍 **Python:** A linguagem de programação principal.
* 🚀 **FastAPI:** Para construir o backend da API de forma rápida e eficiente.
* 🕸️ **Streamlit:** Para criar uma interface de usuário interativa e amigável.
* 🔑 **Google API Client:** Para interagir com a API de Busca do Google.
* ▶️ **YouTube Data API:** Para buscar informações e vídeos relevantes do YouTube.
* 🗣️ **Google AI Python SDK (Gemini):** Para geração de conteúdo com modelos de linguagem avançados.
* 📦 **Pydantic:** Para validação de dados.
* 🌳 **python-dotenv:** Para gerenciar variáveis de ambiente.

## Demonstração em Vídeo

Para ver o LiebeSpector em ação, assista ao vídeo abaixo:

https://www.youtube.com/embed/fKc1hdL0qJE
