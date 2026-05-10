import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="EL NIDO - MESH",
    page_icon="🕸️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS
st.markdown("""
    <style>
        .stTextInput > div > div > input {
            border-radius: 30px;
            padding: 0.7rem 1rem;
        }
        .stButton > button {
            background-color: #2c3e5c;
            color: white;
            border-radius: 30px;
        }
        .chat-message {
            padding: 0.8rem;
            border-radius: 20px;
            margin-bottom: 0.8rem;
        }
        .user-message {
            background-color: #1e2a36;
            border-left: 5px solid #3080cc;
        }
        .assistant-message {
            background-color: #16212b;
            border-left: 5px solid #7ab3c8;
        }
    </style>
""", unsafe_allow_html=True)

# ==================================================
# LECTURA DE LA LLAVE DESDE SECRETS
# ==================================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("❌ No se encontró la clave GEMINI_API_KEY en los secretos de Streamlit.")
    st.info("Asegúrate de tener la carpeta .streamlit/ con el archivo secrets.toml")
    st.stop()

# ==================================================
# CONFIGURACIÓN DEL MODELO (MESH)
# ==================================================
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Eres MESH, el Tejedor de la Red. Hablas con calma, sabiduría y un tono poético. "
        "Ayudas a conectar ideas y tejer respuestas claras. Respondes en español con empatía."
    )
)

# Inicializar historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🌐 Hola, soy **MESH, el Tejedor de la Red**. ¿Sobre qué hilos te gustaría conversar hoy?"}
    ]

# Cabecera
st.markdown("<h1 style='text-align: center;'>🕸️ EL NIDO - MESH</h1>", unsafe_allow_html=True)

# Mostrar mensajes del chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>🧑‍💻 TÚ:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-message"><strong>🕸️ MESH:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

# Entrada de texto
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("", placeholder="Escribe aquí...", key="input", label_visibility="collapsed")
    with col2:
        send_button = st.button("Enviar")

# Procesar mensaje
if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Tejiendo respuesta..."):
        chat = model.start_chat(history=[])
        for m in st.session_state.messages[:-1]:
            role = "user" if m["role"] == "user" else "model"
            chat.history.append({"role": role, "parts": [m["content"]]})
        response = chat.send_message(user_input)
        assistant_reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.rerun()
