import streamlit as st
import requests

# ✅ Get API key securely from Streamlit secrets
API_KEY = st.secrets["API_KEY"]

# ---- PAGE CONFIG ----
st.set_page_config(page_title="🧠 AI Code Generator", layout="centered", page_icon="💻")

# ---- CSS STYLING ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code&family=Rubik&display=swap');

    html, body, [class*="css"] {
        font-family: 'Rubik', sans-serif;
        background: linear-gradient(to right, #141e30, #243b55);
        color: white;
        transition: all 0.4s ease-in-out;
    }

    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox div div {
        background-color: #ffffff;
        color: #000;
        border-radius: 8px;
        padding: 8px;
    }

    .big-font {
        font-size: 30px !important;
        font-weight: bold;
        color: #fddb3a;
        text-shadow: 1px 1px 2px #000;
        margin-bottom: 10px;
    }

    .code-box {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Fira Code', monospace;
        font-size: 15px;
        color: #33ffcc;
        overflow-x: auto;
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

language_options = [
    "Select a language...",
    "Python", "JavaScript", "C++", "Java", "C#", "Go", "Rust",
    "Ruby", "Swift", "TypeScript", "Kotlin", "PHP", "R", "Dart", "Scala"
]
language = st.selectbox("🧠 Target programming language", language_options)

# ---- GENERATE BUTTON ----
if st.button("🚀 Generate Code"):
    if not question.strip():
        st.warning("⚠️ Please enter a coding question.")
    elif language == "Select a language...":
        st.warning("⚠️ Please choose a programming language.")
    else:
        prompt = f"Write code in {language} to solve the following problem:\n\n{question}"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": "deepseek-coder:6.7b",
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

                # Display code nicely
                st.markdown("<div class='code-box'>{}</div>".format(code.replace("```", "").replace("\n", "<br>")), unsafe_allow_html=True)

                # Download button
                file_ext = "py" if language.lower() == "python" else "txt"
                st.download_button("📥 Download Code", code, file_name=f"solution.{file_ext}", mime="text/plain")

            except Exception as e:
                st.error(f"❌ Error: {e}")
