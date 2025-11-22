import streamlit as st
from mistralai import Mistral
import PyPDF2

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Asesor Jurídico)", layout="wide", page_icon="⚡")

# 2. ESTILOS CSS
st.markdown("""
<style>
    .fixed-bar {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        background-color: #0E1117 !important;
        z-index: 999999 !important;
        border-top: 1px solid #303030 !important;
        padding: 10px 20px !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
    }
    .file-indicator {
        background-color: #1E2329;
        color: #4CAF50;
        padding: 8px 15px;
        border-radius: 8px;
        font-size: 0.9rem;
        margin-bottom: 10px;
        border: 1px solid #4CAF50;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .block-container { padding-bottom: 160px !important; }

    @media (max-width: 768px) {
        .fixed-bar { padding: 10px 5px !important; }
        div[data-testid="stForm"] { gap: 0.5rem; }
    }
    div[data-testid="stPopover"] > button { border: none; background: transparent; font-size: 24px; }
</style>
""", unsafe_allow_html=True)

# 3. CLIENTE MISTRAL
try:
    api_key = st.secrets["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    # Usamos el modelo rápido
    MODELO = "mistral-small-latest"
except Exception as e:
    st.error(f"Error de API Key: {e}")

st.title("Asesor Jurídico")


# 4. FUNCIÓN LEER PDF
def extraer_texto_pdf(archivo):
    try:
        reader = PyPDF2.PdfReader(archivo)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text() or ""
        return texto
    except:
        return ""


# 5. MEMORIA
if "messages" not in st.session_state:
    st.session_state.messages = []
if "contexto_documento" not in st.session_state:
    st.session_state.contexto_documento = ""
if "nombre_archivo_activo" not in st.session_state:
    st.session_state.nombre_archivo_activo = None

# 6. MOSTRAR HISTORIAL
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('<div style="height: 120px;"></div>', unsafe_allow_html=True)

# 7. BARRA INFERIOR
with st.container():
    st.markdown('<div class="fixed-bar">', unsafe_allow_html=True)

    # Indicador visual (si ya había uno cargado previamente)
    if st.session_state.nombre_archivo_activo:
        st.markdown(f"""
        <div class='file-indicator'>
            ⚡ <b>Memoria activa:</b> {st.session_state.nombre_archivo_activo}
        </div>
        """, unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([1, 8, 1.5], gap="small")
        with col1:
            with st.popover("📎", help="Cargar documento"):
                files = st.file_uploader("PDF", accept_multiple_files=True, type=['pdf', 'txt'])
        with col2:
            prompt_usuario = st.text_input("Mensaje", placeholder="Escribe algo o solo envía el archivo...",
                                           label_visibility="collapsed")
        with col3:
            submit = st.form_submit_button("➤")
    st.markdown('</div>', unsafe_allow_html=True)

# 8. LÓGICA DE ENVÍO (MODIFICADA PARA RESPONDER AL INSTANTE)
if submit:
    # A. PROCESAMIENTO DE ARCHIVOS
    hay_archivos_nuevos = False

    if files:
        texto_acumulado = ""
        nombres = []
        for f in files:
            txt = ""
            if f.type == "application/pdf":
                txt = extraer_texto_pdf(f)
            elif f.type == "text/plain":
                txt = str(f.read(), 'utf-8')

            texto_acumulado += f"\n--- DOC {f.name} ---\n{txt}\n"
            nombres.append(f.name)

        # Recorte rápido (50k caracteres)
        if len(texto_acumulado) > 50000:
            texto_acumulado = texto_acumulado[:50000] + "\n... [RECORTADO]"

        # Guardamos en memoria
        st.session_state.contexto_documento = texto_acumulado
        st.session_state.nombre_archivo_activo = ", ".join(nombres)
        hay_archivos_nuevos = True

        # TRUCO: Si subió archivo pero NO escribió pregunta, inventamos una automática
        if not prompt_usuario:
            prompt_usuario = "¡He subido un documento! Resúmelo brevemente y dime de qué trata."

    # B. GENERACIÓN DE RESPUESTA
    # Entramos aquí si el usuario escribió algo O si acabamos de inventar el prompt automático
    if prompt_usuario:

        # Guardar mensaje en historial
        st.session_state.messages.append({"role": "user", "content": prompt_usuario})
        with st.chat_message("user"):
            st.write(prompt_usuario)

        # Generar respuesta
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_text = ""
            try:
                instrucciones = """
                Eres un asistente ULTRA RÁPIDO.
                REGLAS:
                1. Responde en MÁXIMO 3 PARRAFOS CORTOS.
                2. Ve directo al grano.
                3. Si te piden resumir, destaca solo lo más vital.
                4. Haz lo que pida la persona
                
                """

                mensajes_api = [{"role": "system", "content": instrucciones}]

                # Contexto del documento
                if st.session_state.contexto_documento:
                    mensajes_api.append({
                        "role": "user",
                        "content": f"DOCUMENTO:\n{st.session_state.contexto_documento}"
                    })

                # Pregunta actual
                mensajes_api.append({"role": "user", "content": prompt_usuario})

                stream_response = client.chat.stream(
                    model=MODELO,
                    messages=mensajes_api
                )

                for chunk in stream_response:
                    if chunk.data.choices[0].delta.content:
                        full_text += chunk.data.choices[0].delta.content
                        placeholder.markdown(full_text + "▌")

                placeholder.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})

                # Si hubo archivos nuevos, forzamos recarga AL FINAL para actualizar la barra verde
                if hay_archivos_nuevos:
                    st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")