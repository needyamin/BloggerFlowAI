# Google Gemini API Setup Guide

## ✅ Good News!
**Google Gemini API is already integrated** into your BloggerFlowAI project! You just need to add your API key.

---

## 🔑 How to Get Your Gemini API Key

1. **Visit Google AI Studio**:
   - Go to: https://aistudio.google.com/app/apikey

2. **Create an API Key**:
   - Click "Get API Key" or "Create API Key"
   - Choose "Create API key in new project" (or use existing project)
   - Copy the generated API key

3. **Add to Your Project**:
   - Open `.env` file
   - Replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key
   ```bash
   GEMINI_API_KEY=AIzaSy...your-actual-key-here
   ```

---

## 🔄 How the AI Failover System Works

Your project uses **2 AI providers** in cascade:

```
1. OpenAI API → First fallback
         ↓ (if fails)
2. Google Gemini API → Second fallback
```

### When Each Provider is Used:

- **OpenAI API** (`OPENAI_API_KEY`): Tried first if configured. 
  - Persona: **Digital Media Strategist**.
  - Optimized for: Complex deep-dives and logical structuring.

- **Google Gemini API** (`GEMINI_API_KEY`): Primary fallback or main driver for mass-volume.
  - Persona: **AdSense Specialist**.
  - Optimized for: E-E-A-T compliance and 2026 news summarization.
  - Free tier: Fixed at 15 requests/minute.

---

## 📋 Current Configuration

In your `src/app/post.py`:
```python
# Failover order:
1. fetch_openai()       → if OPENAI_API_KEY is set
2. fetch_gemini()       → if GEMINI_API_KEY is set
```

In your `.env`:
```bash
# AI APIs
# OPENAI_API_KEY=sk-...
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

---

## 🧪 Testing Your Setup

After adding your Gemini API key, test it:

```bash
# Test Gemini API directly
python scripts/test_gemini.py
```

---

## 💡 Model Capabilities

All providers use the same prompt system and generate:

1. **Outlines**: Multi-section blog post structure
2. **Sections**: Detailed section content
3. **Full Posts**: Complete blog posts with:
   - Title
   - HTML content
   - Labels/tags
   - Real image URLs
   - Real source links

### AI Models Used:

| Provider | Model | Temperature | Max Tokens |
|----------|-------|-------------|------------|
| OpenAI | gpt-4o-mini | 0.3 | 4096 |
| Gemini | gemini-flash-latest | 0.3 | 4096 |

---

## 🎯 Recommended Setup

**For Best Reliability:**
1. Keep Gemini API key as primary (free tier is generous)
2. Optionally add OpenAI key (costs money but very reliable)

---

## 💬 Questions?

- **Q: Do I need both APIs?**
  - A: No! Even one is enough. System will try what you have configured.

- **Q: Which is best?**
  - A: Gemini has a generous free tier. OpenAI is extremely reliable but costs money.

- **Q: Can I use only Gemini?**
  - A: Yes! Just ensure GEMINI_API_KEY is set and OPENAI_API_KEY is commented out.
