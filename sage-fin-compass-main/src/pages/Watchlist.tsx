import { useState } from "react";
import { Eye, Trash2, TrendingUp, TrendingDown, ExternalLink, Plus, Search, ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { useWatchlist } from "@/hooks/useWatchlist";
import { companyStocks } from "@/data/dummyData";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const priceHistory = [
  { t: "9:15", p: 100 }, { t: "10:00", p: 101.2 }, { t: "10:30", p: 100.8 },
  { t: "11:00", p: 102.5 }, { t: "11:30", p: 101.9 }, { t: "12:00", p: 103.1 },
  { t: "12:30", p: 102.4 }, { t: "13:00", p: 103.8 }, { t: "13:30", p: 104.2 },
  { t: "14:00", p: 103.5 }, { t: "14:30", p: 104.8 }, { t: "15:00", p: 105.1 },
  { t: "15:30", p: 104.6 },
];

export default function WatchlistPage() {
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

        {/* Add Company */}
        {showAdd && (
          <div className="glass-card mb-6 p-4">
            <div className="relative mb-3">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search company to add..."
                className="pl-10 bg-background"
                value={addSearch}
                onChange={(e) => setAddSearch(e.target.value)}
              />
            </div>
            <div className="max-h-48 overflow-y-auto space-y-1">
              {filteredAdd.slice(0, 8).map((s) => (
                <div key={s.symbol} className="flex items-center justify-between rounded-lg p-2 hover:bg-accent/50">
                  <div>
                    <span className="font-medium text-sm">{s.symbol}</span>
                    <span className="ml-2 text-xs text-muted-foreground">{s.name}</span>
                    <Badge variant="outline" className="ml-2 text-[10px]">{s.sector}</Badge>
                  </div>
                  <Button size="sm" className="text-xs h-7" onClick={() => { addToWatchlist(s.symbol); setAddSearch(""); }}>
                    <Plus className="h-3 w-3 mr-1" /> Add
                  </Button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Watchlist */}
        {watchlist.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
              <Eye className="h-8 w-8 text-primary" />
            </div>
            <h2 className="font-heading text-xl font-semibold">No Companies in Watchlist</h2>
            <p className="mt-2 max-w-md text-sm text-muted-foreground">
              Add companies to your watchlist to monitor their news, financial reports, and price movements. Your watchlist persists across sessions.
            </p>
            <Button className="mt-4 gap-2" onClick={() => setShowAdd(true)}>
              <Plus className="h-4 w-4" /> Add Your First Company
            </Button>
          </div>
        ) : (
          <div className="space-y-3">
            {watchlist.map((item) => {
              const expanded = expandedSymbol === item.symbol;
              return (
                <div key={item.symbol} className="glass-card overflow-hidden transition-all hover:border-primary/30">
                  <div
                    className="flex items-center justify-between p-4 cursor-pointer"
                    onClick={() => setExpandedSymbol(expanded ? null : item.symbol)}
                  >
                    <div className="flex items-center gap-4">
                      <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent font-heading text-xs font-bold">
                        {item.symbol.slice(0, 2)}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-heading font-semibold">{item.symbol}</span>
                          <Badge variant="outline" className="text-[10px]">{item.sector}</Badge>
                        </div>
                        <span className="text-xs text-muted-foreground">{item.name}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <div className="font-heading text-lg font-bold">₹{item.price.toLocaleString()}</div>
                        <div className={`flex items-center gap-1 text-xs ${item.changePercent >= 0 ? "text-primary" : "text-destructive"}`}>
                          {item.changePercent >= 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                          {item.changePercent >= 0 ? "+" : ""}{item.changePercent}%
                        </div>
                      </div>
                      <div className="flex gap-1">
                        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={(e) => { e.stopPropagation(); removeFromWatchlist(item.symbol); }}>
                          <Trash2 className="h-4 w-4 text-destructive" />
                        </Button>
                        {expanded ? <ChevronUp className="h-4 w-4 text-muted-foreground mt-2" /> : <ChevronDown className="h-4 w-4 text-muted-foreground mt-2" />}
                      </div>
                    </div>
                  </div>

                  {expanded && (
                    <div className="border-t border-border/50 p-4 space-y-4">
                      {/* Mini Chart */}
                      <div className="glass-card p-4">
                        <h4 className="text-xs font-medium text-muted-foreground mb-2">Intraday Price Movement</h4>
                        <ResponsiveContainer width="100%" height={120}>
                          <LineChart data={priceHistory.map(d => ({ ...d, p: d.p * (item.price / 100) }))}>
                            <XAxis dataKey="t" tick={{ fontSize: 10 }} stroke="hsl(var(--muted-foreground))" />
                            <YAxis hide domain={["auto", "auto"]} />
                            <Tooltip
                              contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 8, fontSize: 12 }}
                              formatter={(v: number) => [`₹${v.toFixed(2)}`, "Price"]}
                            />
                            <Line type="monotone" dataKey="p" stroke="hsl(var(--primary))" strokeWidth={2} dot={false} />
                          </LineChart>
                        </ResponsiveContainer>
                      </div>

                      {/* News */}
                      <div>
                        <h4 className="text-sm font-semibold mb-2">Latest News & Reports</h4>
                        {item.news.length > 0 ? (
                          <div className="space-y-3">
                            {item.news.map((n) => (
                              <div key={n.id} className="rounded-lg border border-border/30 bg-background/50 p-3">
                                <div className="flex items-center gap-2 mb-1">
                                  <span className={`h-1.5 w-1.5 rounded-full ${n.sentiment === "positive" ? "bg-primary" : n.sentiment === "negative" ? "bg-destructive" : "bg-warning"}`} />
                                  <Badge variant="secondary" className="text-[10px]">{n.category}</Badge>
                                  <span className="text-[10px] text-muted-foreground">{n.date}</span>
                                </div>
                                <h5 className="text-sm font-medium">{n.title}</h5>
                                <div className="mt-2 rounded border border-primary/20 bg-primary/5 p-2">
                                  <span className="text-[10px] font-medium text-primary">AI Summary</span>
                                  <p className="text-xs text-muted-foreground mt-0.5">{n.summary}</p>
                                </div>
                                <div className="mt-2 flex items-center gap-1 text-[10px] text-muted-foreground">
                                  <ExternalLink className="h-2.5 w-2.5" />
                                  Source: <span className="text-primary">{n.source}</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-xs text-muted-foreground">No recent news found for this company.</p>
                        )}
                      </div>
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
