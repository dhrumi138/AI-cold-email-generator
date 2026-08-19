import os
import html
import re
import json

from dotenv import load_dotenv

import streamlit as st
import streamlit.components.v1 as components
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq

# ============================================================
# OutreachAI — Streamlit UI
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="OutreachAI — Cold Email Generator",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# SaaS Styling
# -----------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

:root {
    --bg: #f7f8fc;
    --card: #ffffff;
    --text: #111827;
    --muted: #667085;
    --border: #e7e9ef;
    --primary: #635bff;
    --primary-dark: #5148e8;
    --soft: #f0efff;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: var(--bg);
}

[data-testid="stHeader"] {
    background: rgba(247,248,252,0.92);
}

.block-container {
    max-width: 1420px;
    padding: 1.5rem 2.5rem 3rem 2.5rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding: 1.3rem 1rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 10px 26px 10px;
}

.brand-mark {
    width: 36px;
    height: 36px;
    border-radius: 11px;
    background: #111827;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 17px;
}

.brand-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: #111827;
}

.brand-name span {
    color: var(--primary);
}

.nav-label {
    color: #98a2b3;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin: 12px 10px 8px;
}

.side-note {
    margin: 20px 6px 0;
    padding: 14px;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: #fafbff;
}

.side-note-title {
    font-size: 12px;
    font-weight: 700;
    color: #344054;
}

.side-note-text {
    font-size: 11px;
    color: #98a2b3;
    line-height: 1.5;
    margin-top: 5px;
}

/* Header */
.page-eyebrow {
    color: var(--primary);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.page-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 32px;
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #101828;
    margin: 0;
}

.page-subtitle {
    color: #667085;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 24px;
}

/* Cards */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 1px 2px rgba(16,24,40,.02);
}

.card-desc {
    color: #98a2b3;
    font-size: 12px;
    margin-bottom: 17px;
}

.step {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 12px;
}

.step-number {
    width: 24px;
    height: 24px;
    border-radius: 8px;
    background: var(--soft);
    color: var(--primary);
    font-size: 11px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
}

.step-text {
    font-size: 13px;
    font-weight: 700;
    color: #344054;
}

/* Inputs */
label, [data-testid="stWidgetLabel"] p {
    font-size: 12px !important;
    font-weight: 700 !important;
    color: #344054 !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    border: 1px solid #dfe2e8;
    border-radius: 11px;
    background: #fff;
    box-shadow: none;
}

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    font-size: 13px;
}

div[data-baseweb="input"]:focus-within > div,
div[data-baseweb="textarea"]:focus-within > div {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(99,91,255,.10);
}

/* Buttons */
.stButton > button {
    border-radius: 11px;
    border: 1px solid #5a52ed;
    background: var(--primary);
    color: white;
    font-weight: 700;
    font-size: 13px;
    min-height: 43px;
    box-shadow: 0 4px 12px rgba(99,91,255,.18);
    transition: all .15s ease;
}

.stButton > button:hover {
    background: var(--primary-dark);
    border-color: var(--primary-dark);
    transform: translateY(-1px);
}

div[data-testid="stDownloadButton"] > button {
    border-radius: 11px;
    min-height: 43px;
    font-weight: 700;
}

/* Metrics */
.metric-card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px 16px;
}

.metric-label {
    color: #98a2b3;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .7px;
}

.metric-value {
    color: #101828;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 22px;
    font-weight: 800;
    margin-top: 3px;
}

/* Email output */
.email-shell {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(16,24,40,.03);
}

.email-top {
    padding: 17px 20px;
    border-bottom: 1px solid var(--border);
    background: #fcfcfd;
}

.email-label {
    font-size: 10px;
    color: #98a2b3;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .9px;
}

.email-content {
    padding: 22px 20px;
    color: #344054;
    font-size: 13px;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
}

.empty-output {
    min-height: 420px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    border: 1px dashed #d9dce5;
    border-radius: 18px;
    background: #fcfcfd;
}

.empty-icon {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    background: var(--soft);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 13px;
    font-size: 22px;
}

.empty-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 15px;
    font-weight: 800;
    color: #344054;
}

.empty-text {
    max-width: 300px;
    color: #98a2b3;
    font-size: 12px;
    line-height: 1.55;
    margin: 5px auto 0;
}

.section-space {
    height: 10px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Session State
# -----------------------------
if "generated_email" not in st.session_state:
    st.session_state.generated_email = ""

if "job_data" not in st.session_state:
    st.session_state.job_data = None

if "generated_count" not in st.session_state:
    st.session_state.generated_count = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "generation_status" not in st.session_state:
    st.session_state.generation_status = "Pending"

if "generation_requested" not in st.session_state:
    st.session_state.generation_requested = False


# -----------------------------
# Helper
# -----------------------------
def remove_unprovided_phone_numbers(text: str) -> str:
    """Remove phone-number-like strings that the model may invent."""
    return re.sub(
        r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)",
        "",
        text,
    ).strip()


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">✦</div>
            <div class="brand-name">Outreach<span>AI</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="nav-label">Workspace</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        ["✦  Generate Email", "◷  History", "⚙  Settings"],
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="side-note">
            <div class="side-note-title">AI-powered outreach</div>
            <div class="side-note-text">
                Turn any job posting into a concise, personalized cold email.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="position:fixed;bottom:18px;color:#98a2b3;font-size:10px;">OutreachAI v1.0 • Powered by Groq</div>',
        unsafe_allow_html=True,
    )


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="page-eyebrow">AI OUTREACH WORKSPACE</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="page-title">Create a better first impression.</h1>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-subtitle">Paste a job posting, add your details, and let AI craft a personalized cold email.</div>',
    unsafe_allow_html=True,
)


# -----------------------------
# History
# -----------------------------
if page == "◷  History":
    st.markdown(
        """
        <div class="card">
            <div class="card-title">Generation history</div>
            <div class="card-desc">
                Your latest generated outreach emails appear here during this session.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.history:
        for index, email in enumerate(reversed(st.session_state.history), start=1):
            st.markdown(f"**Email {index}**")
            st.code(email, language=None)
    else:
        st.info(
            "No generated emails yet. Create your first email from Generate Email."
        )

    st.stop()


# -----------------------------
# Settings
# -----------------------------
if page == "⚙  Settings":
    st.markdown(
        """
        <div class="card">
            <div class="card-title">Workspace settings</div>
            <div class="card-desc">
                Configuration used by the generator.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    st.info("The app reads GROQ_API_KEY from your .env file.")
    st.markdown("**Model:** `openai/gpt-oss-20b`")
    st.markdown("**Temperature:** `0`")

    st.stop()


# -----------------------------
# Main Workspace
# -----------------------------
left, right = st.columns([0.95, 1.05], gap="large")

# ============================================================
# LEFT — INPUTS
# ============================================================
with left:
    st.markdown(
        """
        <div class="card">
            <div class="step">
                <div class="step-number">01</div>
                <div class="step-text">Job posting</div>
            </div>
            <div class="card-desc">
                Tell OutreachAI which role you're targeting.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    job_url = st.text_input(
        "Career page URL",
        value="https://careers.nike.com/lead-technology-business-consultant-itc/job/R-90109",
        placeholder="https://company.com/careers/job...",
        help="Paste the public career page URL.",
    )

    st.markdown(
        '<div class="section-space"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">
            <div class="step">
                <div class="step-number">02</div>
                <div class="step-text">Your profile</div>
            </div>
            <div class="card-desc">
                Give the model enough context to personalize your outreach.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sender_name = st.text_input(
        "Your name",
        placeholder="e.g. Dhrumi Desai",
    )

    current_role = st.text_input(
        "Current role",
        placeholder="e.g. Computer Engineering Student",
    )

    linkedin_profile = st.text_input(
        "LinkedIn profile link",
        placeholder="Optional — https://linkedin.com/in/your-name",
    )

    portfolio_link = st.text_input(
        "Portfolio link",
        placeholder="Optional — https://yourportfolio.com",
    )

    st.markdown(
        '<div style="height:10px;"></div>',
        unsafe_allow_html=True,
    )

    generate = st.button(
        "✦  Generate personalized email",
        use_container_width=True,
        type="primary",
    )

    if generate:
        st.session_state.generation_status = "Generating"
        st.session_state.generation_requested = True
        st.rerun()


# ============================================================
# RIGHT — OUTPUT
# ============================================================
with right:
    st.markdown(
        """
        <div class="card">
            <div class="step">
                <div class="step-number">03</div>
                <div class="step-text">Your generated email</div>
            </div>
            <div class="card-desc">
                A concise email generated from the job posting and your profile.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.generated_email:
        st.markdown(
            """
            <div class="empty-output">
                <div>
                    <div class="empty-icon">✦</div>
                    <div class="empty-title">Your email will appear here</div>
                    <div class="empty-text">
                        Add your details and generate an email to see your personalized outreach.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        safe_email = html.escape(st.session_state.generated_email)

        st.markdown(
            f"""
            <div class="email-shell">
                <div class="email-top">
                    <div class="email-label">Generated cold email</div>
                </div>
                <div class="email-content">{safe_email}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div style="height:10px;"></div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)

        with c1:
            st.download_button(
                "↓  Download .txt",
                data=st.session_state.generated_email,
                file_name="cold_email.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with c2:
            # Browser-side copy button. Unlike st.button + components.html,
            # the click itself happens inside the browser component.
            clipboard_text = json.dumps(
                st.session_state.generated_email
            )

            components.html(
                f"""
                <div style="width:100%;">
                    <button
                        id="copyEmailButton"
                        type="button"
                        style="
                            width:100%;
                            min-height:43px;
                            border-radius:11px;
                            border:1px solid #dfe2e8;
                            background:#ffffff;
                            color:#344054;
                            font-family:Arial,sans-serif;
                            font-size:13px;
                            font-weight:700;
                            cursor:pointer;
                        "
                    >⧉&nbsp; Copy to clipboard</button>

                    <textarea
                        id="copyEmailText"
                        aria-hidden="true"
                        style="
                            position:absolute;
                            left:-10000px;
                            top:-10000px;
                            width:1px;
                            height:1px;
                            opacity:0;
                        "
                    ></textarea>

                    <script>
                        const copyButton =
                            document.getElementById("copyEmailButton");
                        const copyArea =
                            document.getElementById("copyEmailText");
                        const emailText = {clipboard_text};

                        copyButton.addEventListener("click", async () => {{
                            try {{
                                if (
                                    navigator.clipboard &&
                                    navigator.clipboard.writeText
                                ) {{
                                    await navigator.clipboard.writeText(
                                        emailText
                                    );
                                }} else {{
                                    copyArea.value = emailText;
                                    copyArea.focus();
                                    copyArea.select();
                                    document.execCommand("copy");
                                    copyArea.blur();
                                }}

                                copyButton.textContent =
                                    "✓  Copied to clipboard";

                            }} catch (error) {{
                                try {{
                                    copyArea.value = emailText;
                                    copyArea.focus();
                                    copyArea.select();
                                    document.execCommand("copy");
                                    copyArea.blur();

                                    copyButton.textContent =
                                        "✓  Copied to clipboard";
                                }} catch (fallbackError) {{
                                    copyButton.textContent =
                                        "Copy failed — select email manually";
                                }}
                            }}

                            setTimeout(() => {{
                                copyButton.textContent =
                                    "⧉  Copy to clipboard";
                            }}, 1800);
                        }});
                    </script>
                </div>
                """,
                height=55,
            )


# ============================================================
# GENERATION
# ============================================================
if st.session_state.generation_requested:
    st.session_state.generation_requested = False

    if not os.getenv("GROQ_API_KEY"):
        st.session_state.generation_status = "Pending"
        st.error("GROQ_API_KEY was not found. Add it to your .env file.")
        st.stop()

    if not job_url.strip():
        st.session_state.generation_status = "Pending"
        st.warning("Please enter a career page URL.")
        st.stop()

    if not sender_name.strip():
        st.session_state.generation_status = "Pending"
        st.warning("Please enter your name.")
        st.stop()

    with st.spinner("Reading the job posting and crafting your email..."):
        try:
            loader = WebBaseLoader(job_url.strip())
            docs = loader.load()

            if not docs:
                st.session_state.generation_status = "Pending"
                st.error("No content could be loaded from this career page.")
                st.stop()

            page_data = docs[0].page_content

            # Keep scraped content below the Groq TPM limit.
            page_data = page_data[:12000]

            json_parser = JsonOutputParser()

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
You are an expert information extraction assistant.

Extract ONLY the single primary job posting represented by the career-page URL.

IMPORTANT:
- Return exactly ONE job inside the "jobs" array.
- Do NOT extract related jobs, recommended jobs, recently viewed jobs, navigation items, footer content, or other job links.
- Use the main job title and main job description from the page.
- If the page contains multiple job postings, choose the posting that matches the main page URL/title.
- Do not create multiple variations of the same job.

Return ONLY valid JSON.

The JSON MUST follow this structure:

{{
  "jobs": [
    {{
      "role": "",
      "experience": "",
      "skills": [],
      "description": ""
    }}
  ]
}}

The "jobs" array MUST contain exactly one object.

Do not return anything except the JSON.
NO PREAMBLE.
NO EXPLANATION.
NO APOLOGIES.
NO ADDITIONAL TEXT.
""",
                    ),
                    (
                        "human",
                        """
Here is the scraped website text:

{docs}
""",
                    ),
                ]
            )

            model = ChatGroq(
                model="openai/gpt-oss-20b",
                temperature=0,
            )

            template = prompt.format(docs=page_data)
            result = model.invoke(template)
            raw_content = result.content.strip()

            try:
                json_response = json_parser.parse(raw_content)
            except Exception:
                cleaned_content = raw_content

                if "```json" in cleaned_content:
                    cleaned_content = cleaned_content.split("```json", 1)[1]
                    cleaned_content = cleaned_content.split("```", 1)[0].strip()
                elif "```" in cleaned_content:
                    cleaned_content = cleaned_content.split("```", 1)[1]
                    cleaned_content = cleaned_content.split("```", 1)[0].strip()

                if "{" in cleaned_content and "}" in cleaned_content:
                    start = cleaned_content.find("{")
                    end = cleaned_content.rfind("}") + 1
                    cleaned_content = cleaned_content[start:end]

                try:
                    json_response = json.loads(cleaned_content)
                except Exception:
                    st.session_state.generation_status = "Pending"
                    st.error("The AI could not return valid job data from this page.")
                    st.caption(
                        "The career page was loaded, but the model did not return the required JSON format."
                    )
                    st.stop()

            jobs = json_response.get("jobs", [])

            # The product generates one cold email per submitted job URL.
            # Ignore related/recommended jobs even if the model returns them.
            jobs = jobs[:1]

            if not jobs:
                st.session_state.generation_status = "Pending"
                st.error("No job posting could be extracted from this page.")
                st.stop()

            email_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
You are an expert AI assistant specializing in writing professional cold emails.

Generate a personalized cold email based on the job description.

Rules:
- Keep it professional.
- Keep it concise.
- Don't invent information.
- Identify the company and role from the job description when needed.
- If the recipient name is not available, use "Hiring Manager".
- If the LinkedIn profile link is empty, don't mention it.
- If the portfolio link is empty, don't mention it.
- If sender details are empty, don't invent them.
- NEVER invent, assume, or add a phone number.
- NEVER invent an email address.
- NEVER invent a LinkedIn URL or portfolio URL.
- NEVER add placeholder contact information.
- Only include contact information explicitly provided by the user.
- Do not add a phone number after the sender's name.
- Use the portfolio link naturally in the email body, preferably in the closing paragraph.
- If the portfolio link is empty, do not mention it.
- Do not place the portfolio link in the signature.
- End the email signature with this order:
  Best regards,
  {sender_name}
  {current_role}
  {linkedin_profile}
- Only include the LinkedIn line when a LinkedIn profile link was provided.
- LinkedIn must appear below the current role.
- The LinkedIn profile link must be the LAST line of the signature.
- Return ONLY the email.
""",
                    ),
                    (
                        "human",
                        """
### Job Description
{job_description}

### Sender Name
{sender_name}

### Current Role
{current_role}

### LinkedIn Profile Link
{linkedin_profile}

### Portfolio Link
{portfolio_link}
""",
                    ),
                ]
            )

            chain = email_prompt | model
            generated = []

            for job in jobs:
                response = chain.invoke(
                    {
                        "job_description": job.get("description", ""),
                        "sender_name": sender_name,
                        "current_role": current_role,
                        "linkedin_profile": linkedin_profile,
                        "portfolio_link": portfolio_link,
                    }
                )

                email_text = response.content.strip()

                if linkedin_profile.strip():
                    linkedin_pattern = r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+"

                    email_text = re.sub(
                        linkedin_pattern,
                        "",
                        email_text,
                        flags=re.IGNORECASE,
                    )

                    # Remove the model's complete closing/signature so the
                    # application adds exactly one consistent signature.
                    signature_match = re.search(
                        r"(?is)\n\s*(?:best regards|kind regards|regards|sincerely|best)[,:]?\s*.*$",
                        email_text,
                    )

                    if signature_match:
                        email_text = email_text[:signature_match.start()].rstrip()

                    email_text = re.sub(
                        r"\n{3,}",
                        "\n\n",
                        email_text,
                    ).strip()

                    signature_lines = [
                        "Best regards,",
                        sender_name.strip(),
                        current_role.strip(),
                    ]

                    if linkedin_profile.strip():
                        signature_lines.append(linkedin_profile.strip())

                    if portfolio_link.strip():
                        portfolio_line = (
                            "You can view my portfolio here: "
                            + portfolio_link.strip()
                            + "."
                        )

                        # Remove any portfolio URL the model may have already
                        # inserted, then add the exact user-provided link once.
                        portfolio_pattern = r"https?://[^\s<>()]+"
                        existing_portfolio = re.escape(portfolio_link.strip())

                        email_text = re.sub(
                            existing_portfolio,
                            "",
                            email_text,
                        )

                        email_text = re.sub(
                            r"\n{3,}",
                            "\n\n",
                            email_text,
                        ).strip()

                        email_text = (
                            email_text
                            + "\n\n"
                            + portfolio_line
                        )

                    if portfolio_link.strip():
                        portfolio_line = (
                            "You can view my portfolio here: "
                            + portfolio_link.strip()
                            + "."
                        )

                        # Remove any portfolio URL the model may have already
                        # inserted, then add the exact user-provided link once.
                        portfolio_pattern = r"https?://[^\s<>()]+"
                        existing_portfolio = re.escape(portfolio_link.strip())

                        email_text = re.sub(
                            existing_portfolio,
                            "",
                            email_text,
                        )

                        email_text = re.sub(
                            r"\n{3,}",
                            "\n\n",
                            email_text,
                        ).strip()

                        email_text = (
                            email_text
                            + "\n\n"
                            + portfolio_line
                        )

                    email_text = (
                        email_text
                        + "\n\n"
                        + "\n".join(signature_lines)
                    )

                # Remove any phone-number-like strings the model invented.
                email_text = re.sub(
                    r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)",
                    "",
                    email_text,
                )

                # If no LinkedIn was supplied, still remove an invented
                # signature and rebuild only the permitted sender details.
                if not linkedin_profile.strip():
                    signature_match = re.search(
                        r"(?is)\n\s*(?:best regards|kind regards|regards|sincerely|best)[,:]?\s*.*$",
                        email_text,
                    )

                    if signature_match:
                        email_text = email_text[:signature_match.start()].rstrip()

                    signature_lines = [
                        "Best regards,",
                        sender_name.strip(),
                        current_role.strip(),
                    ]

                    if linkedin_profile.strip():
                        signature_lines.append(linkedin_profile.strip())

                    email_text = (
                        email_text
                        + "\n\n"
                        + "\n".join(signature_lines)
                    )

                email_text = re.sub(
                    r"\n{3,}",
                    "\n\n",
                    email_text,
                ).strip()

                generated.append(email_text)

            final_email = "\n\n".join(generated).strip()

            if not final_email:
                st.session_state.generation_status = "Pending"
                st.error("The AI returned an empty email.")
                st.stop()

            st.session_state.generated_email = final_email
            st.session_state.job_data = jobs
            st.session_state.generated_count += len(generated)
            st.session_state.history.append(final_email)
            st.session_state.generation_status = "Ready"

            st.rerun()

        except Exception as e:
            st.session_state.generation_status = "Pending"
            st.error(f"Generation failed: {e}")
            st.caption(
                "Check your URL, internet connection, installed packages, and GROQ_API_KEY."
            )


# -----------------------------
# Bottom Stats
# -----------------------------
st.markdown(
    '<div style="height:18px;"></div>',
    unsafe_allow_html=True,
)

m1, m2 = st.columns(2)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Emails generated</div>
            <div class="metric-value">
                {st.session_state.generated_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    status = st.session_state.generation_status

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">AI status</div>
            <div class="metric-value" style="font-size:18px;">
                {status}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
