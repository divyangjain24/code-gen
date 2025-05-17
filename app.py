import streamlit as st
import requests

# Load OpenAI API key
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# UI Setup
st.set_page_config(page_title="AI Code Generator", layout="centered")
st.markdown("<h1 style='text-align: center; color: #2196F3;'>AI Code Generator 🤖💻</h1>", unsafe_allow_html=True)
st.markdown("### Describe the code you want:")

# Function to generate code from OpenAI
def generate_code(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a professional software engineer who writes clean, working, and commented code."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 1000
    }

    try:
        response = requests.post(OPENAI_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return "⚠️ No code returned from OpenAI."

    except requests.exceptions.RequestException as e:
        return f"❌ API request failed: {str(e)}"
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

# User input
user_prompt = st.text_area("🧠 What should the code do?", placeholder="e.g. Create a BMI calculator in Python")

if st.button("Generate Code"):
    if user_prompt.strip():
        st.markdown("### ✨ Generated Code:")
        generated_code = generate_code(user_prompt)
        st.code(generated_code, language="python")
    else:
        st.warning("Please enter a prompt.")
