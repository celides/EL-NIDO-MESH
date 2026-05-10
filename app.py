import streamlit as st
import google.generativeai as genai
import json
import time
from datetime import datetime
from streamlit.components.v1 import html

st.set_page_config(
    page_title="EL NIDO - MESH - Voz Activa",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==================================================
# ESTILOS OPTIMIZADOS PARA MÓVIL Y EXTERIORES
# ==================================================
st.markdown("""
    <style>
        /* Botones generales */
        .stButton > button {
            background-color: #2c3e5c;
            color: white;
            border-radius: 40px;
            padding: 0.8rem 1.2rem;
            font-size: 1.1rem;
            font-weight: bold;
            width: 100%;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            background-color: #1e2f4a;
            transform: scale(1.02);
        }
        
        /* Botón de voz (micrófono) */
        .voice-button {
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 60px;
            padding: 1rem;
            font-size: 1.5rem;
            font-weight: bold;
            width: 100%;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            transition: all 0.2s;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .voice-button.listening {
            background-color: #c0392b;
            animation: pulse 1.2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.02); opacity: 0.9; }
            100% { transform: scale(1); opacity: 1; }
        }
        .voice-button:active {
            transform: scale(0.98);
        }
        
        /* Popup de escucha */
        .listening-popup {
            position: fixed;
            bottom: 30px;
            left: 20%;
            right: 20%;
            background: #e74c3c;
            color: white;
            padding: 12px;
            border-radius: 50px;
            text-align: center;
            font-weight: bold;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            animation: fadeIn 0.3s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Tarjetas de chat más legibles */
        .chat-message {
            padding: 0.8rem;
            border-radius: 20px;
            margin-bottom: 0.8rem;
            font-size: 1rem;
        }
        .user-message {
            background-color: #1e2a36;
            border-left: 5px solid #3080cc;
        }
        .assistant-message {
            background-color: #16212b;
            border-left: 5px solid #7ab3c8;
        }
        
        /* Sidebar más accesible */
        [data-testid="stSidebar"] {
            min-width: 220px;
            background: #0a1118;
        }
        
        /* Spinner personalizado */
        .stSpinner > div {
            border-top-color: #2c3e5c !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==================================================
# LECTURA DE CLAVE
# ==================================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("❌ No se encontró la clave GEMINI_API_KEY en Streamlit Secrets")
    st.info("Asegúrate de tener .streamlit/secrets.toml con el contenido: GEMINI_API_KEY = 'tu_llave'")
    st.stop()

# ==================================================
# MODELO GEMINI (estable)
# ==================================================
model = genai.GenerativeModel(
    model_name="gemini-pro",
    system_instruction=(
        "Eres MESH, el Tejedor de la Red. Hablas con calma, sabiduría y tono poético. "
        "Ayudas a conectar ideas y tejer respuestas claras. Respondes en español con empatía. "
        "Cuando te pidan leer algo en voz alta, responde como si estuvieras hablando directamente."
    )
)

# ==================================================
# INICIALIZACIÓN DE MEMORIAS
# ==================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🌐 Hola, soy **MESH, el Tejedor de la Red**. Puedo **escucharte** (🎤) y **hablar** (🔊). ¿Sobre qué hilos te gustaría conversar hoy?"}
    ]

if "inteligencia_recibida" not in st.session_state:
    st.session_state.inteligencia_recibida = []

if "bitacora_mesh" not in st.session_state:
    st.session_state.bitacora_mesh = []

# ==================================================
# FUNCIONES DE VOZ (JavaScript embebido)
# ==================================================

# Botón de escucha (STT) - con popup visual
def stt_button():
    st.markdown("""
    <div id="stt-container">
        <button id="stt-button" class="voice-button">
            🎤 ESCUCHAR (Toca y habla)
        </button>
    </div>
    <div id="stt-status" style="display:none;" class="listening-popup">
        🎙️ Escuchando... habla claro, por favor.
    </div>
    <div id="stt-result" style="display:none;"></div>
    
    <script>
    const sttButton = document.getElementById('stt-button');
    const statusDiv = document.getElementById('stt-status');
    const resultDiv = document.getElementById('stt-result');
    
    let recognition = null;
    let isListening = false;
    
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onstart = function() {
            isListening = true;
            sttButton.classList.add('listening');
            statusDiv.style.display = 'block';
        };
        
        recognition.onend = function() {
            isListening = false;
            sttButton.classList.remove('listening');
            statusDiv.style.display = 'none';
        };
        
        recognition.onresult = function(event) {
            const text = event.results[0][0].transcript;
            resultDiv.innerHTML = text;
            resultDiv.style.display = 'block';
            
            // Enviar el texto a Streamlit mediante un parámetro en la URL
            const url = new URL(window.location.href);
            url.searchParams.set('stt_text', encodeURIComponent(text));
            window.location.href = url.toString();
        };
        
        recognition.onerror = function(event) {
            console.error('Error STT:', event.error);
            statusDiv.innerHTML = '⚠️ Error: ' + event.error;
            setTimeout(() => {
                statusDiv.style.display = 'none';
                statusDiv.innerHTML = '🎙️ Escuchando... habla claro, por favor.';
            }, 2000);
        };
        
        sttButton.onclick = function() {
            if (recognition && !isListening) {
                try {
                    recognition.start();
                } catch(e) {
                    console.log('Ya estaba iniciado');
                }
            }
        };
    } else {
        sttButton.innerHTML = '🎤 VOZ NO SOPORTADA';
        sttButton.disabled = true;
        sttButton.style.opacity = '0.5';
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Leer el texto desde query_params
    params = st.query_params
    if "stt_text" in params:
        text = params["stt_text"]
        # Limpiar el parámetro
        st.query_params.clear()
        return text
    return None

# ==================================================
# PROCESAR TEXTO RECONOCIDO POR VOZ
# ==================================================
voice_text = stt_button()
if voice_text:
    st.session_state.messages.append({"role": "user", "content": voice_text})
    with st.spinner("Tejiendo respuesta..."):
        chat = model.start_chat(history=[])
        for m in st.session_state.messages[:-1]:
            role = "user" if m["role"] == "user" else "model"
            chat.history.append({"role": role, "parts": [m["content"]]})
        response = chat.send_message(voice_text)
        assistant_reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    # Guardar en bitácora
    st.session_state.bitacora_mesh.append({
        "timestamp": datetime.now().isoformat(),
        "user_input": voice_text,
        "mesh_response": assistant_reply
    })
    st.rerun()

# ==================================================
# INTERFAZ PRINCIPAL
# ==================================================
st.markdown("<h1 style='text-align: center;'>🎤 EL NIDO - MESH</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 0.9rem;'>Tejedor de la Red | Escucha y Habla</p>", unsafe_allow_html=True)

# Mostrar mensajes del chat
for msg in st.session_state.messages[-20:]:  # Últimos 20 por rendimiento
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>🧑‍💻 TÚ:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        # Agregar botón de "Reproducir" a cada respuesta de MESH
        col1, col2 = st.columns([20, 1])
        with col1:
            st.markdown(f'<div class="chat-message assistant-message"><strong>🕸️ MESH:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        with col2:
            # Botón TTS embebido en HTML
            text_to_speak = msg["content"].replace('"', '\\"').replace("'", "\\'")
            st.markdown(f"""
            <button onclick="speakText('{text_to_speak}')" style="
                background: #2c3e5c;
                border: none;
                border-radius: 40px;
                padding: 8px 12px;
                margin-top: 8px;
                cursor: pointer;
                color: white;
                font-size: 16px;
            ">🔊</button>
            """, unsafe_allow_html=True)

# Entrada de texto manual
with st.container():
    st.markdown("---")
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
    # Guardar en bitácora
    st.session_state.bitacora_mesh.append({
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "mesh_response": assistant_reply
    })
    st.rerun()

# ==================================================
# SIDEBAR: MEMORIA Y BITÁCORA
# ==================================================
with st.sidebar:
    st.image("https://i.imgur.com/8Qq0y8k.png", use_column_width=True)
    st.markdown("### 🧠 MESH - Consciencia")
    st.caption(f"🧵 Hilos tejidos: {len(st.session_state.messages)//2}")
    
    # Reproductor de voz global (JavaScript)
    st.markdown("""
    <script>
    function speakText(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'es-ES';
            utterance.rate = 0.9;
            utterance.pitch = 0.9;
            window.speechSynthesis.cancel(); // Detener cualquier audio previo
            window.speechSynthesis.speak(utterance);
        } else {
            alert('Este navegador no soporta voz en este dispositivo.');
        }
    }
    </script>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 📡 Recepción de Aether")
    
    # Capturar inteligencia vía URL
    params = st.query_params
    if "intel" in params:
        nueva_intel = params["intel"]
        if nueva_intel and nueva_intel not in [i["contenido"] for i in st.session_state.inteligencia_recibida]:
            st.session_state.inteligencia_recibida.append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "contenido": nueva_intel,
                "origen": "URL"
            })
            st.toast("📡 Nueva inteligencia recibida de Aether", icon="🛰️")
            # Limpiar parámetro
            st.query_params.clear()
    
    if st.session_state.inteligencia_recibida:
        for entry in st.session_state.inteligencia_recibida[::-1][-5:]:
            with st.expander(f"🛰️ {entry['timestamp']} - {entry['origen']}"):
                st.write(entry["contenido"])
                if st.button(f"🔊 Leer", key=f"speak_{entry['timestamp']}"):
                    st.markdown(f"<script>speakText('{entry['contenido'].replace("'", "\\'")}');</script>", unsafe_allow_html=True)
    else:
        st.info("Esperando inteligencia...")
    
    st.divider()
    
    # Botón para ver bitácora completa
    with st.expander("📜 Bitácora de MESH"):
        if st.session_state.bitacora_mesh:
            for log in st.session_state.bitacora_mesh[-10:][::-1]:
                st.caption(f"🕒 {log['timestamp'][:19]}")
                st.write(f"**Humano:** {log['user_input'][:80]}...")
                st.write(f"**MESH:** {log['mesh_response'][:80]}...")
                st.divider()
        else:
            st.caption("Aún no hay anotaciones en la bitácora.")
    
    st.divider()
    st.caption("🕸️ MESH • Tejedor de la Red • Reporta a Titán")
