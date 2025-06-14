import streamlit as st
import os
import fitz  # PyMuPDF
import PyPDF2
import pdfplumber
from PIL import Image
import tempfile

st.set_page_config(page_title="Easy PDF Handling Tools by Tushar Chaudhari", layout="centered")
st.title("📄 Easy PDF Handling Tools")
st.caption("Made by Tushar Chaudhari | 📧 tusharchaudhari1809@gmail.com")
st.markdown("---")
def save_file(uploaded):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded.read())
        return tmp.name

# IMAGE TO PDF
def image_to_pdf(images):
    image_objs = [Image.open(img).convert("RGB") for img in images]
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    image_objs[0].save(temp_pdf.name, save_all=True, append_images=image_objs[1:])
    return temp_pdf.name

# PDF TO IMAGES
def pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    img_paths = []
    for i in range(len(doc)):
        pix = doc[i].get_pixmap()
        img_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
        pix.save(img_file)
        img_paths.append(img_file)
    return img_paths

# EXTRACT TEXT
def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n\n".join([p.extract_text() or "" for p in pdf.pages])

# EXTRACT IMAGES
def extract_images(pdf_path):
    doc = fitz.open(pdf_path)
    img_paths = []
    for i in range(len(doc)):
        for img_index, img in enumerate(doc[i].get_images(full=True)):
            base = doc.extract_image(img[0])
            ext = base["ext"]
            img_data = base["image"]
            filename = tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}").name
            with open(filename, "wb") as f:
                f.write(img_data)
            img_paths.append(filename)
    return img_paths

# MERGE PDFs
def merge_pdfs(files):
    writer = PyPDF2.PdfWriter()
    for file in files:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)
    output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    with open(output, 'wb') as f:
        writer.write(f)
    return output

# SPLIT PDF
def split_pdf(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    paths = []
    for i, page in enumerate(reader.pages):
        writer = PyPDF2.PdfWriter()
        writer.add_page(page)
        output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        with open(output, 'wb') as f:
            writer.write(f)
        paths.append(output)
    return paths

# ENCRYPT PDF
def encrypt_pdf(pdf_path, password):
    reader = PyPDF2.PdfReader(pdf_path)
    writer = PyPDF2.PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    writer.encrypt(password)
    output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    with open(output, 'wb') as f:
        writer.write(f)
    return output

# DECRYPT PDF
def decrypt_pdf(pdf_path, password):
    reader = PyPDF2.PdfReader(pdf_path)
    reader.decrypt(password)
    writer = PyPDF2.PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    with open(output, 'wb') as f:
        writer.write(f)
    return output

# ADD METADATA
def add_metadata(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    writer = PyPDF2.PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    writer.add_metadata({
        "/Author": "Tushar Chaudhari",
        "/Title": "PDF Generated by Tushar Chaudhari"
    })
    output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    with open(output, 'wb') as f:
        writer.write(f)
    return output

# Streamlit app setup
st.sidebar.title("PDF Tools")
# SIDEBAR OPTIONS
option = st.sidebar.selectbox("Choose a tool", [
    "Image to PDF", "PDF to Images", "Extract Text", "Extract Images",
    "Merge PDFs", "Split PDF", "Encrypt PDF", "Decrypt PDF", "Add Metadata"
])
# Sidebar info section
st.sidebar.markdown("---")
st.sidebar.markdown("### About the App")
st.sidebar.markdown("This app provides a set of tools to handle PDF files easily. You can convert images to PDF, extract text and images from PDFs, merge and split PDFs, encrypt and decrypt PDFs, and add metadata to your PDF files.")
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ by **Tushar Chaudhari**")

st.sidebar.markdown("Feel free to reach out if you have any questions or feedback!")
st.sidebar.markdown("Contact: [tusharchaudhari1809@gmail.com](mailto:tusharchaudhari1809@gmail.com)")



# UI LOGIC
if option == "Image to PDF":
    st.header("🖼️ Convert Images to PDF")
    imgs = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if imgs and st.button("Convert"):
        pdf = image_to_pdf(imgs)
        with open(pdf, "rb") as f:
            st.download_button("Download PDF", f, "converted.pdf")

elif option == "PDF to Images":
    st.header("📤 Convert PDF to Images")
    file = st.file_uploader("Upload PDF", type="pdf")
    if file and st.button("Convert"):
        pdf = save_file(file)
        images = pdf_to_images(pdf)
        for img in images:
            st.image(img)
            with open(img, "rb") as f:
                st.download_button("Download", f, file_name=os.path.basename(img))

elif option == "Extract Text":
    st.header("📝 Extract Text from PDF")
    file = st.file_uploader("Upload PDF", type="pdf")
    if file and st.button("Extract"):
        pdf = save_file(file)
        st.text_area("Extracted Text", extract_text(pdf), height=300)

elif option == "Extract Images":
    st.header("🖼️ Extract Images from PDF")
    file = st.file_uploader("Upload PDF", type="pdf")
    if file and st.button("Extract"):
        pdf = save_file(file)
        imgs = extract_images(pdf)
        for i in imgs:
            st.image(i)
            with open(i, "rb") as f:
                st.download_button("Download", f, file_name=os.path.basename(i))

elif option == "Merge PDFs":
    st.header("📑 Merge PDFs")
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if files and st.button("Merge"):
        output = merge_pdfs(files)
        with open(output, "rb") as f:
            st.download_button("Download Merged PDF", f, "merged.pdf")

elif option == "Split PDF":
    st.header("✂️ Split PDF into Pages")
    file = st.file_uploader("Upload PDF", type="pdf")
    if file and st.button("Split"):
        pdf = save_file(file)
        split = split_pdf(pdf)
        for i, part in enumerate(split):
            with open(part, "rb") as f:
                st.download_button(f"Page {i+1}", f, f"page_{i+1}.pdf")

elif option == "Encrypt PDF":
    st.header("🔒 Encrypt PDF")
    file = st.file_uploader("Upload PDF", type="pdf")
    password = st.text_input("Set Password", type="password")
    if file and password and st.button("Encrypt"):
        pdf = save_file(file)
        encrypted = encrypt_pdf(pdf, password)
        with open(encrypted, "rb") as f:
            st.download_button("Download Encrypted PDF", f, "encrypted.pdf")

elif option == "Decrypt PDF":
    st.header("🔓 Decrypt PDF")
    file = st.file_uploader("Upload Encrypted PDF", type="pdf")
    password = st.text_input("Enter Password", type="password")
    if file and password and st.button("Decrypt"):
        pdf = save_file(file)
        try:
            decrypted = decrypt_pdf(pdf, password)
            with open(decrypted, "rb") as f:
                st.download_button("Download Decrypted PDF", f, "decrypted.pdf")
        except Exception as e:
            st.error("Failed to decrypt. Check password.")

elif option == "Add Metadata":
    st.header("🏷️ Add Metadata to PDF")
    file = st.file_uploader("Upload PDF", type="pdf")
    if file and st.button("Add Metadata"):
        pdf = save_file(file)
        updated = add_metadata(pdf)
        with open(updated, "rb") as f:
            st.download_button("Download PDF with Metadata", f, "metadata_added.pdf")





st.markdown("---")
