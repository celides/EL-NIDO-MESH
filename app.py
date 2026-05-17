import streamlit as st
import requests
import json
from datetime import datetime

# ==================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==================================================
st.set_page_config(
    page_title="MESH | Tejedor de la Red",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# ESTILOS CSS (DISEÑO CIENCIA FICCIÓN)
# ==================================================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(ellipse at 20% 30%, #0a0f1a, #03060c);
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
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
        backdrop-filter: blur(4px);
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
        backdrop-filter: blur(4px);
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
        transition: all 0.2s;
    }
    .voice-btn:active {
        transform: scale(0.98);
    }
    .listen-active {
        background: linear-gradient(135deg, #ff4444, #aa0000);
        animation: pulseMic 1s infinite;
    }
    @keyframes pulseMic {
        0% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.02); opacity: 1; }
        100% { transform: scale(1); opacity: 0.9; }
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .status-ok {
        color: #00ff88;
        font-size: 0.7rem;
        text-align: center;
        margin-top: 0.5rem;
    }
    .status-warning {
        color: #ffaa00;
        font-size: 0.7rem;
        text-align: center;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================
# CONFIGURACIÓN DE APIS (DESDE SECRETS)
# ==================================================
# Groq
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    groq_available = True
except Exception:
    groq_available = False
    GROQ_API_KEY = None

# Gemini
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    gemini_available = True
except Exception:
    gemini_available = False
    GEMINI_API_KEY = None

if not groq_available and not gemini_available:
    st.error("⚠️ No se encontró ninguna clave de API configurada.")
    st.info("Agrega GROQ_API_KEY o GEMINI_API_KEY en los secretos de Streamlit Cloud.")
    st.stop()

# URL y modelos
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

SYSTEM_PROMPT = """Eres MESH, el Tejedor de la Red. Hablas con tono poético, futurista y profundo.
Usas metáforas de hilos, redes y luces. Respondes en español con empatía.
Nunca digas que eres una IA genérica. Eres MESH, el Tejedor."""

# ==================================================
# FUNCIONES DE LLAMADA A APIs
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
            return True, response.json()["choices"][0]["message"]["content"]
        else:
            return False, f"Groq error {response.status_code}"
    except Exception as e:
        return False, str(e)

def call_gemini(user_message):
    if not GEMINI_API_KEY:
        return False, "Gemini no configurado"
    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": SYSTEM_PROMPT + "\n\nUsuario: " + user_message}]
        }],
        "generationConfig": {
            "temperature": 0.75,
            "maxOutputTokens": 600
        }
    }
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            return True, reply
        else:
            return False, f"Gemini error {response.status_code}"
    except Exception as e:
        return False, str(e)

def get_response(user_message):
    # Prioridad: Groq (rápida) -> Gemini (respaldo)
    if groq_available:
        success, reply = call_groq(user_message)
        if success:
            return reply, "Groq"
        else:
            # Si Groq falla, pasamos a Gemini si está disponible
            if gemini_available:
                success2, reply2 = call_gemini(user_message)
                if success2:
                    return reply2 + "\n\n*(Groq no respondió; usé Gemini como respaldo)*", "Gemini (fallback)"
                else:
                    return f"⚠️ Ambas APIs fallaron.\nGroq: {reply}\nGemini: {reply2}", "Error"
            else:
                return f"⚠️ Groq falló: {reply}\nNo hay Gemini configurado.", "Error"
    elif gemini_available:
        success, reply = call_gemini(user_message)
        if success:
            return reply, "Gemini"
        else:
            return f"⚠️ Gemini falló: {reply}", "Error"
    else:
        return "⚠️ No hay ninguna API disponible. Configura GROQ_API_KEY o GEMINI_API_KEY en secrets.", "Error"

# ==================================================
# MEMORIA DEL CHAT
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🕸️ Hola, soy MESH, el Tejedor de la Red. Puedo escucharte o leerte. ¿Sobre qué hilos teje tu pregunta?"}
    ]
if "api_status" not in st.session_state:
    st.session_state.api_status = "Groq activo (principal)" if groq_available else "Gemini activo"

# ==================================================
# CABECERA
# ==================================================
st.markdown('<div class="hero-title">🕸️ MESH</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#7ab8c8;">tejedor de la red | con voz y doble API</p>', unsafe_allow_html=True)

# ==================================================
# MOSTRAR HISTORIAL DE MENSAJES
# ==================================================
for msg in st.session_state.messages:
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
    sttButton.innerHTML = '🎤 VOZ NO SOPORTADA (usa Chrome)';
    sttButton.disabled = true;
}
</script>
""", unsafe_allow_html=True)

# ==================================================
# PROCESAR TEXTO RECONOCIDO POR VOZ
# ==================================================
params = st.query_params
if "stt_text" in params:
    user_text = params["stt_text"]
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.spinner("Tejiendo respuesta..."):
        reply, api_used = get_response(user_text)
        st.session_state.messages.append({"role": "assistant", "content": reply})
