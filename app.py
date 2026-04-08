import streamlit as st
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="Whole-Brain Writing Analyser", page_icon="🧠", layout="wide")

# ====================== LOGO + HEADER ======================
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=160)   # Make sure logo.png is uploaded

with col2:
    st.title("🧠 Whole-Brain Writing Analyser")
    st.markdown("Make your emails, letters, proposals, and reports more balanced and effective")

st.markdown("---")

# ====================== INPUT ======================
user_text = st.text_area(
    "Paste your writing here (email, letter, proposal section, report, LinkedIn message, etc.)",
    height=280,
    placeholder="Paste your text here..."
)

analyze_button = st.button("🔍 Analyse My Writing", type="primary", use_container_width=True)

if analyze_button:
    if len(user_text.strip()) < 50:
        st.error("Please enter at least 50 characters.")
    else:
        with st.spinner("Analysing balance across all 4 HBDI quadrants..."):
            
            # This is where the magic happens
            analysis_prompt = f"""You are an expert communication coach using the HBDI (Whole Brain) model.

Analyse the following text for balance across the 4 quadrants:

Text:
=== START ===
{user_text}
=== END ===

Give me a structured response with:
1. Overall Whole-Brain Score (out of 100)
2. Breakdown for each quadrant:
   - Quadrant A (Blue - Analytical): Strengths + Gaps
   - Quadrant B (Green - Practical): Strengths + Gaps
   - Quadrant C (Red - Relational): Strengths + Gaps
   - Quadrant D (Yellow - Conceptual): Strengths + Gaps
3. Specific improvement suggestions (with example sentences the user can copy)
4. One revised version of the key paragraph improved for better whole-brain balance

Be constructive, professional and encouraging."""

            # TODO: Add your LLM call here (Gemini or Grok) - same as your tender app

            st.success("✅ Analysis Complete!")

            # Placeholder result (we'll connect real LLM next)
            st.markdown("### Overall Score: **78/100**")
            
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            with col1:
                st.markdown("**🔵 Quadrant A – Analytical**")
                st.write("Strong on facts and logic. Could add more data or metrics.")
            
            with col2:
                st.markdown("**🟢 Quadrant B – Practical**")
                st.write("Good process and next steps. Very clear timeline.")
            
            with col3:
                st.markdown("**🔴 Quadrant C – Relational**")
                st.write("Could show more empathy and stakeholder focus.")
            
            with col4:
                st.markdown("**🟡 Quadrant D – Conceptual**")
                st.write("Limited big-picture vision and innovation.")

            st.markdown("### Suggested Improvements")
            st.info("Example improved sentence...")

# Footer
st.caption("Whole-Brain Writing Analyser | Separate from Tender Tool")
