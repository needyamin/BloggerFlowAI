# 🚀 BloggerFlowAI: Master Monetization Edition
Massive, authoritative, 2026-current blog posts automated for maximum AdSense revenue. This system doesn't just "post news"—it strategically engineers high-CPC digital assets using real-time global context.

## 🌟 Strategic Features
1. **Elite News Induction**: Scans 21+ high-authority sources (Guardian, NYT, Reuters, TechCrunch) to find **2026-only** authentic news.
2. **AdSense E-E-A-T Strategy**: The AI persona is a Digital Media Strategist. It prioritizes Experience, Expertise, Authoritativeness, and Trustworthiness.
3. **High-CPC Categorization**: Automatically maps content to 5 premium, high-paid niches:
   - 🎓 **Education & Learning**
   - ✈️ **Scholarships & Study Abroad**
   - 🌍 **International (Overseas) News**
   - 💻 **Latest Tech News**
   - 📱 **Unique & Innovative Gadget Reviews**
4. **Authority Signaling**: Every post includes "Verified Reporting" timestamps (Date, Day, Time) and clickable source citations to maximize domain trust and AdSense approval.

## 🛠️ Setup
1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configuration**:
   - Update `BLOGGER_BLOG_ID` in `.env`.
   - Place Google Cloud `credentials.json` and `token.json` in `credentials/`.
   - **AI Providers**:
     - **OpenAI API** (Primary): Add `OPENAI_API_KEY` to `.env`.
     - **Google Gemini API** (Fallback): Add `GEMINI_API_KEY` to `.env`.

## 🤖 Integrated Workflow
The system follows a proprietary 3-stage funnel:
1. **COLLECT**: The `Custom Agent` (NewsBot) scrapes real 2026 events from verified feeds.
2. **STRATEGIZE**: AI summarizes news using "Executive Summaries" and high-level industrial terminology.
3. **DEPLOY**: Articles are formatted with semantic HTML (`h2`, `h3`, `p style="justify"`) and posted to Blogger.

## 📄 Project Structure
```
BloggerFlowAI/
├── src/
│   ├── app/           # Main Blogger & Posting Logic
│   ├── models/
│   │   ├── custom_agent/   # 🗞️ NewsBot (Sources & Year Filters)
│   │   └── remote_agent/   # 🧠 AI Providers (OpenAI & Gemini)
│   └── config.py      # Main application config
├── scripts/           # Switch AI, Test Workflows, Deploy tools
├── docs/              # Strategic Guides & Diagrams
├── data/              # 💾 Real-time context (news.json)
└── main.py            # Master Entry Point
```

## 🔄 AI Switcher CLI
Manage your failover stack easily:
```bash
python scripts/switch_ai.py status  # Check current provider
python scripts/switch_ai.py all      # Enable OpenAI -> Gemini Failover
python scripts/switch_ai.py gemini   # Force Gemini Only
```

## ▶️ Usage
- **Normal Operation**: `python main.py`
- **Full Workflow Stress Test**: `python scripts/test_full_workflow.py`
- **Check AI APIs**: `python scripts/switch_ai.py status`

📖 For detailed strategic setup, see **[docs/AI_FAILOVER_DIAGRAM.txt](docs/AI_FAILOVER_DIAGRAM.txt)**.
