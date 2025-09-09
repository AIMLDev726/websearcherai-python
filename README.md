# WebSearch

A lightweight Python library for searching across multiple search engines including Google, Yahoo, Bing, DuckDuckGo, and Brave. This tool provides a unified interface to retrieve search results programmatically without requiring API keys.

## Features

- **Multi-provider support**: Search across Google, Yahoo, Bing, DuckDuckGo, and Brave
- **Flexible result count**: Specify how many results you want to retrieve
- **Content extraction**: Option to fetch full page content from search results
- **Raw HTML access**: Get the raw HTML response for custom parsing
- **User agent rotation**: Built-in user agent management to avoid blocking
- **Clean result format**: Structured output with title, link, snippet, and description

## Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/AIMLDev726/websearcherai-python
cd websearch
pip install requests beautifulsoup4
```

Optional dependency for enhanced user agent support:
```bash
pip install googlesearch-python
```

## Quick Start

```python
from websearch import search

# Basic search
results = search(provider="google", links=5, query="python programming")

for result in results:
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
    print(f"Snippet: {result['snippet']}")
    print("-" * 50)
```

## Usage Examples

### Search Different Providers

```python
# Google search
google_results = search(provider="google", links=3, query="machine learning")

# Yahoo search
yahoo_results = search(provider="yahoo", links=3, query="web development")

# Bing search
bing_results = search(provider="bing", links=3, query="data science")

# DuckDuckGo search
ddg_results = search(provider="duckduckgo", links=3, query="artificial intelligence")

# Brave search
brave_results = search(provider="brave", links=3, query="cybersecurity")
```

### Get Full Page Content

```python
# Extract full content from search result pages
results = search(
    provider="google", 
    links=2, 
    query="climate change", 
    description_full=True
)

for result in results:
    print(f"Full content preview: {result['description'][:200]}...")
```

### Raw HTML Response

```python
# Get raw HTML for custom parsing
html_content = search(
    provider="bing", 
    query="renewable energy", 
    html_raw=True
)

print(f"HTML length: {len(html_content)} characters")
```

## Function Parameters

The `search()` function accepts the following parameters:

- **provider** (str): Search engine to use
  - Options: "google", "yahoo", "bing", "duckduckgo", "brave"
  - Default: "google"

- **links** (int): Number of search results to return
  - Default: 5

- **query** (str): Search query string
  - Required parameter

- **description_full** (bool): Extract full text content from result pages
  - Default: False
  - Note: Enabling this will make requests slower

- **html_raw** (bool): Return raw HTML response instead of parsed results
  - Default: False

## Return Format

When `html_raw=False` (default), the function returns a list of dictionaries:

```python
[
    {
        "title": "Page Title",
        "link": "https://example.com",
        "snippet": "Short description from search results",
        "description": "Full content if description_full=True, otherwise same as snippet"
    },
    # ... more results
]
```

When `html_raw=True`, returns the raw HTML string from the search engine.

## Error Handling

The library includes built-in error handling:

- Network timeouts (15 seconds for search requests, 10 seconds for content extraction)
- Invalid responses from search engines
- Malformed URLs in search results
- Content extraction failures

If errors occur, the function returns an empty list `[]` instead of raising exceptions.

## Technical Details

### User Agent Management

The library automatically rotates between different user agents to avoid detection:
- Chrome on Windows
- Firefox on Windows  
- Chrome on macOS

### Content Extraction

When `description_full=True`, the library:
1. Fetches the full webpage content
2. Removes script and style tags
3. Extracts text from paragraph and content elements
4. Returns a cleaned text summary

### Search Engine Specifics

Each search provider has custom parsing logic to handle their unique HTML structure:

- **Google**: Handles multiple result container formats and URL decoding
- **Yahoo**: Filters out advertisements and handles redirect URLs
- **Bing**: Parses standard result blocks with title and description
- **DuckDuckGo**: Handles their privacy-focused result format
- **Brave**: Extracts links and attempts to find associated headings

## Limitations

- Results depend on search engine availability and structure changes
- Some search engines may implement rate limiting
- Content extraction success varies by target website structure
- No built-in caching mechanism

## Contributing

Feel free to submit issues and enhancement requests. When contributing code:

1. Follow the existing code style
2. Add appropriate error handling
3. Test with multiple search providers
4. Update documentation as needed

## License

This project is provided as-is for educational and research purposes. Please respect the terms of service of the search engines you query.
