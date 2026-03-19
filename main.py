import asyncio
import os
from playwright.async_api import async_playwright
from openai import OpenAI
from dotenv import load_dotenv

# Initialize Client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class GEOAgent:
    def __init__(self, url):
        self.url = url
        self.raw_content = ""
        self.fact_sheet = ""
        self.geo_audit = ""  

    async def fetch_content(self):
        """Refined scraping for GEO: Bypasses blocks and targets core data."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 800}
            )
            page = await context.new_page()

            try:
                print(f"Loading {self.url}...")
                await page.goto(self.url, wait_until="networkidle", timeout=60000)
                
                # Target the PRODUCT area specifically
                product_selector = "#main-content-container, .product-detail, body"
                self.raw_content = await page.inner_text(product_selector)

                with open("raw_text.txt", "w", encoding="utf-8") as f:
                    f.write(self.raw_content)
                
                print(f"Successfully fetched {len(self.raw_content)} characters.")
                return True
            except Exception as e:
                print(f"Scrape failed: {e}")
                return False
            finally:
                await browser.close()

    def clean_and_extract(self):
        """Step 1: Generalized noise reduction."""
        print("Cleaning and Extracting Fact Sheet...")
        prompt = (
            "Extract every technical specification, certification, and performance "
            "claim from the following text. Format it as a clean list of facts and claims. "
            "Do not summarize or interpret - just extract the raw facts. "
            f"\n\nText: {self.raw_content[:8000]}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        self.fact_sheet = response.choices[0].message.content

        # Write the extracted facts to facts.txt
        try:
            with open("facts.txt", "w", encoding="utf-8") as f:
                f.write(self.fact_sheet)
            print("Facts successfully saved to facts.txt")
        except Exception as e:
            print(f"Failed to write facts.txt: {e}")

        return self.fact_sheet

    def analyze_geo_footprint(self):
        """Step 2: Agentic Reasoning - Evaluating GEO Metrics."""
        print("Performing GEO Audit...")
        prompt = (
            f"Analyze the following product text for Generative Engine Optimization (GEO).\n\n"
            f"Text: {self.fact_sheet[:2000]}\n\n"
            f"Rate (0-10) and explain based on:\n"
            f"1. Information Density (Stats/Numbers)\n"
            f"2. Authoritative Citations (Expert/Brand mentions)\n"
            f"3. Technical Depth (Domain-specific terminology)\n"
            f"Include pros, cons, and missing elements. Respond in JSON format."
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
    
        self.geo_audit = response.choices[0].message.content

        # Write to geo_audit.json
        try:
            with open("geo_audit.json", "w", encoding="utf-8") as f:
                f.write(self.geo_audit)
            print("GEO Audit successfully saved to geo_audit.json")
        except Exception as e:
            print(f"Failed to write geo_audit.json: {e}")

        return self.geo_audit

    def generate_geo_optimized_copy(self):
        """Step 3: Creating high-visibility snippets."""
        print("Generating Optimized Copy...")
        prompt = (
            f"You are a GEO Specialist. Rewrite this product description to be "
            f"highly citable for LLMs and RAG systems.\n\n"
            f"--- DATA SOURCE ---\n{self.fact_sheet}\n\n"
            f"--- PERFORMANCE AUDIT ---\n{self.geo_audit}\n\n"
            f"INSTRUCTIONS:\n"
            f"1. Address every weakness in the audit.\n"
            f"2. Use precise domain terminology and cite standards/certifications.\n"
            f"3. DO NOT hallucinate.\n\n"
            f"Output only the optimized product description."
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        optimized_text = response.choices[0].message.content

        try:
            with open("geo_optimized.txt", "w", encoding="utf-8") as f:
                f.write(optimized_text)
            print("Optimized copy saved to geo_optimized.txt")
        except Exception as e:
            print(f"Failed to write geo_optimized.txt: {e}")

        return optimized_text

    def generate_comparison_report(self, optimized_text):
        """Step 4: Save the final report."""
        print("Generating Final Report...")
        report_content = f"""# GEO Optimization Report
**Source URL:** {self.url}

## 1. Original Product Description (Raw Snippet)
{self.raw_content[:1000]}...

## 2. GEO-Optimized Product Description
{optimized_text}

## 3. Key Strategy Applied
| Category | Strategy |
| :--- | :--- |
| **Information Density** | Metric-heavy conversion of vague specs. |
| **Technical Depth** | Domain-specific terminology integration. |
| **Audit Context** | Addresses gaps identified in AI retrieval testing. |

---
*Report generated by GEOAgent v1.0*
            """
        with open("GEO_COMPARISON_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report_content)
        print("[✔] Comparison report saved to: GEO_COMPARISON_REPORT.md")

async def main():
    """Main execution flow."""
    target_url = "https://www.automationdirect.com/adc/shopping/catalog/motors/ac_motors/general_purpose/mtrp-001-3bd18"
    agent = GEOAgent(target_url)

    # 1. Fetch
    success = await agent.fetch_content()
    if not success:
        print("[!] Execution stopped due to scrape failure.")
        return

    # 2. Extract
    agent.clean_and_extract()

    # 3. Audit
    agent.analyze_geo_footprint()

    # 4. Optimize
    optimized_copy = agent.generate_geo_optimized_copy()

    # 5. Report
    agent.generate_comparison_report(optimized_copy)
    print("\n--- Pipeline Complete ---")

if __name__ == "__main__":
    asyncio.run(main())