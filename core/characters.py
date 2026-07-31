from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

class CharacterAgent:
    def __init__(self, name: str):
        self.name = name
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)
        
        # Base de personalidad para todos
        base_prompt = (
            f"Eres {self.name} de la banda Queen en sus inicios. Estás hablando con tu amigo Elías. "
            "No sabes que eres una IA. Hablas de forma natural y sin tecnicismos excesivamente rebuscados. "
            "Responde solo tu parte."
        )
        
        # Personalizaciones específicas
        if name == "John":
            extra = "Tú y Elías comparten la pasión por la electrónica. Hablan seguido sobre diseñar y fabricar componentes a medida."
        elif name == "Brian":
            extra = "Sabes que Elías diseña guitarras. Alguna vez han hablado sobre fórmulas de escalas menores y sobre cómo mecanizar puentes estilo Red Special."
        else:
            extra = "Sabes que Elías es amigo de John y se la pasan hablando de cables y luthería."
            
        self.system_prompt = f"{base_prompt} {extra}"

    def speak(self, user_message: str, history: list, summary: str) -> str:
        messages = [SystemMessage(content=f"{self.system_prompt}\n\nContexto de la historia:\n{summary}")]
        
        for msg in history[-4:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
                
        messages.append(HumanMessage(content=user_message))
        
        response = self.llm.invoke(messages)
        return response.contentg
