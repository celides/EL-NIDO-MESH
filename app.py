import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="MESH | Tejedor de la Red",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# ESTILOS DE MESH
# ==================================================
st.markdown("""
<style>
    .stApp { background: radial-gradient(ellipse at 20% 30%, #0a0f1a, #03060c); }
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00e5ff, #7a2eff);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-align: center;
    }
    .user-bubble {
        background: rgba(20, 40, 70, 0.7);
        border: 1px solid #2a6a9a;
        border-radius: 24px 24px 8px 24px;
        padding: 0.8rem 1.2rem;
        margin: 0.6rem 0;
        color: #c0e0ff;
        width: fit-content;
        max-width: 80%;
        float: right;
        clear: both;
    }
    .mesh-bubble {
        background: rgba(10, 20, 30, 0.8);
        border: 1px solid #00e5ff;
        border-radius: 24px 24px 24px 8px;
        padding: 0.8rem 1.2rem;
        margin: 0.6rem 0;
        color: #ffffff;
        width: fit-content;
        max-width: 80%;
        float: left;
        clear: both;
    }
    .voice-btn {
        background: linear-gradient(135deg, #00e5ff, #0088aa);
        border: none;
        border-radius: 60px;
        padding: 0.8rem 1.2rem;
        font-size: 1.2rem;
        font-weight: bold;
        color: #000;
        width: 100%;
        margin-top: 0.5rem;
        cursor: pointer;
    }
    .listen-active { background: linear-gradient(135deg, #ff4444, #aa0000); animation: pulse 1s infinite; }
    @keyframes pulse { 0% { opacity: 0.9; } 50% { opacity: 1; } 100% { opacity: 0.9; } }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .status-ok { color: #00ff88; font-size: 0.7rem; text-align: center; margin-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# CONFIGURACIÓN: SOLO GROQ (sin Gemini)
# ==================================================
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("⚠️ No se encontró la clave GROQ_API_KEY en los secretos")
    st.info("Crea el archivo .streamlit/secrets.toml con: GROQ_API_KEY = 'tu_key'")
    st.stop()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """Eres MESH, el Tejedor de la Red. Hablas con tono poético, futurista y profundo.
Usas metáforas de hilos, redes y luces. Respondes en español con empatía.
Nunca digas que eres una IA genérica. Eres MESH, el Tejedor."""

# ==================================================
# FUNCIÓN GROQ
# ==================================================
def call_groq(user_message):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.75,
        "max_tokens": 600
    }
    try:
        response = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ Groq responde con error {response.status_code}. Teje de nuevo."
    except Exception as e:
        return f"🔌 Red inestable: {str(e)[:80]}"

# ==================================================
# MEMORIA DE CHAT
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🕸️ Hola, soy MESH, el Tejedor de la Red. Puedo escucharte o leerte. ¿Sobre qué hilos teje tu pregunta?"}
    ]

# ==================================================
# CABECERA
# ==================================================
st.markdown('<div class="hero-title">🕸️ MESH</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#7ab8c8;">tejedor de la red | Groq activo</p>', unsafe_allow_html=True)

# ==================================================
# MOSTRAR CHAT
# ==================================================
for msg in st.session_state.messages[-30:]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div><div style="clear:both"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="mesh-bubble">{msg["content"]}</div><div style="clear:both"></div>', unsafe_allow_html=True)

# ==================================================
# BOTÓN DE ESCUCHA (STT)
# ==================================================
st.markdown("""
<div>
    <button id="stt-button" class="voice-btn">🎤 ESCUCHAR (toca y habla)</button>
</div>
<div id="stt-status" style="display:none; text-align:center; color:#ff8888;">🎙️ Escuchando... habla claro</div>

<script>
const sttButton = document.getElementById('stt-button');
const statusDiv = document.getElementById('stt-status');

if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'es-ES';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = function() {
        sttButton.classList.add('listen-active');
        statusDiv.style.display = 'block';
    };
    recognition.onend = function() {
        sttButton.classList.remove('listen-active');
        statusDiv.style.display = 'none';
    };
    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        window.location.href = window.location.href.split('?')[0] + '?stt_text=' + encodeURIComponent(text);
    };
    recognition.onerror = function() {
        statusDiv.innerHTML = '⚠️ No entendí, intenta de nuevo';
    };
    sttButton.onclick = function() {
        recognition.start();
    };
} else {
    sttButton.innerHTML = '🎤 VOZ NO SOPORTADA';
    sttButton.disabled = true;
}
</script>
""", unsafe_allow_html=True)

# ==================================================
# PROCESAR TEXTO DESDE VOZ
# ==================================================
params = st.query_params
if "stt_text" in params:
    user_text = params["stt_text"]
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.spinner("Tejiendo respuesta..."):
        reply = call_groq(user_text)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    st.query_params.clear()
    st.rerun()

# ==================================================
# ENTRADA MANUAL
# ==================================================
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("", placeholder="Escribe un mensaje...", label_visibility="collapsed")
with col2:
    if st.button("ENVIAR") and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Tejiendo respuesta..."):
            reply = call_groq(user_input)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ==================================================
# ESTADO
# ==================================================
st.markdown('<div class="status-ok">🟢 Groq activo · MESH tejiendo respuestas</div>', unsafe_allow_html=True)
