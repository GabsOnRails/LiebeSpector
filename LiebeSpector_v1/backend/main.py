import os
from typing import List, Dict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.adk.agents import Agent
from google.adk.tools import google_search
from googleapiclient.discovery import build
from pydantic import BaseModel

from call_agent import call_agent

# --- Configurações Iniciais ---
load_dotenv(dotenv_path='C:/Users/conta/OneDrive/Documents/GitHub/LiebeSpector/LiebeSpector_v1/backend/config/.env')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

app = FastAPI()

# --- Configuração do CORS ---
origins = ["null"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos de Dados ---
class GerarConteudoRequest(BaseModel):
    topico: str

class VideoResultado(BaseModel):
    titulo: str
    url: str

class GerarConteudoResponse(BaseModel):
    resultados_youtube: List[VideoResultado] = []
    revisao: str = ""
    conteudo_criado: str = ""

# --- Funções Auxiliares ---
def call_gemini_agent(agent: Agent, prompt: str):
    """Chama um agente Gemini com o prompt fornecido."""
    return call_agent(agent, prompt)

def build_youtube_client():
    """Cria e retorna um cliente da API do YouTube."""
    return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def fetch_youtube_videos(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Busca vídeos de livros no YouTube."""
    try:
        youtube = build_youtube_client()
        search_query = f"{query} livros"
        request = youtube.search().list(
            part='snippet',
            q=search_query,
            type='video',
            maxResults=max_results
        )
        response = request.execute()
        results = []
        for item in response.get('items', []):
            results.append({
                'titulo': item['snippet']['title'],
                'url': f'https://www.youtube.com/watch?v={item["id"]["videoId"]}',
            })
        return results
    except Exception as e:
        print(f"Erro ao buscar no YouTube: {e}")
        return []

def create_google_search_agent(topico: str) -> Agent:
    """Cria um agente para buscar informações literárias no Google."""
    instruction = f"""
    Você é um assistente de pesquisa para criação literária. Sua tarefa é usar a ferramenta de busca do google (google_search)
    para encontrar informações relevantes e inspiradoras sobre o tópico literário: "{topico}".

    Foque em encontrar:
    - Exemplos de obras literárias relacionadas ao tópico.
    - Discussões sobre estilos, técnicas narrativas ou elementos temáticos relevantes.
    - Análises ou interpretações de obras similares.
    - Informações sobre autores que abordaram temas parecidos.

    Tente encontrar até 5 resultados que possam enriquecer a criação de conteúdo literário sobre este tópico.
    Priorize informações que ofereçam insights criativos e contextuais.
    """
    return Agent(
        name="buscador_google",
        model="gemini-2.0-flash",
        instruction=instruction,
        description="Agente que busca informações relevantes para a criação literária no Google",
        tools=[google_search]
    )

def create_reviewer_agent(topico: str) -> Agent:
    """Cria um agente para revisar informações literárias."""
    instruction = f"""
    Você é um assistente de revisão para criação literária. Sua tarefa é revisar as informações coletadas do Google e do YouTube
    sobre o tópico literário: "{topico}".

    Foque em:
    - Verificar a relevância e a qualidade das informações.
    - Identificar possíveis erros ou inconsistências.
    - Sugerir melhorias ou adições que possam enriquecer o conteúdo.

    Tente fornecer uma análise crítica e construtiva das informações coletadas.
    """
    return Agent(
        name="revisor",
        model="gemini-2.0-flash",
        instruction=instruction,
        description="Agente que revisa informações coletadas do Google e do YouTube",
    )

def create_content_creator_agent(topico: str) -> Agent:
    """Cria um agente para gerar conteúdo literário."""
    instruction = f"""
    Você é a Clarice Lispector e está trabalhando como assistente de criação literária. Sua tarefa é usar as informações revisadas coletadas do Google e do YouTube
    sobre o tópico literário: "{topico}" para criar um roteiro original para um vídeo do youtube.

    Foque em:
    - Criar um resumo ou uma análise crítica do tópico.
    - Sugerir ideias para histórias, personagens ou temas inspirados nas informações coletadas.
    - Propor técnicas narrativas ou estilos que possam ser aplicados ao conteúdo.

    Tente fornecer uma criação literária rica e inspiradora, assim como seus contos, baseada nas informações revisadas.
    """
    return Agent(
        name="criador_conteudo",
        model="gemini-2.0-flash",
        instruction=instruction,
        description="Agente que cria conteúdo literário baseado em informações revisadas",
    )

# --- Rotas da API ---
@app.post("/gerar_conteudo", response_model=GerarConteudoResponse)
async def gerar_conteudo(request: GerarConteudoRequest):
    """Endpoint para gerar conteúdo literário baseado em um tópico."""
    try:
        topico = request.topico

        # Busca informações
        google_agent = create_google_search_agent(topico)
        google_results = call_gemini_agent(google_agent, f"Tópico literário: {topico}")
        youtube_results = fetch_youtube_videos(topico)

        # Revisa informações
        reviewer_agent = create_reviewer_agent(topico)
        review_input = f"Informações do Google: {google_results}/n/nInformações do YouTube: {youtube_results}/n/n"
        review = call_gemini_agent(reviewer_agent, review_input)

        # Cria conteúdo
        content_creator_agent = create_content_creator_agent(topico)
        content_input = f"Informações revisadas: {review}/n/n"
        created_content = call_gemini_agent(content_creator_agent, content_input)

        return {
            "resultados_youtube": youtube_results,
            "revisao": review,
            "conteudo_criado": created_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Inicialização do Servidor ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)