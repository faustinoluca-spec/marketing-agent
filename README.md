# APEX Marketing Intelligence

AI-powered marketing campaigns that top agencies charge $50,000+ for. Generated in minutes.

Live Demo: https://marketing-agent-foqkvcvkhtw7fcpbtclsry.streamlit.app

---

## What it does

APEX generates a complete 10-phase marketing strategy plus full content package for any product or company in under 3 minutes.

What you get:
- 10-phase strategy from Business Intelligence to MarTech Stack
- Real-time market research via Google Search API
- Competitor analysis and audience profiling
- 5 Instagram posts with full captions and hashtags
- 3 TikTok video scripts with hooks
- 3 LinkedIn posts
- 7 Tweets
- 2 complete email sequences
- 5 Google Ads with headlines and descriptions
- 5 Meta Ads concepts with targeting
- 4-week editorial calendar day by day
- PDF and Markdown export

---

## Tech Stack

- Frontend: Streamlit
- LLM: Groq llama-3.3-70b-versatile
- Orchestration: LangChain
- Market Research: Serper API
- Hosting: Streamlit Cloud

---

## How to run locally

git clone https://github.com/faustinoluca-spec/marketing-agent
cd marketing-agent
pip install -r requirements.txt

Create a .env file with:
GROQ_KEY=your_key
SERPER_KEY=your_key

Then run:
streamlit run app.py

---

## Author

Luca Faustino - AI Engineer
GitHub: https://github.com/faustinoluca-spec