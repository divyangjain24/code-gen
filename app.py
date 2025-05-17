import streamlit as st

# Toggle for Dark Mode
dark_mode = st.toggle("🌗 Dark Mode")

# Apply CSS styles conditionally
if dark_mode:
    st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #0e1117 !important;
            color: white !important;
        }
        label, div, p, h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
        input, textarea, select {
            background-color: #262730 !important;
            color: white !important;
        }
        .stButton > button {
            background-color: #007acc !important;
            color: white !important;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #005f99 !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        html, body, .stApp {
            background-color: white !important;
            color: black !important;
        }
        label, div, p, h1, h2, h3, h4, h5, h6 {
            color: black !important;
        }
        input, textarea, select {
            background-color: white !important;
            color: black !important;
        }
        .stButton > button {
            background-color: #f0f0f0 !important;
            color: black !important;
            font-weight: bold;
            border: 1px solid #ccc !important;
        }
        .stButton > button:hover {
            background-color: #e0e0e0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# App content
st.title("💻 AI Code Generator")
st.markdown("### 🧠 Describe what you want and pick your language:")

# Inputs
language = st.selectbox("Select a programming language:", ["Python", "JavaScript", "Java", "C++", "Go"])
prompt = st.text_area("Enter your code request:", placeholder="e.g. Create a login page using Python")

# Button
if st.button("✨ Generate Code"):
    st.success(f"Generating code for '{language}' with prompt: '{prompt}'")
