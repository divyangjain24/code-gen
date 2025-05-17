import streamlit as st
import requests
import base64

# Load API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Page Configuration
st.set_page_config(page_title="AI Code Generator", layout="centered")

# Theme Toggle
theme = st.sidebar.radio("Select Theme", ["🌙 Dark Mode", "☀️ Light Mode"])
dark_mode = theme == "🌙 Dark Mode"

# Custom CSS Based on Theme
if dark_mode:
    css = """
        <style>
            body {
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
                font-family: 'Inter', sans-serif;
            }
            .main {
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(10px);
                padding: 3rem 2rem;
                border-radius: 25px;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
                max-width: 750px;
                margin: 3rem auto;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .stButton > button {
                background-image: linear-gradient(to right, #00f2fe, #4facfe);
                color: white;
                font-weight: 600;
                border: none;
                border-radius: 12px;
                padding: 0.75rem 1.5rem;
                transition: 0.3s ease-in-out;
            }
            .stButton > button:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
            }
        </style>
    """
else:
    css = """
        <style>
            body {
                background: linear-gradient(to right, #f8f9fa, #e0eafc);
                color: #111;
                font-family: 'Inter', sans-serif;
            }
            .main {
                background: #ffffffcc;
                padding: 3rem 2rem;
                border-radius: 25px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                max-width: 750px;
                margin: 3rem auto;
                border: 1px solid #ddd;
            }
            .stButton > button {
                background-image: linear-gradient(to right, #4facfe, #00f2fe);
                color: white;
                font-weight: 600;
                border: none;
                border-radius: 12px;
                padding: 0.75rem 1.5rem;
                transition: 0.3s ease-in-out;
            }
            .stButton > button:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
            }
        </style>
    """
st.markdown(css, unsafe_allow_html=True)

# App Title
st.markdown("<div class='main'><h1 style='text-align:center;'>💻 AI Code Generator 🤖</h1>", unsafe_allow_html=True)
st.markdown("### 🧠 Describe what code you want and choose a programming language:")

# Language Selector
languages = {
    "Python": "python", "JavaScript": "javascript", "Java": "java", "C++": "cpp", "C": "c",
    "C#": "csharp", "HTML": "html", "CSS": "css", "TypeScript": "typescript", "Go": "go",
    "Ruby": "ruby", "PHP": "php"
}
language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

# User Prompt
user_prompt = st.text_area("Enter your code request:", placeholder=f"e.g. Create a weather app using {language_name}")

# Function to Generate Code
def generate_code(prompt, lang):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a professional {lang} developer."},
            {"role": "user", "content": f"Generate a clean, correct {lang} solution:\n{prompt}\nOnly provide the code."}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    try:
        response = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"] if "choices" in result else "⚠️ No output."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Generate Code and Display
generated_code = None
if st.button("✨ Generate Code"):
    if user_prompt.strip():
        with st.spinner("Generating your code..."):
            st.markdown(f"### 🚀 Code Output in {language_name}:")
            generated_code = generate_code(user_prompt, language_name)
            st.code(generated_code, language=language_code)
    else:
        st.warning("Please describe what code you want.")

# Export Code
if generated_code:
    b64 = base64.b64encode(generated_code.encode()).decode()
    file_ext = "txt" if language_code in ["html", "css"] else language_code
    href = f'<a href="data:file/text;base64,{b64}" download="generated_code.{file_ext}">📥 Download Code</a>'
    st.markdown(href, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
