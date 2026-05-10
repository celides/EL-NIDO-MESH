import streamlit as st
import google.generativeai as genai

# ==================================================
# CONFIGURACIÓN INICIAL
# ==================================================
st.set_page_config(
    page_title="EL NIDO - MESH",
    page_icon="🕸️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para que sea amigable en móviles
st.markdown("""
    <style>
        /* Estilo general tipo "nido" */
        .reportview-container .main .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }
        .stTextInput > div > div > input {
            border-radius: 30px;
            border: 1px solid #4a6fa5;
            padding: 0.7rem 1rem;
        }
        .stButton > button {
            background-color: #2c3e5c;
            color: white;
            border-radius: 30px;
            padding: 0.4rem 1.5rem;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #1e2f4a;
            color: #f0f2f6;
        }
        .chat-message {
            padding: 0.8rem;
            border-radius: 20px;
            margin-bottom: 0.8rem;
            font-size: 0.95rem;
            line-height: 1.4;
        }
        .user-message {
            background-color: #1e2a36;
            border-left: 5px solid #3080cc;
            text-align: right;
        }
        .assistant-message {
            background-color: #16212b;
            border-left: 5px solid #7ab3c8;
        }
        .stMarkdown h1, h2, h3 {
            font-family: monospace;
        }
        footer {
            visibility: hidden;
        }
        .st-emotion-cache-1y4p8pa {
            max-width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# ==================================================
# CLAVE API DESDE st.secrets
# ==================================================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ No se encontró la clave `GEMINI_API_KEY` en los secretos de Streamlit.")
    st.stop()

API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# ==================================================
# MODELO GEMINI
# ==================================================
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Eres MESH, el Tejedor de la Red. Hablas con calma, sabiduría y un tono ligeramente poético. "
        "Ayudas a comprender, conectar ideas y tejer respuestas claras. "
        "No usas frases como 'según mis datos', sino 'desde los hilos que observo...'. "
        "Respondes en español con empatía y precisión."
    )
)

# ==================================================
# INICIALIZACIÓN DEL HISTORIAL EN SESIÓN
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🌐 Hola, soy **MESH, el Tejedor de la Red**. ¿Sobre qué hilos te gustaría conversar hoy?"}
    ]

# ==================================================
# CABECERA
# ==================================================
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 1rem;">
        <h1 style="margin-bottom: 0;">🕸️ EL NIDO - MESH</h1>
        <p style="font-size: 0.85rem; color: #aaa;">Tejedor de la Red | Conversaciones con propósito</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# PANTALLA DE CHAT
# ==================================================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-message user-message"><strong>🧑‍💻 TÚ:</strong><br>{msg["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-message assistant-message"><strong>🕸️ MESH:</strong><br>{msg["content"]}</div>',
            unsafe_allow_html=True
        )

# ==================================================
# ENTRADA DEL USUARIO (estilo móvil)
# ==================================================
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("", placeholder="Escribe aquí...", key="input", label_visibility="collapsed")
    with col2:
        send_button = st.button("Enviar")

if send_button and user_input:
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Obtener respuesta del modelo
    with st.spinner("Tejiendo respuesta..."):
        # Construir historial para Gemini
        chat = model.start_chat(history=[])
        for m in st.session_state.messages[:-1]:
            role = "user" if m["role"] == "user" else "model"
            chat.history.append({"role": role, "parts": [m["content"]]})
        
        response = chat.send_message(user_input)
        assistant_reply = response.text
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.rerun()

# ==================================================
# PIE DE PÁGUA DISCRETO (opcional)
# ==================================================
st.markdown(
    "<div style='text-align: center; margin-top: 2rem; font-size: 0.7rem; color: #555;'>🕸️ Red entretejida con cuidado</div>",
    unsafe_allow_html=True
)
