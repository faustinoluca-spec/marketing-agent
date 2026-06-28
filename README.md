# APEX Marketing Intelligence 🚀

AI agent that generates complete marketing campaigns in under 3 minutes — the kind top agencies charge $50,000+ for.

## Live Demo

[apex-marketing.streamlit.app](https://marketing-agent-foqkvcvkhtw7fcpbtclsry.streamlit.app)

## What it does

Input a product or company. The agent researches the market in real time and generates a full 10-phase strategy plus complete content package:

**Strategy**
- Business Intelligence & market sizing
- Competitor analysis
- Audience profiling & segmentation
- Positioning and messaging
- Channel strategy
- Content pillars
- Paid media plan
- Influencer strategy
- KPIs & measurement framework
- MarTech stack recommendations

**Content Package**
- 5 Instagram posts with captions and hashtags
- 3 TikTok video scripts with hooks
- 3 LinkedIn posts
- 7 Tweets
- 2 complete email sequences
- 5 Google Ads with headlines and descriptions
- 5 Meta Ads concepts with targeting
- 4-week editorial calendar day by day

Export as PDF or Markdown.

## Tech Stack

- **LLM:** Groq (llama-3.3-70b-versatile)
- **Orchestration:** LangChain
- **Market Research:** Serper API (real-time Google Search)
- **Frontend:** Streamlit
- **Hosting:** Streamlit Cloud

## Run locally

```bash
git clone https://github.com/faustinoluca-spec/marketing-agent
cd marketing-agent
pip install -r requirements.txt
```

Create `.env`:
```env
GROQ_KEY=your_key
SERPER_KEY=your_key
```

```bash
streamlit run app.py
```

## Author

Luca Faustino — AI Engineer  
[github.com/faustinoluca-spec](https://github.com/faustinoluca-spec)
