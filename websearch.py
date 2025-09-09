import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import unquote
import urllib.parse

try:
    from googlesearch.user_agents import get_useragent
except ImportError:
    def get_useragent():
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        return random.choice(agents)

def search(provider="google", links=5, query="", description_full=False, html_raw=False):
    """
    Search web with specified provider
    
    Args:
        provider: Search engine (google, yahoo, bing, duckduckgo, brave)
        links: Number of results to return
        query: Search query string
        description_full: Extract full text content from pages
        html_raw: Return raw HTML response
    
    Returns:
        List of search results with title, link, snippet, description
        or raw HTML string if html_raw=True
    """
    
    if provider in ["google", "bing"]:
        headers = {"User-Agent": get_useragent(), "Accept": "*/*"}
    else:
        headers = {
            "User-Agent": get_useragent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    try:
        if provider == "google":
            url = "https://www.google.com/search"
            params = {"q": query, "num": links + 2, "hl": "en", "start": 0, "safe": "active"}
            cookies = {'CONSENT': 'PENDING+987', 'SOCS': 'CAESHAgBEhIaAB'}
            response = requests.get(url, headers=headers, params=params, cookies=cookies, timeout=15)
            
        elif provider == "yahoo":
            url = "https://search.yahoo.com/search"
            params = {"p": query}
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
        elif provider == "bing":
            url = "https://www.bing.com/search"
            params = {"q": query, "count": links}
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
        elif provider == "duckduckgo":
            url = "https://html.duckduckgo.com/html/"
            params = {"q": query}
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
        elif provider == "brave":
            url = "https://search.brave.com/search"
            params = {"q": query}
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
        else:
            return []
        
        response.raise_for_status()
        
        if html_raw:
            return response.text
            
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        if provider == "google":
            result_block = soup.find_all("div", class_="ezO2md")
            if not result_block:
                result_block = soup.select(".tF2Cxc, .g, .MjjYud")
                
            for result in result_block[:links]:
                try:
                    link_tag = result.find("a", href=True)
                    if not link_tag:
                        continue
                        
                    # Try multiple title selectors
                    title_tag = link_tag.find("span", class_="CVA68e")
                    if not title_tag:
                        title_tag = result.find("h3")
                    if not title_tag:
                        continue
                    
                    # Try multiple description selectors
                    description_tag = result.find("span", class_="FrIlee")
                    if not description_tag:
                        description_tag = result.select_one(".VwiC3b, .s3v9rd, .IsZvec")
                    
                    link = link_tag["href"]
                    if link.startswith('/url?q='):
                        link = unquote(link.split("&")[0].replace("/url?q=", ""))
                    
                    if not link.startswith('http'):
                        continue
                        
                    title = title_tag.get_text(strip=True)
                    snippet = description_tag.get_text(strip=True) if description_tag else ""
                    
                    description = snippet
                    if description_full and link:
                        description = _fetch_full_description(link, headers)
                    
                    results.append({"title": title, "link": link, "snippet": snippet, "description": description})
                except:
                    continue
        
        elif provider == "yahoo":
            blocks = soup.select('.algo, .Sr')
            for block in blocks[:links*3]:
                try:
                    if block.select('.AdTop, .AdHdrTop, .ads') or 'data-matarget="ad"' in str(block):
                        continue
                        
                    link_elem = block.select_one('a[href]')
                    title_elem = block.select_one('h3, .title')
                    snippet_elem = block.select_one('p, .compText p, .fc-dustygray')
                    
                    if not link_elem or not title_elem:
                        continue
                    
                    link = link_elem.get('href', '')
                    
                    if 'RU=' in link:
                        link = urllib.parse.unquote(link.split('RU=')[1].split('/RK=')[0])
                    elif '/rdclk' in link or '/cbclk' in link:
                        if 'RU=' in link:
                            link = urllib.parse.unquote(link.split('RU=')[1].split('/')[0])
                    
                    if not link.startswith('http'):
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    if len(results) >= links:
                        break
                    
                    description = snippet
                    if description_full and link:
                        description = _fetch_full_description(link, headers)
                    
                    results.append({"title": title, "link": link, "snippet": snippet, "description": description})
                except:
                    continue
        
        elif provider == "bing":
            result_block = soup.find_all("li", class_="b_algo")
            for result in result_block[:links]:
                try:
                    link_tag = result.find("a", href=True)
                    title_tag = result.find("h2")
                    description_tag = result.find("p")
                    
                    if link_tag and title_tag:
                        link = link_tag["href"]
                        if not link.startswith('http'):
                            continue
                            
                        title = title_tag.text.strip()
                        snippet = description_tag.text.strip() if description_tag else ""
                        
                        description = snippet
                        if description_full and link:
                            description = _fetch_full_description(link, headers)
                        
                        results.append({"title": title, "link": link, "snippet": snippet, "description": description})
                except:
                    continue
        
        elif provider == "duckduckgo":
            blocks = soup.select('.result, .web-result')
            for block in blocks[:links]:
                try:
                    link_elem = block.select_one('a[href]')
                    title_elem = block.select_one('h2, .result__title')
                    snippet_elem = block.select_one('.result__snippet, p')
                    
                    if not link_elem or not title_elem:
                        continue
                    
                    link = link_elem.get('href', '')
                    
                    if 'uddg=' in link:
                        link = urllib.parse.unquote(link.split('uddg=')[1].split('&')[0])
                    
                    if not link.startswith('http'):
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    description = snippet
                    if description_full and link:
                        description = _fetch_full_description(link, headers)
                    
                    results.append({"title": title, "link": link, "snippet": snippet, "description": description})
                except:
                    continue
        
        elif provider == "brave":
            all_links = soup.select('a[href]')
            for link_elem in all_links:
                try:
                    href = link_elem.get('href', '')
                    if not href.startswith('http'):
                        continue
                    
                    if any(x in href for x in ['google.com', 'yahoo.com', 'bing.com', 'brave.com']):
                        continue
                    
                    title = link_elem.get_text(strip=True)
                    parent = link_elem.parent
                    
                    if parent:
                        heading = parent.select_one('h1, h2, h3, h4')
                        if heading:
                            title = heading.get_text(strip=True)
                    
                    if title and len(title) > 10 and len(results) < links:
                        description = ""
                        if description_full:
                            description = _fetch_full_description(href, headers)
                        
                        results.append({"title": title, "link": href, "snippet": "", "description": description})
                except:
                    continue
        
        return results
        
    except Exception:
        return []

def _fetch_full_description(url, headers):
    """Extract full text content from a webpage"""
    try:
        response = requests.get(url, headers={"User-Agent": get_useragent()}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.decompose()
        
        content_tags = soup.find_all(['p', 'div', 'article', 'section'])
        texts = []
        for tag in content_tags:
            text = tag.get_text(strip=True)
            if text and len(text) > 20:
                texts.append(text)
        
        return ' '.join(texts[:8])
        
    except:
        return ""