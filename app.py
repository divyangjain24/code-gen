import streamlit as st

# --- Theme Toggle ---
dark_mode = st.toggle("🌗 Dark Mode", value=False)

# --- CSS Styling ---
light_css = """
<style>
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    .stTextInput, .stTextArea, .stSelectbox, .stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ccc !important;
    }

    .stButton > button {
        background-color: #007acc !important;
        color: white !important;
        border: none !important;
    }

    .stButton > button:hover {
        background-color: #005f99 !important;
    }

    ::placeholder {
        color: #555 !important;
    }
</style>
"""

dark_css = """
<style>
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }

    .stTextInput, .stTextArea, .stSelectbox, .stButton > button {
        background-color: #1c1f26 !important;
        color: #ffffff !important;
        border: 1px solid #555 !important;
    }

    .stButton > button {
        background-color: #005f99 !important;
        color: white !important;
        border: none !important;
    }

    .stButton > button:hover {
        background-color: #007acc !important;
    }

    ::placeholder {
        color: #aaa !important;
    }
</style>
"""

# Inject appropriate CSS
st.markdown(dark_css if dark_mode else light_css, unsafe_allow_html=True)

# --- UI Layout ---
st.markdown("## 💻 AI Code Generator")
st.markdown("### 🧠 Describe what you want and pick your language:")

language = st.selectbox("Select a programming language:", ["Python", "JavaScript", "Java", "C++", "Go"])

code_request = st.text_area("Enter your code request:", placeholder="e.g. Create a login page using Python")

if st.button("✨ Generate Code"):
    if code_request.strip() == "":
        st.warning("⚠️ Please enter a code request.")
    else:
        st.success(f"✅ Generating {language} code for: `{code_request}`")
        # Placeholder for actual code generation logic
        st.code("# Your generated code will appear here", language=language.lower())
