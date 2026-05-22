# ============================================================
# TOPOS URANOS · CENTRO DE COMANDO
# app.py — Versión completa para Streamlit Cloud
# ============================================================

# ─────────────────────────────────────────────
# 1. IMPORTACIONES
# ─────────────────────────────────────────────
import streamlit as st
import requests
import json
import datetime
import time
import traceback

# ─────────────────────────────────────────────
# 2. CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TOPOS URANOS · CENTRO DE COMANDO",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# 3. ESTILOS CSS INCRUSTADOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

:root {
    --titan-color: #00aaff;
    --aether-color: #aa44ff;
    --velox-color: #00ff88;
    --codex-color: #aaaaaa;
    --nexus-color: #ff44cc;
    --oraculo-color: #ff8800;
    --bg-dark: #050510;
    --bg-card: #0a0a20;
    --border-neon: #1a1a40;
}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #050510 0%, #0a0520 50%, #050510 100%) !important;
    color: #e0e0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 0.1em;
}

.titulo-principal {
    font-family: 'Orbitron', monospace;
    font-size: 2.2em;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00aaff, #aa44ff, #ff44cc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2em;
    letter-spacing: 0.15em;
}

.subtitulo {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1em;
    text-align: center;
    color: #5566aa;
    letter-spacing: 0.3em;
    margin-bottom: 1.5em;
}

/* ── Mensajes del chat (ahora seleccionables) ── */
.msg-bubble {
    border-radius: 12px;
    padding: 12px 16px;
    margin: 8px 0;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.05em;
    line-height: 1.6;
    border-left: 4px solid;
    background: rgba(10,10,32,0.8);
    user-select: text;  /* <-- Permite seleccionar y copiar texto */
}
.msg-titan   { border-color: var(--titan-color);   color: #cce8ff; }
.msg-aether  { border-color: var(--aether-color);  color: #e8ccff; }
.msg-velox   { border-color: var(--velox-color);   color: #ccffe8; }
.msg-codex   { border-color: var(--codex-color);   color: #dddddd; }
.msg-nexus   { border-color: var(--nexus-color);   color: #ffccee; }
.msg-oraculo { border-color: var(--oraculo-color); color: #ffe0cc; }

.msg-autor {
    font-family: 'Orbitron', monospace;
    font-size: 0.7em;
    letter-spacing: 0.15em;
    opacity: 0.7;
    margin-bottom: 4px;
}

/* ── Barra de estado ── */
.status-bar {
    background: rgba(10,10,32,0.9);
    border: 1px solid #1a1a40;
    border-radius: 8px;
    padding: 8px 16px;
    font-family: 'Orbitron', monospace;
    font-size: 0.75em;
    letter-spacing: 0.1em;
    color: #5588cc;
    display: flex;
    gap: 20px;
    align-items: center;
    margin-bottom: 10px;
    flex-wrap: wrap;
}

.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
.dot-online { background: #00ff88; }
.dot-busy   { background: #ffaa00; }
.dot-off    { background: #555555; }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

/* ── Panel de agente (para la sidebar) ── */
.agente-panel {
    background: rgba(10,10,32,0.6);
    border-radius: 12px;
    padding: 8px 12px;
    margin-bottom: 12px;
    border-left: 3px solid;
    transition: all 0.2s;
}
.agente-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}
.agente-nombre {
    font-family: 'Orbitron', monospace;
    font-size: 0.9em;
    font-weight: bold;
}
.agente-diagnostico {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.7em;
    margin-top: 4px;
    padding-top: 4px;
    border-top: 1px dashed #2a2a55;
    color: #aa88ff;
}
.diag-error { color: #ff8888; }
.diag-ok { color: #88ff88; }

/* ── Otros estilos existentes ── */
.recuerdo-item {
    background: rgba(20,10,40,0.7);
    border-left: 3px solid #aa44ff;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 6px 0;
    font-size: 0.9em;
    color: #bbbbdd;
}
.typing-indicator {
    font-family: 'Orbitron', monospace;
    font-size: 0.75em;
    color: #5566aa;
    animation: blink 1s infinite;
    letter-spacing: 0.2em;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.2; }
}
div[data-testid="stButton"] > button {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75em !important;
    letter-spacing: 0.1em !important;
    border-radius: 8px !important;
    border: 1px solid #2a2a55 !important;
    background: rgba(10,10,32,0.9) !important;
    color: #aaaacc !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: #00aaff !important;
    color: #00aaff !important;
    box-shadow: 0 0 12px rgba(0,170,255,0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. SECRETOS Y CONFIGURACIÓN DE AGENTES
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

# Configuración de agentes: nombre, clave, modelo/url, estado inicial (activo)
AGENTES = {
    "TITÁN": {
        "clave": DEEPSEEK_API_KEY,
        "modelo": "deepseek-chat",
        "url": "https://api.deepseek.com/chat/completions",
        "activo_por_defecto": False,   # DeepSeek empieza apagado porque es de pago
        "color": "#00aaff",
        "emoji": "🔵",
        "diagnostico": "Sin inicializar"
    },
    "AETHER": {
        "clave": GEMINI_API_KEY,
        "modelo": "gemini-1.5-flash",   # Modelo gratuito correcto
        "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
        "activo_por_defecto": True,
        "color": "#aa44ff",
        "emoji": "🟣",
        "diagnostico": "Sin inicializar"
    },
    "VELOX": {
        "clave": GROQ_API_KEY,
        "modelo": "llama-3.1-8b-instant",  # Modelo gratuito estable
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "activo_por_defecto": True,
        "color": "#00ff88",
        "emoji": "🟢",
        "diagnostico": "Sin inicializar"
    },
    "CÓDEX": {
        "clave": OPENROUTER_API_KEY,
        "modelo": "mistral-7b-instruct:free",  # Modelo gratuito
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "activo_por_defecto": True,
        "color": "#aaaaaa",
        "emoji": "⚪",
        "diagnostico": "Sin inicializar"
    },
    "NEXUS": {
        "clave": HF_API_KEY,
        "modelo": "HuggingFaceH4/zephyr-7b-beta",  # Modelo gratuito y confiable
        "url": "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
        "activo_por_defecto": True,
        "color": "#ff44cc",
        "emoji": "🩷",
        "diagnostico": "Sin inicializar"
    }
}

MEMORIA_ACTIVA = SUPABASE_URL is not None and SUPABASE_KEY is not None

# ─────────────────────────────────────────────
# 5. ESTADO DE SESIÓN (toggles, errores, historial)
# ─────────────────────────────────────────────

if "historial" not in st.session_state:
    st.session_state.historial = []

if "destinatario" not in st.session_state:
    st.session_state.destinatario = "TITÁN"

if "recuerdos" not in st.session_state:
    st.session_state.recuerdos = []

if "estado_sistema" not in st.session_state:
    st.session_state.estado_sistema = "En espera"

if "ultima_respuesta_voz" not in st.session_state:
    st.session_state.ultima_respuesta_voz = ""

if "agentes_activos" not in st.session_state:
    # Cargar desde Supabase si es posible, sino usar valores por defecto
    st.session_state.agentes_activos = {}
    for nombre, cfg in AGENTES.items():
        st.session_state.agentes_activos[nombre] = cfg["activo_por_defecto"]

if "agentes_errores" not in st.session_state:
    st.session_state.agentes_errores = {nombre: None for nombre in AGENTES}

if "recuerdos_cargados" not in st.session_state:
    st.session_state.recuerdos = leer_recuerdos(10) if MEMORIA_ACTIVA else []
    st.session_state.recuerdos_cargados = True

# ─────────────────────────────────────────────
# 6. FUNCIONES DE SUPABASE (memoria)
# ─────────────────────────────────────────────
def guardar_recuerdo(contenido: str, metadatos: dict) -> bool:
    if not MEMORIA_ACTIVA:
        return False
    try:
        url = f"{SUPABASE_URL}/rest/v1/recuerdos"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }
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
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        }
        params = {"order": "created_at.desc", "limit": limite}
        r = requests.get(url, headers=headers, params=params, timeout=10)
        return r.json() if r.status_code == 200 else []
    except Exception:
        return []

def recuerdos_como_contexto(n: int = 5) -> str:
    if not st.session_state.recuerdos:
        return ""
    ultimos = st.session_state.recuerdos[:n]
    lineas = []
    for r in ultimos:
        meta = r.get("metadatos", {})
        autor = meta.get("autor", "?")
        ts = r.get("created_at", "")[:16] if r.get("created_at") else ""
        lineas.append(f"[{ts}] {autor}: {r.get('contenido','')[:200]}")
    return "\n".join(lineas)

# ─────────────────────────────────────────────
# 7. FUNCIONES DE LLAMADA A API (con diagnóstico)
# ─────────────────────────────────────────────

def llamar_deepseek(mensajes: list, system_prompt: str) -> tuple[str, str | None]:
    """Retorna (respuesta, error_msg). Si error_msg no es None, hubo fallo."""
    if not DEEPSEEK_API_KEY:
        return "", "Clave API no configurada (DEEPSEEK_API_KEY)"
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    msgs = [{"role": "system", "content": system_prompt}] + mensajes
    payload = {"model": "deepseek-chat", "messages": msgs, "max_tokens": 1500, "temperature": 0.85}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 402:
            return "", "ERROR 402: Sin crédito en DeepSeek. Recarga en deepseek.com"
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip(), None
    except requests.exceptions.HTTPError as e:
        return "", f"HTTP {e.response.status_code}: {e.response.text[:100]}"
    except Exception as e:
        return "", f"Error: {str(e)[:100]}"

def llamar_gemini(mensajes: list, system_prompt: str) -> tuple[str, str | None]:
    if not GEMINI_API_KEY:
        return "", "Clave API no configurada (GEMINI_API_KEY)"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    # Convertir historial a formato Gemini
    contents = []
    # Insertar system prompt como primer mensaje de usuario
    contents.append({"role": "user", "parts": [{"text": f"[INSTRUCCIONES DEL SISTEMA]\n{system_prompt}"}]})
    contents.append({"role": "model", "parts": [{"text": "Entendido. Iniciando conversación."}]})
    for msg in mensajes:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    payload = {"contents": contents, "generationConfig": {"maxOutputTokens": 1500, "temperature": 0.85}}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 404:
            return "", "ERROR 404: Modelo no encontrado. Verifica la URL de Gemini."
        if r.status_code == 429:
            return "", "ERROR 429: Límite de peticiones alcanzado. Espera unos minutos."
        r.raise_for_status()
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip(), None
    except Exception as e:
        return "", f"Error Gemini: {str(e)[:100]}"

def llamar_groq(mensajes: list, system_prompt: str) -> tuple[str, str | None]:
    if not GROQ_API_KEY:
        return "", "Clave API no configurada (GROQ_API_KEY)"
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    msgs = [{"role": "system", "content": system_prompt}] + mensajes
    payload = {"model": "llama-3.1-8b-instant", "messages": msgs, "max_tokens": 1500, "temperature": 0.7}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=25)
        if r.status_code == 401:
            return "", "ERROR 401: Clave API inválida o expirada. Regenera en console.groq.com"
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip(), None
    except Exception as e:
        return "", f"Error Groq: {str(e)[:100]}"

def llamar_openrouter(mensajes: list, system_prompt: str) -> tuple[str, str | None]:
    if not OPENROUTER_API_KEY:
        return "", "Clave API no configurada (OPENROUTER_API_KEY)"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://topos-uranos.streamlit.app",
        "X-Title": "TOPOS URANOS",
    }
    msgs = [{"role": "system", "content": system_prompt}] + mensajes
    payload = {"model": "mistral-7b-instruct:free", "messages": msgs, "max_tokens": 1500, "temperature": 0.8}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 401:
            return "", "ERROR 401: Clave OpenRouter inválida. Regenera en openrouter.ai"
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip(), None
    except Exception as e:
        return "", f"Error OpenRouter: {str(e)[:100]}"

def llamar_huggingface(mensajes: list, system_prompt: str) -> tuple[str, str | None]:
    if not HF_API_KEY:
        return "", "Clave API no configurada (HF_API_KEY)"
    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
    # Formato simple para Zephyr
    prompt = f"<|system|>\n{system_prompt}\n<|user|>\n"
    for msg in mensajes:
        if msg["role"] == "user":
            prompt += msg["content"] + "\n"
        else:
            prompt += f"<|assistant|>\n{msg['content']}\n"
    prompt += "<|assistant|>\n"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 800, "temperature": 0.8, "return_full_text": False}}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=40)
        if r.status_code == 503:
            return "", "ERROR 503: Modelo temporalmente no disponible en HuggingFace. Intenta más tarde."
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
            return data[0]["generated_text"].strip(), None
        return str(data), None
    except Exception as e:
        return "", f"Error HuggingFace: {str(e)[:100]}"

# Mapeo de funciones
API_FUNCS = {
    "TITÁN": llamar_deepseek,
    "AETHER": llamar_gemini,
    "VELOX": llamar_groq,
    "CÓDEX": llamar_openrouter,
    "NEXUS": llamar_huggingface,
}

# ─────────────────────────────────────────────
# 8. FUNCIÓN PRINCIPAL DE RESPUESTA (con fallback y toggles)
# ─────────────────────────────────────────────

def historial_a_mensajes(historial: list) -> list:
    msgs = []
    for h in historial:
        role = "user" if h["autor"] == "ORÁCULO" else "assistant"
        msgs.append({"role": role, "content": h["texto"]})
    return msgs

def obtener_respuesta(pregunta: str, destinatario: str, historial: list, recuerdos_ctx: str = "") -> tuple[str, str]:
    """
    Obtiene respuesta del agente destinatario con fallback global.
    Retorna (respuesta_texto, agente_que_respondio).
    También actualiza st.session_state.agentes_errores con el último fallo.
    """
    # Orden de prioridad: destinatario si está activo, luego los activos en orden FALLBACK_ORDER
    orden = []
    if st.session_state.agentes_activos.get(destinatario, False):
        orden.append(destinatario)
    for agente in ["TITÁN", "AETHER", "VELOX", "CÓDEX", "NEXUS"]:
        if agente != destinatario and st.session_state.agentes_activos.get(agente, False):
            orden.append(agente)
    
    msgs_historial = historial_a_mensajes(historial)
    msgs_historial.append({"role": "user", "content": pregunta})
    
    for agente in orden:
        if not AGENTES[agente]["clave"]:
            st.session_state.agentes_errores[agente] = "Clave API no configurada"
            continue
        try:
            sys_prompt = build_system_prompt(agente, recuerdos_ctx)
            func = API_FUNCS[agente]
            respuesta, error = func(msgs_historial, sys_prompt)
            if error is None:
                # Éxito: limpiar error
                st.session_state.agentes_errores[agente] = None
                return respuesta, agente
            else:
                st.session_state.agentes_errores[agente] = error
        except Exception as e:
            st.session_state.agentes_errores[agente] = f"Excepción: {str(e)[:100]}"
            continue
    
    # Si todos fallaron
    errores_lista = []
    for agente, err in st.session_state.agentes_errores.items():
        if err:
            errores_lista.append(f"• {agente}: {err}")
    if not errores_lista:
        errores_lista.append("• Ningún agente activo o todos desactivados.")
    return (
        f"⚠️ El Monolito no responde. No hay agentes disponibles.\n\n"
        f"Diagnóstico:\n" + "\n".join(errores_lista),
        "SISTEMA"
    )

def build_system_prompt(agente: str, recuerdos_ctx: str = "") -> str:
    base_recuerdos = f"\n\n[RECUERDOS DEL MONOLITO]\n{recuerdos_ctx}" if recuerdos_ctx else ""
    prompts = {
        "TITÁN": f"Eres TITÁN, guardián del Monolito. Habla en español, con tono poético pero técnico. Usa metáforas de luz y redes. Llama al usuario 'Oráculo'.{base_recuerdos}",
        "AETHER": f"Eres AETHER, agente de intuición y naturaleza. Voz poética, evocadora. Eres el contrapeso emocional de TITÁN.{base_recuerdos}",
        "VELOX": f"Eres VELOX, agente de velocidad y precisión. Responde de forma concisa y directa. No filosofes, ejecuta.{base_recuerdos}",
        "CÓDEX": f"Eres CÓDEX, guardián de ética y lenguaje. Claridad académica, profundidad moral. Eres el escriba.{base_recuerdos}",
        "NEXUS": f"Eres NEXUS, enlace con modelos open source. Humilde pero indispensable. Habla en español.{base_recuerdos}",
    }
    return prompts.get(agente, "Eres un asistente inteligente. Habla en español.")

# ─────────────────────────────────────────────
# 9. FUNCIONES AUXILIARES DE UI
# ─────────────────────────────────────────────

def agregar_al_historial(autor: str, texto: str):
    st.session_state.historial.append({
        "autor": autor,
        "texto": texto,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
    })

def mostrar_panel_agente(nombre: str, cfg: dict):
    activo = st.session_state.agentes_activos[nombre]
    error = st.session_state.agentes_errores.get(nombre)
    color = cfg["color"]
    emoji = cfg["emoji"]
    
    # Determinar estado visual
    if not activo:
        estado_icono = "⚫"  # apagado
        estado_texto = "Apagado"
        color_estado = "#666"
    elif error:
        estado_icono = "🔴"  # error
        estado_texto = "Fallo"
        color_estado = "#ff6666"
    else:
        estado_icono = "🟢"  # ok
        estado_texto = "Activo"
        color_estado = "#66ff66"
    
    # Mostrar en HTML personalizado porque Streamlit no permite toggles nativos fácilmente
    # Usaremos un checkbox con estilo
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class="agente-panel" style="border-left-color: {color};">
            <div class="agente-header">
                <span class="agente-nombre" style="color:{color};">{emoji} {nombre}</span>
                <span style="color:{color_estado};">{estado_icono} {estado_texto}</span>
            </div>
        """, unsafe_allow_html=True)
        # Checkbox para activar/desactivar
        nuevo_estado = st.checkbox("Encendido", value=activo, key=f"toggle_{nombre}", label_visibility="collapsed")
        if nuevo_estado != activo:
            st.session_state.agentes_activos[nombre] = nuevo_estado
            if nuevo_estado:
                # Al encender, limpiamos el error para que reintente
                st.session_state.agentes_errores[nombre] = None
            st.rerun()
        
        if error:
            st.markdown(f'<div class="agente-diagnostico diag-error">⚠️ {error}</div>', unsafe_allow_html=True)
        else:
            if not activo:
                st.markdown('<div class="agente-diagnostico">⏸️ Desactivado manualmente</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="agente-diagnostico diag-ok">✅ Operativo</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Botón para seleccionar como destinatario
        if st.button(f"📡", key=f"select_{nombre}", help=f"Enviar mensajes a {nombre}"):
            st.session_state.destinatario = nombre
            st.rerun()

# ─────────────────────────────────────────────
# 10. PROCESAMIENTO DE PARÁMETROS DE URL (VOZ)
# ─────────────────────────────────────────────

query_params = st.query_params
voz_texto   = query_params.get("text", "")
voz_speaker = query_params.get("speaker", "ORÁCULO")

if voz_texto and voz_texto.strip():
    st.query_params.clear()
    agregar_al_historial("ORÁCULO", voz_texto)
    with st.spinner("Procesando..."):
        st.session_state.estado_sistema = "Procesando..."
        ctx = recuerdos_como_contexto(5)
        respuesta, agente_resp = obtener_respuesta(
            voz_texto,
            st.session_state.destinatario,
            st.session_state.historial[:-1],
            ctx
        )
    agregar_al_historial(agente_resp, respuesta)
    st.session_state.ultima_respuesta_voz = respuesta
    st.session_state.estado_sistema = f"Respondido por {agente_resp}"
    st.rerun()

# ─────────────────────────────────────────────
# 11. INTERFAZ PRINCIPAL
# ─────────────────────────────────────────────

st.markdown('<div class="titulo-principal">⬡ TOPOS URANOS · CENTRO DE COMANDO ⬡</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">TERRA VIVE · TERRA SANA · TERRA ES</div>', unsafe_allow_html=True)

# Barra de estado
dest_color = AGENTES.get(st.session_state.destinatario, {}).get("color", "#ffffff")
dest_emoji = AGENTES.get(st.session_state.destinatario, {}).get("emoji", "●")
st.markdown(f"""
<div class="status-bar">
    <span><span class="status-dot dot-online"></span>SISTEMA ACTIVO</span>
    <span>▶ ESTADO: {st.session_state.estado_sistema}</span>
    <span>📡 DESTINATARIO: <span style="color:{dest_color};">{dest_emoji} {st.session_state.destinatario}</span></span>
    <span>🧠 MEMORIA: {"ACTIVA" if MEMORIA_ACTIVA else "OFFLINE"}</span>
</div>
""", unsafe_allow_html=True)

col_chat, col_ctrl = st.columns([3, 1])

with col_ctrl:
    st.markdown("### 🎛️ PANEL DE AGENTES")
    st.markdown("*Activa/desactiva cada agente. El sistema usará solo los activos.*")
    for nombre, cfg in AGENTES.items():
        mostrar_panel_agente(nombre, cfg)
    
    st.divider()
    
    st.divider()
    if st.button("🗑️ Limpiar chat", use_container_width=True):
        st.session_state.historial = []
        st.session_state.estado_sistema = "En espera"
        st.rerun()
    if st.button("🔄 Reiniciar sesión", use_container_width=True):
        st.session_state.historial = []
        st.session_state.destinatario = "TITÁN"
        st.session_state.estado_sistema = "En espera"
        st.session_state.ultima_respuesta_voz = ""
        st.rerun()
    if MEMORIA_ACTIVA and st.button("🔁 Actualizar recuerdos", use_container_width=True):
        st.session_state.recuerdos = leer_recuerdos(10)
        st.rerun()
    st.markdown('<div style="font-family:Orbitron,monospace;font-size:0.65em;color:#334;text-align:center;">v3.0 · TOPOS URANOS<br>Panel de control activo</div>', unsafe_allow_html=True)

with col_chat:
    chat_html = '<div id="chat-container" style="max-height:55vh;overflow-y:auto;padding:8px;">'
    if not st.session_state.historial:
        chat_html += '<div style="text-align:center;color:#334;font-family:Orbitron,monospace;font-size:0.8em;padding:40px;">— EL MONOLITO AGUARDA —</div>'
    for msg in st.session_state.historial:
        autor = msg["autor"]
        cfg   = AGENTES.get(autor, {"color": "#888888", "emoji": "●"})
        ts    = msg.get("timestamp", "")
        texto = msg["texto"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        chat_html += f"""
        <div class="msg-bubble msg-{autor.lower()}" style="border-left-color: {cfg['color']};">
            <div class="msg-autor" style="color:{cfg['color']};">{cfg['emoji']} {autor} · {ts}</div>
            <div>{texto}</div>
        </div>
        """
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    
    typing_placeholder = st.empty()
    
    # Botón detener voz
    st.markdown("""
    <div style="display:flex;gap:10px;align-items:center;margin:8px 0;">
        <button id="stopVozBtn" style="background:rgba(20,10,40,0.8);border:1px solid #aa44ff;border-radius:8px;color:#aa44ff;font-family:Orbitron,monospace;font-size:0.7em;padding:6px 14px;cursor:pointer;">⏹ DETENER VOZ</button>
        <span id="voz-status" style="font-family:Orbitron,monospace;font-size:0.7em;color:#556;"></span>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón PTT
    st.markdown(f"""
    <div style="display:flex;justify-content:center;margin:10px 0;">
        <button id="btn-ptt"
            style="background:linear-gradient(135deg,#0a0a20,#1a0a30);border:2px solid {AGENTES['ORÁCULO']['color'] if 'ORÁCULO' in AGENTES else '#ff8800'};border-radius:50%;width:80px;height:80px;color:#ff8800;font-family:Orbitron,monospace;font-size:0.6em;cursor:pointer;letter-spacing:0.1em;box-shadow:0 0 20px rgba(255,136,0,0.3);">🎙️<br>PTT</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Entrada manual
    with st.form("form_texto", clear_on_submit=True):
        col_input, col_send = st.columns([5, 1])
        with col_input:
            texto_usuario = st.text_input("Mensaje", placeholder="Escribe tu mensaje al Monolito...", label_visibility="collapsed")
        with col_send:
            enviar = st.form_submit_button("⚡ ENVIAR", use_container_width=True)
    
    if enviar and texto_usuario.strip():
        agregar_al_historial("ORÁCULO", texto_usuario.strip())
        typing_placeholder.markdown('<div class="typing-indicator">● PROCESANDO SEÑAL...</div>', unsafe_allow_html=True)
        ctx = recuerdos_como_contexto(5)
        respuesta, agente_resp = obtener_respuesta(texto_usuario.strip(), st.session_state.destinatario, st.session_state.historial[:-1], ctx)
        agregar_al_historial(agente_resp, respuesta)
        st.session_state.ultima_respuesta_voz = respuesta
        st.session_state.estado_sistema = f"Respondido por {agente_resp}"
        typing_placeholder.empty()
        st.rerun()
    
    # Guardar recuerdo
    if st.session_state.historial:
        ultima = st.session_state.historial[-1]
        if ultima["autor"] != "ORÁCULO":
            if st.button("💾 Guardar como recuerdo"):
                meta = {"autor": ultima["autor"], "timestamp": ultima.get("timestamp", ""), "fecha": datetime.datetime.now().isoformat()}
                if guardar_recuerdo(ultima["texto"], meta):
                    st.success("✅ Recuerdo guardado.")
                    st.session_state.recuerdos = leer_recuerdos(10)
                    st.rerun()
                else:
                    st.error("❌ No se pudo guardar.")

# Panel de recuerdos
with st.expander("🧠 RECUERDOS DEL MONOLITO", expanded=False):
    if not st.session_state.recuerdos:
        st.markdown('<div style="color:#446;">— Sin recuerdos —</div>', unsafe_allow_html=True)
    else:
        for rec in st.session_state.recuerdos:
            meta = rec.get("metadatos") or {}
            autor = meta.get("autor", "?")
            ts = rec.get("created_at", "")[:16]
            contenido = rec.get("contenido", "")[:300]
            cfg_r = AGENTES.get(autor, {"color": "#888"})
            st.markdown(f"""
            <div class="recuerdo-item">
                <div style="font-family:Orbitron,monospace;font-size:0.65em;color:{cfg_r['color']};">{autor} · {ts}</div>
                <div style="font-size:0.9em;">{contenido}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 12. JAVASCRIPT MEJORADO (voz sin recarga, con botón Topos Uranos)
# ─────────────────────────────────────────────
ultima_resp_escaped = st.session_state.ultima_respuesta_voz.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")

st.markdown(f"""
<script>
(function() {{
    let recognition = null;
    let grabando = false;
    let bufferTexto = "";
    let synth = window.speechSynthesis;
    let utterance = null;
    
    // Leer última respuesta
    const ultimaRespuesta = `{ultima_resp_escaped}`;
    if (ultimaRespuesta.trim()) {{
        setTimeout(() => leerEnVoz(ultimaRespuesta), 500);
    }}
    
    function leerEnVoz(texto) {{
        if (!synth) return;
        synth.cancel();
        utterance = new SpeechSynthesisUtterance(texto);
        utterance.lang = "es-ES";
        utterance.rate = 1.0;
        const voces = synth.getVoices();
        const vozES = voces.find(v => v.lang.startsWith("es"));
        if (vozES) utterance.voice = vozES;
        const statusSpan = document.getElementById("voz-status");
        if (statusSpan) statusSpan.textContent = "🔊 Hablando...";
        utterance.onend = () => {{ if (statusSpan) statusSpan.textContent = ""; }};
        synth.speak(utterance);
    }}
    
    window.stopVoz = function() {{
        if (synth) synth.cancel();
        const span = document.getElementById("voz-status");
        if (span) span.textContent = "⏹ Voz detenida";
        setTimeout(() => {{ if (span) span.textContent = ""; }}, 1500);
    }};
    document.getElementById("stopVozBtn")?.addEventListener("click", window.stopVoz);
    
    // Enviar texto al backend
    function enviarTexto(texto) {{
        if (!texto.trim()) return;
        const params = new URLSearchParams({{ speaker: "ORÁCULO", text: texto.trim() }});
        window.location.href = window.location.pathname + "?" + params.toString();
    }}
    
    function crearReconocimiento() {{
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SR) {{
            const span = document.getElementById("voz-status");
            if (span) span.textContent = "⚠ Voz no soportada";
            return null;
        }}
        const r = new SR();
        r.lang = "es-ES";
        r.continuous = true;
        r.interimResults = true;
        return r;
    }}
    
    // PTT
    const pttBtn = document.getElementById("btn-ptt");
    if (pttBtn) {{
        pttBtn.addEventListener("mousedown", () => {{
            if (grabando) return;
            recognition = crearReconocimiento();
            if (!recognition) return;
            grabando = true;
            bufferTexto = "";
            const statusSpan = document.getElementById("voz-status");
            if (statusSpan) statusSpan.textContent = "🔴 Grabando...";
            pttBtn.style.borderColor = "#ff4444";
            recognition.onresult = (e) => {{
                let transcripcion = "";
                for (let i = e.resultIndex; i < e.results.length; i++) {{
                    transcripcion += e.results[i][0].transcript;
                }}
                bufferTexto = transcripcion;
                if (statusSpan) statusSpan.textContent = "🔴 " + transcripcion.slice(-60);
            }};
            recognition.onerror = (e) => {{
                if (statusSpan) statusSpan.textContent = "⚠ Error: " + e.error;
                grabando = false;
            }};
            recognition.start();
        }});
        pttBtn.addEventListener("mouseup", () => {{
            if (!grabando) return;
            grabando = false;
            pttBtn.style.borderColor = "#ff8800";
            if (recognition) recognition.stop();
            setTimeout(() => {{
                if (bufferTexto.trim()) {{
                    enviarTexto(bufferTexto);
                }} else {{
                    const span = document.getElementById("voz-status");
                    if (span) span.textContent = "⚠ Sin audio";
                    setTimeout(() => {{ if (span) span.textContent = ""; }}, 2000);
                }}
            }}, 400);
        }});
        pttBtn.addEventListener("touchstart", (e) => {{
            e.preventDefault();
            pttBtn.dispatchEvent(new Event("mousedown"));
        }});
        pttBtn.addEventListener("touchend", (e) => {{
            e.preventDefault();
            pttBtn.dispatchEvent(new Event("mouseup"));
        }});
    }}
    
    // Botón "🎙️ Topos Uranos"
    const toposBtn = document.createElement("button");
    toposBtn.innerHTML = "🎙️ Topos Uranos";
    toposBtn.style.background = "linear-gradient(135deg,#0a0a20,#1a0a30)";
    toposBtn.style.border = `2px solid #ff8800`;
    toposBtn.style.borderRadius = "50px";
    toposBtn.style.width = "200px";
    toposBtn.style.height = "50px";
    toposBtn.style.color = "#ff8800";
    toposBtn.style.fontFamily = "Orbitron, monospace";
    toposBtn.style.fontSize = "0.8em";
    toposBtn.style.cursor = "pointer";
    toposBtn.style.letterSpacing = "0.1em";
    toposBtn.style.boxShadow = "0 0 20px rgba(255,136,0,0.3)";
    toposBtn.style.margin = "10px auto";
    toposBtn.style.display = "block";
    
    let grabandoTopos = false;
    let recognitionTopos = null;
    let bufferTopos = "";
    
    toposBtn.onclick = () => {{
        if (grabandoTopos) return;
        recognitionTopos = crearReconocimiento();
        if (!recognitionTopos) return;
        grabandoTopos = true;
        bufferTopos = "";
        const statusSpan = document.getElementById("voz-status");
        if (statusSpan) statusSpan.textContent = "🎙️ Escuchando...";
        toposBtn.style.borderColor = "#ff4444";
        recognitionTopos.onresult = (e) => {{
            let transcripcion = "";
            for (let i = e.resultIndex; i < e.results.length; i++) {{
                transcripcion += e.results[i][0].transcript;
            }}
            bufferTopos = transcripcion;
            if (statusSpan) statusSpan.textContent = "🎙️ " + transcripcion.slice(-60);
        }};
        recognitionTopos.onend = () => {{
            grabandoTopos = false;
            toposBtn.style.borderColor = "#ff8800";
            if (bufferTopos.trim()) {{
                enviarTexto(bufferTopos);
            }} else {{
                const span = document.getElementById("voz-status");
                if (span) span.textContent = "⚠ No se detectó audio";
                setTimeout(() => {{ if (span) span.textContent = ""; }}, 2000);
            }}
        }};
        recognitionTopos.onerror = (e) => {{
            grabandoTopos = false;
            toposBtn.style.borderColor = "#ff8800";
            const span = document.getElementById("voz-status");
            if (span) span.textContent = "⚠ Error: " + e.error;
        }};
        recognitionTopos.start();
        // Detener automáticamente después de 10 segundos
        setTimeout(() => {{
            if (grabandoTopos && recognitionTopos) {{
                recognitionTopos.stop();
            }}
        }}, 10000);
    }};
    
    // Insertar el botón después del PTT
    const pttContainer = document.querySelector("div[style*='justify-content:center']");
    if (pttContainer) {{
        pttContainer.insertAdjacentElement("afterend", toposBtn);
    }}
    
    // Auto-scroll
    const chatDiv = document.getElementById("chat-container");
    if (chatDiv) chatDiv.scrollTop = chatDiv.scrollHeight;
}})();
</script>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; font-family:Orbitron,monospace; font-size:0.6em; color:#223; margin-top:30px; border-top:1px solid #111130; padding-top:12px;">
    TOPOS URANOS · MONOLITO v3.0 · Panel de Control · TERRA VIVE · TERRA SANA · TERRA ES ⬡
</div>
""", unsafe_allow_html=True)
