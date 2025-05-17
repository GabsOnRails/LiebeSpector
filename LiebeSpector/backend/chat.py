import streamlit as st
import requests
import json

# --- Configuração da Página ---
st.set_page_config(page_title="LiebeSpector", page_icon="📚")

# --- Título Centralizado ---
st.markdown("<h1 style='text-align: center;'>LiebeSpector</h1>", unsafe_allow_html=True)

# --- CSS Personalizado ---
st.markdown(
    """
    <style>
        .stChatMessage[data-streamlit=true][aria-label="Mensagem do usuário"] {
            background-color: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Inicialização do Histórico de Mensagens ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Olá! Digite um tópico literário para começarmos.", "avatar": "✍🏻"}]

# --- Exibição do Histórico de Mensagens ---
for message in st.session_state["messages"]:
    avatar = "💭" if message["role"] == "user" else message.get("avatar")
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"], unsafe_allow_html=True)

# --- Campo de Entrada do Usuário ---
prompt = st.chat_input("Digite seu tópico literário...")

# --- Lógica de Envio de Pergunta ---
if prompt:
    # Adiciona a pergunta do usuário ao histórico
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="💭"):
        st.markdown(prompt)

    # --- Requisição ao Backend FastAPI ---
    try:
        url = "http://localhost:8000/gerar_conteudo"
        headers = {"Content-Type": "application/json"}
        data = {"topico": prompt}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Lança uma exceção para erros HTTP
        conteudo = response.json()

        # --- Processamento da Resposta ---
        full_response = ""
        conteudo_para_baixar = ""

        if conteudo.get("resultados_youtube"):
            full_response += "<h2>Resultados do YouTube:</h2><ul>"
            for video in conteudo["resultados_youtube"]:
                full_response += f'<li><a href="{video["url"]}" target="_blank">{video["titulo"]}</a></li>'
            full_response += "</ul><br>"

        if conteudo.get("conteudo_criado"):
            full_response += f"<h2>Conteúdo Criado:</h2><pre>{conteudo['conteudo_criado']}</pre>"
            conteudo_para_baixar = conteudo['conteudo_criado']

        if not full_response:
            full_response = "Nenhum resultado encontrado."

        # Adiciona a resposta do backend ao histórico
        st.session_state["messages"].append({"role": "assistant", "content": full_response, "avatar": "✍🏻"})
        with st.chat_message("assistant", avatar="✍🏻"):
            st.markdown(full_response, unsafe_allow_html=True)

            # --- Botão de Download ---
            if conteudo_para_baixar:
                st.download_button(
                    label="Baixar Conteúdo",
                    data=conteudo_para_baixar.encode('utf-8'),
                    file_name=f"conteudo_{prompt.replace(' ', '_')}.txt",
                    mime="text/plain"
                )

    # --- Tratamento de Erros de Requisição ---
    except requests.exceptions.RequestException as e:
        error_message = f"Erro ao conectar com o backend: {e}"
        st.session_state["messages"].append({"role": "assistant", "content": error_message, "avatar": "✍🏻"})
        with st.chat_message("assistant", avatar="✍🏻"):
            st.error(error_message)
    # --- Tratamento de Erros de Decodificação JSON ---
    except json.JSONDecodeError as e:
        error_message = f"Erro ao decodificar a resposta do backend: {e}"
        st.session_state["messages"].append({"role": "assistant", "content": error_message, "avatar": "✍🏻"})
        with st.chat_message("assistant", avatar="✍🏻"):
            st.error(error_message)