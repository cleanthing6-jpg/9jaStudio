import os
import streamlit as st
import requests
import time

# 1. SUNO CONSOLE GEOMETRY CONFIGURATION
st.set_page_config(page_title="9jaStudio Pro — Suno Workspace", layout="wide")

# Fetch your token safely from your secrets box
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# Initialize permanent feed state memory so generated songs never vanish on click
if "suno_library" not in st.session_state:
    st.session_state.suno_library = []

# =====================================================================
# 2. MAIN SPLIT-SCREEN WORKSPACE LAYOUT (Suno Dual Column Structure)
# =====================================================================
left_panel, right_feed = st.columns([0.8, 1.2], gap="large")

# LEFT PANEL: THE CREATION SIDEBAR CONSOLE
with left_panel:
    st.markdown("### 🎶 Create Tracks")
    st.caption("Configure custom arrangements or input lyrical concepts directly.")
    st.write("---")
    
    # Suno Mode Configuration Switches
    custom_mode = st.toggle("Custom Mode Settings", value=True)
    
    if custom_mode:
        text_prompt = st.text_area("Lyrical Content / Concept", placeholder="Enter your own verses here or type an instrumental concept description...", height=120)
        genre_style = st.text_input("Style of Music (Comma-separated tags)", value="Afrobeat, Amapiano log drum bounce, smooth R&B vibe")
    else:
        text_prompt = st.text_area("Song Description Prompt", placeholder="A heavy bouncing Amapiano track with bright horns...", height=120)
        genre_style = "Automated Core Profile"
        
    track_title = st.text_input("Song Track Title Nomination", value="Untitled Amapiano Jam")
    tempo = st.slider("BPM Rhythm Calibration", 90, 140, 112)
    
    st.write("")
    execute_suno_btn = st.button("✨ CREATE SONG GENERATION")

    # BACKGROUND PROCESSING CHAIN TRIGGER
    if execute_suno_btn:
        with st.spinner("⚡ Spawning generation matrix... Rendering raw audio..."):
            try:
                optimized_prompt = f"Studio quality premium audio track. Style: {genre_style}. Prompt details: {text_prompt} at {tempo} BPM."
                
                # FIXED DIRECT INFERENCE PIPELINE ENDPOINT URL
                API_URL = "https://huggingface.co"
                
                # FIX 403: Standardized high-security authorization headers
                headers = {
                    "Authorization": f"Bearer {HF_TOKEN}",
                    "Content-Type": "application/json"
                }
                
                response = requests.post(API_URL, headers=headers, json={"inputs": optimized_prompt})
                
                # Handle model wake-up cycle (Status 503)
                if response.status_code == 503:
                    st.warning("💤 AI Engine warming up. Retrying sequence in 10 seconds...")
                    time.sleep(10)
                    response = requests.post(API_URL, headers=headers, json={"inputs": optimized_prompt})
                
                if response.status_code == 200:
                    # Append new generated metadata bundle straight into Suno's right-side library array
                    st.session_state.suno_library.insert(0, {
                        "title": track_title,
                        "genre": genre_style if custom_mode else "AI Experimental Core",
                        "bpm": tempo,
                        "bytes": response.content
                    })
                    st.success("🎯 Generation complete! Track routed to your sidebar feed folder.")
                else:
                    st.error(f"Inference authorization barrier (Code {response.status_code}). Check token or try again!")
                    
            except Exception as e:
                st.error(f"Operational architecture failure: {str(e)}")

# RIGHT FEED: THE SUNO STYLE RECEPTACLE DISPLAY FEED
with right_feed:
    st.markdown("### 📂 Song Library Feed")
    st.caption("Your custom generated masters array history stream logs.")
    st.write("---")
    
    if not st.session_state.suno_library:
        st.info("🎵 No tracks generated yet in this studio session. Configure parameters on the left and hit 'Create'!")
    else:
        # Loop through memory array data block inputs and generate clean card rows
        for index, track in enumerate(st.session_state.suno_library):
            with st.container():
                col_box1, col_box2 = st.columns([1.3, 0.7])
                with col_box1:
                    st.markdown(f"#### 🏷️ {track['title']}")
                    st.write(f"🧬 **Style:** `{track['genre']}` | ⏳ **Tempo:** `{track['bpm']} BPM`")
                    st.audio(track['bytes'], format="audio/wav")
                with col_box2:
                    st.write("")
                    st.write("")
                    st.download_button(
                        label="📥 Download WAV",
                        data=track['bytes'],
                        file_name=f"9jaStudio_{track['title'].replace(' ', '_')}.wav",
                        mime="audio/wav",
                        key=f"dl_{index}"
                    )
                st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

# =====================================================================
# 3. DIGITAL WALLET & INTEGRATED BILLING GATE
# =====================================================================
st.markdown("<br><br>---", unsafe_allow_html=True)
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

