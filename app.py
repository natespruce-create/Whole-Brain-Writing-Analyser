import streamlit as st
import json
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="Whole-Brain Writing Analyser", page_icon="🧠", layout="wide")

# ====================== LOGO + HEADER ======================
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=160)

with col2:
    st.title("🧠 Whole-Brain Writing Analyser")
    st.markdown("Make your emails, letters, proposals, reports and messages more balanced and effective")

st.markdown("---")

# ====================== MODEL SELECTOR ======================
model_options = {
    "Gemini 2.5 Flash (Google - FREE to start)": "gemini",
    "Grok 4.1 Fast (xAI - cheap & powerful)": "grok"
}
selected_model_name = st.selectbox("Choose AI Model:", options=list(model_options.keys()), index=0)
selected_model = model_options[selected_model_name]

# ====================== API KEYS ======================
if selected_model == "grok":
    api_key = st.secrets.get("XAI_API_KEY")
    if not api_key:
        st.warning("⚠️ Add your XAI_API_KEY in Streamlit secrets")
else:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.warning("⚠️ Add your GEMINI_API_KEY in Streamlit secrets")

# ====================== TEXT INPUT ======================
user_text = st.text_area(
    "Paste your writing here (email, letter, proposal, report, LinkedIn message, etc.)",
    height=300,
    placeholder="Dear team,\n\nI wanted to follow up on the latest project update..."
)

if st.button("🔍 Analyse My Writing", type="primary", use_container_width=True):
    if len(user_text.strip()) < 50:
        st.error("Please paste at least 50 characters of text.")
    elif not api_key:
        st.error("Missing API key. Please add it in Streamlit secrets.")
    else:
        with st.spinner(f"Analysing with {selected_model_name}..."):
            
            prompt = f"""You are an expert communication coach specialising in HBDI (Whole Brain) thinking.

Analyse the following text and provide a balanced, constructive review:

Text:
=== START ===
{user_text}
=== END ===

Return your analysis in clear markdown with:
1. **Overall Whole-Brain Score** (out of 100)
2. Breakdown for each quadrant:
   - 🔵 Quadrant A (Analytical / Blue)
   - 🟢 Quadrant B (Practical / Green)
   - 🔴 Quadrant C (Relational / Red)
   - 🟡 Quadrant D (Conceptual / Yellow)
   For each: Strengths + Areas for improvement
3. 3–5 specific, actionable improvement suggestions (with example sentences)
4. One revised version of the most important paragraph improved for better whole-brain balance

Be professional, encouraging and practical."""

            try:
                if selected_model == "grok":
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    response = client.chat.completions.create(
                        model="grok-4-1-fast-reasoning",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.4
                    )
                    analysis = response.choices[0].message.content
                else:  # gemini
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(prompt)
                    analysis = response.text

                st.session_state.analysis = analysis
                st.session_state.original_text = user_text

                st.success("✅ Analysis Complete!")
                st.markdown(analysis)

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")

# ====================== PDF DOWNLOAD ======================
if "analysis" in st.session_state:
    if st.button("📄 Download Analysis as PDF", type="primary", use_container_width=True):
        with st.spinner("Creating PDF report..."):
            pdf_bytes = create_writing_analysis_pdf(
                st.session_state.analysis, 
                st.session_state.original_text
            )
            st.download_button(
                label="⬇️ Click here to download the PDF",
                data=pdf_bytes,
                file_name=f"Whole_Brain_Writing_Analysis_{datetime.now().strftime('%Y-%m-%d')}.pdf",
                mime="application/pdf"
            )

# ====================== PDF FUNCTION ======================
def create_writing_analysis_pdf(analysis, original_text):
    class PDF(FPDF):
        def header(self):
            if hasattr(self, 'logo_path') and self.logo_path:
                self.image(self.logo_path, x=10, y=8, w=45)
            self.set_font("Helvetica", "B", 16)
            self.cell(0, 10, "Whole-Brain Writing Analysis", ln=1, align="C")
            self.set_font("Helvetica", "", 10)
            self.cell(0, 6, f"Generated on {datetime.now().strftime('%d %B %Y')}", ln=1, align="C")
            self.ln(12)

    pdf = PDF()
    pdf.logo_path = "logo.png"
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Original Text Summary", ln=1)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, original_text[:800] + "..." if len(original_text) > 800 else original_text)
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Whole-Brain Analysis", ln=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, analysis)

    pdf_output = pdf.output(dest="S")
    if isinstance(pdf_output, bytearray):
        return bytes(pdf_output)
    return pdf_output

st.caption("Whole-Brain Writing Analyser • Separate from Tender Tool")
