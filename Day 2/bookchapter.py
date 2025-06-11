import streamlit as st
import os
import tempfile
import google.generativeai as genai

# ✅ Single API key line
genai.configure(api_key="AIzaSyCaAF8nMeqTfcbcNPPMG6RDiUht5N8sJZs")

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")
# ----------------------------------------------------------
# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# ----------------------------------------------------------
# Function to generate summary, key takeaways, and tags
def generate_summary_and_tags(text, output_format):
    prompt = (
        f"Given the following book chapter content:\n\n{text}\n\n"
        f"Generate:\n"
        f"1. A concise summary (50-100 words)\n"
        f"2. Key takeaways (bullet points)\n"
        f"3. Relevant tags (comma-separated)\n"
        f"4. Generate a book chapter in the format: {output_format}.\n\n"
        "Provide the output in an easy-to-understand format."
    )

    response = model.generate_content(prompt)
    return response.text

# ----------------------------------------------------------
# Streamlit App
st.set_page_config(page_title="📚 Book Chapter Generator", layout="wide")

st.title("📚 Book Chapter Generator with Gemini API")

# Instructions
st.markdown("""
Welcome! Use this application to:
✅ Upload your book chapter (PDF or Text)  
✅ Get a concise summary, key takeaways, and relevant tags  
✅ Generate a book chapter in your desired format  
✅ Download the generated content

**Required Fields for Data Analysts & Book Chapters:**
- Chapter title
- Author name
- Book name
- Data analyst's notes
- Additional context (optional)

**Let's get started!**
""")

# ----------------------------------------------------------
# Input fields
chapter_title = st.text_input("📖 Chapter Title", "")
author_name = st.text_input("✍️ Author Name", "")
book_name = st.text_input("📚 Book Name", "")
analyst_notes = st.text_area("📊 Data Analyst's Notes", "", height=100)
additional_context = st.text_area("📝 Additional Context (Optional)", "", height=100)

# Upload file or paste text
upload_option = st.radio(
    "📤 Upload a PDF/Text file or paste the text directly:",
    ["Upload File", "Paste Text"]
)

uploaded_file = None
pasted_text = None
extracted_text = ""

if upload_option == "Upload File":
    uploaded_file = st.file_uploader("Choose a PDF or text file", type=["pdf", "txt"])
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            extracted_text = extract_text_from_pdf(uploaded_file)
        else:
            extracted_text = uploaded_file.read().decode("utf-8")
else:
    pasted_text = st.text_area("Paste your chapter text here:", "", height=200)
    extracted_text = pasted_text

# Format selection
output_format = st.selectbox(
    "📁 Select output format for your book chapter:",
    ["PDF", "DOCX", "Markdown", "Plain Text"]
)

# ----------------------------------------------------------
# Generate and Download
if extracted_text and chapter_title and author_name and book_name:
    if st.button("🚀 Generate Book Chapter"):
        with st.spinner("Generating content using Gemini API..."):
            final_text = f"""
Chapter Title: {chapter_title}
Author: {author_name}
Book Name: {book_name}
Data Analyst's Notes: {analyst_notes}
Additional Context: {additional_context}

Generated Content:
-------------------
{generate_summary_and_tags(extracted_text, output_format)}
"""
            st.session_state.generated_text = final_text
            st.success("✅ Book chapter generated successfully!")

            # Show generated content
            st.subheader("📄 Generated Book Chapter")
            st.text_area("Here’s your generated chapter:", final_text, height=300)

            # Download button
            file_extension = {
                "PDF": "pdf",
                "DOCX": "docx",
                "Markdown": "md",
                "Plain Text": "txt"
            }[output_format]

            # Save generated text to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                tmp_file.write(final_text.encode("utf-8"))
                tmp_file_path = tmp_file.name

            with open(tmp_file_path, "rb") as f:
                st.download_button(
                    label=f"📥 Download as {file_extension.upper()}",
                    data=f,
                    file_name=f"{chapter_title}.{file_extension}",
                    mime="application/octet-stream"
                )

# ----------------------------------------------------------
# Regenerate Button
if "generated_text" in st.session_state:
    if st.button("🔄 Regenerate Book Chapter"):
        with st.spinner("Regenerating with Gemini API..."):
            regenerated_text = generate_summary_and_tags(extracted_text, output_format)
            st.session_state.generated_text = regenerated_text
            st.success("✅ Book chapter regenerated!")
            st.text_area("🔄 Regenerated Book Chapter:", regenerated_text, height=300)

# ----------------------------------------------------------
# Footer
st.markdown("---")
st.caption("Powered by Gemini API | © 2025 Book Chapter Generator App")

