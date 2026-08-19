OutreachAI is a Streamlit-based SaaS-style cold email generator that turns a public job posting into a concise, personalized outreach email.

Features

AI Job Extraction — Loads a public career page and extracts the primary job posting.

Personalized Cold Email — Uses the job description and your profile details to generate one professional email.

LinkedIn Signature — Places your LinkedIn profile below your name and current role.

Portfolio in Email Body — Places your portfolio link naturally in the email body rather than the signature.

One Email Per Job URL — Ignores related/recommended jobs from the scraped page.

Duplicate Signature Protection — Prevents repeated Best regards sections.

Phone Number Protection — Prevents the model from inventing phone numbers.

Generation Status — Shows Pending → Generating → Ready.

Copy to Clipboard — Browser-side copy action with a fallback method.

Download Email — Download the generated email as a .txt file.

History — Keeps generated emails during the current session.

SaaS UI — Sidebar navigation, workspace cards, metrics, email preview, and settings.

No Separate CSS File — Styling is contained in main.py.

Tech Stack

Python

Streamlit

LangChain

LangChain Community

Groq

openai/gpt-oss-20b

WebBaseLoader

python-dotenv

Project Structure

Cold Email Generator/
│
├── app.py/
│   ├── main.py
│   └── backend.py
│
├── .env
├── requirements.txt
└── README.md

The Streamlit entry point is app.py/main.py.

Application Flow

Job URL + User Details
          ↓
     Streamlit UI
          ↓
     WebBaseLoader
          ↓
    Career Page Text
          ↓
   Content Size Limit
          ↓
     Groq / GPT-OSS
          ↓
    Primary Job Data
          ↓
   Cold Email Generation
          ↓
     Email Cleanup
          ↓
  ┌───────┴────────┐
  ↓                ↓
Copy             Download