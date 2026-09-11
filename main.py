import streamlit as st
from fpdf import FPDF
import base64

st.set_page_config(page_title="ATS Resume Builder Pro", page_icon="📄", layout="wide")

st.markdown("""
<style>
    .header-title {
        font-size: 42px; font-weight: 800;
        background: linear-gradient(90deg, #6C63FF, #00D4FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .resume-card {
        background: white; padding: 30px; border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #eee;
    }
    .skill-tag {
        display: inline-block; background: #F3F4FF; color: #6C63FF;
        padding: 5px 12px; border-radius: 20px; margin: 3px; font-size: 13px; font-weight: 600;
        border: 1px solid #E0E3FF;
    }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.25], gap="large")

with col1:
    st.markdown('<div class="header-title">Resume Builder PRO</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("👤 Personal Info - Yaha Bharo")
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email")
        phone = st.text_input("Phone", placeholder="Enter phone number")
        linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/...")
        location = st.text_input("Location", placeholder="City, India")
    with st.container(border=True):
        education = st.text_area("Education", placeholder="Enter education", height=80)
        skills = st.text_area("Skills (comma se)", placeholder="Python, Java, SQL", height=80)
        projects = st.text_area("Projects", placeholder="Enter projects", height=80)
        experience = st.text_area("Experience", placeholder="Enter experience", height=80)

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
    
    # Live preview me contact check
    contact_preview = f"{email} | {phone} | {location}" if (email or phone) else "Your contact info will show here"

    html_code = f"""
    <div class="resume-card">
        <h2 style="margin:0; text-align:center;">{full_name if full_name else 'Your Name'}</h2>
        <p style="color:#555; font-size:13px; text-align:center;">{contact_preview}<br>{linkedin}</p>
        <div style="background:#F9FAFF; border:1px solid #EAEAEA; border-radius:8px; padding:12px; margin-top:15px;">
            <h4 style="color:#6C63FF; margin:0 0 5px 0;">EDUCATION</h4>
            <p style="font-size:14px; margin:0;">{education if education else '...'}</p>
        </div>
        <div style="background:#F9FAFF; border:1px solid #EAEAEA; border-radius:8px; padding:12px; margin-top:12px;">
            <h4 style="color:#6C63FF; margin:0 0 5px 0;">SKILLS</h4>
            <p style="margin:0;">{skill_html if skill_html else '...'}</p>
        </div>
        <div style="background:#F9FAFF; border:1px solid #EAEAEA; border-radius:8px; padding:12px; margin-top:12px;">
            <h4 style="color:#6C63FF; margin:0 0 5px 0;">PROJECTS</h4>
            <p style="font-size:14px; margin:0;">{projects if projects else '...'}</p>
        </div>
        <div style="background:#F9FAFF; border:1px solid #EAEAEA; border-radius:8px; padding:12px; margin-top:12px;">
            <h4 style="color:#6C63FF; margin:0 0 5px 0;">EXPERIENCE</h4>
            <p style="font-size:14px; margin:0;">{experience if experience else '...'}</p>
        </div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # NAME
        pdf.set_font("Arial", 'B', 20)
        pdf.set_text_color(0,0,0)
        pdf.cell(0, 12, (full_name if full_name else "Your Name").upper(), align='C', ln=True)
        
        # CONTACT - FIXED: Ab sab ayega
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(60,60,60)
        # Line 1
        line1 = []
        if email: line1.append(f"Email: {email}")
        if phone: line1.append(f"Phone: {phone}")
        if location: line1.append(f"{location}")
        if line1:
            pdf.cell(0, 6, " | ".join(line1), align='C', ln=True)
        # Line 2 LinkedIn
        if linkedin:
            pdf.cell(0, 6, f"LinkedIn: {linkedin}", align='C', ln=True)
        
        pdf.ln(6)
        pdf.set_draw_color(200,200,200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(6)

        def box_section(title, content):
            if not content.strip(): content = "Not provided"
            pdf.set_font("Arial", 'B', 11)
            pdf.set_text_color(108,99,255)
            pdf.set_fill_color(249,250,255)
            pdf.set_draw_color(220,220,220)
            pdf.cell(0, 8, f" {title}", border=1, fill=True, ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.set_text_color(0,0,0)
            pdf.multi_cell(0, 7, f" {content}", border=1)
            pdf.ln(4)

        box_section("EDUCATION", education)
        box_section("SKILLS", skills)
        box_section("PROJECTS", projects)
        box_section("EXPERIENCE", experience)
        
        return pdf.output(dest='S').encode('latin-1')

    st.write("")
    if st.button("📥 Download WHITE PDF", use_container_width=True, type="primary"):
        if not full_name or not email:
            st.warning("Bhai Full Name aur Email toh bhar de, nahi toh PDF me kaise ayega?")
        else:
            pdf_bytes = create_pdf()
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Resume.pdf"><div style="width:100%; padding:14px; background:#6C63FF; color:white; text-align:center; border-radius:10px; font-weight:700;">⬇️ Download Now</div></a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("Ho gaya! Ab email, phone sab ayega")
