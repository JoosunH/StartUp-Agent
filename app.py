import streamlit as st

st.set_page_config(layout="wide")

video_html = """
<style>
#myVideo {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100vw;
  height: 102vh;
  object-fit: cover;
}

.overlay {
  position: fixed;
  top: 30%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  z-index: 1;
  width: 80vw;
}

.overlay h1 {
  font-size: 3rem;
  margin-bottom: 0.5em;
}

.overlay p {
  font-size: 1.2rem;
  margin: 0.4em 0;
}


</style>

<video autoplay muted loop id="myVideo">
  <source src="https://videos.pexels.com/video-files/4711694/4711694-uhd_3840_2160_30fps.mp4" type="video/mp4">
</video>

<div class="overlay">
  <h1>Valuate Your Startup Idea with AI</h1>
  <p>✨ This tool helps refine and benchmark your startup ideas using GPT-4 and real market data.</p>
  <p>🚀 Upload pitch decks, compare with competitors, and get tailored strategy advice instantly.</p>
</div>
"""

# Inject video + overlay text
st.markdown(video_html, unsafe_allow_html=True)
# Button positioned precisely below the text
st.markdown("""
    <style>
    .block-container {
        min-width: 1200px;  /* Adjust as needed */
    }
    </style>
""", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

with col3:
    st.markdown("<div style='margin-top: 300px; text-align: center;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Start Now"):
      st.switch_page("pages/analyze.py")

st.markdown("</div>", unsafe_allow_html=True)
