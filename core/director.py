import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

class DirectorAgent:
    def __init__(self):
        # Usamos Flash porque es más rápido para tareas lógicas simples
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
        self.prompt = PromptTemplate.from_template(
            "Eres el Director de la historia. Analiza el mensaje del usuario (Elías). "
            "Personajes disponibles: John, Freddie, Brian, Roger. "
            "Devuelve ÚNICAMENTE un array JSON con los nombres de los personajes que deben responder. "
            "Ejemplo: [\"John\", \"Freddie\"]. Si es ambiguo, elige al menos a John. "
            "\n\nMensaje de Elías: {mensaje}"
        )
    
    def route(self, message: str) -> list:
        chain = self.prompt | self.llm
        respuesta = chain.invoke({"mensaje": message}).content
        try:
            clean_json = respuesta.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        except json.JSONDecodeError:
            return ["John"]