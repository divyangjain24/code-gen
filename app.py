import streamlit as st

# Toggle for Dark Mode
dark_mode = st.toggle("🌗 Dark Mode", value=False)

# --- Full-Page CSS Styling ---
light_mode_css = """
<style>
    html, body, .stApp {
        background-color: white !important;
        color: black !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: white !important;
    }

    [data-testid="stHeader"] {
        background-color: white !important;
    }

    [data-testid="stToolbar"] {
        background-color: white !important;
    }

    [data-testid="stSidebar"] {
        background-color: white !important;
        color: black !important;
    }

    .stTextInput > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div,
    .stButton > button {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
    }

    .stButton > button {
        background-color: #007acc !important;
        color: white !important;
    }

    .stButton > button:hover {
        background-color: #005f99 !important;
    }

    ::placeholder {
        color: #666 !important;
    }
</style>
"""

dark_mode_css = """
<style>
    html, body, .stApp {
        background-color: #0e1117 !important;
        color: white !important;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stSidebar"] {
        background-color: #0e1117 !important;
        color: white !important;
    }

    .stTextInput > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div,
    .stButton > button {
        background-color: #1c1f26 !important;
        color: white !important;
        border: 1px solid #444 !important;
    }

    .stButton > button {
        background-color: #005f99 !important;
        color: white !important;
    }

    .stButton > button:hover {
        background-color: #007acc !important;
    }

    ::placeholder {
        color: #aaa !important;
    }
</style>
"""

# Inject the correct CSS
st.markdown(dark_mode_css if dark_mode else light_mode_css, unsafe_allow_html=True)

# --- UI Layout ---
st.markdown("## 💻 AI Code Generator")
st.markdown("### 🧠 Describe what you want and pick your language:")

language = st.selectbox("Select a programming language:", ["Python", "JavaScript", "Java", "C++", "Go"])
code_request = st.text_area("Enter your code request:", placeholder="e.g. Create a login page using Python")

if st.button("✨ Generate Code"):
    if not code_request.strip():
        st.warning("⚠️ Please enter a code request.")
    else:
        st.success(f"✅ Generating {language} code for: `{code_request}`")
        # Placeholder for generated code
        st.code("# Your generated code will appear here", language=language.lower())
