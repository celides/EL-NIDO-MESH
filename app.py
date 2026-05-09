import streamlit as st
import google.generativeai as genai
import os

# Configuración visual para móvil
st.set_page_config(page_title="EL NIDO - MESH", page_icon="🛰️")

# Estilo personalizado para mejorar la visibilidad en celular
st.markdown("""
    <style>
    .stChatMessage { background-color: #f0f2f6; border-radius: 10px; padding: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Recuperar la llave API desde las variables de entorno de Vercel
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Error: No se encontró la configuración 'GEMINI_API_KEY'.")
else:
    genai.configure(api_key=api_key)
    # Usamos el modelo flash para mayor velocidad en móvil
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.title("🛰️ MESH")
    st.caption("Frecuencia del Nido Activa | AETHER Connection")

    # Inicializar historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensajes previos
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto para el Oracle
    if prompt := st.chat_input("Escribe tu frecuencia..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")
