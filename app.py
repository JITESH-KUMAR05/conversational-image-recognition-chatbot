import streamlit as st
from streamlit.components.v1 import html

from config import Config
from helpers.image_helper import create_temp_file
from helpers.llm_helper import analyze_image_file, stream_parser

page_title = Config.PAGE_TITLE

# Configures page settings
st.set_page_config(page_title=page_title, initial_sidebar_state="expanded", layout="wide")

# Define responsive CSS styles
css_styles = """
<style>
.stApp {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    max-width: 100%;
}

.stTitle {
    font-size: clamp(20px, 4vw, 24px);
    font-weight: bold;
    color: #333;
}

.stText {
    font-size: clamp(14px, 3vw, 16px);
    color: #555;
}

.stImage {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 5px;
    max-width: 100%;
    height: auto;
}

.analysis-container {
    padding: 10px;
    margin: 10px 0;
}

/* Media Queries */
@media (max-width: 768px) {
    .analysis-container {
        flex-direction: column;
    }
}
</style>
"""

# Add CSS styles to the app
html(css_styles)

# Page title
st.title(page_title)

st.markdown("Select an image file to analyze.")

# Displays file upload widget
uploaded_file = st.file_uploader("Choose image file", type=['png', 'jpg', 'jpeg'])

image_model = 'llava:7b'

if chat_input := st.chat_input("What would you like to ask?"):
    if uploaded_file is None:
        st.error('You must select an image file to analyze!')
        st.stop()

    with st.spinner("Processing image..."):
        temp_image = create_temp_file(uploaded_file)
        if temp_image:
            # Responsive columns with dynamic ratios
            screen_width = st.session_state.get('screen_width', 1200)
            col_ratio = [1, 2] if screen_width < 768 else [2, 8]
            
            col1, col2 = st.columns(col_ratio)
            
            with col1:
                # Make image responsive
                img_width = min(300, int(screen_width * 0.3))
                st.image(temp_image, width=img_width, use_column_width=True)
            
            with col2:
                with st.container():
                    st.markdown("### Analysis Results")
                    stream = analyze_image_file(uploaded_file, model=image_model, user_prompt=chat_input)
                    stream_output = st.write_stream(stream_parser(stream))

    st.success("Image analysis complete!")

# Add JavaScript to detect screen width
st.markdown("""
<script>
    // Update screen width in session state
    const updateScreenWidth = () => {
        const width = window.innerWidth;
        sessionStorage.setItem('screen_width', width);
    };
    
    window.addEventListener('resize', updateScreenWidth);
    updateScreenWidth();
</script>
""", unsafe_allow_html=True)