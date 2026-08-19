from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq


# ============================================================
# 🔐 LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# 🤖 INITIALIZE MODEL
# ============================================================

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# ============================================================
# 📋 JSON PARSER
# ============================================================

json_parser = JsonOutputParser()


# ============================================================
# 🔎 JOB EXTRACTION PROMPT
# ============================================================

job_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert information extraction assistant.

Extract the job posting information from the scraped career page.

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

Do not return anything except the JSON.

NO PREAMBLE.
NO EXPLANATION.
NO APOLOGIES.
NO ADDITIONAL TEXT.
"""
        ),
        (
            "human",
            """
Here is the scraped website text:

{docs}
"""
        )
    ]
)


# ============================================================
# ✉️ COLD EMAIL PROMPT
# ============================================================

email_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert AI assistant specializing in writing
professional and personalized cold emails.

Your task is to write a concise and professional cold email
based on the provided job description.

Guidelines:

- Carefully understand the job requirements.
- Highlight how the sender's skills and experience align
  with the role.
- Keep the tone professional, confident and personalized.
- Do not exaggerate or invent qualifications.
- If a company name is provided, use it naturally.
- If no company name is provided, use "Hiring Manager".
- If portfolio links are provided, include only relevant ones.
- If portfolio links are empty, do not mention any portfolio.
- If sender details are provided, use them naturally.
- Do not invent sender information.
- Keep the email concise.
- End with a professional closing.
- Return ONLY the email.
- Do NOT include explanations or preamble.
"""
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


### Company Name

{company_name}


### Portfolio Links

{portfolio_links}
"""
        )
    ]
)


# ============================================================
# 🔎 EXTRACT JOB FROM URL
# ============================================================

def extract_job_from_url(url):

    loader = WebBaseLoader(url)

    docs = loader.load()

    if not docs:
        raise ValueError("No content could be extracted from this URL.")

    page_data = docs[0].page_content

    extraction_chain = job_prompt | model

    result = extraction_chain.invoke(
        {
            "docs": page_data
        }
    )

    json_response = json_parser.parse(result.content)

    jobs = json_response.get("jobs", [])

    if not jobs:
        raise ValueError("No job information could be extracted.")

    return jobs


# ============================================================
# ✉️ GENERATE COLD EMAIL
# ============================================================

def generate_email(
    job_description,
    sender_name,
    current_role,
    company_name="",
    portfolio_links=""
):

    email_chain = email_prompt | model

    response = email_chain.invoke(
        {
            "job_description": job_description,
            "sender_name": sender_name,
            "current_role": current_role,
            "company_name": company_name,
            "portfolio_links": portfolio_links
        }
    )

    return response.content