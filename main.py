from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from datetime import datetime
import markdown

from config import Config
from models import AnalysisResponse, ErrorResponse
from services.search_service import SearchService
from services.ai_service import AIService
from security import limiter, verify_api_key, track_session

app = FastAPI(
    title="Trade Opportunities API",
    description="Analyzes market data and provides trade opportunity insights for specific sectors in India.",
    version="1.1.0"
)

# Register rate limit handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

ai_service = AIService()

def get_html_template(content: str, sector: str):
    """
    Wraps the markdown content in a premium HTML/CSS template.
    """
    html_content = markdown.markdown(content, extensions=['tables', 'fenced_code'])
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{sector} Market Analysis - Trade Intel</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg: #0f172a;
                --card-bg: rgba(30, 41, 59, 0.7);
                --accent: #38bdf8;
                --accent-grad: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
                --text: #f1f5f9;
                --text-muted: #94a3b8;
                --border: rgba(255, 255, 255, 0.1);
            }}
            
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{
                font-family: 'Inter', sans-serif;
                background-color: var(--bg);
                background-image: radial-gradient(circle at 50% 0%, #1e293b 0%, #0f172a 100%);
                color: var(--text);
                line-height: 1.6;
                padding: 40px 20px;
            }}
            
            .container {{
                max-width: 900px;
                margin: 0 auto;
            }}
            
            header {{
                text-align: center;
                margin-bottom: 50px;
            }}
            
            .badge {{
                display: inline-block;
                padding: 6px 16px;
                background: var(--accent-grad);
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 15px;
                box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
            }}
            
            h1 {{
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 10px;
                letter-spacing: -1px;
            }}
            
            .meta {{
                color: var(--text-muted);
                font-size: 0.9rem;
            }}
            
            .report-card {{
                background: var(--card-bg);
                backdrop-filter: blur(12px);
                border: 1px solid var(--border);
                border-radius: 24px;
                padding: 50px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            }}
            
            /* Markdown Styling */
            .report-content h2 {{
                color: var(--accent);
                margin-top: 40px;
                margin-bottom: 20px;
                font-size: 1.5rem;
                border-bottom: 1px solid var(--border);
                padding-bottom: 10px;
            }}
            
            .report-content h3 {{
                margin-top: 30px;
                margin-bottom: 15px;
                color: #bae6fd;
            }}
            
            .report-content p {{
                margin-bottom: 20px;
                color: #cbd5e1;
            }}
            
            .report-content ul, .report-content ol {{
                margin-left: 20px;
                margin-bottom: 20px;
                color: #cbd5e1;
            }}
            
            .report-content li {{
                margin-bottom: 10px;
            }}
            
            .report-content table {{
                width: 100%;
                border-collapse: collapse;
                margin: 30px 0;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 12px;
                overflow: hidden;
            }}
            
            .report-content th, .report-content td {{
                padding: 15px;
                text-align: left;
                border-bottom: 1px solid var(--border);
            }}
            
            .report-content th {{
                background: rgba(56, 189, 248, 0.1);
                color: var(--accent);
                font-weight: 600;
                text-transform: uppercase;
                font-size: 0.75rem;
                letter-spacing: 1px;
            }}
            
            .report-content strong {{
                color: #fff;
            }}
            
            .report-content hr {{
                border: none;
                border-top: 1px solid var(--border);
                margin: 40px 0;
            }}
            
            footer {{
                text-align: center;
                margin-top: 50px;
                color: var(--text-muted);
                font-size: 0.8rem;
            }}
            
            @media (max-width: 600px) {{
                .report-card {{ padding: 25px; }}
                h1 {{ font-size: 1.8rem; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div class="badge">Market Intelligence</div>
                <h1>{sector} Analysis Report</h1>
                <div class="meta">Generated on {datetime.now().strftime('%B %d, %Y')} • Indian Market Insights</div>
            </header>
            
            <div class="report-card">
                <div class="report-content">
                    {html_content}
                </div>
            </div>
            
            <footer>
                &copy; 2026 Trade Intel API • Powered by Gemini Flash • Data from real-time market feeds
            </footer>
        </div>
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <body style="font-family: sans-serif; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; flex-direction: column;">
            <h1 style="color: #38bdf8;">Trade Opportunities API v1.1</h1>
            <p style="color: #94a3b8;">Welcome! To generate a report, use the endpoint below:</p>
            <code style="background: #1e293b; padding: 15px; border-radius: 8px; margin-top: 20px; border: 1px solid #334155;">
                /analyze/{sector}?api_key=your_key
            </code>
            <a href="/analyze/Solar?api_key=admin123" style="margin-top: 30px; color: #38bdf8; text-decoration: none; border: 1px solid #38bdf8; padding: 10px 20px; border-radius: 5px;">Try Example: Solar Sector</a>
        </body>
    </html>
    """

@app.get("/analyze/{sector}", response_class=HTMLResponse)
@limiter.limit(Config.RATE_LIMIT)
async def analyze_sector_endpoint(
    sector: str, 
    request: Request, 
    api_key: str = Depends(verify_api_key)
):
    """
    Analyzes a specific market sector in India and returns a premium HTML report.
    """
    # Track session usage
    track_session(api_key)
    
    # 1. Gather Market Data
    market_data = await SearchService.search_market_data(sector)
    
    if "Error" in market_data and len(market_data) < 50:
        raise HTTPException(status_code=500, detail="Failed to gather market data.")

    # 2. Analyze with Gemini
    report_md = await ai_service.analyze_sector(sector, market_data)
    
    if "Error" in report_md and len(report_md) < 100:
        raise HTTPException(status_code=500, detail=report_md)

    # 3. Render and return the HTML report
    return get_html_template(report_md, sector.capitalize())

@app.get("/session/stats", dependencies=[Depends(verify_api_key)])
async def get_session_stats(api_key: str = Depends(verify_api_key)):
    """
    Returns session usage stats for the current API key.
    """
    return track_session(api_key)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
