import streamlit as st
from config import Config
from helpers.image_helper import create_temp_file
from helpers.llm_helper import analyze_image_file, stream_parser

page_title = Config.PAGE_TITLE

# Configure page settings
st.set_page_config(
    page_title=page_title,
    layout="wide",  # Use wide layout for better control
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        font-family: sans-serif; /* Customize font */
    }
    .st-bb {
        border: 1px solid #ccc; /* Border for boxes */
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .st-h1 {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .st-expanderHeader {
        font-weight: bold;
        background-color: #f0f0f0; /* Background color for expander header */
        padding: 10px;
        border-radius: 5px;
    }
    .image-container {
        max-width: 40%; /* Adjust as needed */
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page title
st.title(page_title)

# Create a container for better spacing control
with st.container():
    col1, col2 = st.columns([1, 2])  # Adjust column widths (1:2 ratio)

    # Image upload section
    with col1:
        st.markdown("**Select an image file to analyze.**")
        with st.container():  # Add a container for image styling
            st.markdown(
                """
                <div class="image-container"> 
                    {0} 
                </div>
                """.format(st.file_uploader("Choose image file", type=['png', 'jpg', 'jpeg'])),
                unsafe_allow_html=True
            )

    # Chat input section
    with col2:
        # Display chat input immediately after image upload
        if chat_input := st.chat_input("What would you like to ask?"):
            if uploaded_file is None:
                st.error('You must select an image file to analyze!')
                st.stop()

            with st.status(":red[Processing image file. DON'T LEAVE THIS PAGE WHILE IMAGE FILE IS BEING ANALYZED...]", expanded=True) as status:
                st.write(":orange[Analyzing Image File...]")

                # Create the audio file
                stream = analyze_image_file(uploaded_file, model=image_model, user_prompt=chat_input)

                # Process and display the stream output
                stream_output = st.write_stream(stream_parser(stream))

                st.write(":green[Done analyzing image file]")
