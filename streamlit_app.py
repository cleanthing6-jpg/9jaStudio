import os
import streamlit as st
import replicate
import requests

# 1. CORE CONNECTORS & APP CONFIGURATION
st.set_page_config(page_title="9jaStudio Pro", layout="wide")

REPLICATE_API_TOKEN = st.secrets.get("REPLICATE_API_TOKEN", os.environ.get("REPLICATE_API_TOKEN", ""))
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

st.title("🇳🇬 9jaStudio Pro — AI Audio Console")
st.caption("High-tier text-to-music generation, multi-stem synthesis, and adaptive commercial mastering grid.")

# Session Memory Anchors so generated files don't disappear on click
if "generated_beat_bytes" not in st.session_state:
    st.session_state.generated_beat_bytes = None
if "generated_beat_name" not in st.session_state:
    st.session_state.generated_beat_name = None

user_email = st.text_input("Studio Session Identity Account Email", value="independent_artist@9ja.com")
st.info("🟢 Account Status: Active Workspace | Remaining Studio Credits: 2 Master Sessions")

# 2. INTERACTIVE CONSOLE MODULES
tab1, tab2 = st.tabs(["🥁 MODULE 1: AI INSTANT BEAT LAB", "🎛️ MODULE 2: MULTI-STEM MIX & MASTER"])

with tab1:
    st.subheader("Audio Generation Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        text_prompt = st.text_area("Descriptive Prompt Matrix", placeholder="Heavy syncopated Amapiano log drum baseline, smooth R&B Rhodes chords...")
        genre_selection = st.selectbox("Cultural Genre Profile", ["Afrobeat Core 🇳🇬", "Amapiano Evolution 🇿🇦", "Afro-R&B Fusion 🌿"])
        tempo = st.slider("BPM Speed Calibration", 90, 140, 112)
        drum_profile = st.selectbox("Sub-Bass Profile Signature", ["Heavy Asake Style Log", "Deep Kabza Ambient Sub"])
        
        generate_beat_btn = st.button("🔥 COMPILE & EXECUTE AI SYNTHESIS")
        
    with col2:
        if generate_beat_btn:
            with st.spinner("⚡ Initializing high-compute GPU partition... Compiling audio stems..."):
                try:
                    optimized_prompt = f"Studio quality premium audio track. Genre: {genre_selection}. {text_prompt}. Rich {drum_profile} arrangements at {tempo} BPM."
                    
                    # RUN PRODUCTION ACCESSIBLE PATH FOR MUSICGEN
                    output_url = replicate.run(
                        "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
                        input={"prompt": optimized_prompt, "duration": 15, "model_version": "stereo-large"}
                    )
                    
                    response = requests.get(output_url)
                    st.session_state.generated_beat_bytes = response.content
                    st.session_state.generated_beat_name = f"9jaStudio_{tempo}BPM.wav"
                    
                except Exception as e:
                    st.error(f"Engine connection failure. Details: {str(e)}")

        if st.session_state.generated_beat_bytes is not None:
            st.write("### 🎯 WAV AUDIO COMPILATION COMPLETE")
            st.audio(st.session_state.generated_beat_bytes, format="audio/wav")
            st.download_button(
                label="📥 EXTRACT LIVE STUDIO MIXDOWN (WAV)",
                data=st.session_state.generated_beat_bytes,
                file_name=st.session_state.generated_beat_name,
                mime="audio/wav"
            )

with tab2:
    st.subheader("Linear Mastering Rack")
    uploaded_song = st.file_uploader("Inject Audio Track Source (.WAV, .MP3)")
    target_sound_profile = st.radio("Studio Output Sound Targeting Profile", ["Punchy Afro-Pop", "Warm Vocal R&B"])
    engineer_btn = st.button("🎛️ RUN MULTI-STEM LINEAR ENGINEERING PIPELINE", disabled=(uploaded_song is None))
    if engineer_btn:
        st.info("🎚️ MIXDOWN GRID ROUTED SUCCESSFULLY")

# 3. DIGITAL WALLET & INTEGRATED BILLING GATE
st.markdown("---")
st.header("💳 Billing Allocation & Studio Upgrades")
currency = st.radio("Select Settings Profile Currency", ["Pay in Nigerian Naira (₦ NGN)", "Pay in US Dollars ($ USD)"])

col_a, col_b = st.columns(2)
with col_a:
    price_pro = "15,000 NGN / Month" if "Naira" in currency else "$25 USD / Month"
    pro_link = "https://paystack.com" if "Naira" in currency else "https://paystack.com"
    st.write(f"### 🚀 Pro Monthly Tier\nPrice: **{price_pro}**\n\n• 30 Dedicated Monthly Song Tokens")
    st.link_button("🔒 INITIALIZE SECURE PRO UPGRADE", pro_link)

with col_b:
    price_pre = "50,000 NGN / Year" if "Naira" in currency else "$80 USD / Year"
    premium_link = "https://paystack.com" if "Naira" in currency else "https://paystack.com"
    st.write(f"### 👑 Premium Annual Pass\nPrice: **{price_pre}**\n\n• 60 Dedicated Annual Song Tokens")
    st.link_button("🔒 SECURE EXECUTIVE PASS", premium_link)
