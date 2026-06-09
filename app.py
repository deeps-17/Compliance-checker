import streamlit as st
from src.evaluator import evaluate_policy
from src.chunker import extract_text_from_upload, prepare_policy_text
from src.report import parse_report, get_score_color

st.set_page_config(
    page_title="DPDP Compliance Checker",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 DPDP Act Compliance Checker")
st.caption("Evaluate any privacy policy against India's Digital Personal Data Protection Act 2023")

st.divider()

# Session state init
if "report" not in st.session_state:
    st.session_state.report = None
if "prev_policy_text" not in st.session_state:
    st.session_state.prev_policy_text = ""

input_method = st.radio("How would you like to provide the privacy policy?",
                         ["Paste text", "Upload file"],
                         horizontal=True)

policy_text = ""

if input_method == "Paste text":
    policy_text = st.text_area(
        "Paste the privacy policy here",
        height=250,
        placeholder="Paste the full text of the privacy policy..."
    )

elif input_method == "Upload file":
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
    if uploaded_file:
        try:
            policy_text = extract_text_from_upload(uploaded_file)
            st.success(f"File loaded successfully — {len(policy_text)} characters extracted.")
        except Exception as e:
            st.error(f"Could not read file: {e}")

# Clear report if policy text changes
if policy_text != st.session_state.prev_policy_text:
    st.session_state.report = None
    st.session_state.prev_policy_text = policy_text

st.divider()

if st.button("Analyse Policy", type="primary", disabled=not policy_text.strip()):
    with st.spinner("Evaluating against DPDP Act 2023..."):
        try:
            raw_result = evaluate_policy(prepare_policy_text(policy_text))
            st.session_state.report = parse_report(raw_result)
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Render report from session state
if st.session_state.report:
    report = st.session_state.report
    color = get_score_color(report["overall_score"])

    st.divider()

    # Overall score
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("**Overall Score**")
        st.markdown(f"### :{color}[{report['overall_score']}]")
    with col2:
        st.markdown("**Summary**")
        st.write(report["overall_summary"])

    st.divider()

    # Pillar breakdown
    st.markdown("### Pillar-by-Pillar Breakdown")

    for pillar in report["pillars"]:
        with st.expander(f"{pillar['badge']} {pillar['name']} — {pillar['status']} ({pillar['section']})"):
            st.markdown("**Assessment**")
            st.write(pillar["reasoning"])

            st.markdown("**Evidence from policy**")
            if pillar["evidence"] == "Not found":
                st.error("Not found in policy.")
            elif pillar["status"] == "Partial":
                st.warning(pillar["evidence"])
            else:
                st.success(pillar["evidence"])

    st.divider()

    # Downloadable report
    md_report = "# DPDP Act 2023 Compliance Report\n\n"
    md_report += f"**Overall Compliance**: {report['overall_score']}\n\n"
    md_report += f"**Summary**: {report['overall_summary']}\n\n"
    md_report += "---\n\n"
    for pillar in report["pillars"]:
        md_report += f"### {pillar['badge']} {pillar['name']} — {pillar['status']} ({pillar['section']})\n"
        md_report += f"**Assessment**:\n{pillar['reasoning']}\n\n"
        md_report += f"**Evidence**:\n*{pillar['evidence']}*\n\n"
        md_report += "---\n\n"

    st.download_button(
        label="📥 Download Compliance Report",
        data=md_report,
        file_name="dpdp_compliance_report.md",
        mime="text/markdown"
    )