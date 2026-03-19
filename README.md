# GEO Agent


[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Scraper-Playwright-green.svg)](https://playwright.dev/python/)
[![OpenAI](https://img.shields.io/badge/AI-GPT--4o-orange.svg)](https://openai.com/)


---
**GEOAgent** is an automated pipeline designed to audit and optimize web content for **Generative Engine Optimization (GEO)**. 

### Why GEO Matters
Large Language Models (LLMs) prioritize content that provides specific metrics, industry standards (NEMA, UL, CE), and precise terminology.

**GEOAgent** ensures your product data is structured so that when an AI engine performs a search, your content is identified as the most authoritative source, increasing your brand's "Share of Model."
In the era of AI-native search (SearchGPT, Perplexity, Gemini), traditional SEO is no longer enough. GEOAgent focuses on making content highly **"citable"** and **"retrievable"** for LLMs and RAG-based systems by maximizing Information Density and Technical Depth.

---

## Key Features

* **Autonomous Browser Automation:** Uses Playwright to bypass headless detection and extract core product data from modern JavaScript-heavy sites.
* **Intelligent Fact Extraction:** Utilizes `gpt-4o-mini` to strip noise (headers, footers, UI text) and isolate raw technical specifications.
* **GEO Audit Engine:** Performs a "First Principles" analysis of Information Density, Authoritative Citations, and Technical Depth using `gpt-4o`.
* **RAG-Ready Optimization:** Rewrites content specifically to increase its retrieval priority in RAG systems without hallucinating data.
* **Automated reporting:** Generates a professional Markdown side-by-side comparison for stakeholders and SEO audits.

---

## Tech Stack

- **Language:** Python 3.13+
- **Scraping:** Playwright (Chromium)
- **Intelligence:** OpenAI API (GPT-4o & GPT-4o-mini)
- **Configuration:** Dotenv for secure environment variable management

---

### Generated Artifacts
The agents produce five distinct files during the optimization lifecycle:

- `raw_text.txt`: The initial raw scrape.
- `facts.txt`: AI-extracted technical fact sheet.
- `geo_audit.json`: The 0-10 score and reasoning for current GEO performance.
- `geo_optimized.txt`: The final, high-density rewritten copy.
- `GEO_COMPARISON_REPORT.md`: A formatted side-by-side report.

---

**Note:** Run `playwright install chromium` after `pip install -r requirements.txt` to set up the browser engine.
