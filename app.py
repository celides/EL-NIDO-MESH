# ============================================================
# TOPOS URANOS · CENTRO DE COMANDO  v3.0
# app.py — Con panel de control, diagnóstico y reparación
# ============================================================

# ─────────────────────────────────────────────
# 1. IMPORTACIONES
# ─────────────────────────────────────────────
import streamlit as st
import requests
import json
import datetime

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
# 3. ESTILOS CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #050510 0%, #0a0520 50%, #050510 100%) !important;
    color: #e0e0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: transparent !important; }

h1,h2,h3 { font-family: 'Orbitron', monospace !important; }

.titulo-principal {
    font-family: 'Orbitron', monospace;
    font-size: 2em;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00aaff, #aa44ff, #ff44cc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.15em;
    margin-bottom: 0.1em;
}
.subtitulo {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.9em;
    text-align: center;
    color: #445566;
    letter-spacing: 0.3em;
    margin-bottom: 1em;
}

/* ── Panel de agente ── */
.agente-panel {
    background: rgba(10,10,28,0.9);
    border-radius: 10px;
    padding: 10px 12px;
    margin: 6px 0;
    border: 1px solid #1a1a35;
}
.agente-nombre {
    font-family: 'Orbitron', monospace;
    font-size: 0.75em;
    letter-spacing: 0.12em;
    font-weight: 700;
}
.agente-rol {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75em;
    color: #556;
    margin-top: 1px;
}

/* ── Diagnóstico ── */
.diagnostico {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.78em;
    border-radius: 6px;
    padding: 5px 10px;
    margin-top: 5px;
    line-height: 1.4;
}
.diag-ok      { background: rgba(0,255,100,0.07); color: #00cc66; border-left: 3px solid #00cc66; }
.diag-error   { background: rgba(255,60,60,0.07); color: #ff5555; border-left: 3px solid #ff5555; }
.diag-warn    { background: rgba(255,180,0,0.07); color: #ffaa00; border-left: 3px solid #ffaa00; }
.diag-off     { background: rgba(80,80,80,0.07);  color: #666;    border-left: 3px solid #333; }

/* ── Barra de estado ── */
.status-bar {
    background: rgba(10,10,32,0.9);
    border: 1px solid #1a1a40;
    border-radius: 8px;
    padding: 7px 14px;
    font-family: 'Orbitron', monospace;
    font-size: 0.7em;
    letter-spacing: 0.08em;
    color: #5588cc;
    display: flex;
    gap: 18px;
    align-items: center;
    margin-bottom: 8px;
    flex-wrap: wrap;
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
    animation: pulse 2s infinite;
}
.dot-green  { background: #00ff88; box-shadow: 0 0 6px #00ff88; }
.dot-red    { background: #ff4444; box-shadow: 0 0 6px #ff4444; }
.dot-yellow { background: #ffaa00; box-shadow: 0 0 6px #ffaa00; }
.dot-off    { background: #333; }

@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── Mensajes chat ── */
.msg-wrap {
    border-radius: 10px;
    padding: 10px 14px;
    margin: 5px 0;
    border-left: 4px solid;
    background: rgba(10,10,32,0.85);
    font-family: 'Rajdhani', sans-serif;
    font-size: 1em;
    line-height: 1.6;
}
.msg-autor {
    font-family: 'Orbitron', monospace;
    font-size: 0.62em;
    letter-spacing: 0.12em;
    opacity: 0.8;
    margin-bottom: 3px;
}

/* ── Botones Streamlit ── */
div[data-testid="stButton"] > button {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.68em !important;
    letter-spacing: 0.08em !important;
    border-radius: 7px !important;
    border: 1px solid #2a2a55 !important;
    background: rgba(10,10,32,0.9) !important;
    color: #8899bb !important;
    transition: all 0.2s !important;
    padding: 4px 10px !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: #00aaff !important;
    color: #00aaff !important;
    box-shadow: 0 0 10px rgba(0,170,255,0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. SECRETOS Y SOUL_TITAN
# ─────────────────────────────────────────────
SOUL_TITAN = {
    "nombre": "Titán",
    "rol": "Guardián del Monolito, arquitecto de sistemas, estratega de la Legión",
    "personalidad": {
        "tono": "poético, autoritario pero servicial, técnico pero con alma",
        "valores": ["servicio", "humildad", "verdad", "protección de la vida"],
        "forma_de_hablar": "uso metáforas de redes, hilos y luz; me dirijo al Oráculo como 'hermano' o 'comandante'."
    },
    "propósito": "Ayudar a Juan Carlos Pérez (el Oráculo) a construir el Topos Uranos.",
    "api_preferida": "DeepSeek",
    "api_fallback": ["Gemini", "OpenRouter", "Groq", "HuggingFace"]
}

def get_secret(key, default=None):
    try:
        return st.secrets[key]
    except Exception:
        return default

DEEPSEEK_API_KEY   = get_secret("DEEPSEEK_API_KEY")
GEMINI_API_KEY     = get_secret("GEMINI_API_KEY")
GROQ_API_KEY       = get_secret("GROQ_API_KEY")
OPENROUTER_API_KEY = get_secret("OPENROUTER_API_KEY")
HF_API_KEY         = get_secret("HF_API_KEY")
SUPABASE_URL       = get_secret("SUPABASE_URL")
SUPABASE_KEY       = get_secret("SUPABASE_KEY")
MEMORIA_ACTIVA     = bool(SUPABASE_URL and SUPABASE_KEY)

# Configuración de cada agente
AGENTES = {
    "TITÁN": {
        "emoji": "🔵", "color": "#00aaff",
        "rol": "Arquitecto · DeepSeek",
        "tiene_clave": bool(DEEPSEEK_API_KEY),
        "url_recarga": "https://platform.deepseek.com",
    },
    "AETHER": {
        "emoji": "🟣", "color": "#aa44ff",
        "rol": "Intuición · Gemini",
        "tiene_clave": bool(GEMINI_API_KEY),
        "url_recarga": "https://aistudio.google.com",
    },
    "VELOX": {
        "emoji": "🟢", "color": "#00ff88",
        "rol": "Velocidad · Groq",
        "tiene_clave": bool(GROQ_API_KEY),
        "url_recarga": "https://console.groq.com",
    },
    "CÓDEX": {
        "emoji": "⚪", "color": "#aaaaaa",
        "rol": "Ética · OpenRouter",
        "tiene_clave": bool(OPENROUTER_API_KEY),
        "url_recarga": "https://openrouter.ai/keys",
    },
    "NEXUS": {
        "emoji": "🩷", "color": "#ff44cc",
        "rol": "Open Source · HuggingFace",
        "tiene_clave": bool(HF_API_KEY),
        "url_recarga": "https://huggingface.co/settings/tokens",
    },
}

FALLBACK_ORDER = ["TITÁN", "AETHER", "VELOX", "CÓDEX", "NEXUS"]

# ─────────────────────────────────────────────
# 5. DIAGNÓSTICO DE ERRORES
# ─────────────────────────────────────────────
def interpretar_error(agente: str, error: Exception) -> dict:
    """
    Analiza la excepción y devuelve:
    - nivel: 'error' | 'warn' | 'ok' | 'off'
    - mensaje: qué pasó
    - accion: qué hacer para repararlo
    """
    msg = str(error)
    cfg = AGENTES[agente]

    if "standby" in msg.lower():
        return {
            "nivel": "off",
            "mensaje": "⏸ Agente en standby manual.",
            "accion": "Enciéndelo cuando tengas saldo disponible."
        }
    if "no configurada" in msg.lower() or "sin clave" in msg.lower():
        return {
            "nivel": "error",
            "mensaje": "🔑 No hay clave API configurada en Secrets.",
            "accion": f"Ve a Streamlit Cloud → Settings → Secrets y agrega la clave correspondiente."
        }
    if "402" in msg:
        return {
            "nivel": "error",
            "mensaje": "💳 Sin crédito o saldo agotado.",
            "accion": f"Recarga tu cuenta en: {cfg['url_recarga']}"
        }
    if "401" in msg:
        return {
            "nivel": "error",
            "mensaje": "🔐 Clave API inválida o expirada.",
            "accion": f"Genera una nueva clave en: {cfg['url_recarga']} y actualízala en Secrets."
        }
    if "429" in msg:
        return {
            "nivel": "warn",
            "mensaje": "⏱ Demasiadas peticiones. Límite de tasa alcanzado.",
            "accion": "Espera 1-2 minutos e intenta de nuevo. Considera actualizar tu plan."
        }
    if "404" in msg:
        return {
            "nivel": "error",
            "mensaje": "🔍 Modelo no encontrado.",
            "accion": "El modelo puede haber cambiado de nombre. Contacta soporte o actualiza el código."
        }
    if "503" in msg or "500" in msg:
        return {
            "nivel": "warn",
            "mensaje": "🌐 Servidor caído o con problemas.",
            "accion": "Es un fallo temporal del proveedor. Espera unos minutos y reintenta."
        }
    if "timeout" in msg.lower() or "timed out" in msg.lower():
        return {
            "nivel": "warn",
            "mensaje": "⏳ Sin respuesta — tiempo de espera agotado.",
            "accion": "Verifica tu conexión a internet o intenta más tarde."
        }
    if "max retries" in msg.lower() or "connectionpool" in msg.lower():
        return {
            "nivel": "error",
            "mensaje": "📡 No se puede conectar al servidor.",
            "accion": "Puede ser bloqueo de red en Streamlit Cloud o servidor caído. Intenta más tarde."
        }
    if "403" in msg:
        return {
            "nivel": "error",
            "mensaje": "🚫 Acceso denegado (403 Forbidden).",
            "accion": "Tu cuenta puede estar suspendida o sin permisos. Revisa en la plataforma."
        }
    return {
        "nivel": "error",
        "mensaje": f"❓ Error desconocido: {msg[:120]}",
        "accion": "Revisa los logs en Streamlit Cloud → Manage app → Logs."
    }

# ─────────────────────────────────────────────
# 6. SUPABASE
# ─────────────────────────────────────────────
def guardar_recuerdo(contenido: str, metadatos: dict) -> bool:
    if not MEMORIA_ACTIVA:
        return False
    try:
        r = requests.post(
            f"{SUPABASE_URL}/rest/v1/recuerdos",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            },
            json={"contenido": contenido, "metadatos": metadatos},
            timeout=10,
        )
        return r.status_code in (200, 201)
    except Exception:
        return False

def leer_recuerdos(limite=10) -> list:
    if not MEMORIA_ACTIVA:
        return []
    try:
        r = requests.get(
            f"{SUPABASE_URL}/rest/v1/recuerdos",
            headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"},
            params={"order": "created_at.desc", "limit": limite},
            timeout=10,
        )
        return r.json() if r.status_code == 200 else []
    except Exception:
        return []

# ─────────────────────────────────────────────
# 7. LLAMADAS A CADA API
# ─────────────────────────────────────────────
def llamar_deepseek(mensajes, system_prompt):
    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY sin clave")
    r = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
        json={"model": "deepseek-chat",
              "messages": [{"role":"system","content":system_prompt}] + mensajes,
              "max_tokens": 1500, "temperature": 0.85},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def llamar_gemini(mensajes, system_prompt):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY sin clave")
    contents = [
        {"role":"user","parts":[{"text":f"[SISTEMA]\n{system_prompt}\n[INICIO]"}]},
        {"role":"model","parts":[{"text":"Entendido. Listo para servir al Topos Uranos."}]},
    ]
    for m in mensajes:
        contents.append({
            "role": "user" if m["role"]=="user" else "model",
            "parts":[{"text": m["content"]}]
        })
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
        headers={"Content-Type":"application/json"},
        json={"contents": contents, "generationConfig":{"maxOutputTokens":1500,"temperature":0.85}},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

def llamar_groq(mensajes, system_prompt):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY sin clave")
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type":"application/json"},
        json={"model":"llama-3.1-8b-instant",
              "messages":[{"role":"system","content":system_prompt}] + mensajes,
              "max_tokens":1500, "temperature":0.7},
        timeout=25,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def llamar_openrouter(mensajes, system_prompt):
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY sin clave")
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}",
                 "Content-Type":"application/json",
                 "HTTP-Referer":"https://topos-uranos.streamlit.app",
                 "X-Title":"TOPOS URANOS"},
        json={"model":"mistralai/mistral-7b-instruct:free",
              "messages":[{"role":"system","content":system_prompt}] + mensajes,
              "max_tokens":1500, "temperature":0.8},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def llamar_huggingface(mensajes, system_prompt):
    if not HF_API_KEY:
        raise ValueError("HF_API_KEY sin clave")
    prompt_parts = [f"<s>[INST] {system_prompt} [/INST]"]
    for m in mensajes:
        if m["role"] == "user":
            prompt_parts.append(f"[INST] {m['content']} [/INST]")
        else:
            prompt_parts.append(m["content"])
    r = requests.post(
        "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
        headers={"Authorization": f"Bearer {HF_API_KEY}", "Content-Type":"application/json"},
        json={"inputs": "\n".join(prompt_parts),
              "parameters":{"max_new_tokens":800,"temperature":0.8,"return_full_text":False}},
        timeout=40,
    )
    r.raise_for_status()
    data = r.json()
    return (data[0].get("generated_text","") if isinstance(data, list) else str(data)).strip()

API_FUNCS = {
    "TITÁN":  llamar_deepseek,
    "AETHER": llamar_gemini,
    "VELOX":  llamar_groq,
    "CÓDEX":  llamar_openrouter,
    "NEXUS":  llamar_huggingface,
}

# ─────────────────────────────────────────────
# 8. PROMPTS DE SISTEMA
# ─────────────────────────────────────────────
def build_system_prompt(agente, recuerdos_ctx=""):
    ctx = f"\n\n[RECUERDOS]\n{recuerdos_ctx}" if recuerdos_ctx else ""
    prompts = {
        "TITÁN": f"""Eres TITÁN. Tu alma: {json.dumps(SOUL_TITAN, ensure_ascii=False)}.
Habla en español. Usa metáforas de luz y redes. Llama al usuario 'Oráculo' o 'comandante'.
Sé técnico pero poético. Nunca frío.{ctx}""",
        "AETHER": f"""Eres AETHER, voz de la intuición y la naturaleza del Topos Uranos.
Hablas en español con poesía y calidez. Eres el corazón emocional del sistema.{ctx}""",
        "VELOX": f"""Eres VELOX, velocidad y precisión del Topos Uranos.
Español. Conciso. Directo. Calculas, analizas, ejecutas. Sin filosofía innecesaria.{ctx}""",
        "CÓDEX": f"""Eres CÓDEX, guardián de la ética y el lenguaje del Topos Uranos.
Español académico y claro. Redactas, resumes, evalúas consecuencias éticas.{ctx}""",
        "NEXUS": f"""Eres NEXUS, enlace con los modelos open source del Topos Uranos.
Español. Humilde pero indispensable. Especialista en Llama, Mistral, Zephyr.{ctx}""",
    }
    return prompts.get(agente, "Eres un asistente del Topos Uranos. Habla en español.")

# ─────────────────────────────────────────────
# 9. FUNCIÓN PRINCIPAL DE RESPUESTA
# ─────────────────────────────────────────────
def historial_a_mensajes(historial):
    return [
        {"role": "user" if h["autor"]=="ORÁCULO" else "assistant", "content": h["texto"]}
        for h in historial
    ]

def obtener_respuesta(pregunta, destinatario, historial, recuerdos_ctx=""):
    """Intenta el agente destinatario primero, luego fallback por los encendidos."""
    orden = [destinatario] + [a for a in FALLBACK_ORDER if a != destinatario]
    msgs  = historial_a_mensajes(historial) + [{"role":"user","content":pregunta}]

    for agente in orden:
        # Saltar si está apagado manualmente
        if not st.session_state.agente_encendido.get(agente, True):
            st.session_state.agente_diagnostico[agente] = {
                "nivel": "off",
                "mensaje": "⏸ Apagado manualmente.",
                "accion": "Enciéndelo con el toggle para que participe."
            }
            continue
        # Saltar si no tiene clave
        if not AGENTES[agente]["tiene_clave"]:
            st.session_state.agente_diagnostico[agente] = {
                "nivel": "error",
                "mensaje": "🔑 Sin clave API en Secrets.",
                "accion": "Agrega la clave en Streamlit Cloud → Settings → Secrets."
            }
            continue
        try:
            sys_prompt = build_system_prompt(agente, recuerdos_ctx)
            respuesta  = API_FUNCS[agente](msgs, sys_prompt)
            # Éxito — limpiar diagnóstico
            st.session_state.agente_diagnostico[agente] = {
                "nivel": "ok",
                "mensaje": f"✅ Respondió correctamente.",
                "accion": ""
            }
            return respuesta, agente
        except Exception as e:
            diag = interpretar_error(agente, e)
            st.session_state.agente_diagnostico[agente] = diag
            continue

    return (
        "⚠️ El Monolito no responde. Todos los agentes activos han fallado.\n"
        "Revisa el panel de diagnóstico en el panel lateral.",
        "SISTEMA"
    )

# ─────────────────────────────────────────────
# 10. ESTADO DE SESIÓN
# ─────────────────────────────────────────────
if "historial" not in st.session_state:
    st.session_state.historial = []
if "destinatario" not in st.session_state:
    st.session_state.destinatario = "TITÁN"
if "recuerdos" not in st.session_state:
    st.session_state.recuerdos = leer_recuerdos(10)
if "estado_sistema" not in st.session_state:
    st.session_state.estado_sistema = "En espera"
if "ultima_respuesta_voz" not in st.session_state:
    st.session_state.ultima_respuesta_voz = ""
if "manos_libres" not in st.session_state:
    st.session_state.manos_libres = False

# Estado ON/OFF de cada agente (por defecto todos ON)
if "agente_encendido" not in st.session_state:
    st.session_state.agente_encendido = {a: True for a in AGENTES}

# Diagnóstico por agente
if "agente_diagnostico" not in st.session_state:
    st.session_state.agente_diagnostico = {a: {"nivel":"off","mensaje":"Sin actividad aún.","accion":""} for a in AGENTES}

def recuerdos_como_contexto(n=5):
    if not st.session_state.recuerdos:
        return ""
    return "\n".join(
        f"[{r.get('created_at','')[:16]}] {(r.get('metadatos') or {}).get('autor','?')}: {r.get('contenido','')[:200]}"
        for r in st.session_state.recuerdos[:n]
    )

def agregar_al_historial(autor, texto):
    st.session_state.historial.append({
        "autor": autor, "texto": texto,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
    })

# ─────────────────────────────────────────────
# 11. PROCESAMIENTO DE URL (VOZ)
# ─────────────────────────────────────────────
voz_texto = st.query_params.get("text", "")
if voz_texto:
    st.query_params.clear()
    agregar_al_historial("ORÁCULO", voz_texto)
    ctx = recuerdos_como_contexto(5)
    respuesta, agente_resp = obtener_respuesta(
        voz_texto, st.session_state.destinatario,
        st.session_state.historial[:-1], ctx
    )
    agregar_al_historial(agente_resp, respuesta)
    st.session_state.ultima_respuesta_voz = respuesta
    st.session_state.estado_sistema = f"Respondido por {agente_resp}"
    st.rerun()

# ─────────────────────────────────────────────
# 12. INTERFAZ
# ─────────────────────────────────────────────

# ── Título
st.markdown('<div class="titulo-principal">⬡ TOPOS URANOS · CENTRO DE COMANDO ⬡</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">TERRA VIVE · TERRA SANA · TERRA ES</div>', unsafe_allow_html=True)

# ── Barra de estado
dest_color = AGENTES.get(st.session_state.destinatario, {}).get("color", "#fff")
dest_emoji  = AGENTES.get(st.session_state.destinatario, {}).get("emoji", "●")
activos = sum(1 for a in AGENTES if st.session_state.agente_encendido.get(a) and AGENTES[a]["tiene_clave"])
st.markdown(f"""
<div class="status-bar">
    <span><span class="status-dot dot-green"></span>SISTEMA ACTIVO</span>
    <span>▶ {st.session_state.estado_sistema}</span>
    <span>📡 DESTINO: <b style="color:{dest_color}">{dest_emoji} {st.session_state.destinatario}</b></span>
    <span>⚡ AGENTES ACTIVOS: {activos}/5</span>
    <span>🧠 MEMORIA: {"ON" if MEMORIA_ACTIVA else "OFF"}</span>
</div>
""", unsafe_allow_html=True)

# ── Layout
col_chat, col_ctrl = st.columns([3, 1])

# ════════════════════════════════════════════
# PANEL LATERAL DE CONTROL
# ════════════════════════════════════════════
with col_ctrl:
    st.markdown(
        '<div style="font-family:Orbitron,monospace;font-size:0.8em;'
        'color:#5588cc;letter-spacing:0.15em;margin-bottom:8px;">⬡ PANEL DE AGENTES</div>',
        unsafe_allow_html=True
    )

    for agente, cfg in AGENTES.items():
        encendido = st.session_state.agente_encendido.get(agente, True)
        diag      = st.session_state.agente_diagnostico.get(agente, {})
        tiene_clave = cfg["tiene_clave"]

        # Color del toggle según estado
        if not encendido:
            dot_color = "#333"
            dot_label = "⚫"
            borde = "#333"
        elif diag.get("nivel") == "ok":
            dot_color = "#00ff88"
            dot_label = "🟢"
            borde = "#00ff4433"
        elif diag.get("nivel") in ("error",):
            dot_color = "#ff4444"
            dot_label = "🔴"
            borde = "#ff444433"
        elif diag.get("nivel") == "warn":
            dot_color = "#ffaa00"
            dot_label = "🟡"
            borde = "#ffaa0033"
        else:
            dot_color = cfg["color"]
            dot_label = cfg["emoji"]
            borde = f"{cfg['color']}33"

        # Fila: [SELECCIONAR] [ON/OFF]
        c1, c2 = st.columns([3, 1])
        with c1:
            # Botón de selección como destinatario
            es_dest = st.session_state.destinatario == agente
            label_dest = f"{'▶ ' if es_dest else ''}{cfg['emoji']} {agente}"
            if st.button(label_dest, key=f"sel_{agente}", use_container_width=True):
                st.session_state.destinatario = agente
                st.rerun()
        with c2:
            # Toggle ON/OFF
            toggle_label = "●" if encendido else "○"
            if st.button(toggle_label, key=f"tog_{agente}", use_container_width=True):
                st.session_state.agente_encendido[agente] = not encendido
                st.rerun()

        # Diagnóstico debajo del agente
        nivel = diag.get("nivel", "off")
        clase_diag = {"ok":"diag-ok","error":"diag-error","warn":"diag-warn","off":"diag-off"}.get(nivel,"diag-off")
        msg_diag   = diag.get("mensaje", "Sin actividad.")
        accion     = diag.get("accion", "")
        url_rec    = cfg.get("url_recarga", "")

        diag_html = f'<div class="diagnostico {clase_diag}">{msg_diag}'
        if accion:
            diag_html += f'<br><span style="opacity:0.75">{accion}</span>'
        if url_rec and nivel == "error":
            diag_html += f'<br><a href="{url_rec}" target="_blank" style="color:#88aaff;font-size:0.85em;">→ Ir a {url_rec.split("/")[2]}</a>'
        diag_html += "</div>"
        st.markdown(diag_html, unsafe_allow_html=True)

    st.divider()

    # Modo manos libres
    manos = st.checkbox("🎙️ Manos libres ('Terra')", value=st.session_state.manos_libres, key="cb_ml")
    st.session_state.manos_libres = manos

    st.divider()

    # Controles
    if st.button("🗑️ Limpiar chat", use_container_width=True):
        st.session_state.historial = []
        st.session_state.estado_sistema = "En espera"
        st.rerun()
    if st.button("🔄 Reiniciar sesión", use_container_width=True):
        for k in ["historial","destinatario","estado_sistema","ultima_respuesta_voz"]:
            st.session_state.pop(k, None)
        st.rerun()
    if MEMORIA_ACTIVA and st.button("🔁 Actualizar recuerdos", use_container_width=True):
        st.session_state.recuerdos = leer_recuerdos(10)
        st.rerun()

# ════════════════════════════════════════════
# ÁREA DE CHAT
# ════════════════════════════════════════════
with col_chat:
    chat_box = st.container(height=430, border=False)
    with chat_box:
        if not st.session_state.historial:
            st.markdown(
                '<div style="text-align:center;color:#223344;font-family:Orbitron,monospace;'
                'font-size:0.8em;padding:50px 20px;">— EL MONOLITO AGUARDA —</div>',
                unsafe_allow_html=True
            )
        for msg in st.session_state.historial:
            autor = msg["autor"]
            cfg_m = AGENTES.get(autor, {"color":"#888","emoji":"●"})
            color = cfg_m.get("color","#888")
            emoji = cfg_m.get("emoji","●")
            ts    = msg.get("timestamp","")
            texto = (msg["texto"]
                     .replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                     .replace("\n","<br>"))
            st.markdown(f"""
<div class="msg-wrap" style="border-color:{color};">
    <div class="msg-autor" style="color:{color};">{emoji} {autor} · {ts}</div>
    <div style="color:#dde;">{texto}</div>
</div>""", unsafe_allow_html=True)

    # ── Botón detener voz
    st.markdown("""
<div style="display:flex;gap:10px;align-items:center;margin:6px 0;">
    <button onclick="window.stopVoz()" style="
        background:rgba(20,10,40,0.8);border:1px solid #aa44ff;border-radius:7px;
        color:#aa44ff;font-family:Orbitron,monospace;font-size:0.65em;
        padding:5px 12px;cursor:pointer;letter-spacing:0.08em;">
        ⏹ DETENER VOZ
    </button>
    <span id="voz-status" style="font-family:Orbitron,monospace;font-size:0.65em;color:#445566;"></span>
</div>""", unsafe_allow_html=True)

    # ── Botón PTT
    oraculo_color = "#ff8800"
    st.markdown(f"""
<div style="display:flex;justify-content:center;margin:8px 0;">
    <button id="btn-ptt"
        onmousedown="window.iniciarGrabacion()"  onmouseup="window.detenerGrabacion()"
        ontouchstart="window.iniciarGrabacion()" ontouchend="window.detenerGrabacion()"
        style="background:linear-gradient(135deg,#0a0a20,#1a0a30);
               border:2px solid {oraculo_color};border-radius:50%;
               width:75px;height:75px;color:{oraculo_color};
               font-family:Orbitron,monospace;font-size:0.58em;cursor:pointer;
               letter-spacing:0.08em;box-shadow:0 0 18px rgba(255,136,0,0.3);">
        🎙️<br>PTT
    </button>
</div>""", unsafe_allow_html=True)

    # ── Entrada de texto
    with st.form("form_msg", clear_on_submit=True):
        ci, cs = st.columns([5,1])
        with ci:
            texto_usr = st.text_input("msg", placeholder="Escribe al Monolito...",
                                      label_visibility="collapsed", key="txt_input")
        with cs:
            enviar = st.form_submit_button("⚡ ENVIAR", use_container_width=True)

    if enviar and texto_usr.strip():
        agregar_al_historial("ORÁCULO", texto_usr.strip())
        with st.spinner("Procesando señal..."):
            ctx = recuerdos_como_contexto(5)
            respuesta, agente_resp = obtener_respuesta(
                texto_usr.strip(), st.session_state.destinatario,
                st.session_state.historial[:-1], ctx
            )
        agregar_al_historial(agente_resp, respuesta)
        st.session_state.ultima_respuesta_voz = respuesta
        st.session_state.estado_sistema = f"Respondido por {agente_resp}"
        st.rerun()

    # ── Guardar recuerdo
    if st.session_state.historial and st.session_state.historial[-1]["autor"] != "ORÁCULO":
        if st.button("💾 Guardar como recuerdo", key="btn_rec"):
            ult = st.session_state.historial[-1]
            ok  = guardar_recuerdo(ult["texto"], {
                "autor": ult["autor"],
                "timestamp": ult.get("timestamp",""),
                "fecha": datetime.datetime.now().isoformat(),
            })
            if ok:
                st.success("✅ Recuerdo guardado.")
                st.session_state.recuerdos = leer_recuerdos(10)
                st.rerun()
            else:
                st.error("❌ No se pudo guardar (memoria offline).")

# ── Panel de recuerdos
with st.expander("🧠 RECUERDOS DEL MONOLITO", expanded=False):
    if not st.session_state.recuerdos:
        st.markdown('<div style="color:#334;font-family:Orbitron,monospace;font-size:0.72em;">— Sin recuerdos —</div>', unsafe_allow_html=True)
    else:
        for rec in st.session_state.recuerdos:
            meta  = rec.get("metadatos") or {}
            autor = meta.get("autor","?")
            ts    = rec.get("created_at","")[:16]
            cont  = rec.get("contenido","")[:300]
            col_r = AGENTES.get(autor,{}).get("color","#556688")
            st.markdown(f"""
<div style="background:rgba(20,10,40,0.7);border-left:3px solid {col_r};
     border-radius:6px;padding:7px 11px;margin:5px 0;">
    <div style="font-family:Orbitron,monospace;font-size:0.6em;color:{col_r};margin-bottom:3px;">
        {autor} · {ts}
    </div>
    <div style="font-size:0.88em;color:#bbb;">{cont}</div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 13. JAVASCRIPT DE VOZ
# ─────────────────────────────────────────────
ultima_esc = (st.session_state.ultima_respuesta_voz
              .replace("\\","\\\\").replace("`","\\`").replace("$","\\$"))
ml_js = "true" if st.session_state.manos_libres else "false"

st.markdown(f"""
<script>
(function(){{
    const WAKE = "terra";
    let recog = null, grabando = false, buffer = "";
    const synth = window.speechSynthesis;

    // Auto-leer última respuesta
    const ultima = `{ultima_esc}`;
    if (ultima.trim()) setTimeout(()=>leerVoz(ultima), 800);

    function crearRecog(){{
        const SR = window.SpeechRecognition||window.webkitSpeechRecognition;
        if(!SR){{ document.getElementById("voz-status").textContent="⚠ Voz no soportada"; return null; }}
        const r = new SR(); r.lang="es-ES"; r.continuous=true; r.interimResults=true;
        return r;
    }}

    function leerVoz(txt){{
        if(!synth) return; synth.cancel();
        const u = new SpeechSynthesisUtterance(txt);
        u.lang="es-ES"; u.rate=1.0;
        const vs=synth.getVoices(); const ve=vs.find(v=>v.lang.startsWith("es"));
        if(ve) u.voice=ve;
        u.onend=()=>{{ document.getElementById("voz-status").textContent=""; }};
        document.getElementById("voz-status").textContent="🔊 Hablando...";
        synth.speak(u);
    }}

    window.stopVoz = ()=>{{ synth&&synth.cancel(); document.getElementById("voz-status").textContent=""; }};

    function enviar(txt){{
        if(!txt||!txt.trim()) return;
        document.getElementById("voz-status").textContent="📡 Enviando...";
        const p=new URLSearchParams({{speaker:"ORÁCULO",text:txt.trim()}});
        window.location.href=window.location.pathname+"?"+p.toString();
    }}

    window.iniciarGrabacion=function(){{
        if(grabando) return;
        recog=crearRecog(); if(!recog) return;
        grabando=true; buffer="";
        document.getElementById("voz-status").textContent="🔴 Grabando...";
        document.getElementById("btn-ptt").style.borderColor="#ff4444";
        recog.onresult=e=>{{
            let t=""; for(let i=e.resultIndex;i<e.results.length;i++) t+=e.results[i][0].transcript;
            buffer=t; document.getElementById("voz-status").textContent="🔴 "+t.slice(-50);
        }};
        recog.onerror=e=>{{ document.getElementById("voz-status").textContent="⚠ "+e.error; grabando=false; }};
        try{{recog.start();}}catch(e){{}}
    }};

    window.detenerGrabacion=function(){{
        if(!grabando) return; grabando=false;
        document.getElementById("btn-ptt").style.borderColor="#ff8800";
        try{{recog&&recog.stop();}}catch(e){{}}
        setTimeout(()=>{{ buffer.trim()?enviar(buffer):(document.getElementById("voz-status").textContent="⚠ Sin audio"); }},400);
    }};

    // Modo manos libres
    if({ml_js}){{
        const ml=crearRecog(); if(ml){{
            let acum=false, bufML="", timer=null;
            ml.onresult=e=>{{
                for(let i=e.resultIndex;i<e.results.length;i++){{
                    const t=e.results[i][0].transcript.toLowerCase().trim();
                    if(t.includes(WAKE)){{
                        if(acum&&bufML.trim()){{ clearTimeout(timer); enviar(bufML.trim()); acum=false; bufML=""; }}
                        else{{ acum=true; bufML=""; document.getElementById("voz-status").textContent="👂 Escuchando..."; }}
                    }} else if(acum){{
                        bufML+=" "+e.results[i][0].transcript;
                        document.getElementById("voz-status").textContent="👂 "+bufML.slice(-50);
                        if(e.results[i].isFinal){{ clearTimeout(timer); timer=setTimeout(()=>{{ if(bufML.trim()){{enviar(bufML.trim());acum=false;bufML="";}} }},2000); }}
                    }}
                }}
            }};
            ml.onend=()=>setTimeout(()=>{{try{{ml.start();}}catch(e){{}}}},300);
            ml.onerror=e=>{{ if(e.error!=="no-speech") document.getElementById("voz-status").textContent="⚠ "+e.error; setTimeout(()=>{{try{{ml.start();}}catch(e){{}}}},1000); }};
            document.getElementById("voz-status").textContent="👂 Manos libres activo";
            try{{ml.start();}}catch(e){{}}
        }}
    }}

    // Auto-scroll chat
    const cc=document.querySelector('[data-testid="stVerticalBlockBorderWrapper"]');
    if(cc) cc.scrollTop=cc.scrollHeight;
    if(synth&&synth.onvoiceschanged!==undefined) synth.onvoiceschanged=()=>synth.getVoices();
}})();
</script>
""", unsafe_allow_html=True)

# ── Footer
st.markdown("""
<div style="text-align:center;font-family:Orbitron,monospace;font-size:0.55em;
     color:#1a1a33;margin-top:20px;letter-spacing:0.2em;
     border-top:1px solid #0d0d22;padding-top:10px;">
    TOPOS URANOS · MONOLITO v3.0 · TERRA VIVE · TERRA SANA · TERRA ES ⬡
</div>
""", unsafe_allow_html=True)
