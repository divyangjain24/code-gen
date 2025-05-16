import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

# ---- PAGE CONFIG ----
st.set_page_config(page_title="🧠 AI Code Generator", layout="centered", page_icon="💻")

# ---- CSS STYLING ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code&family=Rubik&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Rubik', sans-serif;
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
    }

    .stTextInput > div > div > input {
        background-color: #f0f2f6;
        color: #000;
    }

    .stTextArea textarea {
        background-color: #f0f2f6;
        color: #000;
    }

    .stSelectbox div div {
        background-color: #f0f2f6;
        color: #000;
    }

    .big-font {
        font-size: 26px !important;
        font-weight: bold;
        color: #fddb3a;
    }

    .highlight {
        background-color: #ff9a00;
        padding: 3px 6px;
        border-radius: 4px;
    }

    .code-box {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Fira Code', monospace;
        font-size: 15px;
        color: #33ffcc;
    }

    .stButton>button {
        border-radius: 10px;
        background: #fddb3a;
        color: black;
        border: none;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background: #ff9a00;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---- TITLE ----
st.markdown("<div class='big-font'>🤖 AI Code Generator</div>", unsafe_allow_html=True)
st.write("Ask coding questions and get AI-generated solutions instantly!")

# ---- INPUTS ----
question = st.text_area("📝 Your coding question", height=200)

language = st.selectbox("🧠 Target programming language", [
    "Python", "JavaScript", "C++", "Java", "C#", "Go", "Rust", "Ruby", "Swift", "TypeScript", "Kotlin", "PHP", "R", "Dart", "Scala"
])

# ---- GENERATE BUTTON ----
if st.button("🚀 Generate Code"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        prompt = f"Write code in {language} to solve the following problem:\n\n{question}"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
          "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        with st.spinner("⏳ Thinking... generating your code"):
            try:
                res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
                res.raise_for_status()
                code = res.json()['choices'][0]['message']['content']

                st.success("✅ Code generated!")

                st.markdown("<div class='code-box'>{}</div>".format(code.replace("```", "").replace("\n", "<br>")), unsafe_allow_html=True)

                st.download_button("📥 Download Code", code, file_name=f"solution.{language.lower()}", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Error: {e}")
