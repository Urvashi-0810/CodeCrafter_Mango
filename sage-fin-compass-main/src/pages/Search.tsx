import { useState } from "react";
import { Search as SearchIcon, ExternalLink, TrendingUp, TrendingDown, Minus, Plus, BookmarkPlus, Filter } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { newsData, companyStocks, type NewsItem } from "@/data/dummyData";
import { useWatchlist } from "@/hooks/useWatchlist";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<NewsItem[]>([]);
  const [searched, setSearched] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const { addToWatchlist, isInWatchlist } = useWatchlist();

  const categories = ["all", "Earnings", "Deals", "Banking", "Energy", "Automobile"];

  const handleSearch = () => {
    if (!query.trim()) return;
    const q = query.toLowerCase();
    const filtered = newsData.filter(
      (n) =>
        n.title.toLowerCase().includes(q) ||
        n.summary.toLowerCase().includes(q) ||
        n.relatedCompanies.some((c) => c.toLowerCase().includes(q)) ||
        n.tags.some((t) => t.toLowerCase().includes(q))
    );
    setResults(filtered.length > 0 ? filtered : newsData);
    setSearched(true);
  };

  const filteredResults = selectedCategory === "all" ? results : results.filter((r) => r.category === selectedCategory);

  const matchingStocks = searched
    ? companyStocks.filter(
        (s) =>
          s.symbol.toLowerCase().includes(query.toLowerCase()) ||
          s.name.toLowerCase().includes(query.toLowerCase())
      )
    : [];

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <TickerBar />

      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="font-heading text-3xl font-bold">Financial Search</h1>
          <p className="mt-1 text-muted-foreground">Search for company reports, news, and financial data from across the web</p>
        </div>

        {/* Search Bar */}
        <div className="flex gap-3 mb-6">
          <div className="relative flex-1">
            <SearchIcon className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search company name, ticker, or topic (e.g., Reliance, TCS, banking)"
              className="pl-10 bg-card border-border/50 h-12"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />
          </div>
          <Button className="h-12 px-8 glow-green" onClick={handleSearch}>
            <SearchIcon className="h-4 w-4 mr-2" /> Search
          </Button>
        </div>

        {searched && (
          <>
            {/* Matching Stocks */}
            {matchingStocks.length > 0 && (
              <div className="mb-6">
                <h2 className="font-heading text-lg font-semibold mb-3">Matching Companies</h2>
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {matchingStocks.map((s) => (
                    <div key={s.symbol} className="glass-card p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div>
                          <span className="font-heading text-sm font-bold">{s.symbol}</span>
                          <span className="ml-2 text-xs text-muted-foreground">{s.name}</span>
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-7 text-xs"
                          onClick={() => addToWatchlist(s.symbol)}
                          disabled={isInWatchlist(s.symbol)}
                        >
                          {isInWatchlist(s.symbol) ? "In Watchlist" : (
                            <><BookmarkPlus className="h-3 w-3 mr-1" /> Watch</>
                          )}
                        </Button>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-lg font-bold">₹{s.price.toLocaleString()}</span>
                        <span className={`flex items-center gap-0.5 text-sm ${s.changePercent >= 0 ? "text-primary" : "text-destructive"}`}>
                          {s.changePercent >= 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                          {s.changePercent >= 0 ? "+" : ""}{s.changePercent}%
                        </span>
                      </div>
                      <div className="mt-2 flex gap-2 text-xs text-muted-foreground">
                        <span>MCap: {s.marketCap}</span>
                        <span>PE: {s.pe}</span>
                        <span>Vol: {s.volume}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Category Filters */}
            <div className="flex items-center gap-2 mb-4 flex-wrap">
              <Filter className="h-4 w-4 text-muted-foreground" />
              {categories.map((c) => (
                <Button
                  key={c}
                  variant={selectedCategory === c ? "default" : "outline"}
                  size="sm"
                  className="text-xs capitalize"
                  onClick={() => setSelectedCategory(c)}
                >
                  {c}
                </Button>
              ))}
            </div>

            {/* Results */}
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">{filteredResults.length} results found</p>
              {filteredResults.map((item) => (
                <div key={item.id} className="glass-card p-5 transition-all hover:border-primary/30">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className={`inline-block h-2 w-2 rounded-full ${
                          item.sentiment === "positive" ? "bg-primary" : item.sentiment === "negative" ? "bg-destructive" : "bg-warning"
                        }`} />
                        <Badge variant="secondary" className="text-[10px]">{item.category}</Badge>
                        <span className="text-xs text-muted-foreground">{item.date}</span>
                      </div>
                      <h3 className="font-heading text-base font-semibold leading-snug">{item.title}</h3>
                      
                      {/* AI Summary */}
                      <div className="mt-3 rounded-lg border border-primary/20 bg-primary/5 p-3">
                        <div className="flex items-center gap-1 mb-1">
                          <span className="text-[10px] font-medium text-primary">AI Summary</span>
                        </div>
                        <p className="text-sm text-muted-foreground leading-relaxed">{item.summary}</p>
                      </div>

                      {/* Expanded Detail */}
                      {expandedId === item.id && (
                        <div className="mt-3 p-3 rounded-lg bg-card border border-border/50">
                          <p className="text-sm text-foreground/80 leading-relaxed whitespace-pre-line">{item.fullContent}</p>
                        </div>
                      )}

                      {/* Tags & Source */}
                      <div className="mt-3 flex items-center gap-2 flex-wrap">
                        {item.tags.map((t) => (
                          <Badge key={t} variant="outline" className="text-[10px]">{t}</Badge>
                        ))}
                        <span className="ml-auto flex items-center gap-1 text-xs text-muted-foreground">
                          <ExternalLink className="h-3 w-3" />
                          Source: <a href={item.sourceUrl} className="text-primary hover:underline">{item.source}</a>
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="mt-3 flex gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-xs"
                      onClick={() => setExpandedId(expandedId === item.id ? null : item.id)}
                    >
                      {expandedId === item.id ? (
                        <><Minus className="h-3 w-3 mr-1" /> Less</>
                      ) : (
                        <><Plus className="h-3 w-3 mr-1" /> Read Full</>
                      )}
                    </Button>
                    {item.relatedCompanies.map((c) => (
                      <Button
                        key={c}
                        variant="outline"
                        size="sm"
                        className="text-xs"
                        onClick={() => addToWatchlist(c)}
                        disabled={isInWatchlist(c)}
                      >
                        <BookmarkPlus className="h-3 w-3 mr-1" />
                        {isInWatchlist(c) ? `${c} in Watchlist` : `Add ${c} to Watchlist`}
                      </Button>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {!searched && (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
              <SearchIcon className="h-8 w-8 text-primary" />
            </div>
            <h2 className="font-heading text-xl font-semibold">Search Financial Data</h2>
            <p className="mt-2 max-w-md text-sm text-muted-foreground">
              Enter a company name, ticker symbol, or topic to find financial reports, news, and insights scraped from across the web.
            </p>
            <div className="mt-4 flex flex-wrap gap-2 justify-center">
              {["Reliance", "TCS", "Banking", "HDFC", "Infosys"].map((s) => (
                <Button key={s} variant="outline" size="sm" className="text-xs" onClick={() => { setQuery(s); }}>
                  {s}
                </Button>
              ))}
            </div>
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
