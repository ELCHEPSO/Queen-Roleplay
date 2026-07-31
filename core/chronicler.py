import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

class ChroniclerAgent:
    def __init__(self, memory_file="memory/story_summary.txt"):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)
        self.memory_file = memory_file
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                f.write("La historia inicia en la escuela de arte. Elías es un estudiante con gran interés en la electrónica y la luthería, amigo cercano de John Deacon.")

    def get_summary(self) -> str:
        with open(self.memory_file, 'r', encoding='utf-8') as f:
            return f.read()

    def update_summary_and_title(self, current_summary: str, last_interaction: str):
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
                
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            f.write(nuevo_resumen)
            
        return titulo, nuevo_resumen