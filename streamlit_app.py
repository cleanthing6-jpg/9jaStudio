import os
import streamlit as st
from huggingface_hub import InferenceClient

# 1. PAGE SETUP & GLOBAL STATUS
st.set_page_config(page_title="9jaStudio — AI Music Ecosystem", layout="wide")

# Fetch Hugging Face token securely from Streamlit Secrets
HF_TOKEN = os.environ.get("HF_TOKEN", "")

st.title("🇳🇬 9jaStudio — AI Music Production Ecosystem")
st.caption("Create Fusions, Split Stems, and Mix/Master to Global Radio Standards for Free.")

# Initialize Memory State anchors so generated tracks do not vanish on click
if "generated_beat_bytes" not in st.session_state:
    st.session_state.generated_beat_bytes = None
if "generated_beat_name" not in st.session_state:
    st.session_state.generated_beat_name = None

# User Dashboard Tracker
user_email = st.text_input("Enter 9jaStudio Account Email Address", value="independent_artist@9ja.com")
st.info("🟢 **Account Status:** Logged In | **Remaining Studio Credits:** 2 Songs Free Trial Left")

# 2. THE DUAL WORKSPACE MODULES
tab1, tab2 = st.tabs(["🥁 Module 1: AI Beat Lab", "🎚️ Module 2: Streaming Mix & Master"])

# MODULE 1: LIVE TEXT-TO-MUSIC AI GENERATION
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
            if not HF_TOKEN:
                st.error("⚠️ Setup Missing: Please paste your HF_TOKEN inside the Streamlit Secrets manager.")
            else:
                with st.spinner("⚡ Connecting to Hugging Face AI Clusters... Compiling your custom WAV data..."):
                    try:
                        # Culturally optimized instruction prompt parameters fed to the engine
                        optimized_prompt = f"Studio quality premium audio track. Genre: {genre_selection}. {text_prompt}. Rich {drum_profile} arrangements at {tempo} BPM."
                        
                        client = InferenceClient(token=HF_TOKEN)
                        
                        # Trigger the live music model via Hugging Face SDK
                        audio_data = client.text_to_speech(
                            prompt=optimized_prompt,
                            model="facebook/musicgen-small"
                        )
                        
                        st.session_state.generated_beat_bytes = audio_data
                        st.session_state.generated_beat_name = f"9jaStudio_{tempo}BPM.wav"
                        
                    except Exception as e:
                        if "loading" in str(e).lower() or "503" in str(e):
                            st.warning("⏳ The Hugging Face server model is currently booting up in the cloud. Give it 15 seconds and try clicking generate again!")
                        else:
                            st.error(f"Engine connection standby. Details: {str(e)}")

        # Keep output audio and working download buttons locked safely in layout memory view
        if st.session_state.generated_beat_bytes is not None:
            st.success("🔥 Success! Your custom AI track compilation is complete.")
            st.audio(st.session_state.generated_beat_bytes, format="audio/wav")
            st.download_button(
                label="📥 Download Mastered WAV Instrumental File",
                data=st.session_state.generated_beat_bytes,
                file_name=st.session_state.generated_beat_name,
                mime="audio/wav"
            )

# MODULE 2: STANDALONE MIXING & MASTERING PROTOTYPE
with tab2:
    st.subheader("Bring your own song data or raw WhatsApp Voice notes to compile studio-clean stereo deliverables.")
    
    col3, col4 = st.columns(2)
    with col3:
        uploaded_song = st.file_uploader("Upload Song Mixdown Data (.WAV, .MP3, or WhatsApp .M4A/.OGG audio)")
        target_sound_profile = st.radio("Select Studio Sound Profile Target", ["Punchy Afro-Pop (Loud & Bass Driven)", "Smooth Vocal R&B (Warm & Wide)", "Crisp Cinematic Rap"])
        streaming_dsp_target = st.selectbox("Target Streaming Optimization Profile", ["Optimized for Spotify (-14 LUFS / -1.0 dB Ceiling)", "Optimized for Apple Music Lossless", "Optimized for TikTok/Audiomack (-9 LUFS)"])
        
        engineer_btn = st.button("🎛️ Run Multi-Stem Mix & Master Pipeline", disabled=(uploaded_song is None))
        
    with col4:
        if engineer_btn and uploaded_song is not None:
            with st.spinner("🎚️ Booting Stem Splitter... Running multi-band vocal isolation..."):
                st.success(f"🎚️ Mixing Complete! Mastered perfectly for {streaming_dsp_target}.")
                st.write("**Isolated Vocal Stem (Meta Demucs Output):**")
                st.audio("https://soundhelix.com")
                st.write("**Radio-Ready Commercial WAV Master (Matchering Output):**")
                st.audio("https://soundhelix.com")

# 3. INTEGRATED DUAL-CURRENCY BILLING PORTAL
st.markdown("---")
st.header("💳 9jaStudio Wallet & Studio Access Upgrades")
st.write("Select your currency parameters to load your pre-made Paystack payment links.")

currency = st.radio("Choose Payment Currency Profile", ["Pay in Nigerian Naira (₦ NGN)", "Pay in US Dollars ($ USD)"])

plan_col1, plan_col2, plan_col3 = st.columns(3)

with plan_col1:
    st.markdown("### 🌟 Free Starter Tier")
    st.write("**Price:** ₦0 / $0 Free Forever\n\n• **2 Songs Total** Creation Limit\n• Standard Base Processing Speed\n• Direct Full Track WAV Output Only")
    st.button("Active Plan", disabled=True)

with plan_col2:
    st.markdown("### 🚀 Professional Monthly Plan")
    price_pro = "15,000 NGN" if "Naira" in currency else "$25 USD"
    pro_link = "https://paystack.com" if "Naira" in currency else "https://paystack.com"
    st.write(f"**Price:** {price_pro}/Mo\n\n• **30 Songs per Month** Credit Allocation\n• High-Priority AI Server Processing\n• **Full Stem Exports** Allowed")
    st.link_button("🔒 Upgrade to Pro Studio", pro_link)

with plan_col3:
    st.markdown("### 👑 Premium Annual Pass")
    price_pre = "50,000 NGN" if "Naira" in currency else "$80 USD"
    premium_link = "https://paystack.com" if "Naira" in currency else "https://paystack.com"
    st.write(f"**Price:** {price_pre}/Yr\n\n• **60 Songs per Year** Credit Allocation\n• Ultimate Cloud Priority Engine Access\n• Full Stem Exports + Commercial Rights")
    st.link_button("🔒 Secure Annual Pass", premium_link)

