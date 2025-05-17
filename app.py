import streamlit as st

# Title
st.title("💻 AI Code Generator")

# Dark mode toggle
dark_mode = st.toggle("Dark Mode")

# CSS for dark mode
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
    .stSelectbox > div {
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #555 !important;
    }

    .stButton > button {
        background-color: #007acc !important;
        color: white !important;
        border: none !important;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #005f99 !important;
        color: white !important;
    }

    ::placeholder {
        color: #bbb !important;
    }
</style>
"""

# CSS for light mode
light_mode_css = """
<style>
    html, body, .stApp {
        background-color: white !important;
        color: black !important;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stSidebar"] {
        background-color: white !important;
        color: black !important;
    }

    .stTextInput > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
    }

    .stButton > button {
        background-color: #f0f0f0 !important;
        color: black !important;
        border: 1px solid #ccc !important;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #e0e0e0 !important;
        color: black !important;
    }

    ::placeholder {
        color: #666 !important;
    }
</style>
"""

# Apply the correct CSS
if dark_mode:
    st.markdown(dark_mode_css, unsafe_allow_html=True)
else:
    st.markdown(light_mode_css, unsafe_allow_html=True)

# Page content
st.markdown("### 🧠 Describe what you want and pick your language:")

language = st.selectbox("Select a programming language:", ["Python", "JavaScript", "Java", "C++", "Go"])
prompt = st.text_area("Enter your code request:", placeholder="e.g. Create a login page using Python")

if st.button("✨ Generate Code"):
    st.success(f"Generating code for '{language}' with prompt: '{prompt}'")
    # Your actual generation logic goes here
