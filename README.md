# Auto Post Blogger AI
Massive, realistic, 10,000+ word blog posts automated for Blogger.com.

## 🚀 How it Works
1. **Modular Generation**: The system generates a detailed 15-section outline and then fetches each section individually to achieve industry-leading depth and word count.
2. **Investigative Journalism**: The AI is tuned to skip generic fluff and use real-world data, live authority links (Wikipedia, Gov, etc.), and copyright-free images.
3. **Automated Stitching**: The Python engine cleans and merges all sections into a perfect single HTML post.

## 🛠️ Setup
1. **Install Python Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Deploy AI Engine**:
   ```bash
   cd worker-ai-gpt-oss-120b
   npm install
   & "C:\Program Files\nodejs\npm.cmd" run deploy
   ```
3. **Configuration**:
   - Update `BLOGGER_BLOG_ID` in `config.py` or `.env`.
   - Place your Google Cloud `credentials.json` in the root folder.

## 📄 Core Files
- `blogger_post.py`: Coordinates the multi-stage 10,000-word generation and posting.
- `scheduler.py`: Runs the automation on a daily schedule.
- `config.py`: Manages the strictly allowed topics and Worker URL.
- `realtime_data_collect_bot/`: Fetches trending news from RSS feeds to populate the generation pipeline.
- `worker-ai-gpt-oss-120b/`: The Cloudflare Worker AI source (Investigative Journalist persona).

## ▶️ Usage
- **Generate & Post Now**: `python blogger_post.py`
- **Start Automation**: `python scheduler.py`
- **Collect Trending News**: `cd realtime_data_collect_bot && python bot.py`
