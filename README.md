# 🌪️ Chat PDF con Mistral AI - "Profe Mistral"

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red)
![Mistral AI](https://img.shields.io/badge/AI-Mistral_Large-orange)

Una aplicación inteligente que te permite chatear con tus documentos PDF y archivos de texto. Desarrollada con *Streamlit* y la potencia de *Mistral AI*, esta herramienta actúa como un profesor paciente que explica conceptos complejos de forma sencilla.

## 🚀 Características Principales

* *🧠 IA Avanzada:* Utiliza el modelo mistral-large-latest para una comprensión profunda del texto.
* *📄 Análisis de Documentos:* Sube múltiples archivos PDF o TXT y la IA leerá su contenido automáticamente.
* *👨‍🏫 Personalidad "Profe":* El sistema está instruido para explicar temas técnicos con analogías sencillas y lenguaje cercano.
* *📱 Diseño Responsive:* Interfaz optimizada con CSS personalizado para funcionar perfectamente en PC y Móviles.
* *✂️ Gestión de Memoria:* Sistema inteligente que recorta documentos excesivamente largos y optimiza el historial del chat para evitar errores de tokens.

## 🛠️ Instalación y Uso Local

Sigue estos pasos para ejecutar el proyecto en tu máquina:

1.  *Clonar el repositorio:*
    bash
    git clone [https://github.com/TU_USUARIO/chat-pdf-mistral.git](https://github.com/TU_USUARIO/chat-pdf-mistral.git)
    cd chat-pdf-mistral
    

2.  *Crear un entorno virtual (Opcional pero recomendado):*
    bash
    python -m venv .venv
    source .venv/bin/activate  # En Mac/Linux
    .\.venv\Scripts\activate   # En Windows
    

3.  *Instalar dependencias:*
    bash
    pip install -r requirements.txt
    

4.  *Configurar la API Key:*
    Crea una carpeta llamada .streamlit en la raíz y dentro un archivo secrets.toml:
    toml
    # .streamlit/secrets.toml
    MISTRAL_API_KEY = "PEGAR_TU_CLAVE_DE_MISTRAL_AQUI"
    

5.  *Ejecutar la aplicación:*
    bash
    streamlit run app.py
    

## ⚙️ Tecnologías Utilizadas

* **[Streamlit](https://streamlit.io/):** Para la interfaz de usuario web interactiva.
* **[Mistral AI SDK](https://docs.mistral.ai/):** Motor de inteligencia artificial generativa.
* **[PyPDF2](https://pypi.org/project/PyPDF2/):** Para la extracción de texto desde archivos PDF.

## 📸 Capturas de Pantalla

(Aquí puedes subir una imagen de tu app funcionando si quieres impresionar más a los jueces)

## 📄 Licencia

Este proyecto fue creado para propósitos educativos y de demostración.

---
Hecho con ❤️ para el Hackathon de IA.
}
