import streamlit as st
from fpdf import FPDF
import base64

st.set_page_config(page_title="ATS Resume Builder", page_icon="📄", layout="wide")

st.markdown("""
<style>
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        border-radius: 10px; border: 1px solid #e0e0e0;
    }
    .resume-card {
        background: white; padding: 30px; border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 5px solid #6C63FF;
    }
    .header-title {
        font-size: 38px; font-weight: 800;
        background: linear-gradient(90deg, #6C63FF, #48C6EF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="header-title">ATS Resume Builder</div>', unsafe_allow_html=True)
    st.subheader("Personal Info")
    full_name = st.text_input("Full Name", placeholder="Enter your full name")
    email = st.text_input("Email", placeholder="yourname@gmail.com")
    phone = st.text_input("Phone", placeholder="9876543210")
    linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/yourname")
    st.subheader("Education")
    education = st.text_area("Education", placeholder="B.Tech CSE - College Name", height=80)
    st.subheader("Skills")
    skills = st.text_area("Skills", placeholder="Python, Java, SQL", height=80)
    st.subheader("Experience")
    experience = st.text_area("Experience", placeholder="Intern at ABC Company", height=120)

with col2:
    st.markdown("### Live Preview")
    preview_name = full_name if full_name else "Your Name"
    preview_contact = f"{email} | {phone}" if (email or phone) else "Your details here"
    st.markdown(f"""
    <div class="resume-card">
        <h2 style="margin:0;">{preview_name}</h2>
        <p style="color:#6C63FF; font-size:14px;">{preview_contact}</p>
        <hr>
        <h4>EDUCATION</h4><p>{education if education else '...'}</p>
        <h4>SKILLS</h4><p>{skills if skills else '...'}</p>
        <h4>EXPERIENCE</h4><p>{experience if experience else '...'}</p>
    </div>
    """, unsafe_allow_html=True)

    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 22)
        pdf.cell(0, 12, full_name, ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(100,100,100)
        pdf.cell(0, 8, f"{email} | {phone} | {linkedin}", ln=True)
        pdf.set_text_color(0,0,0)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "EDUCATION", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 6, education)
        pdf.ln(3)
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "SKILLS", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 6, skills)
        pdf.ln(3)
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "EXPERIENCE", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 6, experience)
        return pdf.output(dest='S').encode('latin-1')

    if st.button("Download as PDF", use_container_width=True, type="primary"):
        if not full_name:
            st.error("Pehle Full Name bhar de bhai!")
        else:
            pdf_bytes = create_pdf()
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{full_name}_Resume.pdf" style="text-decoration:none;"><button style="width:100%; padding:12px; background:#6C63FF; color:white; border:none; border-radius:10px; font-size:16px;">Click Here to Download</button></a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("PDF Ready!")
