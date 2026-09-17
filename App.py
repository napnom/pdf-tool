import streamlit as st
from pypdf import PdfReader, PdfWriter
import io
import os

# Set up page configuration and title
st.set_page_config(page_title="My Mini iLovePDF", page_icon="📄", layout="centered")
st.title("Multi-Tool PDF Web App")
st.write("A locally hosted alternative to iLovePDF.")

# Sidebar navigation for choosing features
option = st.sidebar.selectbox("Choose a tool", ["Merge PDFs", "Extract Pages", "Word to PDF"])

# Tool 1: Merge PDFs functionality using pypdf and BytesIO streams
if option == "Merge PDFs":
    st.header(" Merge Multiple PDFs")
    uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
    if uploaded_files and st.button("Merge Files"):
        writer = PdfWriter()
        for uploaded_file in uploaded_files:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                writer.add_page(page)
        output_pdf = io.BytesIO()
        writer.write(output_pdf)
        output_pdf.seek(0)
        st.download_button("📥 Download Merged PDF", data=output_pdf, file_name="merged_document.pdf", mime="application/pdf")

# Tool 2: Extract specific pages or ranges
elif option == "Extract Pages":
    st.header(" Extract Pages from PDF")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        total_pages = len(reader.pages)
        page_range = st.text_input("Enter page numbers/range (e.g., 1, 3, 5-7):", value="1")
        if st.button("Extract Pages"):
            writer = PdfWriter()
            pages_to_extract = set()
            try:
                for part in page_range.split(','):
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        pages_to_extract.update(range(start - 1, end))
                    else:
                        pages_to_extract.add(int(part) - 1)
                for page_num in sorted(pages_to_extract):
                    if 0 <= page_num < total_pages:
                        writer.add_page(reader.pages[page_num])
                output_pdf = io.BytesIO()
                writer.write(output_pdf)
                output_pdf.seek(0)
                st.download_button("📥 Download Extracted Pages", data=output_pdf, file_name="extracted_pages.pdf", mime="application/pdf")
            except Exception:
                st.error("Invalid page range format.")

# Tool 3: Convert Word to PDF via dxpdf utility
# Tool 3: Convert Word to PDF via docx2pdf
elif option == "Word to PDF":
    st.header("Convert Word Document (.docx) to PDF")
    uploaded_file = st.file_uploader("Upload a Word file", type=["docx"])
    
    if uploaded_file:
        temp_docx = "temp_input.docx"
        temp_pdf = "temp_output.pdf"
        
        # Save uploaded file locally
        with open(temp_docx, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        try:
            # Import library inside block to ensure it loads cleanly
            from docx2pdf import convert
            
            # Perform conversion cleanly natively on Windows
            convert(temp_docx, temp_pdf)
            
            # Read converted file
            with open(temp_pdf, "rb") as f:
                pdf_bytes = f.read()
                
            st.success("Conversion successful!")
            st.download_button(
                "📥 Download Converted PDF", 
                data=pdf_bytes, 
                file_name=uploaded_file.name.replace(".docx", ".pdf"), 
                mime="application/pdf"
            )
            
        except Exception as e:
            st.error(f"Error during conversion: {e}")
            
        finally:
            # Clean up temp files safely even if execution crashed
            if os.path.exists(temp_docx):
                os.remove(temp_docx)
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)
