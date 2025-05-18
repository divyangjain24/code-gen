import streamlit as st
import requests
import base64

# Page Settings
st.set_page_config(
    page_title="AI Code Generator",
    page_icon="💡",
    layout="centered"
)

# Sidebar Branding & Navigation
with st.sidebar:
    st.image("https://i.ibb.co/F3xT1jK/codegen.png", width=100)
    st.markdown("## AI Code Generator")
    st.markdown("Crafted by [Divyang Jain](https://www.linkedin.com/in/divyang-jain-276032291)")
    st.markdown("---")
    st.markdown("### 📢 Features")
    st.markdown("- Multi-language support\n- Code optimization\n- Instant download")
    st.markdown("### 📞 Contact")
    st.markdown("- Email: Narutouzu@gmail.com\n- Phone: 8630062115")

# Custom Styles
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #1a1a1d !important;
            color: #f1f1f1 !important;
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton > button {
            background: linear-gradient(90deg, #00c9ff, #92fe9d);
            color: black !important;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            padding: 0.5em 1.2em;
            transition: 0.3s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #009ec3, #4be585);
        }
        textarea, input, select {
            background-color: #2a2a2e !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
        }
        .app-title {
            font-size: 2.2em;
            text-align: center;
            margin-bottom: 1rem;
            color: #00d1ff;
            font-weight: 800;
        }
        .export-button {
            text-align: right;
            margin-top: 10px;
        }
        hr {
            border: none;
            border-top: 1px solid #444;
            margin: 2em 0;
        }
    </style>
    <div class="app-title">AI Code Generator</div>
""", unsafe_allow_html=True)

# Secret API Key
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Supported Languages
languages = {
    "Python": "py", "JavaScript": "js", "Java": "java", "C++": "cpp",
    "C": "c", "C#": "cs", "HTML": "html", "CSS": "css", "TypeScript": "ts",
    "Go": "go", "Ruby": "rb", "PHP": "php"
}

# UI Elements
st.markdown("### 🧠 Describe what you want and pick your language:")

language_name = st.selectbox("Select a programming language:", list(languages.keys()))
language_code = languages[language_name]

user_prompt = st.text_area("Enter your code request:", placeholder=f"e.g. Create a login page using {language_name}")


# Code Generation Function
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
        return f"❌ Network Error: {str(e)}"
    except KeyError:
        return "❌ API Error: Unexpected response format."
    except Exception as e:
        return f"❌ Unknown Error: {str(e)}"

# Generate Code
if st.button("✨ Generate Code"):
    if user_prompt.strip():
        with st.spinner("Generating your code..."):
            code_output = generate_code(user_prompt, language_name)
            st.markdown(f"### 🚀 Code Output in {language_name}:")
            st.code(code_output, language=language_code)

            # Download Option
            b64 = base64.b64encode(code_output.encode()).decode()
            href = f'<a href="data:file/text;base64,{b64}" download="generated_code.{language_code}">📥 Download Code</a>'
            st.markdown(f"<div class='export-button'>{href}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a description for the code.")

# Footer
st.markdown("""
<hr>
<div style='text-align: center; font-size: 0.9em;'>
    © 2025 AI Code Generator | Built with ❤️ by Divyang Jain
</div>
""", unsafe_allow_html=True)
