import streamlit as st
import requests
import json
import datetime

st.set_page_config(page_title="TOPOS URANOS", layout="wide")

# ---------- ESTILOS ----------
st.markdown("""
<style>
.msg-bubble { border-radius: 12px; padding: 10px; margin: 8px 0; border-left: 4px solid; background: #0a0a20; user-select: text; }
.msg-autor { font-family: monospace; font-size: 0.7em; opacity: 0.7; }
.status-bar { background: #0a0a20; border-radius: 8px; padding: 8px; margin-bottom: 10px; font-family: monospace; }
.agente-panel { background: #0a0a20; border-radius: 8px; padding: 8px; margin-bottom: 12px; border-left: 3px solid; }
.diag-error { color: #ff8888; font-size: 0.7em; }
.diag-ok { color: #88ff88; font-size: 0.7em; }
</style>
""", unsafe_allow_html=True)

# ---------- LECTURA DE SECRETS ----------
def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return None

# Diccionario con todas las claves (None si no existen)
CLAVES = {
    "GEMINI": get_secret("GEMINI_API_KEY"),
    "GROQ": get_secret("GROQ_API_KEY"),
    "OPENROUTER": get_secret("OPENROUTER_API_KEY"),
    "HF": get_secret("HF_API_KEY"),
    "DEEPSEEK": get_secret("DEEPSEEK_API_KEY"),
}

# Mostrar diagnóstico de claves en la sidebar (sin mostrar el valor)
st.sidebar.markdown("### 🔑 Estado de claves API")
for nombre, clave in CLAVES.items():
    estado = "✅" if clave else "❌"
    st.sidebar.markdown(f"{estado} {nombre}")

# ---------- FUNCIONES DE API (corregidas) ----------
def llamar_gemini(prompt, system_prompt):
    key = CLAVES["GEMINI"]
    if not key:
        return None, "❌ Clave Gemini no configurada"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": f"{system_prompt}\n\nUsuario: {prompt}"}]
        }],
        "generationConfig": {"maxOutputTokens": 1000, "temperature": 0.7}
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json()
            texto = data["candidates"][0]["content"]["parts"][0]["text"]
            return texto, None
        else:
            return None, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return None, str(e)

def llamar_groq(prompt, system_prompt):
    key = CLAVES["GROQ"]
    if not key:
        return None, "❌ Clave Groq no configurada"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"], None
        else:
            return None, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return None, str(e)

def llamar_openrouter(prompt, system_prompt):
    key = CLAVES["OPENROUTER"]
    if not key:
        return None, "❌ Clave OpenRouter no configurada"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": "mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"], None
        else:
            return None, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return None, str(e)

def llamar_huggingface(prompt, system_prompt):
    key = CLAVES["HF"]
    if not key:
        return None, "❌ Clave HuggingFace no configurada"
    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {key}"}
    full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{prompt}\n<|assistant|>\n"
    try:
        r = requests.post(url, headers=headers, json={"inputs": full_prompt, "parameters": {"max_new_tokens": 800}}, timeout=40)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", "").strip(), None
            return str(data), None
        else:
            return None, f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return None, str(e)

# Mapeo de agentes a funciones
AGENTES = {
    "AETHER (Gemini)": llamar_gemini,
    "VELOX (Groq)": llamar_groq,
    "CÓDEX (OpenRouter)": llamar_openrouter,
    "NEXUS (HuggingFace)": llamar_huggingface,
}

# ---------- ESTADO DE SESIÓN ----------
if "historial" not in st.session_state:
    st.session_state.historial = []
if "agente_activo" not in st.session_state:
    st.session_state.agente_activo = "AETHER (Gemini)"
if "ultimo_error" not in st.session_state:
    st.session_state.ultimo_error = None

# ---------- INTERFAZ ----------
st.markdown('<div style="text-align:center; font-size:2em;">⬡ TOPOS URANOS ⬡</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;">TERRA VIVE · TERRA SANA · TERRA ES</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3,1])
with col1:
    # Mostrar historial
    for msg in st.session_state.historial:
        color = "#ff8800" if msg["autor"] == "ORÁCULO" else "#00aaff"
        st.markdown(f"""
        <div class="msg-bubble" style="border-left-color:{color}">
            <div class="msg-autor">{msg["autor"]} · {msg["ts"]}</div>
            {msg["texto"]}
        </div>
        """, unsafe_allow_html=True)
    
    # Entrada de texto
    with st.form("chat_form"):
        texto = st.text_input("Mensaje", placeholder="Escribe tu mensaje...", label_visibility="collapsed")
        enviar = st.form_submit_button("⚡ ENVIAR")
    
    if enviar and texto:
        st.session_state.historial.append({
            "autor": "ORÁCULO",
            "texto": texto,
            "ts": datetime.datetime.now().strftime("%H:%M:%S")
        })
        agente_nombre = st.session_state.agente_activo
        func = AGENTES[agente_nombre]
        system_prompt = "Eres un asistente útil llamado Topos Uranos. Hablas español de forma poética pero clara. Ayudas a Juan Carlos Pérez."
        with st.spinner(f"Consultando a {agente_nombre}..."):
            respuesta, error = func(texto, system_prompt)
        if error:
            respuesta = f"⚠️ Error: {error}"
            st.session_state.ultimo_error = error
        else:
            st.session_state.ultimo_error = None
        st.session_state.historial.append({
            "autor": agente_nombre,
            "texto": respuesta,
            "ts": datetime.datetime.now().strftime("%H:%M:%S")
        })
        st.rerun()

with col2:
    st.markdown("### 🎛️ Panel de control")
    # Selector de agente
    agente_seleccionado = st.radio(
        "Agente activo",
        list(AGENTES.keys()),
        index=list(AGENTES.keys()).index(st.session_state.agente_activo)
    )
    if agente_seleccionado != st.session_state.agente_activo:
        st.session_state.agente_activo = agente_seleccionado
        st.rerun()
    
    # Mostrar diagnóstico del agente actual
    st.markdown("---")
    st.markdown("### 📡 Diagnóstico")
    clave_presente = CLAVES[agente_seleccionado.split()[0]] is not None
    if clave_presente:
        st.markdown('<span class="diag-ok">✅ Clave presente</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="diag-error">❌ Clave no configurada</span>', unsafe_allow_html=True)
    
    if st.session_state.ultimo_error:
        st.markdown(f'<span class="diag-error">⚠️ Último error: {st.session_state.ultimo_error[:100]}</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Limpiar chat"):
        st.session_state.historial = []
        st.rerun()
