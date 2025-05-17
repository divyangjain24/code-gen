import streamlit as st
import requests

# Load API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Page configuration
st.set_page_config(page_title="AI Code Generator", layout="centered")

# Dark mode toggle
dark_mode = st.toggle("🌗 Dark Mode", value=False)

# CSS styles based on theme
bg_color = "#1e1e1e" if dark_mode else "#f0f2f6"
card_color = "#2d2d2d" if dark_mode else "white"
text_color = "white" if dark_mode else "#000"
button_color = "#007acc" if not dark_mode else "#00c8ff"
button_hover = "#005f99" if not dark_mode else "#0096cc"

# Apply custom styles
st.markdown(f"""
    <style>
        body {{
            background: {bg_color};
            color: {text_color};
        }}
        .main {{
            background: {card_color};
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            max-width: 800px;
            margin: auto;
            color: {text_color};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {button_color};
            font-family: 'Courier New', monospace;
            text-align: center;
        }}
        .stTextArea, .stSelectbox, .stDownloadButton, .stButton > button {{
            font-size: 1rem;
            border-radius: 10px;
        }}
        .stButton > button {{
            background-color: {button_color};
            color: white;
            padding: 0.6rem 1.3rem;
            border: none;
            font-weight: bold;
        }}
        .stButton > button:hover {{
            background-color: {button_hover};
            transform: scale(1.04);
        }}
    </style>
""", unsafe_allow_html=True)

# Main container
st.markdown("<div class='main'>", unsafe_allow_html=True)
st.markdown("### 💻 AI Code Generator")
st.markdown("### 🧠 Describe what you want and pick your language:")

# Language selection
languages = {
    "Python": "py", "JavaScript": "js", "Java": "java",
    "C++": "cpp", "C": "c", "C#": "cs", "HTML": "html",
    "CSS": "css", "TypeScript": "ts", "Go": "go",
    "Ruby": "rb", "PHP": "php"
}
language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

# User input
user_prompt = st.text_area("Enter your code request:", placeholder=f"e.g. Create a login page using {language_name}")

# API Call function
def generate_code(prompt, lang):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a professional {lang} developer who writes clean, efficient, and well-commented code."},
            {"role": "user", "content": f"Generate an optimal and correct {lang} solution for:\n{prompt}\nOnly provide the code without explanations."}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }
    try:
        response = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "⚠️ No code returned from the model."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Generate Code + Download
if st.button("✨ Generate Code"):
    if user_prompt.strip():
        with st.spinner("Generating your code..."):
            code_output = generate_code(user_prompt, language_name)
            st.markdown(f"### 🚀 Code Output in {language_name}:")
            st.code(code_output, language=language_code)

            st.download_button(
                label="📥 Download Code",
                data=code_output,
                file_name=f"generated_code.{language_code}",
                mime="text/plain"
            )
    else:
        st.warning("Please enter a description for the code.")

st.markdown("</div>", unsafe_allow_html=True)
