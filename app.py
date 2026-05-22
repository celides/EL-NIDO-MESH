# ============================================================
# TOPOS URANOS · CENTRO DE COMANDO
# app.py — Versión final con diagnóstico y toggles
# ============================================================

import streamlit as st
import requests
import json
import datetime
import time

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TOPOS URANOS · CENTRO DE COMANDO",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# ESTILOS CSS (resumidos por brevedad, pero incluyen todo lo necesario)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
html, body, [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #050510 0%, #0a0520 50%, #050510 100%) !important; color: #e0e0ff !important; font-family: 'Rajdhani', sans-serif !important; }
.titulo-principal { font-family: 'Orbitron', monospace; font-size: 2.2em; font-weight: 900; text-align: center; background: linear-gradient(90deg, #00aaff, #aa44ff, #ff44cc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2em; letter-spacing: 0.15em; }
.subtitulo { font-family: 'Rajdhani', sans-serif; font-size: 1em; text-align: center; color: #5566aa; letter-spacing: 0.3em; margin-bottom: 1.5em; }
.msg-bubble { border-radius: 12px; padding: 12px 16px; margin: 8px 0; font-family: 'Rajdhani', sans-serif; font-size: 1.05em; line-height: 1.6; border-left: 4px solid; background: rgba(10,10,32,0.8); user-select: text; }
.msg-titan { border-color: #00aaff; } .msg-aether { border-color: #aa44ff; } .msg-velox { border-color: #00ff88; } .msg-codex { border-color: #aaaaaa; } .msg-nexus { border-color: #ff44cc; } .msg-oraculo { border-color: #ff8800; }
.msg-autor { font-family: 'Orbitron', monospace; font-size: 0.7em; letter-spacing: 0.15em; opacity: 0.7; margin-bottom: 4px; }
.status-bar { background: rgba(10,10,32,0.9); border: 1px solid #1a1a40; border-radius: 8px; padding: 8px 16px; font-family: 'Orbitron', monospace; font-size: 0.75em; display: flex; gap: 20px; flex-wrap: wrap; }
.agente-panel { background: rgba(10,10,32,0.6); border-radius: 12px; padding: 8px 12px; margin-bottom: 12px; border-left: 3px solid; }
.agente-diagnostico { font-size: 0.7em; margin-top: 4px; color: #aa88ff; }
.diag-error { color: #ff8888; } .diag-ok { color: #88ff88; }
.recuerdo-item { background: rgba(20,10,40,0.7); border-left: 3px solid #aa44ff; border-radius: 6px; padding: 8px 12px; margin: 6px 0; }
.typing-indicator { font-family: 'Orbitron', monospace; font-size: 0.75em; color: #5566aa; animation: blink 1s infinite; }
@keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0.2; } }
div[data-testid="stButton"] > button { font-family: 'Orbitron', monospace !important; border-radius: 8px !important; background: rgba(10,10,32,0.9) !important; color: #aaaacc !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LECTURA DE SECRETOS
# ─────────────────────────────────────────────
def get_secret(key: str, default=None):
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return default

DEEPSEEK_API_KEY    = get_secret("DEEPSEEK_API_KEY")
GEMINI_API_KEY      = get_secret("GEMINI_API_KEY")
GROQ_API_KEY        = get_secret("GROQ_API_KEY")
OPENROUTER_API_KEY  = get_secret("OPENROUTER_API_KEY")
HF_API_KEY          = get_secret("HF_API_KEY")
SUPABASE_URL        = get_secret("SUPABASE_URL")
SUPABASE_KEY        = get_secret("SUPABASE_KEY")

MEMORIA_ACTIVA = SUPABASE_URL is not None and SUPABASE_KEY is not None

# Configuración de agentes
AGENTES = {
    "TITÁN":   {"clave": DEEPSEEK_API_KEY,   "activo_por_defecto": False, "color": "#00aaff", "emoji": "🔵"},
    "AETHER":  {"clave": GEMINI_API_KEY,     "activo_por_defecto": True,  "color": "#aa44ff", "emoji": "🟣"},
    "VELOX":   {"clave": GROQ_API_KEY,       "activo_por_defecto": True,  "color": "#00ff88", "emoji": "🟢"},
    "CÓDEX":   {"clave": OPENROUTER_API_KEY, "activo_por_defecto": True,  "color": "#aaaaaa", "emoji": "⚪"},
    "NEXUS":   {"clave": HF_API_KEY,         "activo_por_defecto": True,  "color": "#ff44cc", "emoji": "🩷"},
}

# ─────────────────────────────────────────────
# FUNCIONES DE SUPABASE (deben ir ANTES de usarlas)
# ─────────────────────────────────────────────
def guardar_recuerdo(contenido: str, metadatos: dict) -> bool:
    if not MEMORIA_ACTIVA:
        return False
    try:
        url = f"{SUPABASE_URL}/rest/v1/recuerdos"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "return=minimal"}
        payload = {"contenido": contenido, "metadatos": metadatos}
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        return r.status_code in (200, 201)
    except Exception:
        return False

def leer_recuerdos(limite: int = 10) -> list:
    if not MEMORIA_ACTIVA:
        return []
    try:
        url = f"{SUPABASE_URL}/rest/v1/recuerdos"
        headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
        params = {"order": "created_at.desc", "limit": limite}
        r = requests.get(url, headers=headers, params=params, timeout=10)
        return r.json() if r.status_code == 200 else []
    except Exception:
        return []

def recuerdos_como_contexto(n: int = 5) -> str:
    recs = st.session_state.get("recuerdos", [])
    if not recs:
        return ""
    lineas = []
    for r in recs[:n]:
        meta = r.get("metadatos", {})
        autor = meta.get("autor", "?")
        ts = r.get("created_at", "")[:16] if r.get("created_at") else ""
        lineas.append(f"[{ts}] {autor}: {r.get('contenido','')[:200]}")
    return "\n".join(lineas)

# ─────────────────────────────────────────────
# FUNCIONES DE LLAMADA A API (simplificadas pero funcionales)
# ─────────────────────────────────────────────
def llamar_gemini(mensajes, system_prompt):
    if not GEMINI_API_KEY:
        return "", "Clave API no configurada"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    contents = [{"role": "user", "parts": [{"text": f"[SISTEMA] {system_prompt}"}]}]
    for msg in mensajes:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    payload = {"contents": contents, "generationConfig": {"maxOutputTokens": 1500}}
    try:
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip(), None
        else:
            return "", f"Error {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return "", str(e)

def llamar_groq(mensajes, system_prompt):
    if not GROQ_API_KEY:
        return "", "Clave API no configurada"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    msgs = [{"role": "system", "content": system_prompt}] + mensajes
    payload = {"model": "llama-3.1-8b-instant", "messages": msgs, "max_tokens": 1500}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=25)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip(), None
        else:
            return "", f"Error {r.status_code}"
    except Exception as e:
        return "", str(e)

def llamar_openrouter(mensajes, system_prompt):
    if not OPENROUTER_API_KEY:
        return "", "Clave API no configurada"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    msgs = [{"role": "system", "content": system_prompt}] + mensajes
    payload = {"model": "mistral-7b-instruct:free", "messages": msgs, "max_tokens": 1500}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip(), None
        else:
            return "", f"Error {r.status_code}"
    except Exception as e:
        return "", str(e)

def llamar_huggingface(mensajes, system_prompt):
    if not HF_API_KEY:
        return "", "Clave API no configurada"
    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    prompt = f"<|system|>\n{system_prompt}\n<|user|>\n" + "\n".join([m["content"] for m in mensajes if m["role"]=="user"]) + "\n<|assistant|>\n"
    try:
        r = requests.post(url, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 800}}, timeout=40)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data)>0:
                return data[0].get("generated_text", "").strip(), None
            return str(data), None
        else:
            return "", f"Error {r.status_code}"
    except Exception as e:
        return "", str(e)

# DeepSeek opcional (lo dejamos pero empieza apagado)
def llamar_deepseek(mensajes, system_prompt):
    if not DEEPSEEK_API_KEY:
        return "", "Clave no configurada"
    # Implementación omitida por brevedad, similar a las demás
    return "", "DeepSeek no implementado en demo"

API_FUNCS = {
    "TITÁN": llamar_deepseek,
    "AETHER": llamar_gemini,
    "VELOX": llamar_groq,
    "CÓDEX": llamar_openrouter,
    "NEXUS": llamar_huggingface,
}

# ─────────────────────────────────────────────
# INICIALIZACIÓN DE ESTADO (después de las funciones)
# ─────────────────────────────────────────────
if "historial" not in st.session_state:
    st.session_state.historial = []
if "destinatario" not in st.session_state:
    st.session_state.destinatario = "AETHER"  # Cambiado a AETHER porque DeepSeek está apagado
if "recuerdos" not in st.session_state:
    st.session_state.recuerdos = leer_recuerdos(10) if MEMORIA_ACTIVA else []
if "estado_sistema" not in st.session_state:
    st.session_state.estado_sistema = "En espera"
if "ultima_respuesta_voz" not in st.session_state:
    st.session_state.ultima_respuesta_voz = ""
if "agentes_activos" not in st.session_state:
    st.session_state.agentes_activos = {nombre: cfg["activo_por_defecto"] for nombre, cfg in AGENTES.items()}
if "agentes_errores" not in st.session_state:
    st.session_state.agentes_errores = {nombre: None for nombre in AGENTES}

# ─────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ─────────────────────────────────────────────
def agregar_al_historial(autor, texto):
    st.session_state.historial.append({"autor": autor, "texto": texto, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")})

def historial_a_mensajes(historial):
    return [{"role": "user" if h["autor"]=="ORÁCULO" else "assistant", "content": h["texto"]} for h in historial]

def obtener_respuesta(pregunta, destinatario, historial, recuerdos_ctx):
    orden = []
    if st.session_state.agentes_activos.get(destinatario, False):
        orden.append(destinatario)
    for agente in ["AETHER","VELOX","CÓDEX","NEXUS","TITÁN"]:
        if agente != destinatario and st.session_state.agentes_activos.get(agente, False):
            orden.append(agente)
    msgs = historial_a_mensajes(historial)
    msgs.append({"role": "user", "content": pregunta})
    for agente in orden:
        if not AGENTES[agente]["clave"]:
            st.session_state.agentes_errores[agente] = "Clave API no configurada"
            continue
        sys_prompt = f"Eres {agente}, asistente del Monolito. Habla en español. {recuerdos_ctx}"
        respuesta, error = API_FUNCS[agente](msgs, sys_prompt)
        if error is None:
            st.session_state.agentes_errores[agente] = None
            return respuesta, agente
        else:
            st.session_state.agentes_errores[agente] = error
    errores = [f"{a}: {st.session_state.agentes_errores[a]}" for a in orden if st.session_state.agentes_errores.get(a)]
    return f"⚠️ No hay agentes disponibles.\nDiagnóstico:\n" + "\n".join(errores), "SISTEMA"

# ─────────────────────────────────────────────
# INTERFAZ PRINCIPAL
# ─────────────────────────────────────────────
st.markdown('<div class="titulo-principal">⬡ TOPOS URANOS · CENTRO DE COMANDO ⬡</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">TERRA VIVE · TERRA SANA · TERRA ES</div>', unsafe_allow_html=True)

# Barra de estado
dest_color = AGENTES.get(st.session_state.destinatario, {}).get("color", "#fff")
st.markdown(f"""
<div class="status-bar">
    <span>🟢 SISTEMA ACTIVO</span>
    <span>📡 DESTINATARIO: {st.session_state.destinatario}</span>
    <span>🧠 MEMORIA: {'ACTIVA' if MEMORIA_ACTIVA else 'OFFLINE'}</span>
</div>
""", unsafe_allow_html=True)

col_chat, col_ctrl = st.columns([3,1])
with col_ctrl:
    st.markdown("### 🎛️ PANEL DE AGENTES")
    for nombre, cfg in AGENTES.items():
        activo = st.session_state.agentes_activos[nombre]
        error = st.session_state.agentes_errores.get(nombre)
        estado = "🟢 Activo" if activo and not error else ("🔴 Fallo" if activo and error else "⚫ Apagado")
        st.markdown(f'<div class="agente-panel" style="border-left-color:{cfg["color"]}"><b>{cfg["emoji"]} {nombre}</b> {estado}</div>', unsafe_allow_html=True)
        nuevo = st.checkbox("Encendido", value=activo, key=f"toggle_{nombre}")
        if nuevo != activo:
            st.session_state.agentes_activos[nombre] = nuevo
            if nuevo:
                st.session_state.agentes_errores[nombre] = None
            st.rerun()
        if error:
            st.markdown(f'<div class="agente-diagnostico diag-error">⚠️ {error}</div>', unsafe_allow_html=True)
        elif activo:
            st.markdown('<div class="agente-diagnostico diag-ok">✅ Operativo</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button(f"📡 Seleccionar {nombre}", key=f"sel_{nombre}"):
            st.session_state.destinatario = nombre
            st.rerun()
    if st.button("🗑️ Limpiar chat"): st.session_state.historial = []; st.rerun()
    if st.button("🔄 Reiniciar"): st.session_state.clear(); st.rerun()

with col_chat:
    for msg in st.session_state.historial:
        cfg = AGENTES.get(msg["autor"], {"color":"#888","emoji":"●"})
        st.markdown(f'<div class="msg-bubble" style="border-left-color:{cfg["color"]}"><div class="msg-autor">{cfg["emoji"]} {msg["autor"]} · {msg["timestamp"]}</div>{msg["texto"]}</div>', unsafe_allow_html=True)
    with st.form("input_form"):
        texto = st.text_input("Mensaje", placeholder="Escribe...", label_visibility="collapsed")
        if st.form_submit_button("Enviar") and texto:
            agregar_al_historial("ORÁCULO", texto)
            ctx = recuerdos_como_contexto(5)
            resp, agente = obtener_respuesta(texto, st.session_state.destinatario, st.session_state.historial[:-1], ctx)
            agregar_al_historial(agente, resp)
            st.session_state.estado_sistema = f"Respondido por {agente}"
            st.rerun()
