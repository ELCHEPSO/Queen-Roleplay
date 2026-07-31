import streamlit as st
from supabase import create_client, Client
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

class ChroniclerAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)
        
        # 1. Conectar a Supabase usando los secretos de Streamlit
        url: str = st.secrets["SUPABASE_URL"]
        key: str = st.secrets["SUPABASE_KEY"]
        self.supabase: Client = create_client(url, key)
        
        # 2. Inicializar la memoria en la nube si está vacía
        # Usamos el id=1 para guardar siempre el resumen principal de esta historia
        response = self.supabase.table("story_memory").select("*").eq("id", 1).execute()
        
        if not response.data:
            estado_inicial = "La historia inicia en la escuela de arte. Elías es un estudiante con gran interés en la electrónica y la luthería, amigo cercano de John Deacon."
            self.supabase.table("story_memory").insert({"id": 1, "summary": estado_inicial}).execute()

    def get_summary(self) -> str:
        # Extraer el resumen directamente de la nube
        response = self.supabase.table("story_memory").select("summary").eq("id", 1).execute()
        if response.data:
            return response.data[0]["summary"]
        return "Error al cargar la memoria."

    def update_summary_and_title(self, current_summary: str, last_interaction: str):
        # ¡La cadena de LangChain se queda igual!
        prompt = PromptTemplate.from_template(
            "Eres el Cronista. Basado en el resumen actual y la última interacción, genera: "
            "1. Un nuevo título corto para este capítulo. "
            "2. Un resumen actualizado e integrador (max 3 párrafos). "
            "Formato estricto:\nTITULO: [Título]\nRESUMEN: [Resumen]\n\n"
            "Resumen Actual: {summary}\nÚltima interacción: {interaction}"
        )
        chain = prompt | self.llm
        respuesta = chain.invoke({"summary": current_summary, "interaction": last_interaction}).content
        
        titulo = "Capítulo Desconocido"
        nuevo_resumen = current_summary
        
        for linea in respuesta.split('\n'):
            if linea.startswith("TITULO:"):
                titulo = linea.replace("TITULO:", "").strip()
            elif linea.startswith("RESUMEN:"):
                nuevo_resumen = respuesta.split("RESUMEN:")[1].strip()
                
        # 3. Guardar el nuevo resumen sobreescribiendo el anterior en Supabase
        self.supabase.table("story_memory").update({"summary": nuevo_resumen}).eq("id", 1).execute()
            
        return titulo, nuevo_resumen
