# SCOPE.md

**Target**
books.toscrape.com (permitted practice sandbox).

**Robots.txt & Permissions**
No restrictions exist for this domain.

**Rate Limit**
1.5 seconds polite delay between requests. Exponential backoff for 429 errors starting at 2 seconds.

**What I Will Not Touch**
Only extracting public catalogue data (title, price, stock). No images or login-walled areas.

**Commercial Context Differences**
Would implement asynchronous scraping (aiohttp), rotating proxies, and direct database injection (PostgreSQL).
