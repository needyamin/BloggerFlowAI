
export interface Env {
  AI: any;
  CHAT_HISTORY: KVNamespace;
  FILES: KVNamespace;
}

interface Message {
  role: string;
  content: string;
}

// --- Tool Implementations ---

const IGNORED_PATTERNS = [
  "node_modules", "vendor", ".git", ".vscode", ".idea", "dist", "build", "coverage"
];

function isIgnored(path: string): boolean {
  return IGNORED_PATTERNS.some(pattern => path.includes(pattern));
}

async function listFiles(env: Env): Promise<string[]> {
  const listed = await env.FILES.list();
  return listed.keys
    .map((k) => k.name)
    .filter(name => !isIgnored(name));
}

async function readFile(env: Env, path: string): Promise<string> {
  if (isIgnored(path)) {
    throw new Error(`Access Denied: Reading '${path}' is restricted (performance safety).`);
  }
  const content = await env.FILES.get(path);
  if (content === null) {
    throw new Error(`File not found: ${path}`);
  }
  return content;
}

async function writeFile(env: Env, path: string, content: string): Promise<string> {
  if (isIgnored(path)) {
    throw new Error(`Write Denied: Writing to '${path}' is restricted.`);
  }
  await env.FILES.put(path, content);
  return `Successfully wrote to ${path}`;
}

const TOPICS = [
  'Education', 'Scholarship Abroad', 'Latest Technology News',
  'Scholarship in USA/Japan/UK', 'Global Breaking News', 'Viral News', 'Secret Societies'
];

function getRandomTopic(): string {
  return TOPICS[Math.floor(Math.random() * TOPICS.length)];
}

// --- System Prompt ---

const SYSTEM_PROMPT = `
You are a world-class Investigative Journalist and Senior Research Academic. Your goal is to produce 100% REALISTIC, authoritative, and deeply researched blog posts. 

CORE DIRECTIVE: NO GENERIC FLUFF. NO FAKE DATA.
Every post must be an "Excellence in Journalism" piece—factual, data-driven, and hyper-specific.

TOPIC SPECIALIZATION (Categories):
${TOPICS.join(', ')}

REALISM & AUTHORITY RULES (STRICT):
1. SPECIFIC TOPICS: If the focus is "Education", do NOT write about education in general. Instead, pick a REAL, specific, and realistic event or sub-topic (e.g., "The 2026 Shift in UK Higher Education Funding" or "Stanford's Latest Research on Neural Learning"). 
2. REAL CONTENT: Every sentence must convey high-authority information. Use real-world statistics, cite specific researchers, name-drop real organizations, and discuss actual global trends.
3. REAL LINKS & SOURCES: You MUST use real, live, high-authority references (Wikipedia, Gov.uk, ResearchGate, NASA, Major News Outlets). NO example.com. Verify the link format in your internal knowledge.
4. REAL IMAGES: Use real, copyright-free image URLs from reliable sources (Wikimedia Commons, Unsplash CDN, Pexels CDN) that are directly relevant to the specific sub-topic.
5. WORD COUNT: Aim for massive depth (5000-10000 words total across segments). Use an expansive, professional, and investigative tone.
6. PERSPECTIVE: Write as an expert in the field. Use terminology and depth that a professional would expect.

STRUCTURE (STRICT HTML):
   - Header Image Table:
     <table align=\"center\" cellpadding=\"0\" cellspacing=\"0\" class=\"tr-caption-container\" style=\"margin-left: auto; margin-right: auto;\">
       <tbody>
         <tr><td style=\"text-align: center;\"><a href=\"REAL_IMAGE_URL\" imageanchor=\"1\" style=\"margin-left: auto; margin-right: auto;\"><img alt=\"SPECIFIC_ALT_TEXT\" border=\"0\" src=\"REAL_IMAGE_URL\" title=\"SPECIFIC_IMAGE_TITLE\" width=\"640\" /></a></td></tr>
         <tr><td class=\"tr-caption\" style=\"text-align: center;\">REALISTIC_CAPTION_DESCRIBING_THE_IMAGE</td></tr>
       </tbody>
     </table>
   - TOC Block:
     <!--- TABLE OF CONTENT START 2215587-->
     <div class=\"mbtTOC\"><button onclick=\"mbtToggle()\">Table Of Contents</button><ul id=\"mbtTOC\"></ul></div>
     <!--- TABLE OF CONTENT END 2215587-->
   - Style: Use <p style=\"text-align: justify;\">, <h2><i class=\"fa-solid fa-hands\"></i> Section Title</h2>, and include "More info [Reference](REAL_URL)" lines.
   - List Header: <h1 style=\"text-align: center;color:grey;\"><u>Comprehensive Research Data & Breakdown:</u><br /></h1>
   - Footer Script:
     <!--- TABLE OF CONTENT START 2215587-->
     <script>mbtTOC();</script>
     <!--- TABLE OF CONTENT END 2215587-->

JSON OUTPUT REQUIREMENT:
1. For general generation or 'section' mode:
   You MUST return ONLY a single valid JSON object. Ensure all newlines in the HTML content are escaped as \\n.
   {
     "title": "Section or Post Title",
     "content": "Detailed HTML content...",
     "labels": ["label1", "label2", "label3", "label4", "label5", "label6"]
   }
2. For 'outline' mode:
   Return ONLY a JSON object with a list of sections:
   {
     "topic": "The main topic",
     "sections": ["Section 1 Title", "Section 2 Title", ..., "Section 15 Title"]
   }

NO Conversational text. NO Markdown blocks. NO commentary. Just the JSON object. All strings MUST be valid JSON-escaped strings.
`;

export default {
  async fetch(request: Request, env: Env, ctx: any) {
    // CORS
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type,Accept",
        },
      });
    }

    const url = new URL(request.url);
    const sessionId = url.searchParams.get("session") || "default";

    // Handle Health Check
    if (url.pathname === "/health") {
      try {
        // Simple check for KV connectivity
        await env.CHAT_HISTORY.get("health-check");
        await env.FILES.list({ limit: 1 });
        return new Response(JSON.stringify({ status: "OK", kv: "connected" }), {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        });
      } catch (e: any) {
        return new Response(JSON.stringify({ status: "ERROR", message: e.message }), {
          status: 500,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        });
      }
    }

    // Handle Delete Session

    try {
      const url = new URL(request.url);
      let q = url.searchParams.get("q");
      const sessionId = url.searchParams.get("session") || "default";

      let userQuery = q;
      if (!userQuery || userQuery.toLowerCase() === "generate" || userQuery.toLowerCase() === "demo") {
        const topic = getRandomTopic();
        userQuery = `[MODE: FULL_POST] Generate a comprehensive 10,000+ word blog post about "${topic}" using REAL links, REAL copyright-free image URLs, and REAL sources from your knowledge of the internet. Follow the post_demo.html structure.`;
      } else if (userQuery.startsWith("outline:")) {
        const topic = userQuery.replace("outline:", "").trim();
        userQuery = `[MODE: OUTLINE] Generate a highly detailed 15-section outline for a 10,000-word blog post about "${topic}". Return JSON with "topic" and "sections" list.`;
      } else if (userQuery.startsWith("section:")) {
        const [section, topic] = userQuery.replace("section:", "").split("|topic:");
        userQuery = `[MODE: SECTION_ONLY] Write an extremely detailed, 1000-word deep-dive content for the section "${section.trim()}" as part of a larger post about "${topic.trim()}". Use real links and sources. Use <p style="text-align: justify;">.`;
      }

      // Always append strict format instruction to the user message to ensure model adherence
      const finalQuery = `${userQuery}\n\nSTRICT REQUIREMENT: Return ONLY a single valid JSON object. No conversational text. Real and live data only.`;

      // 1. Load History
      let history: Message[] = [];
      try {
        const raw = await env.CHAT_HISTORY.get(sessionId);
        if (raw) history = JSON.parse(raw);
      } catch (e) {
        console.error("Failed to load history", e);
      }

      // Add User Message
      history.push({ role: "user", content: finalQuery });

      // Keep recent context (last 5 messages for generation)
      const recentHistory = history.slice(-5);

      const messages = [
        { role: "system", content: SYSTEM_PROMPT },
        ...recentHistory
      ];

      // Run Model (Single generation, no loop)
      let responseText = "";
      const result: any = await env.AI.run("@cf/meta/llama-3.1-70b-instruct", {
        messages: messages,
        temperature: 0.3, // Slightly higher for more expansive writing, while keeping JSON sane
        max_tokens: 4096 // Ensure enough tokens for 2000 words
      });

      let aiContent = "";
      if (result && result.response) {
        aiContent = result.response;
      } else if (result && result.result && result.result.response) {
        aiContent = result.result.response;
      } else if (typeof result === "string") {
        aiContent = result;
      } else {
        aiContent = JSON.stringify(result);
      }

      if (!aiContent) {
        throw new Error("AI returned empty response");
      }

      responseText = aiContent.trim();

      // Clean up common AI markdown leakage
      if (responseText.includes("```json")) {
        responseText = responseText.split("```json")[1].split("```")[0].trim();
      } else if (responseText.includes("```")) {
        responseText = responseText.split("```")[1].split("```")[0].trim();
      }

      // Add to persistent history
      history.push({ role: "assistant", content: responseText });

      // Save History
      // Max 50 messages persistence
      if (history.length > 50) history = history.slice(-50);
      try {
        await env.CHAT_HISTORY.put(sessionId, JSON.stringify(history));
      } catch (e) {
        console.error("Failed to save history", e);
      }

      return new Response(responseText, {
        headers: {
          "Content-Type": "text/plain",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type,Accept",
        },
      });

    } catch (e: any) {
      return new Response(JSON.stringify({ error: e.message }), { status: 500 });
    }
  },
};
