import { useState, useEffect } from "react";
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
