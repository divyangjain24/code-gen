import streamlit as st
import requests
import base64

# --- Config ---
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

st.set_page_config(
    page_title="AI Code Generator",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Styling ---
st.markdown("""
<style>
    /* Base & typography */
    html, body, .stApp {
        background-color: #121212;
        color: #E0E0E0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        transition: background-color 0.5s ease, color 0.5s ease;
    }

    /* Header */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        padding: 20px 0;
        border-bottom: 1px solid #333;
        background-color: #1E1E1E;
        box-shadow: 0 2px 8px rgb(0 201 255 / 0.3);
        position: sticky;
        top: 0;
        z-index: 99;
    }
    .app-header img {
        height: 70px;
        width: 70px;
        filter: drop-shadow(0 0 5px #00c9ff);
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    .app-header img:hover {
        transform: rotate(15deg) scale(1.1);
    }
    .app-title {
        font-size: 38px;
        font-weight: 900;
        color: #00c9ff;
        text-shadow: 0 0 10px #00c9ff;
        user-select: none;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        border-right: 1px solid #333;
        padding-top: 30px;
    }
    .sidebar-profile-image {
        border-radius: 50%;
        width: 140px;
        margin: 0 auto 20px auto;
        display: block;
        border: 3px solid #00c9ff;
        filter: drop-shadow(0 0 8px #00c9ff);
        transition: transform 0.4s ease;
    }
    .sidebar-profile-image:hover {
        transform: scale(1.1);
    }
    .info-section {
        margin: 0 10px 30px 10px;
        font-size: 16px;
        line-height: 1.6;
    }
    .info-title {
        color: #00c9ff;
        font-weight: 700;
        font-size: 22px;
        margin-bottom: 10px;
        text-align: center;
        user-select: none;
    }
    .info-text, .info-link {
        color: #bbb;
        display: block;
        margin: 6px 0;
        user-select: text;
    }
    .info-link {
        color: #40e0d0;
        text-decoration: none;
        font-weight: 600;
    }
    .info-link:hover {
        color: #00b4a0;
        text-decoration: underline;
    }

    /* Main area layout */
    .main-container {
        padding: 20px 40px;
        max-width: 1400px;
        margin: auto;
    }
    .inputs-col {
        padding-right: 30px;
    }
    .output-col {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 15px rgb(0 201 255 / 0.15);
        min-height: 350px;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #262730 !important;
        color: white !important;
        border-radius: 6px !important;
    }

    /* Text area */
    textarea, input {
        background-color: #262730 !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1.5px solid #00c9ff !important;
        padding: 10px !important;
        font-size: 16px !important;
        transition: border-color 0.3s ease;
    }
    textarea:focus, input:focus {
        border-color: #40e0d0 !important;
        outline: none !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00c9ff, #40e0d0);
        color: #0a0a0a;
        font-weight: 700;
        font-size: 18px;
        padding: 12px 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgb(64 224 208 / 0.5);
        transition: background 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #40e0d0, #00c9ff);
        cursor: pointer;
    }

    /* Reset button */
    .reset-button {
        margin-top: 12px;
        background: #444;
        color: #eee !important;
        border-radius: 12px;
        border: none;
        width: 100%;
        padding: 10px;
        font-weight: 600;
        transition: background 0.25s ease;
    }
    .reset-button:hover {
        background: #555;
        cursor: pointer;
    }

    /* Code output */
    .output-area pre {
        font-size: 14px !important;
        line-height: 1.4 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        background-color: #121212 !important;
        color: #40e0d0 !important;
        overflow-x: auto !important;
        box-shadow: inset 0 0 10px #00c9ff;
    }

    /* Download & Copy buttons container */
    .action-buttons {
        display: flex;
        justify-content: flex-end;
        gap: 15px;
        margin-top: 15px;
    }
    .action-btn {
        background: #00c9ff;
        color: #0a0a0a !important;
        font-weight: 700;
        padding: 8px 18px;
        border-radius: 10px;
        box-shadow: 0 3px 8px rgb(0 201 255 / 0.6);
        border: none;
        transition: background 0.3s ease;
        cursor: pointer;
    }
    .action-btn:hover {
        background: #40e0d0;
    }

    /* Feedback Section */
    .feedback-container {
        margin-top: 50px;
        background-color: #1E1E1E;
        border-radius: 15px;
        padding: 25px 30px;
        box-shadow: 0 0 25px rgb(0 201 255 / 0.2);
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    .feedback-title {
        color: #00c9ff;
        font-weight: 700;
        font-size: 24px;
        margin-bottom: 15px;
        user-select: none;
    }
    .feedback-textarea {
        background-color: #262730 !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1.5px solid #00c9ff !important;
        padding: 12px !important;
        font-size: 16px !important;
        width: 100%;
        resize: vertical;
        min-height: 100px;
    }
    .feedback-submit-btn {
        margin-top: 12px;
        width: 100%;
    }

    /* Tooltip */
    [data-tooltip] {
        position: relative;
        cursor: help;
    }
    [data-tooltip]:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: #00c9ff;
        color: #0a0a0a;
        padding: 6px 10px;
        border-radius: 6px;
        white-space: nowrap;
        font-size: 13px;
        font-weight: 600;
        box-shadow: 0 0 6px rgb(0 201 255 / 0.8);
        opacity: 1;
        pointer-events: auto;
        z-index: 1000;
    }
    [data-tooltip]::after {
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.25s ease;
    }

</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="app-header">
    <img src="https://img.icons8.com/ios-filled/70/00c9ff/code.png" alt="Logo" title="AI Code Generator"/>
    <div class="app-title" title="AI Code Generator">AI Code Generator</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(
        '<img class="sidebar-profile-image" src="https://avatars.githubusercontent.com/u/583231?v=4" alt="Profile Image"/>',
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class="info-section">
        <h2 class="info-title">About the Developer</h2>
        <p class="info-text">Email: Narutouzu@gmail.com</p>
        <p class="info-text">Instagram: <a href="https://www.instagram.com/__morningstar7854/" target="_blank" class="info-link">morningstar7854</a></p>
        <p class="info-text">Phone Number: 8630062115</p>
        <p class="info-text">YouTube Channel: <a href="https://www.youtube.com/@alron-mind" target="_blank" class="info-link">Alron Mind</a></p>
        <p class="info-text">LinkedIn: <a href="https://www.linkedin.com/in/divyang-jain-276032291" target="_blank" class="info-link">Divyang Jain</a></p>
    </div>
    """, unsafe_allow_html=True)

# --- Main layout with columns ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])

languages = {
    "Python": "py", "JavaScript": "js", "Java": "java",
    "C++": "cpp", "C": "c", "C#": "cs", "HTML": "html",
    "CSS": "css", "TypeScript": "ts", "Go": "go",
    "Ruby": "rb", "PHP": "php"
}

with col1:
    st.markdown('### 🧠 Describe what you want and pick your language:')
    language_name = st.selectbox(
        "Select a programming language:",
        list(languages.keys()),
        index=0,
        help="Choose the language you want the code generated in."
    )
    language_code = languages[language_name]

    user_prompt = st.text_area(
        "Enter your code request:",
        placeholder=f"e.g. Create a responsive login page using {language_name}",
        height=180,
        max_chars=1000
    )

    # Buttons side by side
    btn_col1, btn_col2 = st.columns(2)
    generate_clicked = btn_col1.button("✨ Generate Code")
    reset_clicked = btn_col2.button("🧹 Reset")

with col2:
    st.markdown("### 🚀 Code Output")
    output_placeholder = st.empty()

# --- Reset input ---


# --- Function to generate code ---
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
        "max_tokens": 1200
    }
    try:
        response = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"❌ Network/API error: {str(e)}. Check your API key and connection."
    except KeyError:
        return "❌ Error: Unexpected API response format."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# --- Generate Code ---
if generate_clicked:
    if not user_prompt.strip():
        st.warning("Please enter a description for the code.")
    else:
        with st.spinner("Generating your code..."):
            code_output = generate_code(user_prompt, language_name)

        # Display with line numbers, syntax highlighting
        output_placeholder.code(code_output, language=language_code)

        # Buttons: Download & Copy
       
