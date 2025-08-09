#!/usr/bin/env python3
"""
Web Scraping Tools for Pilar2 Agents
כלי web scraping לסוכני Pilar2
"""

import os
import time
import logging
import requests
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
from pathlib import Path

# Safe imports with fallbacks
try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False
    logging.warning("BeautifulSoup not available. Web scraping will be limited.")

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logging.warning("Selenium not available. Dynamic content scraping will be limited.")

try:
    import PyPDF2
    import io
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logging.warning("PyPDF2 not available. PDF reading will be limited.")

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class ScrapingResult:
    """Result of web scraping operation"""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

class WebScrapingTools:
    """Safe web scraping tools for Pilar2 agents"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 30
        self.max_retries = 3
        self.driver = None
        
    def _safe_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Make a safe HTTP request with error handling"""
        try:
            for attempt in range(self.max_retries):
                try:
                    response = self.session.request(
                        method, 
                        url, 
                        timeout=self.timeout,
                        **kwargs
                    )
                    response.raise_for_status()
                    return response
                except requests.exceptions.RequestException as e:
                    if attempt == self.max_retries - 1:
                        logger.error(f"Failed to fetch {url} after {self.max_retries} attempts: {e}")
                        return None
                    time.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            return None
    
    def _get_selenium_driver(self) -> Optional[webdriver.Chrome]:
        """Get Selenium WebDriver with safe configuration"""
        if not SELENIUM_AVAILABLE:
            return None
            
        try:
            if self.driver is None:
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                
            return self.driver
        except Exception as e:
            logger.error(f"Failed to initialize Selenium driver: {e}")
            return None
    
    def scrape_webpage(self, url: str, use_selenium: bool = False) -> ScrapingResult:
        """
        Safely scrape a webpage
        
        Args:
            url: URL to scrape
            use_selenium: Whether to use Selenium for dynamic content
            
        Returns:
            ScrapingResult with extracted content
        """
        try:
            # Validate URL
            if not url.startswith(('http://', 'https://')):
                return ScrapingResult(
                    url=url,
                    title="",
                    content="",
                    metadata={},
                    success=False,
                    error_message="Invalid URL format"
                )
            
            # Try Selenium first if requested and available
            if use_selenium and SELENIUM_AVAILABLE:
                result = self._scrape_with_selenium(url)
                if result.success:
                    return result
            
            # Fallback to requests + BeautifulSoup
            return self._scrape_with_requests(url)
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return ScrapingResult(
                url=url,
                title="",
                content="",
                metadata={},
                success=False,
                error_message=str(e)
            )
    
    def _scrape_with_requests(self, url: str) -> ScrapingResult:
        """Scrape webpage using requests and BeautifulSoup"""
        response = self._safe_request(url)
        if not response:
            return ScrapingResult(
                url=url,
                title="",
                content="",
                metadata={},
                success=False,
                error_message="Failed to fetch page"
            )
        
        try:
            if not BEAUTIFULSOUP_AVAILABLE:
                # Fallback to basic text extraction
                content = response.text
                title = url
            else:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract title
                title_tag = soup.find('title')
                title = title_tag.get_text().strip() if title_tag else url
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Extract text content
                content = soup.get_text()
                
                # Clean up whitespace
                lines = (line.strip() for line in content.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                content = ' '.join(chunk for chunk in chunks if chunk)
            
            metadata = {
                'content_type': response.headers.get('content-type', ''),
                'status_code': response.status_code,
                'encoding': response.encoding,
                'size': len(response.content)
            }
            
            return ScrapingResult(
                url=url,
                title=title,
                content=content,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error parsing content from {url}: {e}")
            return ScrapingResult(
                url=url,
                title="",
                content="",
                metadata={},
                success=False,
                error_message=f"Failed to parse content: {str(e)}"
            )
    
    def _scrape_with_selenium(self, url: str) -> ScrapingResult:
        """Scrape webpage using Selenium for dynamic content"""
        driver = self._get_selenium_driver()
        if not driver:
            return ScrapingResult(
                url=url,
                title="",
                content="",
                metadata={},
                success=False,
                error_message="Selenium driver not available"
            )
        
        try:
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract title
            title = driver.title
            
            # Extract content
            body = driver.find_element(By.TAG_NAME, "body")
            content = body.text
            
            metadata = {
                'method': 'selenium',
                'url': driver.current_url,
                'page_source_length': len(driver.page_source)
            }
            
            return ScrapingResult(
                url=url,
                title=title,
                content=content,
                metadata=metadata,
                success=True
            )
            
        except TimeoutException:
            return ScrapingResult(
                url=url,
                title="",
                content="",
                metadata={},
                success=False,
                error_message="Page load timeout"
            )
        except Exception as e:
            logger.error(f"Selenium error scraping {url}: {e}")
            return ScrapingResult(
                url=url,
                title="",
                content="",
                metadata={},
                success=False,
                error_message=f"Selenium error: {str(e)}"
            )
    
    def scrape_multiple_pages(self, urls: List[str], use_selenium: bool = False) -> Dict[str, ScrapingResult]:
        """Scrape multiple webpages safely"""
        results = {}
        
        for url in urls:
            try:
                result = self.scrape_webpage(url, use_selenium)
                results[url] = result
                
                # Add delay between requests to be respectful
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                results[url] = ScrapingResult(
                    url=url,
                    title="",
                    content="",
                    metadata={},
                    success=False,
                    error_message=str(e)
                )
        
        return results
    
    def extract_specific_content(self, url: str, selectors: Dict[str, str], use_selenium: bool = False) -> Dict[str, str]:
        """
        Extract specific content using CSS selectors
        
        Args:
            url: URL to scrape
            selectors: Dictionary of {name: css_selector}
            use_selenium: Whether to use Selenium
            
        Returns:
            Dictionary of extracted content
        """
        if not BEAUTIFULSOUP_AVAILABLE:
            return {"error": "BeautifulSoup not available"}
        
        result = self.scrape_webpage(url, use_selenium)
        if not result.success:
            return {"error": result.error_message}
        
        try:
            if use_selenium and SELENIUM_AVAILABLE:
                return self._extract_with_selenium(url, selectors)
            else:
                return self._extract_with_beautifulsoup(result.content, selectors)
                
        except Exception as e:
            logger.error(f"Error extracting specific content from {url}: {e}")
            return {"error": str(e)}
    
    def _extract_with_beautifulsoup(self, html_content: str, selectors: Dict[str, str]) -> Dict[str, str]:
        """Extract content using BeautifulSoup"""
        soup = BeautifulSoup(html_content, 'html.parser')
        extracted = {}
        
        for name, selector in selectors.items():
            try:
                elements = soup.select(selector)
                if elements:
                    extracted[name] = ' '.join(elem.get_text().strip() for elem in elements)
                else:
                    extracted[name] = ""
            except Exception as e:
                logger.error(f"Error extracting {name} with selector {selector}: {e}")
                extracted[name] = ""
        
        return extracted
    
    def _extract_with_selenium(self, url: str, selectors: Dict[str, str]) -> Dict[str, str]:
        """Extract content using Selenium"""
        driver = self._get_selenium_driver()
        if not driver:
            return {"error": "Selenium driver not available"}
        
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            extracted = {}
            for name, selector in selectors.items():
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        extracted[name] = ' '.join(elem.text.strip() for elem in elements)
                    else:
                        extracted[name] = ""
                except Exception as e:
                    logger.error(f"Error extracting {name} with selector {selector}: {e}")
                    extracted[name] = ""
            
            return extracted
            
        except Exception as e:
            logger.error(f"Selenium error extracting content from {url}: {e}")
            return {"error": str(e)}
    
    def scrape_tax_rates(self, country: str = "israel") -> Dict[str, Any]:
        """Scrape tax rates from government websites"""
        # This is a placeholder - would need specific URLs and selectors
        tax_urls = {
            "israel": "https://taxauthority.gov.il/rates",
            "oecd": "https://oecd.org/tax/tax-policy/tax-database.htm"
        }
        
        url = tax_urls.get(country.lower(), tax_urls["israel"])
        result = self.scrape_webpage(url)
        
        if result.success:
            # Parse tax rates from content (simplified)
            return {
                "country": country,
                "source": url,
                "content": result.content[:1000],  # First 1000 chars
                "timestamp": result.timestamp
            }
        else:
            return {
                "country": country,
                "error": result.error_message
            }
    
    def scrape_oecd_documents(self, document_type: str = "pillar-two") -> Dict[str, Any]:
        """Scrape OECD documents"""
        oecd_urls = {
            "pillar-two": "https://www.oecd.org/tax/beps/",
            "guidance": "https://www.oecd.org/tax/beps/",
            "implementation": "https://www.oecd.org/tax/beps/"
        }
        
        url = oecd_urls.get(document_type, oecd_urls["pillar-two"])
        result = self.scrape_webpage(url)
        
        if result.success:
            return {
                "document_type": document_type,
                "source": url,
                "title": result.title,
                "content": result.content[:2000],  # First 2000 chars
                "timestamp": result.timestamp
            }
        else:
            return {
                "document_type": document_type,
                "error": result.error_message
            }
    
    def scrape_israel_tax_authority(self, section: str = "general") -> Dict[str, Any]:
        """
        Scrape information from Israel Tax Authority website
        """
        try:
            base_url = "https://www.gov.il/he/departments/ministry_of_finance/tax_authority"
            
            # Different sections of the tax authority
            section_urls = {
                "general": base_url,
                "rates": f"{base_url}/tax_rates",
                "regulations": f"{base_url}/regulations",
                "international": f"{base_url}/international_taxation"
            }
            
            url = section_urls.get(section, base_url)
            result = self.scrape_webpage(url)
            
            if result.success:
                return {
                    "success": True,
                    "content": result.content,
                    "title": result.title,
                    "url": url
                }
            else:
                return {
                    "success": False,
                    "error": result.error_message,
                    "url": url
                }
                
        except Exception as e:
            logger.error(f"Error scraping Israel Tax Authority: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def scrape_israel_tax_treaties(self, country: str = "all") -> Dict[str, Any]:
        """
        Scrape Israel tax treaties from government website
        """
        try:
            treaties_url = "https://www.gov.il/he/Departments/DynamicCollectors/international_agreements?skip=0&limit=10&type=03"
            
            result = self.scrape_webpage(treaties_url)
            
            if not result.success:
                return {
                    "success": False,
                    "error": result.error_message
                }
            
            # Parse treaties list
            treaties = self._parse_treaties_list(result.content)
            
            if country.lower() != "all":
                treaties = [t for t in treaties if country.lower() in t.get("title", "").lower()]
            
            return {
                "success": True,
                "treaties": treaties,
                "total_count": len(treaties)
            }
            
        except Exception as e:
            logger.error(f"Error scraping Israel tax treaties: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_treaties_list(self, html_content: str) -> List[Dict[str, str]]:
        """
        Parse treaties list from HTML content
        """
        treaties = []
        
        if not BEAUTIFULSOUP_AVAILABLE:
            return treaties
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for treaty links (this is a generic approach)
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                # Filter for tax treaty related links
                if any(keyword in href.lower() or keyword in title.lower() 
                       for keyword in ['treaty', 'agreement', 'convention', 'tax']):
                    treaties.append({
                        "title": title,
                        "url": href if href.startswith('http') else f"https://www.gov.il{href}",
                        "country": self._extract_country_from_title(title)
                    })
            
            return treaties
            
        except Exception as e:
            logger.error(f"Error parsing treaties list: {e}")
            return treaties
    
    def _extract_country_from_title(self, title: str) -> str:
        """
        Extract country name from treaty title
        """
        # Common country patterns in Hebrew and English
        countries = {
            'ארצות הברית': 'USA', 'USA': 'USA', 'United States': 'USA',
            'בריטניה': 'UK', 'UK': 'UK', 'United Kingdom': 'UK',
            'גרמניה': 'Germany', 'Germany': 'Germany',
            'צרפת': 'France', 'France': 'France',
            'איטליה': 'Italy', 'Italy': 'Italy',
            'ספרד': 'Spain', 'Spain': 'Spain',
            'הולנד': 'Netherlands', 'Netherlands': 'Netherlands',
            'בלגיה': 'Belgium', 'Belgium': 'Belgium',
            'שוויץ': 'Switzerland', 'Switzerland': 'Switzerland',
            'אוסטריה': 'Austria', 'Austria': 'Austria',
            'פולין': 'Poland', 'Poland': 'Poland',
            'צ\'כיה': 'Czech Republic', 'Czech Republic': 'Czech Republic',
            'הונגריה': 'Hungary', 'Hungary': 'Hungary',
            'רומניה': 'Romania', 'Romania': 'Romania',
            'בולגריה': 'Bulgaria', 'Bulgaria': 'Bulgaria',
            'יוון': 'Greece', 'Greece': 'Greece',
            'פורטוגל': 'Portugal', 'Portugal': 'Portugal',
            'אירלנד': 'Ireland', 'Ireland': 'Ireland',
            'דנמרק': 'Denmark', 'Denmark': 'Denmark',
            'נורבגיה': 'Norway', 'Norway': 'Norway',
            'שבדיה': 'Sweden', 'Sweden': 'Sweden',
            'פינלנד': 'Finland', 'Finland': 'Finland',
            'אוסטרליה': 'Australia', 'Australia': 'Australia',
            'סין': 'China', 'China': 'China'
        }
        
        for hebrew, english in countries.items():
            if hebrew in title or english in title:
                return english
        
        return "Unknown"
    
    def download_and_read_pdf(self, pdf_url: str) -> Dict[str, Any]:
        """
        Download and read PDF content from URLs
        """
        if not PDF_AVAILABLE:
            return {
                "success": False,
                "error": "PyPDF2 not available"
            }
        
        try:
            # Download PDF
            response = self._safe_request(pdf_url)
            if not response:
                return {
                    "success": False,
                    "error": "Failed to download PDF"
                }
            
            # Read PDF content
            pdf_content = self._extract_pdf_text(response.content)
            
            return {
                "success": True,
                "content": pdf_content,
                "url": pdf_url
            }
            
        except Exception as e:
            logger.error(f"Error reading PDF from {pdf_url}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_pdf_text(self, pdf_content: bytes) -> str:
        """
        Extract text from PDF content
        """
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            return f"Error reading PDF: {str(e)}"
    
    def get_israel_tax_treaty_content(self, country: str) -> Dict[str, Any]:
        """
        Get full content of Israel tax treaty with specific country
        """
        try:
            # First get the treaties list
            treaties_result = self.scrape_israel_tax_treaties()
            
            if not treaties_result.get("success"):
                return treaties_result
            
            treaties = treaties_result.get("treaties", [])
            
            # Find treaty for specific country
            target_treaty = None
            for treaty in treaties:
                if country.lower() in treaty.get("country", "").lower() or \
                   country.lower() in treaty.get("title", "").lower():
                    target_treaty = treaty
                    break
            
            if not target_treaty:
                return {
                    "success": False,
                    "error": f"No treaty found for {country}"
                }
            
            # Download and read the treaty PDF
            pdf_result = self.download_and_read_pdf(target_treaty["url"])
            
            if pdf_result.get("success"):
                return {
                    "success": True,
                    "treaty_title": target_treaty["title"],
                    "country": target_treaty["country"],
                    "content": pdf_result["content"],
                    "url": target_treaty["url"]
                }
            else:
                return pdf_result
                
        except Exception as e:
            logger.error(f"Error getting treaty content for {country}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_all_israel_tax_treaties_content(self) -> Dict[str, Any]:
        """
        Get content of all Israel tax treaties
        """
        try:
            # Get treaties list
            treaties_result = self.scrape_israel_tax_treaties()
            
            if not treaties_result.get("success"):
                return treaties_result
            
            treaties = treaties_result.get("treaties", [])
            results = {}
            
            # Process each treaty
            for treaty in treaties:
                country = treaty.get("country", "Unknown")
                try:
                    pdf_result = self.download_and_read_pdf(treaty["url"])
                    results[country] = {
                        "success": pdf_result.get("success", False),
                        "title": treaty["title"],
                        "content": pdf_result.get("content", ""),
                        "url": treaty["url"]
                    }
                    if not pdf_result.get("success"):
                        results[country]["error"] = pdf_result.get("error", "Unknown error")
                except Exception as e:
                    results[country] = {
                        "success": False,
                        "error": str(e),
                        "title": treaty["title"],
                        "url": treaty["url"]
                    }
            
            return {
                "success": True,
                "treaties": results,
                "total_processed": len(results)
            }
            
        except Exception as e:
            logger.error(f"Error getting all treaties content: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error closing Selenium driver: {e}")
            finally:
                self.driver = None
        
        if self.session:
            self.session.close()
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()

# Global instance for reuse
web_scraping_tools = WebScrapingTools()
