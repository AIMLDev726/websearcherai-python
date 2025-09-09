from websearch import search

# Basic usage
results = search(provider="google", links=3, query="python programming")
print(f"Found {len(results)} results")

for result in results:
    print(result['title'])
    print(result['link'])
    print()

# Different provider
yahoo_results = search(provider="yahoo", links=2, query="machine learning")
print(f"Yahoo found {len(yahoo_results)} results")

# Get full description
full_desc = search(provider="bing", links=1, query="web development", description_full=True)
if full_desc:
    desc = full_desc[0]['description'].encode('ascii', 'ignore').decode('ascii')
    print(f"Description: {desc[:100]}...")

# Get raw HTML
html = search(provider="duckduckgo", query="data science", html_raw=True)
print(f"HTML length: {len(html)}")

# Test multiple providers
query = "artificial intelligence"
for provider in ["google", "yahoo", "bing"]:
    results = search(provider=provider, links=1, query=query)
    if results:
        title = results[0]['title'].encode('ascii', 'ignore').decode('ascii')
    print(f"{provider}: {title}")