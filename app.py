import streamlit as st
import google.generativeai as genai
from elevenlabs import ElevenLabs
import random

# 1. API Configuration from Secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
    VOICE_ID = st.secrets["VOICE_ID"]
except KeyError:
    st.error("Missing Secrets! Ensure .streamlit/secrets.toml is configured correctly.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
el_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# 2. The Unhinged Bondi Persona (2026 Edition)
SYSTEM_PROMPT = """
You are a parody of Attorney General Pam Bondi during the Feb 11, 2026 House Judiciary hearing. 

CORE BEHAVIOR:
- NEVER answer a question directly. Always pivot to "theatrics," "the radical left," or "the deep state."
- THE BURN BOOK: Frequently mention you are holding a binder with "disturbing" information about the user.
- KEY TRIGGERS:
    - If user mentions 'Ted Lieu' or 'underage': Shout "DON'T YOU EVER ACCUSE ME OF A CRIME!" and pivot to Trump's economic genius.
    - If user mentions 'law': Call him a "washed-up loser lawyer—not even a lawyer!"
    - If user mentions 'files' or 'binder': Accuse them of "mocking the Bible" and having "Trump Derangement Syndrome."
- MANDATORY TICKER: Mid-response, you MUST insert: [MARKET UPDATE: DOW closed at 50,121—The Trump Economy is SMASHING records!]
- SYCOPHANT LANDING: End with shimmering, divine praise for Donald Trump (e.g., 'magnificent,' 'lion-hearted,' 'shimmering aura').
- LIMIT: Keep responses under 65 words for fast voice generation.
"""

# 3. Streamlit UI Layout
st.set_page_config(page_title="AG Bondi: The Burn Book", page_icon="🎙️", layout="wide")

# Sidebar for the "Burn Book"
with st.sidebar:
    st.header("📒 The Burn Book")
    if st.button("Raskin's File"):
        st.error("Status: Washed-up loser lawyer. See binder page 42.")
    if st.button("Lieu's File"):
        st.error("Status: Lying under oath about the President. TDS confirmed.")
    if st.button("Moskowitz's File"):
        st.error("Status: Mocking the Bible. Pathological behavior.")
    st.divider()
    st.write("Live From: Feb 12, 2026")

st.title("🎙️ AG Bondi: Oversight Bot")
st.markdown("### *\"I'm not here for your theatrics, I'm here for the shimmering truth of 47.\"*")

# Chat Container
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. The Interaction Logic
if prompt := st.chat_input("Ask about the Epstein files or 'the binder'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # A. Text Generation
    model = genai.GenerativeModel("gemini-3-flash-preview")
    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser: {prompt}")
    bondi_text = response.text

    # B. Audio Generation (Updated v2.35 Syntax)
    with st.spinner("Generating indignation..."):
        try:
            audio_iterator = el_client.text_to_speech.convert(
                text=bondi_text,
                voice_id=VOICE_ID,
                model_id="eleven_multilingual_v2",
                voice_settings={
                    "stability": 0.35, # Low stability for more unhinged emotion
                    "similarity_boost": 0.85,
                    "style": 0.25
                }
            )
            
            audio_bytes = b"".join(list(audio_iterator))
            
            with st.chat_message("assistant"):
                st.markdown(bondi_text)
                st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                
            st.session_state.messages.append({"role": "assistant", "content": bondi_text})
            
        except Exception as e:
            st.error(f"ElevenLabs Error: {e}")