import streamlit as st
import google.generativeai as genai

# Configuración visual para móvil
st.set_page_config(page_title="EL NIDO - MESH", page_icon="🛰️")

# Estilo personalizado
st.markdown("<style>.stChatMessage { background-color: #f0f2f6; border-radius: 10px; }</style>", unsafe_allow_html=True)

# --- REVISIÓN DE LLAVE (SISTEMA STREAMLIT) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = None

if not api_key:
    st.error("Error: Falta la llave API en los 'Secrets' de Streamlit.")
    st.info("Asegúrate de haber pegado: GEMINI_API_KEY = 'tu_llave' en Advanced Settings.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.title("🛰️ MESH")
    st.caption("Frecuencia del Nido Activa | AETHER Connection")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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
