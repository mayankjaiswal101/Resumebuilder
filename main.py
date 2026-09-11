import streamlit as st
from fpdf import FPDF
import base64

st.set_page_config(page_title="ATS Resume Builder Pro", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .header-title {
        font-size: 42px; font-weight: 800;
        background: linear-gradient(90deg, #6C63FF, #00D4FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .resume-card {
        background: white; padding: 35px; border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); border: 1px solid #eee;
    }
    .skill-tag {
        display: inline-block; background: #EEF0FF; color: #6C63FF;
        padding: 5px 12px; border-radius: 20px; margin: 3px; font-size: 13px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.25], gap="large")

with col1:
    st.markdown('<div class="header-title">Resume Builder PRO</div>', unsafe_allow_html=True)
    st.caption("Recruiter-approved • ATS Optimized")
    with st.container(border=True):
        st.subheader("👤 Personal Info")
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email")
        phone = st.text_input("Phone", placeholder="Enter phone number")
        linkedin = st.text_input("LinkedIn / Portfolio", placeholder="Enter LinkedIn link")
        location = st.text_input("Location", placeholder="Enter your city")
    with st.container(border=True):
        st.subheader("Details")
        education = st.text_area("Education", placeholder="Enter your education", height=80)
        skills = st.text_area("Skills (comma se alag)", placeholder="Python, Java, SQL", height=80)
        projects = st.text_area("Projects", placeholder="Enter your projects", height=80)
        experience = st.text_area("Experience", placeholder="Enter your experience", height=80)

filled = sum([1 for x in [full_name, email, phone, education, skills, projects, experience] if x.strip() != ""])
ats_score = int((filled / 7) * 100)

with col2:
    st.markdown("### 👀 Live Preview")
    st.progress(ats_score, text=f"ATS Score: {ats_score}%")
    
    skill_html = ""
    if skills:
        for s in skills.split(','):
            if s.strip():
                skill_html += f'<span class="skill-tag">{s.strip()}</span> '
    else:
        skill_html = "<i style='color:#999;'>Skills will appear here</i>"

    html_code = f"""
    <div class="resume-card" style="border-top: 6px solid #6C63FF;">
        <h1 style="margin:0;">{full_name if full_name else 'Your Name'}</h1>
        <p style="color:#666; font-size:13px;">{email if email else 'email'} | {phone if phone else 'phone'} | {location if location else 'location'}<br>{linkedin if linkedin else ''}</p>
        <hr>
        <h4 style="color:#6C63FF;">EDUCATION</h4>
        <p style="font-size:14px;">{education if education else 'Your education details...'}</p>
        <h4 style="color:#6C63FF;">SKILLS</h4>
        <p>{skill_html}</p>
        <h4 style="color:#6C63FF;">PROJECTS</h4>
        <p style="font-size:14px;">{projects if projects else 'Your projects...'}</p>
        <h4 style="color:#6C63FF;">EXPERIENCE</h4>
        <p style="font-size:14px;">{experience if experience else 'Your experience...'}</p>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

    st.write("")
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(108,99,255)
        pdf.rect(0,0,210,25,'F')
        pdf.set_y(6)
        pdf.set_font("Arial", 'B', 20); pdf.set_text_color(255,255,255)
        pdf.cell(0, 10, full_name if full_name else "Your Name", align='C', ln=True)
        pdf.ln(15); pdf.set_text_color(0,0,0)
        pdf.set_font("Arial", 'B', 12); pdf.cell(0, 8, "EDUCATION", ln=True); pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 6, education); pdf.ln(3)
        pdf.set_font("Arial", 'B', 12); pdf.cell(0, 8, "SKILLS", ln=True); pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 6, skills); pdf.ln(3)
        pdf.set_font("Arial", 'B', 12); pdf.cell(0, 8, "PROJECTS", ln=True); pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 6, projects); pdf.ln(3)
        pdf.set_font("Arial", 'B', 12); pdf.cell(0, 8, "EXPERIENCE", ln=True); pdf.set_font("Arial", '', 11); pdf.multi_cell(0, 6, experience)
        return pdf.output(dest='S').encode('latin-1')

    if st.button("📥 Download PRO PDF", use_container_width=True, type="primary"):
        if not full_name:
            st.warning("Please enter your name first")
        else:
            pdf_bytes = create_pdf()
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Resume.pdf"><div style="width:100%; padding:14px; background:#6C63FF; color:white; text-align:center; border-radius:10px; font-weight:700;">⬇️ Click to Download</div></a>'
            st.markdown(href, unsafe_allow_html=True)
            st.balloons()
