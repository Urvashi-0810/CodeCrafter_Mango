import { useState } from "react";
import { BarChart3, TrendingUp, TrendingDown, Minus, ArrowLeft, ExternalLink, Tag } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { marketInsights, stockTicker, type MarketInsightItem } from "@/data/dummyData";

export default function MarketInsightsPage() {
  const gainers = [...stockTicker].sort((a, b) => b.change - a.change).slice(0, 5);
  const losers = [...stockTicker].sort((a, b) => a.change - b.change).slice(0, 5);
  const [selectedInsight, setSelectedInsight] = useState<MarketInsightItem | null>(null);

  if (selectedInsight) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <TickerBar />
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          <Button variant="ghost" className="mb-4 gap-2" onClick={() => setSelectedInsight(null)}>
            <ArrowLeft className="h-4 w-4" /> Back to Market Insights
          </Button>
          <div className="glass-card p-5">
            <div className="flex items-center gap-2 mb-4">
              <span className={`inline-flex h-6 w-6 items-center justify-center rounded-full ${
                  selectedInsight.sentiment === "positive" ? "bg-primary/20" : selectedInsight.sentiment === "negative" ? "bg-destructive/20" : "bg-warning/20"
                }`}>
                {selectedInsight.sentiment === "positive" ? (
                  <TrendingUp className="h-3 w-3 text-primary" />
                ) : selectedInsight.sentiment === "negative" ? (
                  <TrendingDown className="h-3 w-3 text-destructive" />
                ) : (
                  <Minus className="h-3 w-3 text-warning" />
                )}
              </span>
              <Badge variant="outline" className="text-xs">{selectedInsight.category}</Badge>
              <span className="text-xs text-muted-foreground">{selectedInsight.date}</span>
            </div>
            <h1 className="font-heading text-2xl font-bold leading-tight">{selectedInsight.title}</h1>

            {/* AI Summary */}
            <div className="mt-4 rounded-lg border border-primary/20 bg-primary/5 p-4">
              <span className="text-xs font-medium text-primary">AI Summary</span>
              <p className="mt-1 text-sm text-muted-foreground leading-relaxed">{selectedInsight.summary}</p>
            </div>

            {/* Full Content */}
            <div className="mt-6 prose prose-sm prose-invert max-w-none">
              {selectedInsight.fullContent.split("\n\n").map((para, i) => (
                <p key={i} className="text-sm text-foreground/80 leading-relaxed mb-3">{para}</p>
              ))}
            </div>

            {/* Tags & Source */}
            <div className="mt-6 flex items-center gap-2 flex-wrap border-t border-border/50 pt-4">
              <Tag className="h-3.5 w-3.5 text-muted-foreground" />
              {selectedInsight.tags.map((t) => (
                <Badge key={t} variant="outline" className="text-[10px]">{t}</Badge>
              ))}
              <span className="ml-auto flex items-center gap-1 text-xs text-muted-foreground">
                <ExternalLink className="h-3 w-3" />
                Source: <a href={selectedInsight.sourceUrl} className="text-primary hover:underline">{selectedInsight.source}</a>
              </span>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <TickerBar />

      <div className="w-full max-w-[1600px] mx-auto px-6 lg:px-10 py-6">
        <div className="mb-8">
          <h1 className="font-heading text-3xl font-bold flex items-center gap-2">
            <BarChart3 className="h-8 w-8 text-primary" /> Market Insights
          </h1>
          <p className="mt-1 text-muted-foreground">Quick summaries of what's moving the financial markets today</p>
        </div>

        {/* Indices */}
        <div className="grid gap-4 sm:grid-cols-3 mb-8">
          {[
            { name: "NIFTY 50", value: "23,567.80", change: "+1.2%", up: true },
            { name: "SENSEX", value: "77,845.20", change: "+1.1%", up: true },
            { name: "BANK NIFTY", value: "49,234.50", change: "-0.3%", up: false },
          ].map((idx) => (
            <div key={idx.name} className="glass-card p-4">
              <span className="text-xs text-muted-foreground">{idx.name}</span>
              <div className="flex items-center gap-2 mt-1">
                <span className="font-heading text-xl font-bold">{idx.value}</span>
                <span className={`flex items-center gap-0.5 text-sm font-medium ${idx.up ? "text-primary" : "text-destructive"}`}>
                  {idx.up ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                  {idx.change}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Top Gainers / Losers */}
        <div className="grid gap-6 md:grid-cols-2 mb-8">
          <div className="glass-card p-5">
            <h3 className="font-heading text-base font-semibold flex items-center gap-2 mb-3">
              <TrendingUp className="h-4 w-4 text-primary" /> Top Gainers
            </h3>
            <div className="space-y-2">
              {gainers.map((s) => (
                <div key={s.symbol} className="flex items-center justify-between rounded-lg p-2 hover:bg-accent/30">
                  <span className="text-sm font-medium">{s.symbol}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-sm">₹{s.price.toLocaleString()}</span>
                    <span className="text-sm text-primary font-medium">▲ {s.change.toFixed(1)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="glass-card p-5">
            <h3 className="font-heading text-base font-semibold flex items-center gap-2 mb-3">
              <TrendingDown className="h-4 w-4 text-destructive" /> Top Drops 
            </h3>
            <div className="space-y-2">
              {losers.map((s) => (
                <div key={s.symbol} className="flex items-center justify-between rounded-lg p-2 hover:bg-accent/30">
                  <span className="text-sm font-medium">{s.symbol}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-sm">₹{s.price.toLocaleString()}</span>
                    <span className="text-sm text-destructive font-medium">▼ {Math.abs(s.change).toFixed(1)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Insights Feed - Inshorts style */}
        <h2 className="font-heading text-xl font-bold mb-4">Latest Insights</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {marketInsights.map((item) => (
            <div key={item.id} className="glass-card p-5 cursor-pointer transition-all hover:border-primary/30" onClick={() => setSelectedInsight(item)}>
              <div className="flex items-center gap-2 mb-3">
                <span className={`inline-flex h-6 w-6 items-center justify-center rounded-full ${
                  item.sentiment === "positive" ? "bg-primary/20" : item.sentiment === "negative" ? "bg-destructive/20" : "bg-warning/20"
                }`}>
                  {item.sentiment === "positive" ? (
                    <TrendingUp className="h-3 w-3 text-primary" />
                  ) : item.sentiment === "negative" ? (
                    <TrendingDown className="h-3 w-3 text-destructive" />
                  ) : (
                    <Minus className="h-3 w-3 text-warning" />
                  )}
                </span>
                <Badge variant="secondary" className="text-[10px]">{item.category}</Badge>
                <span className="ml-auto text-xs text-muted-foreground">{item.date}</span>
              </div>
              <h3 className="font-heading text-sm font-semibold leading-snug">{item.title}</h3>
              <p className="mt-2 text-xs text-muted-foreground leading-relaxed">{item.summary}</p>
            </div>
          ))}
        </div>
      </div>

      <Footer />
    </div>
  );
}
