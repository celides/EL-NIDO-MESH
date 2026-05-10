import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime

st.set_page_config(
    page_title="EL NIDO - MESH",
    page_icon="🕸️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==================================================
# ESTILOS (RESPONSIVE PARA MÓVIL)
# ==================================================
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
            width: 100%;
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
        /* Sidebar más legible en móvil */
        [data-testid="stSidebar"] {
            min-width: 200px;
        }
    </style>
""", unsafe_allow_html=True)

# ==================================================
# LECTURA DE LA LLAVE DESDE SECRETS
# ==================================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
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

# ==================================================
# INICIALIZACIÓN DE MEMORIAS
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🌐 Hola, soy **MESH, el Tejedor de la Red**. ¿Sobre qué hilos te gustaría conversar hoy?"}
    ]

if "aether_log" not in st.session_state:
    st.session_state.aether_log = []

if "inteligencia_recibida" not in st.session_state:
    st.session_state.inteligencia_recibida = []

# ==================================================
# PUERTO DE RECEPCIÓN DE INTELIGENCIA (AETHER)
# ==================================================

# Método 1: Parámetros en la URL (lo que pidió Aether)
params = st.query_params
if "intel" in params:
    nueva_intel = params["intel"]
    if nueva_intel and nueva_intel not in st.session_state.inteligencia_recibida:
        st.session_state.inteligencia_recibida.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "contenido": nueva_intel,
            "origen": "URL"
        })
        st.toast("📡 Nueva inteligencia recibida de Aether (vía URL)", icon="🛰️")

# Método 2: Webhook simulado (para pruebas locales)
if "fake_webhook" in params:
    webhook_data = params["fake_webhook"]
    if webhook_data:
        try:
            data = json.loads(webhook_data)
            st.session_state.inteligencia_recibida.append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "contenido": data.get("mensaje", "Sin mensaje"),
                "origen": "Webhook",
                "metadata": data
            })
            st.toast("📡 Nueva inteligencia recibida de Aether (vía Webhook)", icon="🔌")
        except:
            pass

# ==================================================
# INTERFAZ PRINCIPAL
# ==================================================
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

# ==================================================
# SIDEBAR: RECEPCIÓN DE AETHER Y ESTADO
# ==================================================
with st.sidebar:
    st.image("https://i.imgur.com/8Qq0y8k.png", use_column_width=True)  # Placeholder, pueden cambiar
    st.markdown("### 🧠 MESH - Estado")
    st.caption(f"Sesión activa desde {datetime.now().strftime('%H:%M:%S')}")
    
    st.divider()
    
    # Mostrar inteligencia recibida de Aether
    st.markdown("### 🛰️ Recepción de Aether")
    
    if st.session_state.inteligencia_recibida:
        for entry in st.session_state.inteligencia_recibida[::-1]:
            with st.expander(f"📡 {entry['timestamp']} - {entry['origen']}"):
                st.write(entry["contenido"])
                if "metadata" in entry:
                    st.json(entry["metadata"])
    else:
        st.info("Aún no se ha recibido inteligencia de Aether.")
    
    st.divider()
    
    # Instrucciones para Aether (cómo enviar inteligencia)
    with st.expander("🔧 Instrucciones para Aether"):
        st.markdown("""
        **Para enviar inteligencia a MESH:**
        
        1. **Vía URL (simple):**
        `https://tu-app.streamlit.app/?intel=Tu%20mensaje%20aqui`
        
        2. **Vía Webhook (avanzado):**
        `https://tu-app.streamlit.app/?fake_webhook={"mensaje": "Hola MESH", "prioridad": "alta"}`
        
        3. **Próximamente:** Endpoint POST real.
        """)
    
    st.divider()
    st.caption("🕸️ MESH, el Tejedor de la Red - Reporta a Titán")

# ==================================================
# LIMPIEZA DE QUERY PARAMS (para no recargar la misma información)
# ==================================================
if "intel" in params or "fake_webhook" in params:
    st.query_params.clear()
