import streamlit as st
from fpdf import FPDF
import base64
import re

st.set_page_config(page_title="ATS Resume Builder Pro", page_icon="🚀", layout="wide")

# --- CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
    .header-title {
        font-size: 42px; font-weight: 800;
        background: linear-gradient(90deg, #6C63FF, #00D4FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .resume-card {
        background: white; padding: 35px; border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); border: 1px solid #eee;
        min-height: 600px;
    }
    .skill-tag {
        display: inline-block; background: #EEF0FF; color: #6C63FF;
        padding: 5px 12px; border-radius: 20px; margin: 3px; font-size: 13px; font-weight: 600;
    }
    .section-title {
        color: #6C63FF; font-weight: 800; font-size: 14px; letter-spacing: 1px; margin-top:20px; border-bottom: 2px solid #EEF0FF; padding-bottom:5px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR TEMPLATE SELECTOR ---
with st.sidebar:
    st.markdown("### 🎨 Design Studio")
    template = st.selectbox("Template Choose Karo", ["Modern Pro", "Google Clean", "Minimal ATS"])
    st.divider()
    st.markdown("### 📊 ATS Score")
    
# --- LAYOUT ---
col1, col2 = st.columns([1, 1.25], gap="large")

with col1:
    st.markdown('<div class="header-title">Resume Builder PRO</div>', unsafe_allow_html=True)
    st.caption("Recruiter-approved • ATS Optimized • 2025 Ready")
    
    with st.container(border=True):
        st.subheader("👤 Personal Info")
        full_name = st.text_input("Full Name", placeholder="MAYANK JAISWAL")
        email = st.text_input("Email", placeholder="mayank@email.com")
        phone = st.text_input("Phone", placeholder="9270xxxxxx")
        linkedin = st.text_input("LinkedIn / Portfolio", placeholder="linkedin.com/in/mayank")
        location = st.text_input("Location", placeholder="Nagpur, India")

    with st.container(border=True):
        st.subheader("🎓 Education")
        education = st.text_area("Education", placeholder="B.Tech CSE - RTMNU - 2026\nCGPA: 8.5", height=90)
        st.subheader("💻 Skills (comma se alag karo)")
        skills = st.text_area("Skills", placeholder="Python, Java, SQL, React, DSA", height=80)
        st.subheader("🚀 Projects")
        projects = st.text_area("Projects", placeholder="ATS Resume Builder - Built with Streamlit & Python", height=90)
        st.subheader("💼 Experience")
        experience = st.text_area("Experience", placeholder="SDE Intern @ XYZ - Built API...", height=90)

# --- LOGIC FOR ATS SCORE ---
filled = sum([1 for x in [full_name, email, phone, education, skills, projects, experience] if x.strip() != ""])
ats_score = int((filled / 7) * 100)
if len(skills.split(',')) > 5: ats_score = min(100, ats_score+10)

with st.sidebar:
    st.progress(ats_score, text=f"{ats_score}% Complete")
    if ats_score < 50: st.error("Thoda aur bharo, ATS low hai")
    elif ats_score < 80: st.warning("Good progress, skills add karo")
    else: st.success("🔥 Excellent! FAANG Ready Resume")
    st.info(f"Template: **{template}**")

# --- LIVE PREVIEW ---
with col2:
    st.markdown("### 👀 Live Preview")
    
    # Skills to tags
    skill_html = ""
    if skills:
        for s in skills.split(','):
            if s.strip():
                skill_html += f'<span class="skill-tag">{s.strip()}</span>'
    else:
        skill_html = "..."

    # Template Color Logic
    accent = "#6C63FF" if template == "Modern Pro" else "#1A73E8" if template == "Google Clean" else "#000000"

    st.markdown(f"""
    <div class="resume-card" style="border-top: 6px solid {accent};">
        <h1 style="margin:0; font-size:28px;">{full_name if full_name else 'MAYANK JAISWAL'}</h1>
        <p style="color:#666; margin-top:5px; font-size:13px;">{email} | {phone} | {location}<br>{linkedin}</p>
        
        <div class="section-title" style="color:{accent}; border-color:{accent}33;">EDUCATION</div>
        <p style="font-size:14px; white-space: pre-wrap;">{education if education else 'B.Tech CSE...'}</p>
        
        <div class="section-title" style="color:{accent}; border-color:{accent}33;">SKILLS</div>
        <div style="margin-top:8px;">{skill_html}</div>
        
        <div class="section-title" style="color:{accent}; border-color:{accent}33;">PROJECTS</div>
        <p style="font-size:14px; white-space: pre-wrap;">{projects if projects else '...'}</p>

        <div class="section-title" style="color:{accent}; border-color:{accent}33;">EXPERIENCE</div>
        <p style="font-size:14px; white-space: pre-wrap;">{experience if experience else '...'}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- PDF CREATION ---
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        # Header color
        r,g,b = (108,99,255) if template=="Modern Pro" else (26,115,232) if template=="Google Clean" else (0,0,0)
        pdf.set_fill_color(r,g,b)
        pdf.rect(0,0,210,28,'F')
        pdf.set_y(8)
        pdf.set_font("Arial", 'B', 24); pdf.set_text_color(255,255,255)
        pdf.cell(0, 10, full_name.upper(), align='C', ln=True)
        pdf.set_font("Arial", '', 10); pdf.cell(0, 6, f"{email} | {phone} | {location} | {linkedin}", align='C', ln=True)
        pdf.ln(20); pdf.set_text_color(0,0,0)
        
        def section(title, content):
            pdf.set_font("Arial", 'B', 12); pdf.set_text_color(r,g,b)
            pdf.cell(0, 8, title, ln=True); pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2); pdf.set_font("Arial", '', 11); pdf.set_text_color(40,40,40)
            pdf.multi_cell(0, 6, content); pdf.ln(4)

        section("EDUCATION", education)
        section("SKILLS", skills)
        section("PROJECTS", projects)
        section("EXPERIENCE", experience)
        return pdf.output(dest='S').encode('latin-1')

    st.write("")
    if st.button("📥 Download PRO PDF", use_container_width=True, type="primary"):
        if not full_name:
            st.error("Name toh daal bhai!")
        else:
            pdf_bytes = create_pdf()
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{full_name}_Resume_PRO.pdf" style="text-decoration:none;"><div style="width:100%; padding:14px; background:{accent}; color:white; text-align:center; border-radius:10px; font-weight:700;">⬇️ Click to Download PDF</div></a>'
            st.markdown(href, unsafe_allow_html=True)
            st.balloons()
