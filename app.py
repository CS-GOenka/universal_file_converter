import streamlit as st
import os
from markitdown import MarkItDown
import fitz  # PyMuPDF
import requests

st.set_page_config(page_title="Universal Doc Converter", page_icon="📄")

def convert_pdf_to_text(uploaded_file):
    """Fallback robust PDF conversion using PyMuPDF"""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("markdown")  # Attempts to preserve layout
    return text

def main():
    st.title("📄 Universal File-to-Markdown")
    st.info("Upload Word, Excel, PPT, or PDF files below.")

    mid = MarkItDown()

    uploaded_files = st.file_uploader("Choose files", 
                                     type=["pdf", "docx", "xlsx", "pptx", "html"], 
                                     accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            with st.expander(f"Processing: {uploaded_file.name}", expanded=True):
                try:
                    if file_ext == ".pdf":
                        # Use the more reliable PyMuPDF for PDFs
                        md_content = convert_pdf_to_text(uploaded_file)
                    else:
                        # Use MarkItDown for Office Docs
                        result = mid.convert_stream(uploaded_file, file_extension=file_ext)
                        md_content = result.text_content

                    if not md_content.strip():
                        st.warning("⚠️ The file appears to be empty or an image-only scan.")
                    
                    st.text_area("Preview", md_content, height=250, key=uploaded_file.name)
                    
                    st.download_button(
                        "📥 Download Markdown",
                        md_content,
                        file_name=f"{base_name}_converted.md",
                        key=f"dl_{uploaded_file.name}"
                    )
                except Exception as e:
                    st.error(f"⚠️ Could not read {uploaded_file.name}. Error details: {e}")

if __name__ == "__main__":
    main()
