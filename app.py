import streamlit as st
import requests

# Load API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Page Configuration
st.set_page_config(page_title="AI Code Generator", layout="centered")

# Custom CSS for Aesthetic UI
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #141e30, #243b55);
            color: white;
        }
        .main {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(8px);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            max-width: 700px;
            margin: auto;
        }
        h1 {
            text-align: center;
            color: #00d4ff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stButton > button {
            background-color: #00d4ff;
            color: black;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            border-radius: 10px;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #009ec3;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# App Title and Description
st.markdown("<div class='main'><h1>💻 AI Code Generator 🤖</h1>", unsafe_allow_html=True)
st.markdown("### 🧠 Describe what code you want and choose a programming language:")

# Language Selector
languages = {
    "Python": "python",
    "JavaScript": "javascript",
    "Java": "java",
    "C++": "cpp",
    "C": "c",
    "C#": "csharp",
    "HTML": "html",
    "CSS": "css",
    "TypeScript": "typescript",
    "Go": "go",
    "Ruby": "ruby",
    "PHP": "php"
}
language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

# User Input Text Area
user_prompt = st.text_area(
    "Enter your code request:",
    placeholder=f"e.g. Create a weather app using {language_name}"
)

# Function to Generate Code using OpenRouter API
def generate_code(prompt, lang):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a professional {lang} developer who writes clean, efficient, and well-commented code."},
            {"role": "user", "content": f"Generate an optimal and correct {lang} solution for the following task:\n{prompt}\nOnly provide the code without explanations."}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    try:
        response = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return "⚠️ No code returned from the model."
    except requests.exceptions.RequestException as e:
        return f"❌ API request failed: {str(e)}"
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

# Generate Button and Output Display
if st.button("✨ Generate Code"):
    if user_prompt.strip():
        with st.spinner("Generating your code..."):
            st.markdown(f"### 🚀 Code Output in {language_name}:")
            generated_code = generate_code(user_prompt, language_name)
            st.code(generated_code, language=language_code)
    else:
        st.warning("Please enter a description for the code.")

st.markdown("</div>", unsafe_allow_html=True)
