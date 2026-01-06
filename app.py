import streamlit as st
import os
import logging
import traceback
import tempfile
from markitdown import MarkItDown
import requests

# 1. Setup Logging to Terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Debug Doc Converter", page_icon="🔍")

def main():
    st.title("📄 Universal Converter (Debug Mode)")
    st.info("Check the terminal for real-time logs. Errors will appear below if conversion fails.")

    # Initialize MarkItDown
    try:
        # We initialize without a session first to minimize complexity
        md = MarkItDown()
        logger.info("MarkItDown Engine Initialized Successfully.")
    except Exception as e:
        st.error(f"Engine Init Failed: {e}")
        logger.error(f"Engine Init Failed: {e}")
        return

    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            logger.info(f"--- Starting Process for: {uploaded_file.name} ---")
            
            with st.expander(f"Processing: {uploaded_file.name}", expanded=True):
                try:
                    # 2. Save to a temporary file
                    # This is the most 'fail-proof' way to handle PDFs
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    logger.info(f"File saved to temp path: {tmp_path}")
                    st.write(f"⏳ Attempting conversion for `{file_ext}`...")

                    # 3. Perform Conversion
                    # We use convert() on the path instead of convert_stream()
                    logger.info(f"Calling md.convert() for {tmp_path}")
                    result = md.convert(tmp_path)
                    
                    md_content = result.text_content
                    logger.info(f"Conversion successful for {uploaded_file.name}")

                    # 4. Display Result
                    st.success("✅ Conversion Successful")
                    st.text_area("Content Preview", md_content, height=300, key=f"prev_{uploaded_file.name}")
                    
                    st.download_button(
                        label="Download Markdown",
                        data=md_content,
                        file_name=f"{base_name}.md",
                        key=f"dl_{uploaded_file.name}"
                    )

                    # Cleanup temp file
                    os.remove(tmp_path)
                    logger.info(f"Temporary file {tmp_path} removed.")

                except Exception as e:
                    # 5. Show Full Error on UI
                    error_stack = traceback.format_exc()
                    logger.error(f"Failed to convert {uploaded_file.name}")
                    logger.error(error_stack)
                    
                    st.error(f"❌ **Could not read {uploaded_file.name}**")
                    st.warning("Technical Error Log:")
                    st.code(error_stack, language='python')

if __name__ == "__main__":
    main()
