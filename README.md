# 🚀 BloggerFlowAI: Master Monetization Edition (2026)

**BloggerFlowAI** is a high-performance, automated content engineering system designed to build high-CPC digital assets. It doesn't just "generate text"—it strategically crafts authoritative, multi-thousand-word blog posts optimized for **Google AdSense E-E-A-T** (Experience, Expertise, Authoritativeness, and Trustworthiness).

---

## 🌟 Strategic Features

### 1. 🗞️ High-Authority News Induction
The system features a custom **Newsbot Agent** that scans 21+ global high-authority sources (BBC, NYT, Reuters, TechCrunch, etc.) and strictly filters for **2026-relevant news**. 
- **Year Filtering**: Ensures all context is current and future-facing.
- **Deduplication**: Never posts the same story twice.
- **Metadata Extraction**: Captures sources, links, and exact publishing times for authority signaling.

### 2. 🧠 Massive Generation Engine (3,000 - 12,000+ Words)
Unlike basic bots, BloggerFlowAI uses a multi-phase generation strategy:
- **PHASE 1: Strategic Outlining**: AI drafts a 10-15 section roadmap based on the day's top news.
- **PHASE 2: Section Deep-Dives**: Each section is generated individually as an "800+ word deep-dive," ensuring incredible detail and technical depth.
- **Recovery Logic**: If a section fails, the system automatically triggers a "Single-shot Recovery" to ensure the article is never blank.

### 3. 🎯 Dynamic Niche Control
Control your niches and topics directly from your `.env` file without touching a single line of code:
- **TOPICS**: Define a list of high-CPC subjects (Education, Scholarships, Tech, Gadgets).
- **CATEGORIES**: Tell the AI exactly what AdSense categories to aim for. The AI dynamically reinjects these into its system prompt for every session.

### 4. 💰 AdSense Optimization & E-E-A-T
- **Semantic HTML**: Hierarchical `<h2>`, `<h3>` tags and justified text paragraphs.
- **Authority Signals**: Automatically prepends "Verified Reports" with exact timestamps.
- **Trust Citations**: Injects clickable source links into the content to build domain authority.

---

## 🛠️ Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configuration (`.env`)
Copy `example_env` to `.env` and fill in your keys:
- **`BLOGGER_BLOG_ID`**: Your Google Blogger unique ID.
- **`GEMINI_API_KEY`**: Get your key at [Google AI Studio](https://ai.google.dev/).
- **`OUTLINE_SECTIONS`**: Set to `15` for massive posts.
- **`SECTION_WORDS`**: Set to `800` for extreme detail.

### 3. Google API Setup
Place your `credentials.json` in the `credentials/` folder. On first run, it will open a browser for OAuth2 authentication.

### 4. Run to Post
```bash
python main.py
```

---

## 📄 Project Architecture

```
BloggerFlowAI/
├── src/
│   ├── app/           # Core Logic & Blogger Posting (post.py)
│   ├── models/
│   │   ├── custom_agent/   # 🗞️ NewsBot (Feed scanning & 2026 filtering)
│   │   └── remote_agent/   # 🧠 AI Providers (New google-genai SDK)
│   └── config.py      # Master Config (reads from .env)
├── data/              # 💾 Real-time context (news.json)
├── credentials/       # � Google API keys & tokens
└── main.py            # Master Entry Point
```

---

## ⚙️ Advanced Configuration (via `.env`)

| Variable | Description |
| :--- | :--- |
| `RUN_MODE` | `direct` for immediate post, `scheduler` for automated runs. |
| `TOPICS` | Comma-separated list for random topic selection. |
| `CATEGORIES` | Custom AdSense categories the AI should prioritize. |
| `MAX_NEWS_ITEMS` | Limits the number of sources cited in the article. |
| `FORCE_POST` | Skips word-count checks to ensure a post always goes live. |

---

## 📈 Failover & Robustness
The system uses the latest **google-genai v1.0+** SDK with **Gemini-Flash** for high-speed, JSON-native responses. If the primary AI provider fails or hits a quota, the system provides detailed logging and attempts a single-shot recovery content to ensure your site stays active.

---
*Developed for 2026 High-Authority Digital Asset Management.*
