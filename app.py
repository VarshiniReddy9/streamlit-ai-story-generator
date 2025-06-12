import streamlit as st
from PIL import Image
import google.generativeai as genai
import io

# Configure your Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) 
# Use Gemini 1.5 Flash model
model = genai.GenerativeModel("models/gemini-1.5-flash")

st.set_page_config(page_title="Image to Story Generator", layout="centered")
st.title("📸📝 Image to Story Generator")
st.write("Upload an image and watch AI turn it into a short story!")

# Genre selector
genre = st.selectbox("Choose a story genre", ["Fairy Tale", "Adventure", "Sci-Fi", "Mystery", "Children"])

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    image_bytes = uploaded_file.read()

    prompt = f"""
    Imagine you're a creative writer. Based on the image I upload, write a short story in the style of a {genre}.

    Make it imaginative and engaging. Aim for about 100-200 words. Keep it appropriate for general audiences.
    """

    with st.spinner("Crafting your story..."):
        try:
            response = model.generate_content([
                prompt,
                {"mime_type": "image/png", "data": image_bytes}
            ])
            story = response.text
            st.subheader("📖 Your AI-Generated Story")
            st.write(story)

            # Optional: Download story as text file
            st.download_button("📥 Download Story", story, file_name="story.txt")

        except Exception as e:
            st.error("❌ Error generating story. Please try with a different image.")
            st.exception(e)
