import streamlit as st
import requests
import base64

# API Config
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Page Settings
st.set_page_config(
    page_title="AI Code Generator",
    page_icon="💡",
    layout="centered"
)

# Custom Styles (Dark Mode Only)
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #0e1117 !important;
            color: white !important;
        }
        label, div, p, h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
        textarea, input, select {
            background-color: #262730 !important;
            color: white !important;
        }
        .stButton > button {
            background-color: #00c9ff !important;
            color: black !important;
            font-weight: bold;
            border-radius: 8px;
        }
        .stButton > button:hover {
            background-color: #009ec3 !important;
        }
        div[data-baseweb="select"] *, div[data-baseweb="popover"] * {
            background-color: #262730 !important;
            color: white !important;
        }
        .export-button {
            text-align: right;
            margin-top: 10px;
        }
        .app-header {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 25px;
            padding: 10px;
            border-bottom: 1px solid #333;
        }
        .app-title {
            font-size: 30px;
            font-weight: 700;
            letter-spacing: 1px;
        }
        .info-section {
            margin-top: 50px;
            border-top: 2px solid #4a5568;
            padding-top: 20px;
        }
        .info-title {
            color: #f56565;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4);
        }
        .info-text {
            color: #cbd5e0;
            line-height: 1.7;
            margin-bottom: 10px;
        }
        .info-link {
            color: #81e6d8;
            text-decoration: none;
            font-weight: 600;
        }
        .info-link:hover {
            color: #319796;
            text-decoration: underline;
        }
    </style>

    <div class="app-header">
        <div class="app-title">AI Code Generator</div>
    </div>
""", unsafe_allow_html=True)

# UI Inputs
st.markdown("### 🧠 Describe what you want and pick your language:")

languages = {
    "Python": "py", "JavaScript": "js", "Java": "java",
    "C++": "cpp", "C": "c", "C#": "cs", "HTML": "html",
    "CSS": "css", "TypeScript": "ts", "Go": "go",
    "Ruby": "rb", "PHP": "php"
}

language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

user_prompt = st.text_area("Enter your code request:", placeholder=f"e.g. Create a login page using {language_name}")

# Generate Code Function
def generate_code(prompt, lang):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a professional {lang} developer."},
            {"role": "user", "content": f"Generate an optimal and correct {lang} solution for:\n{prompt}\nOnly provide the code."}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    try:
        response = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"❌ Error: {str(e)}.  Please check your network connection and OpenRouter API key."
    except KeyError:
        return "❌ Error: Could not extract code from the API response.  The API may have returned an unexpected format."
    except Exception as e:
        return f"❌ Error: An unexpected error occurred: {str(e)}"

# Button to Generate Code
if st.button("✨ Generate Code"):
    if user_prompt.strip():
        with st.spinner("Generating your code..."):
            code_output = generate_code(user_prompt, language_name)
            st.markdown(f"### 🚀 Code Output in {language_name}:")
            st.code(code_output, language=language_code)

            # Download option
            b64 = base64.b64encode(code_output.encode()).decode()
            href = f'<a href="data:file/text;base64,{b64}" download="generated_code.{language_code}">📥 Download Code</a>'
            st.markdown(f"<div class='export-button'>{href}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a description for the code.")

# Your Information Section
st.markdown("""
<div class="info-section">
    <h2 class="info-title">About the Developer</h2>
    <p class="info-text">Email: Narutouzu@gmail.com</p>
    <p class="info-text">Instagram: <a href="https://www.instagram.com/morningstar7854/" target="_blank" class="info-link">morningstar7854</a></p>
    <p class="info-text">Phone Number: 8630062115</p>
    <p class="info-text">YouTube Channel: <a href="https://www.youtube.com/@alron-mind" target="_blank" class="info-link">Alron Mind</a></p>
    <p class="info-text">LinkedIn: <a href="https://www.linkedin.com/in/divyang-jain-276032291?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" target="_blank" class="info-link">Divyang Jain</a></p>
    
    
</div>
""", unsafe_allow_html=True)
