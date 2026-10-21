import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Freelance Proposal AI Agent", page_icon="🚀", layout="wide")
st.title("🚀 Freelance Proposal & Portfolio AI Agent")
st.write("Paste the client's job description and your portfolio below to generate a high-converting proposal in seconds!")

api_key = st.secrets.get("GEMINI_API_KEY", None)
if not api_key:
    api_key = st.sidebar.text_input("Enter your free Gemini API Key:", type="password")

col1, col2 = st.columns(2)

with col1:
    freelancer_info = st.text_area(
        "1. Your Skills & Portfolio Links:", 
        placeholder="e.g., I am a Full-Stack Web Developer.\nMy past projects:\n1. E-commerce Store (link) - Built with React & Node\n2. SaaS Landing Page (link) - High converting UI...",
        height=200
    )
    tone = st.selectbox("Proposal Tone:", ["Friendly & Conversational", "Professional & Direct", "Short & Punchy"])

with col2:
    job_post = st.text_area(
        "2. Client's Job Description:", 
        placeholder="Paste the complete job post from Upwork, Fiverr, or Freelancer here...",
        height=250
    )

if st.button("✨ Generate Winning Proposal", use_container_width=True):
    if not api_key:
        st.error("API Key missing! Please enter your Gemini API Key in the sidebar or admin settings.")
    elif not freelancer_info or not job_post:
        st.warning("Please fill in both your portfolio details and the client's job description.")
    else:
        with st.spinner("Analyzing job post and crafting your winning proposal..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-3.8-flash')
                
                prompt = f"""
                You are an Elite Freelance Proposal Strategist. 
                Tone: {tone}
                
                Freelancer Profile & Portfolio:
                {freelancer_info}
                
                Client's Job Description:
                {job_post}
                
                Tasks:
                1. 🎯 **Client's Main Pain Point:** Briefly explain in 1-2 sentences what the client actually wants to achieve.
                2. ⚠️ **Hidden Requirements / Tricks:** Mention if the client included any secret word or specific question to answer in the job post.
                3. 📝 **The Winning Proposal (Ready to Copy-Paste):** Write a high-converting proposal under 180 words. Start with a strong hook addressing their problem, naturally include ONLY the most relevant portfolio item from the freelancer's list as proof of work, and end with a smart open-ended question. Avoid boring generic intros like "I have X years of experience"!
                4. 💡 **Pro Interview Tip:** Give 1 actionable tip to win this specific client during the chat/interview.
                """
                
                response = model.generate_content(prompt)
                st.success("Proposal Generated Successfully!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
