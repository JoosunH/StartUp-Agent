import streamlit as st
from tools.Doc_embadder import process_document
from agent import analyze_competitors

st.set_page_config(page_title="Analyze Startup Idea", layout="wide")

st.title("💡 Startup Idea Analyzer")
st.markdown("Enter your idea below to get market insights, competitor benchmarks, and strategic suggestions.")

idea = st.text_input("✏️ What's your startup idea?")
country_code = st.text_input("📍 Enter your Country code (e.g., US, IN, UK)")
city = st.text_input("🏙️ Enter your City")

st.markdown("### 📄 Optionally, upload your pitch deck (PDF) for deeper analysis:")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    with open("uploaded_pitch.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.info(f"✅ Uploaded: {uploaded_file.name}")
    with st.spinner("📚 Processing pitch deck..."):
        process_document("uploaded_pitch.pdf")  # 👈 Same path your backend expects
    st.success("📂 Pitch deck processed and indexed.")

if st.button("Analyze Now"):
    if not idea:
        st.warning("Please enter an idea first.")
    else:
        with st.spinner("Analyzing with GPT and SerpAPI..."):
            result = analyze_competitors(idea, city, country_code)
            st.success("✅ Analysis complete!")

            st.subheader("📊Analysis")
            st.write(result.get("Market Analysis", "N/A"))

            st.subheader("🏢 Competitors")
            st.write(result.get("Competitors", "N/A"))

            st.subheader("💡 suggestion")
            st.write(result.get("Suggestions", "N/A"))
            
            st.subheader("Text summary")
            st.write(result.get("Text summary", "N/A"))
