import streamlit as st
import os
from markitdown import MarkItDown
import requests

st.set_page_config(page_title="Universal Doc Converter", page_icon="📄")

def main():
    st.title("📄 Universal File-to-Markdown")
    
    # Setup MarkItDown with a stable session
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    mid = MarkItDown(requests_session=session)

    uploaded_files = st.file_uploader("Upload Docs (PDF, Word, Excel, etc.)", 
                                     type=["pdf", "docx", "xlsx", "pptx", "html"], 
                                     accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            with st.expander(f"📄 {uploaded_file.name}", expanded=True):
                try:
                    # Crucial: Pass the extension hint for PDFs
                    result = mid.convert_stream(uploaded_file, file_extension=file_ext)
                    md_content = result.text_content
                    
                    st.text_area("Preview", md_content, height=250, key=uploaded_file.name)
                    
                    # Download button
                    st.download_button(
                        "Download .md",
                        md_content,
                        file_name=f"{os.path.splitext(uploaded_file.name)[0]}.md"
                    )
                except Exception as e:
                    st.error(f"⚠️ Could not read {uploaded_file.name}. Error: {e}")

if __name__ == "__main__":
    main()
