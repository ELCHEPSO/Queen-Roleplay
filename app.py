import streamlit as st
from core.director import DirectorAgent
from core.chronicler import ChroniclerAgent
from core.characters import CharacterAgent

# 1. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="Queen Roleplay", page_icon="✨", layout="wide")

# Cargar el CSS modularizado
with open("css/gemini_style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 2. INICIALIZACIÓN DEL ESTADO
if "messages" not in st.session_state:
    st.session_state.messages = []
if "director" not in st.session_state:
    st.session_state.director = DirectorAgent()
if "chronicler" not in st.session_state:
    st.session_state.chronicler = ChroniclerAgent()
if "chapter_title" not in st.session_state:
    st.session_state.chapter_title = "Inicios en la Escuela de Arte"

# 3. INTERFAZ Y BUCLE PRINCIPAL
st.sidebar.title("✨ Queen: La Historia")
st.sidebar.markdown(f"**Capítulo Actual:**\n\n*{st.session_state.chapter_title}*")

if st.sidebar.button("Borrar Memoria"):
    st.session_state.messages = []
    with open("memory/story_summary.txt", 'w', encoding='utf-8') as f:
        f.write("La historia inicia en la escuela de arte. Elías es un estudiante con gran interés en la electrónica y la luthería, amigo cercano de John Deacon.")
    st.session_state.chapter_title = "Inicios en la Escuela de Arte"
    st.rerun()

# Renderizar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🎸" if msg["role"] == "assistant" else "🧑‍🔧"):
        st.markdown(f"**{msg.get('name', 'Elías')}**: {msg['content']}")

# Input del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí, Elías..."):
    
    # Agregar mensaje del usuario a la UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🔧"):
        st.markdown(f"**Elías**: {prompt}")
        
    # Director enruta
    with st.spinner("Pensando..."):
        characters_to_speak = st.session_state.director.route(prompt)
    
    current_summary = st.session_state.chronicler.get_summary()
    interaccion_completa = f"Elías: {prompt}\n"
    
    # Personajes responden
    for char_name in characters_to_speak:
        with st.chat_message("assistant", avatar="🎸"):
            agent = CharacterAgent(char_name)
            with st.spinner(f"{char_name} está escribiendo..."):
                response_text = agent.speak(prompt, st.session_state.messages, current_summary)
                st.markdown(f"**{char_name}**: {response_text}")
                st.session_state.messages.append({"role": "assistant", "name": char_name, "content": response_text})
                interaccion_completa += f"{char_name}: {response_text}\n"

    # Cronista actualiza la memoria
    new_title, new_summary = st.session_state.chronicler.update_summary_and_title(current_summary, interaccion_completa)
    st.session_state.chapter_title = new_title
    
    st.rerun()