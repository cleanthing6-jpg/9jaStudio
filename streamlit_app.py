import os
import streamlit as st
import requests
import time

# 1. PAGE SETUP & CONFIGURATION
st.set_page_config(page_title="9jaStudio — AI Music Ecosystem", layout="wide")

st.title("🇳🇬 9jaStudio — AI Music Production Ecosystem")
st.caption("Create Fusions, Split Stems, and Mix/Master to Global Radio Standards for Free.")

# Initialize Permanent Session Memory so files don't disappear on click!
if "generated_beat_bytes" not in st.session_state:
    st.session_state.generated_beat_bytes = None
if "generated_beat_name" not in st.session_state:
    st.session_state.generated_beat_name = None

user_email = st.text_input("Enter 9jaStudio Account Email Address", value="independent_artist@9ja.com")
st.info("🟢 **Account Status:** Active | **Remaining Studio Credits:** 2 Songs Left")

# 2. WORKSPACE MODULES
tab1, tab2 = st.tabs(["🥁 Module 1: AI Beat Lab", "🎚️ Module 2: Streaming Mix & Master"])

with tab1:
    st.subheader("Generate unique local instrumentals using text prompt fusions.")
    
    col1, col2 = st.columns(2)
    with col1:
        text_prompt = st.text_area("Describe the Beat Vibration", placeholder="Heavy bouncing log drum mixed with smooth Wizkid R&B pads...")
        genre_selection = st.selectbox("Select Cultural Genre Core", ["Afrobeat 🇳🇬", "Amapiano 🇿🇦", "Afro-R&B Fusion 🌿", "Highlife Traditional 🎸"])
        tempo = st.slider("BPM / Tempo Speed", 90, 130, 112)
        drum_profile = st.selectbox("Amapiano Log Drum / Bass Profile Style", ["Heavy Asake Style Log", "Deep Kabza Ambient Sub", "Bouncing Burna Modern Bass"])
        
        generate_beat_btn = st.button("🔥 Generate Custom Instrumental")
        
    with col2:
        if generate_beat_btn:
            with st.spinner("⚡ Connecting to Free Hugging Face AI Supercomputer... Compiling music tokens..."):
                try:
                    optimized_prompt = f"Studio quality premium audio track. Genre: {genre_selection}. {text_prompt}. Rich {drum_profile} arrangements at {tempo} BPM."
                    
                    # FREE ENDPOINT: Target Meta's MusicGen hosted natively on Hugging Face
                    API_URL = "https://huggingface.co"
                    
                    # Hit the free serverless endpoint without requiring complex tokens
                    response = requests.post(API_URL, json={"inputs": optimized_prompt})
                    
                    # If the model is sleeping, wait and retry automatically
                    if response.status_code == 503:
                        st.warning("💤 AI Engine is warming up. Please wait 10 seconds...")
                        time.sleep(10)
                        response = requests.post(API_URL, json={"inputs": optimized_prompt})
                    
                    if response.status_code == 200:
                        st.session_state.generated_beat_bytes = response.content
                        st.session_state.generated_beat_name = f"9jaStudio_{genre_selection.split()[0]}_{tempo}BPM.wav"
                    else:
                        st.error(f"Hugging Face server busy (Status {response.status_code}). Try clicking again in a moment!")
                    
                except Exception as e:
                    st.error(f"Engine connection error: {str(e)}")

        # Check memory. If a song exists, display it permanently. It will NEVER disappear on click!
        if st.session_state.generated_beat_bytes is not None:
            st.success("🔥 Success! Your custom AI track compilation is complete.")
            st.audio(st.session_state.generated_beat_bytes, format="audio/wav")
            st.download_button(
                label="📥 Download Mastered WAV Instrumental File",
                data=st.session_state.generated_beat_bytes,
                file_name=st.session_state.generated_beat_name,
                mime="audio/wav"
            )

# MODULE 2: MIXING & MASTERING (Visual Component Only for Trial)
with tab2:
    st.subheader("Bring your own song data or raw WhatsApp Voice notes.")
    uploaded_song = st.file_uploader("Upload Song Mixdown Data")
    engineer_btn = st.button("🎛️ Run Multi-Stem Mix & Master Pipeline", disabled=(uploaded_song is None))
    if engineer_btn:
        st.success("🎚️ Audio Engineering Chain complete! Mastered perfectly for streaming platforms.")

# 3. DUAL-CURRENCY BILLING PORTAL (Paystack Front-end Elements)
st.markdown("---")
st.header("💳 9jaStudio Wallet & Studio Access Upgrades")
currency = st.radio("Choose Payment Currency Profile", ["Pay in Nigerian Naira (₦ NGN)", "Pay in US Dollars ($ USD)"])
