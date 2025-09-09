"""
WebSearch - A simple Python web search library

Usage:
    from websearch import search
    
    results = search(provider="google", links=5, query="python programming")
    
Supported providers: google, yahoo, bing, duckduckgo, brave
"""

from .websearch import search

__version__ = "1.0.0"
__all__ = ["search"]