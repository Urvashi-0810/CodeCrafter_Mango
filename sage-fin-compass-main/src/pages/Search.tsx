import { useState, useMemo, useEffect } from "react";
import { Search as SearchIcon, ExternalLink, TrendingUp, TrendingDown, Minus, Plus, BookmarkPlus, Filter, FileText, Download, BarChart3, Clock, X, CheckCircle, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { newsData, companyStocks, type NewsItem } from "@/data/dummyData";
import { toast } from "sonner";
import { useWatchlist } from "@/hooks/useWatchlist";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip, BarChart, Bar, Cell } from "recharts";

const generateCandlestickData = (basePrice: number) => {
  let currentPrice = basePrice * 0.8; // Start 20% lower to show growth
  return Array.from({ length: 30 }).map((_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (30 - i));
    
    const open = currentPrice;
    const volatility = basePrice * 0.04;
    const close = currentPrice + (Math.random() - 0.45) * volatility;
    const high = Math.max(open, close) + Math.random() * (volatility * 0.5);
    const low = Math.min(open, close) - Math.random() * (volatility * 0.5);
    
    currentPrice = close;
    
    return {
      date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      open: parseFloat(open.toFixed(2)),
      close: parseFloat(close.toFixed(2)),
      high: parseFloat(high.toFixed(2)),
      low: parseFloat(low.toFixed(2)),
      price: parseFloat(close.toFixed(2)), // For Area chart fallback
      isGreen: close >= open
    };
  });
};

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="glass-card p-3 shadow-xl border-border/50 text-xs">
        <p className="font-bold mb-2 border-b pb-1">{label}</p>
        <div className="grid grid-cols-2 gap-x-4 gap-y-1">
          <span className="text-muted-foreground">Open:</span>
          <span className="font-medium text-right">₹{data.open}</span>
          <span className="text-muted-foreground">Close:</span>
          <span className={`font-medium text-right ${data.isGreen ? 'text-primary' : 'text-destructive'}`}>₹{data.close}</span>
          <span className="text-muted-foreground">High:</span>
          <span className="font-medium text-right">₹{data.high}</span>
          <span className="text-muted-foreground">Low:</span>
          <span className="font-medium text-right">₹{data.low}</span>
        </div>
      </div>
    );
  }
  return null;
};

// Custom shape for candlestick
const Candlestick = (props: any) => {
  const { x, y, width, height, low, high, open, close } = props;
  const isGrowing = close >= open;
  const color = isGrowing ? '#16a34a' : '#dc2626';
  
  // Calculate relative positions (since Recharts Bar gives us y and height based on the [min(open,close), max(open,close)] range)
  const ratio = height / Math.max(Math.abs(open - close), 0.001);
  const yTop = y;
  const yBottom = y + height;
  
  const yHigh = y - (high - Math.max(open, close)) * ratio;
  const yLow = yBottom + (Math.min(open, close) - low) * ratio;

  return (
    <g>
      <line x1={x + width / 2} y1={yHigh} x2={x + width / 2} y2={yLow} stroke={color} strokeWidth={2} />
      <rect x={x} y={yTop} width={width} height={height} fill={color} stroke={color} rx={2} />
    </g>
  );
};


export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<NewsItem[]>([]);
  const [searched, setSearched] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedSector, setSelectedSector] = useState("All Sectors");
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [selectedNews, setSelectedNews] = useState<NewsItem | null>(null);

  const handleDownloadReport = (type: string, quarter: string, symbol: string) => {
    const html = `<html><head><title>${symbol} ${quarter} ${type}</title><style>body{font-family:'Segoe UI',system-ui,sans-serif;max-width:800px;margin:40px auto;line-height:1.6;color:#333}h1{color:#16a34a;border-bottom:2px solid #16a34a;padding-bottom:10px}table{width:100%;border-collapse:collapse;margin:20px 0}th,td{border:1px solid #ddd;padding:12px;text-align:left}th{background:#f8faff;color:#16a34a}.footer{margin-top:50px;font-size:12px;color:#888;text-align:center}</style></head><body><h1>${symbol} Corporation</h1><h2>${quarter} ${type}</h2><p>This document serves as the official financial disclosure for ${symbol} for the period of ${quarter}.</p><h3>Financial Highlights</h3><table><tr><th>Metric</th><th>Value (in Cr)</th><th>YoY Growth</th></tr><tr><td>Revenue</td><td>₹12,450</td><td style="color:green">+14.2%</td></tr><tr><td>EBITDA</td><td>₹3,120</td><td style="color:green">+18.5%</td></tr><tr><td>Net Profit</td><td>₹1,890</td><td style="color:green">+12.1%</td></tr></table><h3>Management Discussion</h3><p>The company has demonstrated resilient growth across all core segments despite macroeconomic headwinds. Strong execution in the digital transformation pipeline yielded unprecedented margins in the current quarter.</p><div class="footer">CONFIDENTIAL - Generated by Sage FinCompass AI System</div></body></html>`;
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${symbol}_${quarter}_${type.replace(/ /g, '_')}.html`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success(`Successfully downloaded ${quarter} ${type}`);
  };

  const handleAddToWatchlist = (symbol: string) => {
    addToWatchlist(symbol);
    toast.success(`${symbol} has been securely tracked in your Watchlist!`);
  };

  const { addToWatchlist, isInWatchlist } = useWatchlist();

  
  useEffect(() => {
    if (query.trim() !== "" || selectedSector !== "All Sectors") {
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
    }
  }, [selectedSector]);

  const categories = ["all", "Earnings", "Deals", "Banking", "Energy", "Automobile"];
  const sectors = ["All Sectors", "Finance", "Banking", "IT", "FMCG", "Energy", "Healthcare"];

  const handleSearch = () => {
    if (!query.trim() && selectedSector === "All Sectors") return;
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
          (selectedSector === "All Sectors" || s.sector === selectedSector) &&
          (s.symbol.toLowerCase().includes(query.toLowerCase()) ||
          s.name.toLowerCase().includes(query.toLowerCase()) || query.trim() === '')
      )
    : [];

  const mainStock = matchingStocks.length > 0 ? matchingStocks[0] : null;
  const candleData = useMemo(() => mainStock ? generateCandlestickData(mainStock.price) : [], [mainStock]);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <TickerBar />

      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="font-heading text-3xl font-bold">Financial Search</h1>
          <p className="mt-1 text-muted-foreground">Analyze companies, quarterly reports, and live market sentiments</p>
        </div>

        {/* Enhanced Search Bar with Filters */}
        <div className="flex flex-col md:flex-row gap-3 mb-8 bg-card p-4 rounded-xl border shadow-sm">
          <div className="relative flex-1">
            <SearchIcon className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search company (e.g., Reliance, HDFC)..."
              className="pl-11 bg-background border-border h-12 text-lg shadow-inner"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
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
          <div className="grid gap-8 lg:grid-cols-3 animate-in fade-in slide-in-from-bottom-4 duration-500">
            
            {/* Left Column: Chart, Reports, News */}
            <div className="lg:col-span-2 space-y-8">
              
              {/* Main Company Header & Chart */}
              <div className="glass-card p-6 border-t-4 border-t-primary">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <div className="flex items-center gap-3 mb-1">
                      <h2 className="font-heading text-3xl font-bold">{mainStock.name}</h2>
                      <Badge variant="secondary" className="text-xs bg-primary/10 text-primary">{mainStock.symbol}</Badge>
                    </div>
                    <p className="text-muted-foreground">{mainStock.sector} Sector • NSE</p>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-bold">₹{mainStock.price.toLocaleString()}</div>
                    <div className={`flex items-center justify-end gap-1 font-medium ${mainStock.changePercent >= 0 ? "text-primary" : "text-destructive"}`}>
                      {mainStock.changePercent >= 0 ? <TrendingUp className="h-5 w-5" /> : <TrendingDown className="h-5 w-5" />}
                      {mainStock.changePercent >= 0 ? "+" : ""}{mainStock.changePercent}%
                    </div>
                  </div>
                </div>

                <h3 className="text-sm font-semibold mb-4 text-muted-foreground flex items-center gap-2"><BarChart3 className="h-4 w-4"/> 30-Day Price Action (Candlestick)</h3>
                <div className="h-[300px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={candleData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" opacity={0.2} vertical={false} />
                      <XAxis dataKey="date" tick={{fontSize: 10}} tickMargin={10} minTickGap={15} />
                      <YAxis domain={['dataMin - 100', 'dataMax + 100']} tick={{fontSize: 10}} width={60} tickFormatter={(v) => `₹${v}`} />
                      <Tooltip content={<CustomTooltip />} cursor={{fill: 'var(--primary)', opacity: 0.05}} />
                      <Bar 
                        dataKey={(data) => [Math.min(data.open, data.close), Math.max(data.open, data.close)]} 
                        shape={(props) => <Candlestick {...props} {...props.payload} />}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Quarterly Reports Section */}
              <div className="glass-card p-6">
                <h3 className="font-heading text-xl font-bold mb-4 flex items-center gap-2">
                  <FileText className="h-5 w-5 text-primary" /> Investor Relations & Quarterly Reports
                </h3>
                <div className="grid sm:grid-cols-2 gap-4">
                  {[
                    { quarter: "Q3 FY24", date: "Jan 15, 2024", type: "Earnings Presentation", size: "4.2 MB" },
                    { quarter: "Q3 FY24", date: "Jan 15, 2024", type: "Financial Results", size: "1.8 MB" },
                    { quarter: "Q2 FY24", date: "Oct 12, 2023", type: "Earnings Presentation", size: "3.9 MB" },
                    { quarter: "FY23", date: "May 20, 2023", type: "Annual Report", size: "12.5 MB" }
                  ].map((report, i) => (
                    <div key={i} className="flex items-center justify-between p-4 rounded-xl border bg-background/50 hover:bg-card hover:shadow-sm transition-all group">
                      <div className="flex gap-3 items-center">
                        <div className="h-10 w-10 flex items-center justify-center bg-red-50 text-red-600 rounded-lg dark:bg-red-900/20 dark:text-red-400">
                          <FileText className="h-5 w-5" />
                        </div>
                        <div>
                          <p className="font-semibold text-sm">{report.quarter} {report.type}</p>
                          <p className="text-xs text-muted-foreground flex items-center gap-2 mt-0.5">
                            <Clock className="h-3 w-3" /> {report.date} • PDF • {report.size}
                          </p>
                        </div>
                      </div>
                      <Button onClick={() => handleDownloadReport(report.type, report.quarter, mainStock.symbol)} variant="ghost" size="icon" className="group-hover:text-primary group-hover:bg-primary/10 transition-colors">
                        <Download className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Related News */}
              <div>
                <h3 className="font-heading text-xl font-bold mb-4 flex items-center gap-2">
                  <span className="relative flex h-3 w-3 mr-1">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
                  </span>
                  Latest News on {mainStock.name}
                </h3>
                <div className="space-y-4">
                  {filteredResults.slice(0, 3).map((item) => (
                    <div key={item.id} onClick={() => setSelectedNews(item)} className="cursor-pointer glass-card p-5 shadow-sm transition-all hover:shadow-md hover:border-primary/50">
                      <div className="flex items-center gap-2 mb-2">
                        <span className={`inline-block h-2 w-2 rounded-full ${
                          item.sentiment === "positive" ? "bg-primary" : item.sentiment === "negative" ? "bg-destructive" : "bg-warning"
                        }`} />
                        <Badge variant="secondary" className="text-[10px]">{item.category}</Badge>
                        <span className="text-xs text-muted-foreground">{item.date}</span>
                      </div>
                      <h4 className="font-heading text-md font-bold leading-snug mb-2">{item.title}</h4>
                      <p className="text-sm text-muted-foreground leading-relaxed">{item.summary}</p>
                      <div className="mt-4 flex items-center justify-between">
                        <div className="flex gap-2">
                          {item.tags.map((t) => (
                            <Badge key={t} variant="outline" className="text-[10px] opacity-70">{t}</Badge>
                          ))}
                        </div>
                        <a href={item.sourceUrl} className="text-xs text-primary font-medium hover:underline flex items-center gap-1">
                          Read on {item.source} <ExternalLink className="h-3 w-3" />
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>

            {/* Right Column: Stats & Other companies */}
            <div className="space-y-6">
              <div className="glass-card p-6">
                <Button 
                  className={`w-full mb-6 h-12 text-md font-bold shadow-md transition-all ${isInWatchlist(mainStock.symbol) ? 'bg-secondary text-foreground hover:bg-secondary/80' : 'glow-green'}`}
                  onClick={() => handleAddToWatchlist(mainStock.symbol)}
                  variant={isInWatchlist(mainStock.symbol) ? 'outline' : 'default'}
                >
                  {isInWatchlist(mainStock.symbol) ? (
                    <><CheckCircle className="mr-2 h-5 w-5 text-primary" /> Tracked in Watchlist</>
                  ) : (
                    <><BookmarkPlus className="mr-2 h-5 w-5" /> Add to Watchlist</>
                  )}
                </Button>

                <h4 className="font-bold text-sm uppercase tracking-wider text-muted-foreground mb-4 border-b pb-2">Company Overview</h4>
                <div className="space-y-4">
                  <div className="flex justify-between items-center bg-background/50 p-3 rounded-lg border">
                    <span className="text-sm text-muted-foreground">Market Cap</span>
                    <span className="font-bold">{mainStock.marketCap}</span>
                  </div>
                  <div className="flex justify-between items-center bg-background/50 p-3 rounded-lg border">
                    <span className="text-sm text-muted-foreground">P/E Ratio</span>
                    <span className="font-bold">{mainStock.pe}</span>
                  </div>
                  <div className="flex justify-between items-center bg-background/50 p-3 rounded-lg border">
                    <span className="text-sm text-muted-foreground">Volume</span>
                    <span className="font-bold">{mainStock.volume}</span>
                  </div>
                  <div className="flex justify-between items-center bg-background/50 p-3 rounded-lg border">
                    <span className="text-sm text-muted-foreground">52W High</span>
                    <span className="font-bold text-primary">₹{(mainStock.price * 1.15).toFixed(0)}</span>
                  </div>
                  <div className="flex justify-between items-center bg-background/50 p-3 rounded-lg border">
                    <span className="text-sm text-muted-foreground">52W Low</span>
                    <span className="font-bold text-destructive">₹{(mainStock.price * 0.82).toFixed(0)}</span>
                  </div>
                </div>
              </div>

              {matchingStocks.length > 1 && (
                <div className="glass-card p-6">
                  <h4 className="font-bold text-sm uppercase tracking-wider text-muted-foreground mb-4 border-b pb-2">Other Matches</h4>
                  <div className="space-y-3">
                    {matchingStocks.slice(1, 5).map(s => (
                      <div key={s.symbol} className="flex justify-between items-center p-3 hover:bg-background/80 rounded-lg cursor-pointer transition-colors border border-transparent hover:border-border" onClick={() => setQuery(s.symbol)}>
                        <div>
                          <p className="font-bold text-sm">{s.symbol}</p>
                          <p className="text-xs text-muted-foreground">{s.sector}</p>
                        </div>
                        <div className="text-right">
                          <p className="font-bold text-sm">₹{s.price}</p>
                          <p className={`text-xs ${s.changePercent >= 0 ? "text-primary" : "text-destructive"}`}>
                            {s.changePercent >= 0 ? "+" : ""}{s.changePercent}%
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
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
                  <Button key={s} variant="outline" className="text-xs rounded-full border-border/60 hover:border-primary hover:text-primary transition-all shadow-sm" onClick={() => { setQuery(s); handleSearch(); }}>
                    <TrendingUp className="h-3 w-3 mr-1.5 text-primary/70" /> {s}
                  </Button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      
      {selectedNews && (
        <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm animate-in fade-in flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
          <div className="glass-card w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-2xl relative animate-in zoom-in-95 duration-200 border-primary/20">
            <Button
              variant="ghost"
              size="icon"
              className="absolute right-4 top-4 rounded-full bg-background/50 hover:bg-destructive hover:text-destructive-foreground z-10"
              onClick={() => setSelectedNews(null)}
            >
              <X className="h-5 w-5" />
            </Button>
            
            <div className="p-8 sm:p-12">
              <div className="flex items-center gap-3 mb-6 flex-wrap">
                <Badge className="bg-primary/10 text-primary hover:bg-primary/20 border-none">{selectedNews.category}</Badge>
                <div className="flex items-center gap-2 text-sm text-muted-foreground font-medium">
                  <Clock className="h-4 w-4" />
                  {selectedNews.date}
                </div>
                <div className="flex items-center gap-2 ml-auto">
                  <span className={`inline-block h-2.5 w-2.5 rounded-full ${
                    selectedNews.sentiment === "positive" ? "bg-primary" : selectedNews.sentiment === "negative" ? "bg-destructive" : "bg-warning"
                  } shadow-sm`} />
                  <span className="text-sm font-semibold capitalize text-muted-foreground">
                    {selectedNews.sentiment} Sentiment
                  </span>
                </div>
              </div>

              <h2 className="font-heading text-3xl sm:text-4xl font-bold leading-tight mb-8">
                {selectedNews.title}
              </h2>

              <div className="bg-primary/5 border border-primary/20 rounded-xl p-6 mb-10 shadow-sm relative overflow-hidden">
                <div className="absolute top-0 left-0 w-1.5 h-full bg-primary" />
                <h3 className="text-sm font-bold text-primary flex items-center gap-2 mb-3 tracking-wide uppercase">
                  <Sparkles className="h-4 w-4" /> AI Generated Summary
                </h3>
                <p className="text-foreground/90 leading-relaxed font-medium">
                  {selectedNews.summary}
                </p>
              </div>

              <div className="prose prose-slate dark:prose-invert max-w-none">
                <p className="text-lg leading-relaxed text-slate-700 dark:text-slate-300 font-serif whitespace-pre-line">
                  {selectedNews.fullContent || "Extensive market analysis and comprehensive breakdown of the core strategic components associated with this development."}
                </p>
              </div>
              
              <div className="mt-12 pt-8 border-t border-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
                <div className="space-y-2">
                  <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">Related Assets</p>
                  <div className="flex flex-wrap gap-2">
                    {selectedNews.relatedCompanies.map(c => (
                      <Badge key={c} variant="outline" className="cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors" onClick={() => { setSelectedNews(null); setQuery(c); handleSearch(); }}>
                        {c}
                      </Badge>
                    ))}
                  </div>
                </div>
                <Button variant="outline" className="gap-2 shrink-0 shadow-sm font-semibold" onClick={() => window.open(selectedNews.sourceUrl, '_blank')}>
                  Read source on {selectedNews.source} <ExternalLink className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
}
