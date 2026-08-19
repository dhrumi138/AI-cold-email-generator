from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Load Career Page
# -----------------------------
url = "https://careers.nike.com/lead-technology-business-consultant-itc/job/R-90109"

loader = WebBaseLoader(url)
docs = loader.load()

# Extract only the webpage text
page_data = docs[0].page_content

# -----------------------------
# JSON Parser
# -----------------------------
json_parser = JsonOutputParser()

# -----------------------------
# Prompt to Extract Job Details
# -----------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert information extraction assistant.

Extract all job postings from the scraped career page.

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

# -----------------------------
# LLM
# -----------------------------
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# -----------------------------
# Extract Jobs
# -----------------------------
template = prompt.format(docs=page_data)

result = model.invoke(template)

print("\nExtracted JSON:\n")
print(result.content)

json_response = json_parser.parse(result.content)

print("\nType of Parsed Response:")
print(type(json_response))

# -----------------------------
# Email Prompt
# -----------------------------
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
- If company name is empty, use "Hiring Manager".
- If portfolio links are empty, don't mention them.
- If sender details are empty, don't invent them.
- Return ONLY the email.
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

chain = email_prompt | model

# -----------------------------
# User Inputs
# -----------------------------
sender_name = input("\nEnter your name: ")
current_role = input("Enter your current role: ")
company_name = input("Enter company name (Press Enter to skip): ")
portfolio_links = input("Enter portfolio link (Press Enter to skip): ")

# -----------------------------
# Generate Email
# -----------------------------
jobs = json_response["jobs"]

for job in jobs:

    response = chain.invoke(
        {
            "job_description": job["description"],
            "sender_name": sender_name,
            "current_role": current_role,
            "company_name": company_name,
            "portfolio_links": portfolio_links,
        }
    )

   
    print("GENERATED COLD EMAIL")
    
    print(response.content)
    