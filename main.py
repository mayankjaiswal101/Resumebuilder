import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Resume Builder", page_icon="📄")
st.title("📄 ATS Resume Builder")

# Form
name = st.text_input("Full Name", "Akshad")
email = st.text_input("Email", "akshad@gmail.com")
phone = st.text_input("Phone", "9876543210")
education = st.text_area("Education", "B.Tech in CSE - XYZ College")
skills = st.text_area("Skills", "Python, Java, SQL, Machine Learning")
experience = st.text_area("Experience", "Intern at ABC Company - 3 months")
projects = st.text_area("Projects", "Resume Builder App using Python")

if st.button("Generate Resume PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, name, ln=True, align='C')
    
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Email: {email} | Phone: {phone}", ln=True, align='C')
    pdf.ln(10)
    
    def add_section(title, content):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 7, content)
        pdf.ln(5)
    
    add_section("EDUCATION", education)
    add_section("SKILLS", skills)
    add_section("EXPERIENCE", experience)
    add_section("PROJECTS", projects)
    
    pdf_file = f"{name}_Resume.pdf"
    pdf.output(pdf_file)
    
    with open(pdf_file, "rb") as f:
        st.success("Resume Ban Gaya! 👇")
        st.download_button("Download PDF", f, file_name=pdf_file)

