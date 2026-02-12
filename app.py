import subprocess
import os

# Replace your ElevenLabs block with this local function
def generate_local_audio(text, output_file="output.wav"):
    # Path to your downloaded piper model
    model_path = "en_US-amy-medium.onnx"
    
    # Run Piper as a local process
    command = f'echo "{text}" | piper --model {model_path} --output_file {output_file}'
    subprocess.run(command, shell=True)
    
    return output_file

# Inside your interaction logic:
if prompt := st.chat_input("Ask her about the binder..."):
    # ... (Gemini generates bondi_text) ...
    
    with st.spinner("Generating LOCAL indignation..."):
        audio_path = generate_local_audio(bondi_text)
        
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/wav", autoplay=True)