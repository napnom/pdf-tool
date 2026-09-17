import streamlit as st
from pypdf import PdfReader, PdfWriter
import io
import os

# Set up page configuration and title
st.set_page_config(page_title="My Mini iLovePDF", page_icon="📄", layout="centered")
st.title("Multi-Tool PDF Web App")
st.write("A locally hosted alternative to iLovePDF.")

# Sidebar navigation for choosing features
option = st.sidebar.selectbox("Choose a tool", ["Merge PDFs", "Extract Pages", "Word to PDF", "MOV to MP4"])


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
# Tool 3: Convert Word to PDF via libreoffice on Cloud Linux
elif option == "Word to PDF":
    st.header("✨ Convert Word Document (.docx) to PDF")
    uploaded_file = st.file_uploader("Upload a Word file", type=["docx"])
    
    if uploaded_file:
        temp_docx = "temp_input.docx"
        
        # Save uploaded file locally
        with open(temp_docx, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        try:
            import subprocess
            import platform
            
            st.info("Converting document... Please wait.")
            
            # Check if running on Windows (Local) or Linux (Streamlit Cloud)
            if platform.system() == "Windows":
                from docx2pdf import convert
                temp_pdf = "temp_output.pdf"
                convert(temp_docx, temp_pdf)
            else:
                # Cloud Environment Linux Subprocess Execution
                # Uses headless LibreOffice to securely parse and build the PDF
                subprocess.run(
                    ["libreoffice", "--headless", "--convert-to", "pdf", temp_docx],
                    check=True
                )
                temp_pdf = "temp_input.pdf"  # LibreOffice naming convention output
            
            # Read converted file bytes
            with open(temp_pdf, "rb") as f:
                pdf_bytes = f.read()
                
            st.success("Conversion successful!")
            st.download_button(
                "📥 Download Converted PDF", 
                data=pdf_bytes, 
                file_name=uploaded_file.name.replace(".docx", ".pdf"), 
                mime="application/pdf"
            )
            
            # Post-cleanup
            os.remove(temp_pdf)
            
        except Exception as e:
            st.error(f"Error during conversion: {e}")
            
        finally:
            if os.path.exists(temp_docx):
                os.remove(temp_docx)

# Tool 4: Convert MOV to MP4 via FFmpeg
elif option == "MOV to MP4":
    st.header("🎬 Convert MOV Video to MP4")
    uploaded_file = st.file_uploader("Upload a .mov video file", type=["mov"])
    
    if uploaded_file:
        temp_mov = "temp_input.mov"
        temp_mp4 = "temp_output.mp4"
        
        # Save uploaded file locally
        with open(temp_mov, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        try:
            import ffmpeg
            
            st.info("Processing video conversion... This might take a moment depending on file size.")
            
            # Execute efficient H.264 video conversion via FFmpeg
            (
                ffmpeg
                .input(temp_mov)
                .output(temp_mp4, vcodec='libx264', acodec='aac', loglevel="error")
                .overwrite_output()
                .run()
            )
            
            # Read converted video bytes
            with open(temp_mp4, "rb") as f:
                video_bytes = f.read()
                
            st.success("Conversion successful!")
            st.download_button(
                "📥 Download MP4 Video", 
                data=video_bytes, 
                file_name=uploaded_file.name.replace(".mov", ".mp4"), 
                mime="video/mp4"
            )
            
        except Exception as e:
            st.error(f"Error during video conversion: {e}")
            
        finally:
            # Safe cleanup of temporary media assets
            if os.path.exists(temp_mov):
                os.remove(temp_mov)
            if os.path.exists(temp_mp4):
                os.remove(temp_mp4)
