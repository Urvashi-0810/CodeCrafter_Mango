import sys

# 1. Refactor Search.tsx
search_path = 'c:/Users/urvas/OneDrive/Desktop/CodeCrafters/CodeCrafter_Mango/sage-fin-compass-main/src/pages/Search.tsx'
with open(search_path, 'r', encoding='utf-8') as f:
    s_content = f.read()

# I will rewrite the entire Search.tsx to be completely clean since I extracted the complex component.
search_code = """import { useState, useEffect } from "react";
import { Search as SearchIcon, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { newsData, companyStocks, type NewsItem } from "@/data/dummyData";
import { useSearchParams } from "react-router-dom";
import CompanyDashboard from "@/components/CompanyDashboard";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<NewsItem[]>([]);
  const [searched, setSearched] = useState(false);
  const [selectedSector, setSelectedSector] = useState("All Sectors");
  const [searchParams] = useSearchParams();

  const sectors = ["All Sectors", "Finance", "Banking", "IT", "FMCG", "Energy", "Healthcare", "Automobile", "Telecom"];

  const executeSearch = (q: string, sector: string) => {
    const qLower = q.toLowerCase();
    const filtered = newsData.filter(
      (n) =>
        n.title.toLowerCase().includes(qLower) ||
        n.summary.toLowerCase().includes(qLower) ||
        n.relatedCompanies.some((c) => c.toLowerCase().includes(qLower)) ||
        n.tags.some((t) => t.toLowerCase().includes(qLower))
    );
    setResults(filtered.length > 0 ? filtered : newsData);
    setSearched(true);
  };

  useEffect(() => {
    const qParam = searchParams.get('q');
    if (qParam && !searched && query === "") {
      setQuery(qParam);
      executeSearch(qParam, selectedSector);
    }
  }, [searchParams, searched, query, selectedSector]);

  useEffect(() => {
    if (query.trim() !== "" || selectedSector !== "All Sectors") {
      executeSearch(query, selectedSector);
    }
  }, [selectedSector]);

  const handleSearch = () => {
    if (!query.trim() && selectedSector === "All Sectors") return;
    executeSearch(query, selectedSector);
  };

  const matchingStocks = searched
    ? companyStocks.filter(
        (s) =>
          (selectedSector === "All Sectors" || s.sector === selectedSector) &&
          (s.symbol.toLowerCase().includes(query.toLowerCase()) ||
          s.name.toLowerCase().includes(query.toLowerCase()) || query.trim() === '')
      )
    : [];

  const mainStock = matchingStocks.length > 0 ? matchingStocks[0] : null;

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <TickerBar />

      <div className="container mx-auto px-4 py-8 flex-1">
        <div className="mb-8">
          <h1 className="font-heading text-3xl font-bold">Financial Search</h1>
          <p className="mt-1 text-muted-foreground">Analyze companies, quarterly reports, and live market sentiments</p>
        </div>

        <div className="flex flex-col md:flex-row gap-3 mb-8 bg-card p-4 rounded-xl border shadow-sm">
          <div className="relative flex-1">
            <SearchIcon className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search company (e.g., Reliance, HDFC)..."
              className="pl-11 bg-background border-border h-12 text-lg shadow-inner"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  executeSearch(query, selectedSector);
                }
              }}
            />
          </div>
          <div className="flex gap-3">
            <select 
              className="h-12 px-4 rounded-md border bg-background text-sm font-medium outline-none focus:ring-2 focus:ring-primary/50"
              value={selectedSector}
              onChange={(e) => setSelectedSector(e.target.value)}
            >
              {sectors.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
            <Button className="h-12 px-8 glow-green text-md" onClick={handleSearch}>
              Analyze
            </Button>
          </div>
        </div>

        {searched && mainStock && (
          <CompanyDashboard 
            mainStock={mainStock} 
            filteredResults={results} 
            matchingStocks={matchingStocks}
            onRelatedCompanyClick={(sym) => { 
               setQuery(sym); 
               executeSearch(sym, selectedSector); 
            }} 
          />
        )}

        {!searched && (
          <div className="flex flex-col items-center justify-center py-24 text-center animate-in fade-in duration-700">
            <div className="relative mb-6">
              <div className="absolute inset-0 rounded-full bg-primary/20 blur-xl animate-pulse"></div>
              <div className="relative flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 border border-primary/20 shadow-lg">
                <SearchIcon className="h-10 w-10 text-primary" />
              </div>
            </div>
            <h2 className="font-heading text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-foreground to-foreground/60">
              Deep-Dive Financial Search
            </h2>
            <p className="mt-3 max-w-lg text-sm text-muted-foreground leading-relaxed">
              Instantly access candlestick charts, official quarterly reports, AI-summarized news, and fundamental metrics for any tracked asset.
            </p>
            <div className="mt-8">
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-4">Trending Searches</p>
              <div className="flex flex-wrap gap-3 justify-center">
                {["Reliance", "TCS", "HDFC", "Infosys", "ITC"].map((s) => (
                  <Button key={s} variant="outline" className="text-xs rounded-full border-border/60 hover:border-primary hover:text-primary transition-all shadow-sm" onClick={() => { setQuery(s); executeSearch(s, selectedSector); }}>
                    <TrendingUp className="h-3 w-3 mr-1.5 text-primary/70" /> {s}
                  </Button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
"""
with open(search_path, 'w', encoding='utf-8') as f:
    f.write(search_code)


# 2. Refactor Watchlist.tsx to drop the mini-dashboard accordion and use CompanyDashboard
watchlist_path = 'c:/Users/urvas/OneDrive/Desktop/CodeCrafters/CodeCrafter_Mango/sage-fin-compass-main/src/pages/Watchlist.tsx'
with open(watchlist_path, 'r', encoding='utf-8') as f:
    w_content = f.read()

w_code = """import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Eye, Trash2, TrendingUp, TrendingDown, Plus, Search, ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { useWatchlist } from "@/hooks/useWatchlist";
import { companyStocks } from "@/data/dummyData";
import CompanyDashboard from "@/components/CompanyDashboard";

export default function WatchlistPage() {
  const navigate = useNavigate();
  const { watchlist, addToWatchlist, removeFromWatchlist } = useWatchlist();
  const [expandedSymbol, setExpandedSymbol] = useState<string | null>(null);
  const [addSearch, setAddSearch] = useState("");
  const [showAdd, setShowAdd] = useState(false);

  const filteredAdd = companyStocks.filter(
    (s) =>
      (s.symbol.toLowerCase().includes(addSearch.toLowerCase()) ||
        s.name.toLowerCase().includes(addSearch.toLowerCase())) &&
      !watchlist.some((w) => w.symbol === s.symbol)
  );

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <TickerBar />

      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="font-heading text-3xl font-bold flex items-center gap-2">
              <Eye className="h-8 w-8 text-primary" /> My Watchlist
            </h1>
            <p className="mt-1 text-muted-foreground">Monitor companies and their latest news, reports & price movements</p>
          </div>
          <Button onClick={() => setShowAdd(!showAdd)} className="gap-2 glow-green">
            <Plus className="h-4 w-4" /> Add Company
          </Button>
        </div>

        {showAdd && (
          <div className="glass-card mb-6 p-4">
            <div className="relative mb-3">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search company to add..."
                className="pl-10 bg-background border-border shadow-inner"
                value={addSearch}
                onChange={(e) => setAddSearch(e.target.value)}
              />
            </div>
            <div className="max-h-48 overflow-y-auto space-y-1">
              {filteredAdd.slice(0, 8).map((s) => (
                <div key={s.symbol} className="flex items-center justify-between rounded-lg p-2 hover:bg-accent/50 cursor-pointer">
                  <div>
                    <span className="font-medium text-sm">{s.symbol}</span>
                    <span className="ml-2 text-xs text-muted-foreground">{s.name}</span>
                    <Badge variant="outline" className="ml-2 text-[10px]">{s.sector}</Badge>
                  </div>
                  <Button size="sm" className="text-xs h-7 hover:bg-primary/20" variant="ghost" onClick={() => { addToWatchlist(s.symbol); setAddSearch(""); }}>
                    <Plus className="h-3 w-3 mr-1" /> Add
                  </Button>
                </div>
              ))}
            </div>
          </div>
        )}

        {watchlist.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center animate-in fade-in duration-500">
            <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
              <Eye className="h-8 w-8 text-primary" />
            </div>
            <h2 className="font-heading text-xl font-semibold">No Companies in Watchlist</h2>
            <p className="mt-2 max-w-md text-sm text-muted-foreground">
              Add companies to your watchlist to monitor their news, financial reports, and price movements.
            </p>
            <Button className="mt-4 gap-2" onClick={() => setShowAdd(true)}>
              <Plus className="h-4 w-4" /> Add Your First Company
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            {watchlist.map((item) => {
              const expanded = expandedSymbol === item.symbol;
              return (
                <div key={item.symbol} className="glass-card overflow-hidden transition-all hover:border-primary/50 shadow-sm animate-in fade-in slide-in-from-bottom-2 duration-300">
                  <div
                    className="flex items-center justify-between p-5 cursor-pointer hover:bg-background/50"
                    onClick={() => setExpandedSymbol(expanded ? null : item.symbol)}
                  >
                    <div className="flex items-center gap-4">
                      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary font-heading text-sm font-bold shadow-inner">
                        {item.symbol.slice(0, 2)}
                      </div>
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-heading font-bold text-lg">{item.symbol}</span>
                          <Badge variant="secondary" className="text-[10px] bg-background border">{item.sector}</Badge>
                        </div>
                        <span className="text-sm text-muted-foreground font-medium">{item.name}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-6">
                      <div className="text-right">
                        <div className="font-heading text-xl font-bold">₹{item.price.toLocaleString()}</div>
                        <div className={`flex items-center justify-end gap-1 text-sm font-medium ${item.changePercent >= 0 ? "text-primary" : "text-destructive"}`}>
                          {item.changePercent >= 0 ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                          {item.changePercent >= 0 ? "+" : ""}{item.changePercent}%
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button variant="ghost" size="icon" className="h-10 w-10 hover:bg-destructive/10 hover:text-destructive transition-colors" onClick={(e) => { e.stopPropagation(); removeFromWatchlist(item.symbol); }}>
                          <Trash2 className="h-4 w-4" />
                        </Button>
                        <div className="ml-2 flex items-center justify-center h-8 w-8 rounded-full bg-accent text-muted-foreground hover:bg-primary/20 hover:text-primary transition-colors">
                            {expanded ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
                        </div>
                      </div>
                    </div>
                  </div>

                  {expanded && (
                    <div className="border-t-2 border-primary/20 bg-background/30 p-4 sm:p-6 lg:p-8 animate-in slide-in-from-top-2 duration-300">
                      <CompanyDashboard 
                        mainStock={item} 
                        filteredResults={item.news} 
                        hideRightColumn={true} 
                        onRelatedCompanyClick={(c) => navigate('/search?q=' + c)} 
                      />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
"""
with open(watchlist_path, 'w', encoding='utf-8') as f:
    f.write(w_code)

print("Linked CompanyDashboard into Search and Watchlist!")
