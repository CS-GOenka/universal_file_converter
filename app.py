import streamlit as st
import os
from markitdown import MarkItDown
import requests

# Page Configuration
st.set_page_config(page_title="Universal Doc Converter", page_icon="📄", layout="wide")

def main():
    st.title("📄 Universal File-to-Markdown Converter")
    st.markdown("Upload your Office docs, PDFs, or HTML files to get clean, LLM-ready Markdown text.")

    # Initialize MarkItDown with custom request settings for stability
    # We use a session to apply the User-Agent and timeout globally
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    
    # MarkItDown supports passing a custom requests session
    mid = MarkItDown(requests_session=session)

    # [2] Upload Area
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["docx", "xlsx", "pptx", "pdf", "html", "htm"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.divider()
        
        for uploaded_file in uploaded_files:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            with st.expander(f"Processing: {uploaded_file.name}", expanded=True):
                try:
                    # [3] Resilience: Processing the file within a try-except block
                    # We pass the file stream directly to MarkItDown
                    # Note: We provide the file extension so MarkItDown knows how to parse it
                    result = mid.convert_stream(uploaded_file, file_extension=file_extension)
                    converted_text = result.text_content

                    # [2] Instant Preview
                    st.text_area(
                        label="Extracted Content",
                        value=converted_text,
                        height=300,
                        key=f"text_{uploaded_file.name}"
                    )

                    # [2 & 4] Download Options
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            label="📥 Download as Markdown (.md)",
                            data=converted_text,
                            file_name=f"{base_name}_converted.md",
                            mime="text/markdown",
                            key=f"md_{uploaded_file.name}"
                        )
                    
                    with col2:
                        st.download_button(
                            label="📥 Download as Text (.txt)",
                            data=converted_text,
                            file_name=f"{base_name}_converted.txt",
                            mime="text/plain",
                            key=f"txt_{uploaded_file.name}"
                        )

                except Exception as e:
                    # [3] Polite Error Handling
                    st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                    # Optional: Uncomment for debugging
                    # st.info(f"Technical details: {str(e)}")

if __name__ == "__main__":
    main()
