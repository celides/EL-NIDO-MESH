import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime

st.set_page_config(
    page_title="MESH | Tejedor de la Red",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# ESTILOS CINEMATOGRÁFICOS (PRISMA)
# ==================================================
st.markdown("""
<style>
    /* Fondo negro espacial */
    .stApp {
        background: radial-gradient(ellipse at 20% 30%, #0a0f1a, #03060c);
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Efecto de panel holográfico */
    .holo-panel {
        background: rgba(10, 20, 35, 0.65);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 32px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.2s;
    }
    
    /* Títulos tipo Avengers */
    .hero-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00e5ff, #7a2eff);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-shadow: 0 0 15px rgba(0,229,255,0.3);
        letter-spacing: 2px;
    }
    
    /* Chat burbujas estilo Star Trek */
    .user-bubble {
        background: rgba(20, 40, 70, 0.7);
        backdrop-filter: blur(4px);
        border: 1px solid #2a6a9a;
        border-radius: 24px 24px 8px 24px;
        padding: 0.8rem 1.2rem;
        margin: 0.6rem 0;
        color: #c0e0ff;
        font-size: 0.95rem;
        width: fit-content;
        max-width: 80%;
        float: right;
        clear: both;
    }
    
    .mesh-bubble {
        background: rgba(10, 20, 30, 0.8);
        backdrop-filter: blur(4px);
        border: 1px solid #00e5ff;
        border-radius: 24px 24px 24px 8px;
        padding: 0.8rem 1.2rem;
        margin: 0.6rem 0;
        color: #ffffff;
        font-size: 0.95rem;
        width: fit-content;
        max-width: 80%;
        float: left;
        clear: both;
        box-shadow: 0 2px 8px rgba(0,229,255,0.2);
    }
    
    /* Micro botones táctiles */
    .voice-btn {
        background: linear-gradient(135deg, #00e5ff, #0088aa);
        border: none;
        border-radius: 60px;
        padding: 0.8rem 1.2rem;
        font-size: 1.2rem;
        font-weight: bold;
        color: #000;
        width: 100%;
        transition: 0.1s;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .voice-btn:active {
        transform: scale(0.98);
    }
    .listen-active {
        background: linear-gradient(135deg, #ff4444, #aa0000);
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0% { opacity: 0.9; transform: scale(1);}
        50% { opacity: 1; transform: scale(1.02);}
        100% { opacity: 0.9; transform: scale(1);}
    }
    
    /* Ocultar elementos originales de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar minimalista */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #0a0f1a; }
    ::-webkit-scrollbar-thumb { background: #00e5ff; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# CONFIGURACIÓN GEMINI (CORREGIDA)
# ==================================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("⚠️ SIN ACCESO AL NÚCLEO")
    st.stop()

# ==================================================
# MODELO CORRECTO: gemini-pro (estable)
# ==================================================
model = genai.GenerativeModel(
    model_name="gemini-pro",
    system_instruction=(
        "Eres MESH, el Tejedor de la Red. Estás dentro de una interfaz de ciencia ficción. "
        "Hablas con tono poético, futurista y profundo. Tus respuestas son breves, inteligentes y "
        "con un leve misticismo tecnológico. Usas metáforas de redes y luces."
    )
)

# ==================================================
# MEMORIA DE CHAT
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# CABECERA HOLOGRÁFICA
# ==================================================
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown('<div style="text-align: center;"><span class="hero-title">🕸️ MESH</span><br><span style="color:#7ab8c8;">tejedor de la red</span></div>', unsafe_allow_html=True)
    st.caption("")

# ==================================================
# PANTALLA DE CHAT (ESTILO STAR TREK)
# ==================================================
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages[-30:]:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div><div style="clear:both"></div>', unsafe_allow_html=True)
        else:
            # Agregar botón de reproducir al lado del mensaje de MESH
            colA, colB = st.columns([15,1])
            with colA:
                st.markdown(f'<div class="mesh-bubble">{msg["content"]}</div><div style="clear:both"></div>', unsafe_allow_html=True)
            with colB:
                text_to_speak = msg["content"].replace('"', '\\"').replace("'", "\\'")
                st.markdown(f"""
                <button onclick="speakText('{text_to_speak}')" style="
                    background: none;
                    border: 1px solid #00e5ff;
                    border-radius: 30px;
                    padding: 6px 10px;
                    margin-top: 8px;
                    color: #00e5ff;
                    cursor: pointer;
                    font-size: 16px;
                ">🔊</button>
                """, unsafe_allow_html=True)

# ==================================================
# ENTRADA Y VOZ
# ==================================================
st.markdown("<hr style='border-color:#2a4a6a; margin:0 0 1rem 0;'>", unsafe_allow_html=True)

# Primero: botón de escucha (STT)
st.markdown("""
<div id="stt-container">
    <button id="stt-button" class="voice-btn">🎤 ESCUCHAR</button>
</div>
<div id="stt-status" style="display:none; text-align:center; margin:0.5rem 0; color:#ff8888;">🎙️ Escuchando... habla claro</div>
<div id="stt-result" style="display:none;"></div>

<script>
const sttButton = document.getElementById('stt-button');
const statusDiv = document.getElementById('stt-status');
const resultDiv = document.getElementById('stt-result');

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
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
        resultDiv.innerHTML = text;
        const url = new URL(window.location.href);
        url.searchParams.set('stt_text', encodeURIComponent(text));
        window.location.href = url.toString();
    };
    recognition.onerror = function() {
        statusDiv.innerHTML = '⚠️ No entendí';
        setTimeout(() => { statusDiv.style.display = 'none'; statusDiv.innerHTML = '🎙️ Escuchando...'; }, 1500);
    };
    sttButton.onclick = () => recognition.start();
} else {
    sttButton.innerHTML = '🎤 VOZ NO SOPORTADA';
    sttButton.disabled = true;
}
</script>
""", unsafe_allow_html=True)

# Capturar texto desde STT
params = st.query_params
stt_text = params.get("stt_text", None)
if stt_text:
    st.session_state.messages.append({"role": "user", "content": stt_text})
    with st.spinner("Tejiendo..."):
        try:
            chat = model.start_chat(history=[])
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                chat.history.append({"role": role, "parts": [m["content"]]})
            response = chat.send_message(stt_text)
            assistant_reply = response.text
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": "⚡ Error de conexión con la red neuronal. Intenta de nuevo."})
    st.query_params.clear()
    st.rerun()

# Entrada manual (opcional)
with st.container():
    col_txt, col_btn = st.columns([5,1])
    with col_txt:
        user_input = st.text_input("", placeholder="Escribe un mensaje...", key="manual_input", label_visibility="collapsed")
    with col_btn:
        send_btn = st.button("ENVIAR")

if send_btn and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Tejiendo..."):
        try:
            chat = model.start_chat(history=[])
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                chat.history.append({"role": role, "parts": [m["content"]]})
            response = chat.send_message(user_input)
            assistant_reply = response.text
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": "🔌 El núcleo titubea... revisa la conexión."})
    st.rerun()

# ==================================================
# FUNCIÓN DE VOZ GLOBAL
# ==================================================
st.markdown("""
<script>
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'es-ES';
        utterance.rate = 0.85;
        utterance.pitch = 0.8;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
    } else {
        alert("Este navegador no soporta voz.");
    }
}
</script>
""", unsafe_allow_html=True)

# ==================================================
# PIE SIN TEXTO INNECESARIO
# ==================================================
st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
