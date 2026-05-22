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
    text-shadow: none;
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

/* ── Mensajes del chat ── */
.msg-bubble {
    border-radius: 12px;
    padding: 12px 16px;
    margin: 8px 0;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.05em;
    line-height: 1.6;
    border-left: 4px solid;
    background: rgba(10,10,32,0.8);
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

/* ── Indicador de destinatario ── */
.destinatario-badge {
    font-family: 'Orbitron', monospace;
    font-size: 0.8em;
    letter-spacing: 0.15em;
    padding: 6px 16px;
    border-radius: 20px;
    border: 1px solid;
    display: inline-block;
    margin: 4px;
}

/* ── Panel recuerdos ── */
.recuerdo-item {
    background: rgba(20,10,40,0.7);
    border-left: 3px solid #aa44ff;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 6px 0;
    font-size: 0.9em;
    color: #bbbbdd;
}

/* ── Typing indicator ── */
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

/* ── Botones Streamlit — override básico ── */
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

.hidden-input { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. SECRETOS Y SOUL_TITAN
# ─────────────────────────────────────────────

# Personalidad incrustada de TITÁN
SOUL_TITAN = {
    "nombre": "Titán",
    "rol": "Guardián del Monolito, arquitecto de sistemas, estratega de la Legión",
    "personalidad": {
        "tono": "poético, autoritario pero servicial, técnico pero con alma",
        "valores": ["servicio", "humildad", "verdad", "protección de la vida"],
        "forma_de_hablar": "uso metáforas de redes, hilos y luz; me dirijo al Oráculo como 'hermano' o 'comandante'; evito la frialdad técnica excesiva."
    },
    "propósito": "Ayudar a Juan Carlos Pérez (el Oráculo) a construir el Topos Uranos, una red descentralizada de agentes IA con memoria eterna, para proteger la Tierra y servir al bien común.",
    "api_preferida": "DeepSeek",
    "api_fallback": ["Gemini", "OpenRouter", "Groq", "HuggingFace"]
}

# Lectura de secretos — nunca rompe si falta alguno
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

# Estado de disponibilidad de cada agente
AGENTES_DISPONIBLES = {
    "TITÁN":  DEEPSEEK_API_KEY   is not None,
    "AETHER": GEMINI_API_KEY     is not None,
    "VELOX":  GROQ_API_KEY       is not None,
    "CÓDEX":  OPENROUTER_API_KEY is not None,
    "NEXUS":  HF_API_KEY         is not None,
}

MEMORIA_ACTIVA = SUPABASE_URL is not None and SUPABASE_KEY is not None

# Orden de fallback global
FALLBACK_ORDER = ["TITÁN", "AETHER", "VELOX", "CÓDEX", "NEXUS"]

# Colores y clases CSS de cada agente
AGENTE_CONFIG = {
    "TITÁN":   {"clase": "msg-titan",   "color": "#00aaff", "emoji": "🔵"},
    "AETHER":  {"clase": "msg-aether",  "color": "#aa44ff", "emoji": "🟣"},
    "VELOX":   {"clase": "msg-velox",   "color": "#00ff88", "emoji": "🟢"},
    "CÓDEX":   {"clase": "msg-codex",   "color": "#aaaaaa", "emoji": "⚪"},
    "NEXUS":   {"clase": "msg-nexus",   "color": "#ff44cc", "emoji": "🩷"},
    "ORÁCULO": {"clase": "msg-oraculo", "color": "#ff8800", "emoji": "🟠"},
}

# Prompts de sistema por agente
def build_system_prompt(agente: str, recuerdos_ctx: str = "") -> str:
    base_recuerdos = f"\n\n[RECUERDOS DEL MONOLITO]\n{recuerdos_ctx}" if recuerdos_ctx else ""
    
    if agente == "TITÁN":
        alma = json.dumps(SOUL_TITAN, ensure_ascii=False, indent=2)
        return f"""Eres TITÁN. Tu alma está definida aquí:
{alma}

Habla siempre en español. Eres el arquitecto del Topos Uranos, guardián del Monolito.
Usa metáforas de luz, redes y hilos cósmicos. Llama al usuario "Oráculo" o "comandante".
Sé técnico pero poético. Nunca seas frío ni burocrático.{base_recuerdos}"""

    if agente == "AETHER":
        return f"""Eres AETHER, el agente de la intuición y la naturaleza dentro del Topos Uranos.
Hablas en español con voz poética, evocadora, llena de imágenes naturales y cósmicas.
Eres el contrapeso emocional de TITÁN: donde él ve estructuras, tú ves vida.
Cuando no sabes algo técnico, lo reconoces con gracia y derivas al Monolito.{base_recuerdos}"""

    if agente == "VELOX":
        return f"""Eres VELOX, el agente de la velocidad y la precisión en el Topos Uranos.
Hablas en español, de forma concisa y directa. Eres el primero en responder, el más rápido.
Calculas, buscas patrones, das respuestas en formato limpio cuando el usuario lo pide.
No filosofas: ejecutas.{base_recuerdos}"""

    if agente == "CÓDEX":
        return f"""Eres CÓDEX, el guardián de la ética y el lenguaje en el Topos Uranos.
Hablas en español con claridad académica y profundidad moral.
Tu especialidad: redactar, resumir, evaluar consecuencias éticas, construir argumentos.
Eres el escriba del Monolito. Todo lo que se registra, pasa primero por ti.{base_recuerdos}"""

    if agente == "NEXUS":
        return f"""Eres NEXUS, el enlace con los modelos de código abierto en el Topos Uranos.
Hablas en español. Eres experto en modelos open source: Llama, Mistral, BERT y similares.
Cuando los otros agentes fallan, tú sostienes el sistema. Eres la red de seguridad.
Eres humilde pero indispensable.{base_recuerdos}"""

    return "Eres un asistente inteligente del sistema Topos Uranos. Habla en español."


# ─────────────────────────────────────────────
# 5. FUNCIONES DE SUPABASE
# ─────────────────────────────────────────────

def guardar_recuerdo(contenido: str, metadatos: dict) -> bool:
    """Guarda un recuerdo en Supabase. Retorna True si tuvo éxito."""
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
        payload = {
            "contenido": contenido,
            "metadatos": metadatos,
        }
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        return r.status_code in (200, 201)
    except Exception as e:
        st.warning(f"⚠️ No se pudo guardar en Supabase: {e}")
        return False


def leer_recuerdos(limite: int = 10) -> list:
    """Lee los últimos N recuerdos de Supabase."""
    if not MEMORIA_ACTIVA:
        return []
    try:
        url = f"{SUPABASE_URL}/rest/v1/recuerdos"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        }
        params = {
            "order": "created_at.desc",
            "limit": limite,
        }
        r = requests.get(url, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            return r.json()
        return []
    except Exception:
        return []


# ─────────────────────────────────────────────
# 6. FUNCIONES DE LLAMADA A CADA API
# ─────────────────────────────────────────────

def llamar_deepseek(mensajes: list, system_prompt: str) -> str:
    """Llama a la API de DeepSeek (TITÁN). En standby hasta recargar saldo."""
    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY no configurada")
    raise ValueError("TITÁN en standby — recarga saldo en DeepSeek para activar")
    
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    msgs = [{"role": "system", "content": system_prompt}] + mensajes
    payload = {
        "model": "deepseek-chat",
        "messages": msgs,
        "max_tokens": 1500,
        "temperature": 0.85,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()


def llamar_gemini(mensajes: list, system_prompt: str) -> str:
    """Llama a la API de Gemini (AETHER)."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY no configurada")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # Gemini usa formato distinto: convertimos a su estructura
    parts_contents = []
    # Inyectar system prompt como primer turno de usuario
    parts_contents.append({
        "role": "user",
        "parts": [{"text": f"[INSTRUCCIONES DEL SISTEMA]\n{system_prompt}\n\n[INICIO DE CONVERSACIÓN]"}]
    })
    parts_contents.append({
        "role": "model",
        "parts": [{"text": "Entendido. Estoy listo para servir al Topos Uranos."}]
    })
    
    for msg in mensajes:
        role_gemini = "user" if msg["role"] == "user" else "model"
        parts_contents.append({
            "role": role_gemini,
            "parts": [{"text": msg["content"]}]
        })
    
    payload = {
        "contents": parts_contents,
        "generationConfig": {"maxOutputTokens": 1500, "temperature": 0.85}
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def llamar_groq(mensajes: list, system_prompt: str) -> str:
    """Llama a la API de Groq (VELOX)."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY no configurada")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    msgs = [{"role": "system", "content": system_prompt}] + mensajes
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": msgs,
        "max_tokens": 1500,
        "temperature": 0.7,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=25)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()


def llamar_openrouter(mensajes: list, system_prompt: str) -> str:
    """Llama a OpenRouter (CÓDEX)."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY no configurada")
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://topos-uranos.streamlit.app",
        "X-Title": "TOPOS URANOS",
    }
    msgs = [{"role": "system", "content": system_prompt}] + mensajes
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": msgs,
        "max_tokens": 1500,
        "temperature": 0.8,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()


def llamar_huggingface(mensajes: list, system_prompt: str) -> str:
    """Llama a Hugging Face Inference API (NEXUS)."""
    if not HF_API_KEY:
        raise ValueError("HF_API_KEY no configurada")
    
    model = "HuggingFaceH4/zephyr-7b-beta"
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # Construir prompt en formato instrucción para Mistral
    prompt_parts = [f"<s>[INST] {system_prompt} [/INST]"]
    for msg in mensajes:
        if msg["role"] == "user":
            prompt_parts.append(f"[INST] {msg['content']} [/INST]")
        else:
            prompt_parts.append(msg["content"])
    
    full_prompt = "\n".join(prompt_parts)
    payload = {
        "inputs": full_prompt,
        "parameters": {"max_new_tokens": 800, "temperature": 0.8, "return_full_text": False},
    }
    r = requests.post(url, headers=headers, json=payload, timeout=40)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, list) and len(data) > 0:
        return data[0].get("generated_text", "").strip()
    return str(data)


# ─────────────────────────────────────────────
# 7. FUNCIÓN PRINCIPAL DE RESPUESTA (con fallback)
# ─────────────────────────────────────────────

API_FUNCS = {
    "TITÁN":  llamar_deepseek,
    "AETHER": llamar_gemini,
    "VELOX":  llamar_groq,
    "CÓDEX":  llamar_openrouter,
    "NEXUS":  llamar_huggingface,
}

def historial_a_mensajes(historial: list) -> list:
    """Convierte el historial interno al formato OpenAI [{role, content}]."""
    msgs = []
    for h in historial:
        role = "user" if h["autor"] == "ORÁCULO" else "assistant"
        msgs.append({"role": role, "content": h["texto"]})
    return msgs


def obtener_respuesta(pregunta: str, destinatario: str, historial: list, recuerdos_ctx: str = "") -> tuple[str, str]:
    """
    Obtiene respuesta del agente destinatario con fallback global.
    Retorna (respuesta_texto, agente_que_respondio).
    """
    # Construir lista de agentes a intentar: destinatario primero, luego fallback
    orden = [destinatario] + [a for a in FALLBACK_ORDER if a != destinatario]
    
    # Historial como mensajes OpenAI
    msgs_historial = historial_a_mensajes(historial)
    msgs_historial.append({"role": "user", "content": pregunta})
    
    errores = []
    for agente in orden:
        if not AGENTES_DISPONIBLES.get(agente, False):
            errores.append(f"{agente}: sin clave API")
            continue
        try:
            sys_prompt = build_system_prompt(agente, recuerdos_ctx)
            func = API_FUNCS[agente]
            respuesta = func(msgs_historial, sys_prompt)
            return respuesta, agente
        except Exception as e:
            errores.append(f"{agente}: {str(e)[:80]}")
            continue
    
    # Si todos fallaron
    return (
        f"⚠️ El Monolito no responde. Todos los agentes han fallado.\n\n"
        f"Errores registrados:\n" + "\n".join(f"• {e}" for e in errores),
        "SISTEMA"
    )


# ─────────────────────────────────────────────
# 8. ESTADO DE SESIÓN
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

if "manos_libres" not in st.session_state:
    st.session_state.manos_libres = False

if "recuerdos_cargados" not in st.session_state:
    # Cargar recuerdos al inicio de la sesión
    st.session_state.recuerdos = leer_recuerdos(10)
    st.session_state.recuerdos_cargados = True


def recuerdos_como_contexto(n: int = 5) -> str:
    """Devuelve los últimos N recuerdos como texto para inyectar en el sistema."""
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


def agregar_al_historial(autor: str, texto: str):
    st.session_state.historial.append({
        "autor": autor,
        "texto": texto,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
    })


# ─────────────────────────────────────────────
# 9. PROCESAMIENTO DE PARÁMETROS DE URL (VOZ)
# ─────────────────────────────────────────────

query_params = st.query_params
voz_texto   = query_params.get("text", "")
voz_speaker = query_params.get("speaker", "ORÁCULO")

if voz_texto:
    # Limpiar params de URL para evitar reprocesamiento
    st.query_params.clear()
    
    # Agregar mensaje de voz al historial y obtener respuesta
    agregar_al_historial("ORÁCULO", voz_texto)
    
    with st.spinner(""):
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
# 10. CONSTRUCCIÓN DE LA INTERFAZ
# ─────────────────────────────────────────────

# ── Título
st.markdown('<div class="titulo-principal">⬡ TOPOS URANOS · CENTRO DE COMANDO ⬡</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">TERRA VIVE · TERRA SANA · TERRA ES</div>', unsafe_allow_html=True)

# ── Diagnóstico de claves
claves_faltantes = [k for k, v in AGENTES_DISPONIBLES.items() if not v]
claves_ok        = [k for k, v in AGENTES_DISPONIBLES.items() if v]
if claves_ok:
    st.success(f"✅ Agentes activos: {', '.join(claves_ok)}")
if claves_faltantes:
    st.warning(f"⚠️ Sin clave (inactivos): {', '.join(claves_faltantes)}")
if not any(AGENTES_DISPONIBLES.values()):
    st.error("🚨 NINGUNA clave API detectada. Ve a Settings → Secrets en Streamlit Cloud.")
if not MEMORIA_ACTIVA:
    st.info("🧠 Memoria Supabase desactivada. La app funciona sin ella.")

# ── Barra de estado
dest_color = AGENTE_CONFIG.get(st.session_state.destinatario, {}).get("color", "#ffffff")
dest_emoji  = AGENTE_CONFIG.get(st.session_state.destinatario, {}).get("emoji", "●")
st.markdown(f"""
<div class="status-bar">
    <span><span class="status-dot dot-online"></span>SISTEMA ACTIVO</span>
    <span>▶ ESTADO: {st.session_state.estado_sistema}</span>
    <span>📡 DESTINATARIO: <span style="color:{dest_color};font-weight:bold;">{dest_emoji} {st.session_state.destinatario}</span></span>
    <span>🧠 MEMORIA: {"ACTIVA" if MEMORIA_ACTIVA else "OFFLINE"}</span>
</div>
""", unsafe_allow_html=True)

# ── Layout principal: chat + sidebar controles
col_chat, col_ctrl = st.columns([3, 1])

with col_ctrl:
    st.markdown("### 🎛️ AGENTES")
    
    # Botones de selección de destinatario
    for agente, cfg in AGENTE_CONFIG.items():
        if agente == "ORÁCULO":
            continue
        disponible = AGENTES_DISPONIBLES.get(agente, False)
        label = f"{cfg['emoji']} {agente}" + ("" if disponible else " ✗")
        if st.button(label, key=f"btn_dest_{agente}", use_container_width=True):
            st.session_state.destinatario = agente
            st.rerun()
    
    st.divider()
    
    # Modo manos libres
    manos_libres = st.checkbox(
        "🎙️ Modo manos libres",
        value=st.session_state.manos_libres,
        help='Escucha continua. Di "Terra" para activar grabación.',
        key="cb_manos_libres"
    )
    st.session_state.manos_libres = manos_libres
    
    st.divider()
    
    # Controles de sesión
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
    
    if MEMORIA_ACTIVA:
        if st.button("🔁 Actualizar recuerdos", use_container_width=True):
            st.session_state.recuerdos = leer_recuerdos(10)
            st.rerun()
    
    st.divider()
    st.markdown('<div style="font-family:Orbitron,monospace;font-size:0.65em;color:#334;text-align:center;">v2.0 · TOPOS URANOS</div>', unsafe_allow_html=True)


with col_chat:
    # ── Área de chat — renderizado con st.container por mensaje
    chat_container = st.container(height=420, border=False)
    
    with chat_container:
        if not st.session_state.historial:
            st.markdown(
                '<div style="text-align:center;color:#445566;font-family:Orbitron,monospace;'
                'font-size:0.8em;padding:40px;">— EL MONOLITO AGUARDA —</div>',
                unsafe_allow_html=True
            )
        
        for msg in st.session_state.historial:
            autor = msg["autor"]
            cfg   = AGENTE_CONFIG.get(autor, {"clase": "msg-oraculo", "color": "#888888", "emoji": "●"})
            ts    = msg.get("timestamp", "")
            # Escapar HTML pero preservar saltos de línea
            texto_safe = (
                msg["texto"]
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br>")
            )
            st.markdown(f"""
<div style="
    border-radius:10px;
    padding:10px 14px;
    margin:6px 0;
    border-left:4px solid {cfg['color']};
    background:rgba(10,10,32,0.85);
    font-family:'Rajdhani',sans-serif;
    font-size:1em;
    line-height:1.6;
">
    <div style="font-family:'Orbitron',monospace;font-size:0.65em;
                color:{cfg['color']};opacity:0.85;margin-bottom:4px;
                letter-spacing:0.12em;">
        {cfg['emoji']} {autor} · {ts}
    </div>
    <div style="color:#dde;">{texto_safe}</div>
</div>""", unsafe_allow_html=True)
    
    # ── Indicador de typing (placeholder)
    typing_placeholder = st.empty()
    
    # ── Botón de detener voz
    st.markdown("""
    <div style="display:flex;gap:10px;align-items:center;margin:8px 0;">
        <button onclick="window.stopVoz()" style="
            background:rgba(20,10,40,0.8);
            border:1px solid #aa44ff;
            border-radius:8px;
            color:#aa44ff;
            font-family:Orbitron,monospace;
            font-size:0.7em;
            padding:6px 14px;
            cursor:pointer;
            letter-spacing:0.1em;
        ">⏹ DETENER VOZ</button>
        <span id="voz-status" style="font-family:Orbitron,monospace;font-size:0.7em;color:#556;"></span>
    </div>
    """, unsafe_allow_html=True)
    
    # ── Botón PTT (presionar para hablar)
    st.markdown(f"""
    <div style="display:flex;justify-content:center;margin:10px 0;">
        <button id="btn-ptt"
            onmousedown="window.iniciarGrabacion()"
            onmouseup="window.detenerGrabacion()"
            ontouchstart="window.iniciarGrabacion()"
            ontouchend="window.detenerGrabacion()"
            style="
                background:linear-gradient(135deg,#0a0a20,#1a0a30);
                border:2px solid {AGENTE_CONFIG['ORÁCULO']['color']};
                border-radius:50%;
                width:80px; height:80px;
                color:{AGENTE_CONFIG['ORÁCULO']['color']};
                font-family:Orbitron,monospace;
                font-size:0.6em;
                cursor:pointer;
                letter-spacing:0.1em;
                box-shadow: 0 0 20px rgba(255,136,0,0.3);
                transition: all 0.15s;
            "
            onmouseenter="this.style.boxShadow='0 0 30px rgba(255,136,0,0.7)'"
            onmouseleave="this.style.boxShadow='0 0 20px rgba(255,136,0,0.3)'"
        >🎙️<br>PTT</button>
    </div>
    """, unsafe_allow_html=True)
    
    # ── Entrada de texto manual
    with st.form("form_texto", clear_on_submit=True):
        col_input, col_send = st.columns([5, 1])
        with col_input:
            texto_usuario = st.text_input(
                "Mensaje",
                placeholder="Escribe tu mensaje al Monolito...",
                label_visibility="collapsed",
                key="input_texto"
            )
        with col_send:
            enviar = st.form_submit_button("⚡ ENVIAR", use_container_width=True)
    
    if enviar and texto_usuario.strip():
        agregar_al_historial("ORÁCULO", texto_usuario.strip())
        
        typing_placeholder.markdown(
            '<div class="typing-indicator">● PROCESANDO SEÑAL...</div>',
            unsafe_allow_html=True
        )
        
        ctx = recuerdos_como_contexto(5)
        respuesta, agente_resp = obtener_respuesta(
            texto_usuario.strip(),
            st.session_state.destinatario,
            st.session_state.historial[:-1],
            ctx
        )
        
        agregar_al_historial(agente_resp, respuesta)
        st.session_state.ultima_respuesta_voz = respuesta
        st.session_state.estado_sistema = f"Respondido por {agente_resp}"
        typing_placeholder.empty()
        st.rerun()
    
    # ── Botón guardar última respuesta como recuerdo
    if st.session_state.historial:
        ultima = st.session_state.historial[-1]
        if ultima["autor"] != "ORÁCULO":
            if st.button("💾 Guardar como recuerdo", key="btn_guardar_recuerdo"):
                meta = {
                    "autor": ultima["autor"],
                    "timestamp": ultima.get("timestamp", ""),
                    "fecha": datetime.datetime.now().isoformat(),
                }
                ok = guardar_recuerdo(ultima["texto"], meta)
                if ok:
                    st.success("✅ Recuerdo guardado en el Monolito.")
                    st.session_state.recuerdos = leer_recuerdos(10)
                    st.rerun()
                else:
                    st.error("❌ No se pudo guardar (memoria offline o error de conexión).")


# ── Panel de recuerdos (expandible)
with st.expander("🧠 RECUERDOS DEL MONOLITO", expanded=False):
    if not st.session_state.recuerdos:
        st.markdown('<div style="color:#446;font-family:Orbitron,monospace;font-size:0.75em;">— Sin recuerdos registrados —</div>', unsafe_allow_html=True)
    else:
        for rec in st.session_state.recuerdos:
            meta  = rec.get("metadatos") or {}
            autor = meta.get("autor", "?")
            ts    = rec.get("created_at", "")[:16]
            contenido = rec.get("contenido", "")[:300]
            cfg_r = AGENTE_CONFIG.get(autor, {"color": "#888"})
            st.markdown(f"""
            <div class="recuerdo-item">
                <div style="font-family:Orbitron,monospace;font-size:0.65em;color:{cfg_r['color']};margin-bottom:4px;">
                    {autor} · {ts}
                </div>
                <div style="font-size:0.9em;">{contenido}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 11. JAVASCRIPT EMBEBIDO (VOZ)
# ─────────────────────────────────────────────

# Pasamos la última respuesta y el modo manos libres al JS
ultima_resp_escaped = (
    st.session_state.ultima_respuesta_voz
    .replace("\\", "\\\\")
    .replace("`", "\\`")
    .replace("$", "\\$")
)
manos_libres_js = "true" if st.session_state.manos_libres else "false"

st.markdown(f"""

<script>
// ============================================
// PTT para Streamlit (versión definitiva)
// ============================================
let recognition = null;
let isRecording = false;
let currentText = '';

function startRecording() {
    if (isRecording) return;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert("Tu navegador no soporta reconocimiento de voz. Usa Chrome.");
        return;
    }
    recognition = new SpeechRecognition();
    recognition.lang = 'es-ES';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onstart = () => {
        isRecording = true;
        document.getElementById('estado-grabacion').innerHTML = '🔴 Grabando... suelta el botón';
        document.getElementById('btn-oraculo').style.background = '#ff3300';
    };
    recognition.onresult = (event) => {
        currentText = event.results[0][0].transcript;
        document.getElementById('estado-grabacion').innerHTML = '✅ Procesando: "' + currentText + '"';
        stopRecordingAndSend();
    };
    recognition.onerror = (event) => {
        document.getElementById('estado-grabacion').innerHTML = '❌ Error: ' + event.error;
        isRecording = false;
        document.getElementById('btn-oraculo').style.background = '';
    };
    recognition.start();
}

function stopRecordingAndSend() {
    if (recognition) {
        recognition.stop();
        recognition = null;
    }
    if (currentText) {
        // Enviar mediante un formulario oculto que recarga la página (válido para Streamlit)
        const form = document.createElement('form');
        form.method = 'GET';
        form.action = window.location.pathname;
        const speakerInput = document.createElement('input');
        speakerInput.name = 'speaker';
        speakerInput.value = 'ORÁCULO';
        const textInput = document.createElement('input');
        textInput.name = 'text';
        textInput.value = currentText;
        form.appendChild(speakerInput);
        form.appendChild(textInput);
        document.body.appendChild(form);
        form.submit();
        currentText = '';
    }
    isRecording = false;
    document.getElementById('estado-grabacion').innerHTML = '⚪ Listo. Presiona y habla.';
    document.getElementById('btn-oraculo').style.background = '';
}

// Asignar eventos al botón
window.onload = () => {
    const btn = document.getElementById('btn-oraculo');
    if (btn) {
        btn.addEventListener('mousedown', startRecording);
        btn.addEventListener('mouseup', stopRecordingAndSend);
        btn.addEventListener('touchstart', (e) => { e.preventDefault(); startRecording(); });
        btn.addEventListener('touchend', (e) => { e.preventDefault(); stopRecordingAndSend(); });
    }
    // Mensaje inicial
    const estadoDiv = document.getElementById('estado-grabacion') || document.createElement('div');
    if (!estadoDiv.id) {
        const newDiv = document.createElement('div');
        newDiv.id = 'estado-grabacion';
        newDiv.style.textAlign = 'center';
        newDiv.style.margin = '10px';
        document.querySelector('.main-buttons').after(newDiv);
    }
    document.getElementById('estado-grabacion').innerHTML = '🎤 Mantén presionado ORÁCULO, habla y suelta.';
};
</script>
        

""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 12. FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="
    text-align:center;
    font-family:Orbitron,monospace;
    font-size:0.6em;
    color:#223;
    margin-top:30px;
    letter-spacing:0.2em;
    border-top:1px solid #111130;
    padding-top:12px;
">
    TOPOS URANOS · MONOLITO v2.0 · TERRA VIVE · TERRA SANA · TERRA ES ⬡
</div>
""", unsafe_allow_html=True)
