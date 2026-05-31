"""
DealLens Web Scraper Service
Fetches and cleans website content for analysis.
"""
import httpx
import trafilatura
from bs4 import BeautifulSoup
from loguru import logger

from app.config import settings


async def scrape_website(url: str) -> str:
    """
    Fetch and extract clean text content from a website URL.
    Uses trafilatura for high-quality text extraction with BeautifulSoup fallback.
    """
    try:
        # Validate and normalize URL
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

        async with httpx.AsyncClient(
            timeout=settings.SCRAPER_TIMEOUT,
            follow_redirects=True,
            verify=False,
        ) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

        html_content = response.text

        # Primary: Use trafilatura for best quality extraction
        extracted = trafilatura.extract(
            html_content,
            include_links=False,
            include_tables=True,
            favor_precision=True,
        )

        if extracted and len(extracted.strip()) > 200:
            logger.info(f"Trafilatura extracted {len(extracted)} chars from {url}")
            return extracted[: settings.SCRAPER_MAX_CHARS]

        # Fallback: BeautifulSoup extraction
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]):
            tag.decompose()

        # Try to find main content areas
        main_content = soup.find("main") or soup.find("article") or soup.find("div", class_=lambda x: x and any(
            kw in str(x).lower() for kw in ["content", "main", "about", "description"]
        ))

        if main_content:
            text = main_content.get_text(separator=" ", strip=True)
        else:
            text = soup.get_text(separator=" ", strip=True)

        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = " ".join(lines)

        logger.info(f"BeautifulSoup extracted {len(clean_text)} chars from {url}")
        return clean_text[: settings.SCRAPER_MAX_CHARS]

    except httpx.TimeoutException:
        logger.warning(f"Timeout scraping {url}")
        return ""
    except httpx.HTTPStatusError as e:
        logger.warning(f"HTTP error {e.response.status_code} scraping {url}")
        return ""
    except Exception as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        return ""


async def search_company_info(company_name: str) -> str:
    """
    Attempt to find company information through search-like queries.
    Returns additional context for analysis.
    """
    # For V1, we'll return empty string and rely on the LLM's knowledge
    # V2 can integrate with real search APIs (Bing, Google, etc.)
    return ""