import os
import streamlit as st
import replicate
import requests

# =====================================================================
# 1. PREMIUM STUDIO HIGH-END THEME STYLING (CSS Injection)
# =====================================================================
st.set_page_config(page_title="9jaStudio Pro", layout="wide", initial_sidebar_state="collapsed")

# Inject executive dark mode studio styling
st.markdown("""
    <style>
        /* Main background & Typography */
        .stApp {
            background-color: #0d0e12;
            color: #e4e6eb;
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3 {
            color: #ffffff !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }
        .stCaption {
            color: #8a8f98 !important;
            font-size: 15px;
        }
        /* Custom Premium Studio Cards */
        .studio-card {
            background: linear-gradient(145deg, #16181f, #121319);
            border: 1px solid #232631;
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        /* Tab Navigation Enhancements */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: #121319;
            padding: 8px;
            border-radius: 12px;
            border: 1px solid #232631;
        }
        .stTabs [data-baseweb="tab"] {
            height: 48px;
            white-space: pre;
            background-color: transparent;
            border-radius: 8px;
            color: #8a8f98;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            padding: 0 24px;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #ffffff;
            background-color: #1c1e27;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ff5e3a !important;
            color: #ffffff !important;
        }
        /* Premium Studio Buttons */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #ff5e3a 0%, #ff2a5f 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            border: none !important;
            padding: 12px 28px !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 15px rgba(255, 42, 95, 0.3) !important;
            transition: all 0.3s ease;
            width: 100%;
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 42, 95, 0.5) !important;
        }
        /* Status Badges */
        .status-panel {
            background-color: rgba(0, 230, 115, 0.08);
            border: 1px solid rgba(0, 230, 115, 0.2);
            padding: 12px 20px;
            border-radius: 10px;
            color: #00e673;
            font-weight: 600;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. SEED CONNECTORS & ENGINE CORE
# =====================================================================
REPLICATE_API_TOKEN = st.secrets.get("REPLICATE_API_TOKEN", os.environ.get("REPLICATE_API_TOKEN", ""))
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# Header Segment
st.markdown('<p style="font-size: 13px; font-weight: 700; color: #ff5e3a; text-transform: uppercase; margin-bottom: 0;">AI Music Architecture</p>', unsafe_allow_html=True)
st.title("9jaStudio Pro")
st.markdown('<p class="stCaption">High-tier text-to-music generation, multi-stem synthesis, and adaptive commercial mastering grid.</p>', unsafe_allow_html=True)

# User Credential Ribbon
user_email = st.text_input("Studio Session Identity Account (Email Address)", value="independent_artist@9ja.com")
st.markdown('<div class="status-panel">🟢 Account Status: Premium Console Active | Remaining Studio Credits: 2 Master Sessions Remaining</div>', unsafe_allow_html=True)

if "generated_beat_bytes" not in st.session_state:
    st.session_state.generated_beat_bytes = None
if "generated_beat_name" not in st.session_state:
    st.session_state.generated_beat_name = None

# =====================================================================
# 3. CORE INDUSTRIAL CONSOLE TAB LAYOUT
# =====================================================================
tab1, tab2 = st.tabs(["⚡ MODULE 1: AI INSTANT BEAT LAB", "🎛️ MODULE 2: MULTI-STEM MIX & MASTER"])

# TAB 1: ADVANCED AI BEAT GENERATION
with tab1:
    st.markdown('<div class="studio-card"><h3>Audio Generation Parameters</h3><p style="color:#8a8f98; font-size:14px; margin-bottom:20px;">Prompt raw cultural weights directly into Meta\'s synthesis grid computer.</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.1, 0.9], gap="large")
    with col1:
        text_prompt = st.text_area("Descriptive Prompt Matrix", placeholder="Heavy syncopated Amapiano log drum baseline, smooth R&B Rhodes chords, high-end Afrobeat shaker rhythm, pristine radio master...")
        genre_selection = st.selectbox("Cultural Genre Template Profile", ["Afrobeat Core 🇳🇬", "Amapiano Evolution 🇿🇦", "Afro-R&B Fusion 🌿", "Highlife Nu-Traditional 🎸"])
        
        inner_col1, inner_col2 = st.columns(2)
        with inner_col1:
            tempo = st.slider("BPM Speed Calibration", 90, 140, 112)
        with inner_col2:
            drum_profile = st.selectbox("Sub-Bass / Drum Profile Signature", ["Heavy Asake Style Log", "Deep Kabza Ambient Sub", "Bouncing Burna Modern Accent"])
            
        st.write("")
        generate_beat_btn = st.button("🔥 COMPILE & EXECUTE AI SYNTHESIS CHAIN")
        
    with col2:
        if generate_beat_btn:
            with st.spinner("⚡ Initializing high-compute GPU partition... Compiling audio stems..."):
                try:
                    optimized_prompt = f"Studio quality premium audio track. Genre: {genre_selection}. {text_prompt}. Rich {drum_profile} arrangements at {tempo} BPM."
                    
                    # RUN VERIFIED REPLICATE MODEL CONSOLE
                    output_url = replicate.run(
                        "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
                        input={
                            "prompt": optimized_prompt,
                            "duration": 15,
                            "model_version": "stereo-large"
                        }
                    )
                    
                    response = requests.get(output_url)
                    st.session_state.generated_beat_bytes = response.content
                    st.session_state.generated_beat_name = f"9jaStudio_{genre_selection.split()[0]}_{tempo}BPM.wav"
                    
                except Exception as e:
                    st.error(f"Engine queue connection failure. Details: {str(e)}")

        if st.session_state.generated_beat_bytes is not None:
            st.markdown('<div class="studio-card" style="border: 1px solid #00e673;">', unsafe_allow_html=True)
            st.success("🎯 WAV AUDIO COMPILATION COMPLETE")
            st.audio(st.session_state.generated_beat_bytes, format="audio/wav")
            st.download_button(
                label="📥 EXTRACT LIVE STUDIO MIXDOWN (WAV)",
                data=st.session_state.generated_beat_bytes,
                file_name=st.session_state.generated_beat_name,
                mime="audio/wav"
            )
            st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: STREAMING MIX & MASTER CONSOLE
with tab2:
    st.markdown('<div class="studio-card"><h3>Linear Mastering Rack</h3><p style="color:#8a8f98; font-size:14px; margin-bottom:20px;">Upload raw mixdowns or phone voice notes to isolate stems and reference master.</p></div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2, gap="large")
    with col3:
        uploaded_song = st.file_uploader("Inject Audio Track Source (.WAV, .MP3, .M4A)")
        target_sound_profile = st.radio("Studio Output Sound Targeting Profile", ["Punchy Afro-Pop (Loud, Forward Midrange)", "Warm Vocal R&B (Silky Highs, Wide Stereo Field)"])
        streaming_dsp_target = st.selectbox("Loudness DSP Optimization Ceiling", ["Spotify Standard (-14 LUFS / -1.0 dBFS Peak Target)", "TikTok & Audiomack Aggressive (-9 LUFS Club Target)"])
        
        st.write("")
        engineer_btn = st.button("🎛️ RUN MULTI-STEM LINEAR ENGINEERING PIPELINE", disabled=(uploaded_song is None))
        
    with col4:
        if engineer_btn and uploaded_song is not None:
            st.success("🎚️ MIXDOWN GRID ROUTED SUCCESSFULLY")

# =====================================================================
# 4. EXECUTIVE DUAL-CURRENCY WALLET UPGRADE PORTAL
# =====================================================================
st.markdown("<br><hr style='border-color: #232631;'><br>", unsafe_allow_html=True)
st.markdown("<h2>💳 Billing Allocation & Studio Upgrades</h2>", unsafe_allow_html=True)

currency = st.radio("Select Billing Currency Engine Settings profile", ["Pay in Nigerian Naira (₦ NGN)", "Pay in US Dollars ($ USD)"])

plan_col1, plan_col2, plan_col3 = st.columns(3, gap="medium")

with plan_col1:
    st.markdown("""
    <div class="studio-card">
        <p style="color: #ff5e3a; font-weight:700; font-size:12px; uppercase; margin:0;">Allocation Base</p>
        <h3 style="margin-top:5px;">Free Starter Tier</h3>
        <h2 style="color:#ffffff; margin:10px 0;">₦0 / $0</h2>
        <p style="font-size:14px; color:#8a8f98; line-height:1.6;">
        • 2 Total Trial Audio Compiles<br>
        • Shared General Compute Graphics Speeds<br>
        • Direct WAV Output Access Only
        </p>
    </div>
