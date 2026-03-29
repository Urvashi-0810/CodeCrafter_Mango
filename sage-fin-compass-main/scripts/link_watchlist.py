import sys

# 1. Update Watchlist.tsx
watchlist_path = 'c:/Users/urvas/OneDrive/Desktop/CodeCrafters/CodeCrafter_Mango/sage-fin-compass-main/src/pages/Watchlist.tsx'
with open(watchlist_path, 'r', encoding='utf-8') as f:
    w_content = f.read()

if 'from "react-router-dom"' not in w_content:
    w_content = w_content.replace('import { useState } from "react";', 'import { useState } from "react";\nimport { useNavigate } from "react-router-dom";')

if 'const navigate = useNavigate();' not in w_content:
    w_content = w_content.replace('export default function WatchlistPage() {', 'export default function WatchlistPage() {\n  const navigate = useNavigate();')

old_click = 'onClick={() => setExpandedSymbol(expanded ? null : item.symbol)}'
new_click = 'onClick={() => navigate(`/search?q=${item.symbol}`)}'
w_content = w_content.replace(old_click, new_click)

# Optional: remove the whole expanded block or leave it. Leaving it is fine because it will never trigger.
# But just in case, it's safer to leave to avoid regex errors.

with open(watchlist_path, 'w', encoding='utf-8') as f:
    f.write(w_content)

# 2. Update Search.tsx
search_path = 'c:/Users/urvas/OneDrive/Desktop/CodeCrafters/CodeCrafter_Mango/sage-fin-compass-main/src/pages/Search.tsx'
with open(search_path, 'r', encoding='utf-8') as f:
    s_content = f.read()

if 'useSearchParams' not in s_content:
    s_content = s_content.replace('import { useState, useMemo, useEffect } from "react";', 'import { useState, useMemo, useEffect } from "react";\nimport { useSearchParams } from "react-router-dom";')

auto_search_code = '''
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const qParam = searchParams.get('q');
    if (qParam && !searched && query === "") {
      setQuery(qParam);
      const qLower = qParam.toLowerCase();
      const filtered = newsData.filter(
        (n) =>
          n.title.toLowerCase().includes(qLower) ||
          n.summary.toLowerCase().includes(qLower) ||
          n.relatedCompanies.some((c) => c.toLowerCase().includes(qLower)) ||
          n.tags.some((t) => t.toLowerCase().includes(qLower))
      );
      setResults(filtered.length > 0 ? filtered : newsData);
      setSearched(true);
    }
  }, [searchParams, searched, query]);
'''

if 'const [searchParams] = useSearchParams();' not in s_content:
    s_content = s_content.replace('const categories = ["all"', auto_search_code + '\n  const categories = ["all"')

with open(search_path, 'w', encoding='utf-8') as f:
    f.write(s_content)

print("Linked Watchlist to Search successfully!")
