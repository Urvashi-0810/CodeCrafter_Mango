import { useState } from "react";
import { Shield, ExternalLink, AlertTriangle, ChevronRight, ArrowLeft, Tag } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { regulatoryData, type RegulatoryItem } from "@/data/dummyData";

export default function RegulatoryPage() {
  const [selectedItem, setSelectedItem] = useState<RegulatoryItem | null>(null);
  const [filterCategory, setFilterCategory] = useState("all");

  const categories = ["all", ...Array.from(new Set(regulatoryData.map((r) => r.category)))];

  const filtered = filterCategory === "all" ? regulatoryData : regulatoryData.filter((r) => r.category === filterCategory);

  if (selectedItem) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <TickerBar />
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          <Button variant="ghost" className="mb-4 gap-2" onClick={() => setSelectedItem(null)}>
            <ArrowLeft className="h-4 w-4" /> Back to Regulatory Hub
          </Button>
          <div className="glass-card p-5">
            <div className="flex items-center gap-2 mb-4">
              <Badge variant={selectedItem.impact === "high" ? "destructive" : "secondary"} className="text-xs">
                {selectedItem.impact.toUpperCase()} IMPACT
              </Badge>
              <Badge variant="outline" className="text-xs">{selectedItem.category}</Badge>
              <span className="text-xs text-muted-foreground">{selectedItem.date}</span>
            </div>
            <h1 className="font-heading text-2xl font-bold leading-tight">{selectedItem.title}</h1>

            {/* AI Summary */}
            <div className="mt-4 rounded-lg border border-primary/20 bg-primary/5 p-4">
              <span className="text-xs font-medium text-primary">AI Summary</span>
              <p className="mt-1 text-sm text-muted-foreground leading-relaxed">{selectedItem.summary}</p>
            </div>

            {/* Full Content */}
            <div className="mt-6 prose prose-sm prose-invert max-w-none">
              {selectedItem.fullContent.split("\n\n").map((para, i) => (
                <p key={i} className="text-sm text-foreground/80 leading-relaxed mb-3">{para}</p>
              ))}
            </div>

            {/* Tags & Source */}
            <div className="mt-6 flex items-center gap-2 flex-wrap border-t border-border/50 pt-4">
              <Tag className="h-3.5 w-3.5 text-muted-foreground" />
              {selectedItem.tags.map((t) => (
                <Badge key={t} variant="outline" className="text-[10px]">{t}</Badge>
              ))}
              <span className="ml-auto flex items-center gap-1 text-xs text-muted-foreground">
                <ExternalLink className="h-3 w-3" />
                Source: <a href={selectedItem.sourceUrl} className="text-primary hover:underline">{selectedItem.source}</a>
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
            <Shield className="h-8 w-8 text-primary" /> Regulatory Hub
          </h1>
          <p className="mt-1 text-muted-foreground">
            RBI guidelines, SEBI regulations, budget insights, and policy changes — summarized for financial institutions
          </p>
        </div>

        {/* Category Filters */}
        <div className="flex gap-2 mb-6 flex-wrap">
          {categories.map((c) => (
            <Button
              key={c}
              variant={filterCategory === c ? "default" : "outline"}
              size="sm"
              className="text-xs capitalize"
              onClick={() => setFilterCategory(c)}
            >
              {c}
            </Button>
          ))}
        </div>

        {/* Inshorts-style Cards */}
        <div className="grid gap-4 md:grid-cols-2">
          {filtered.map((item) => (
            <div
              key={item.id}
              className="glass-card p-5 cursor-pointer transition-all hover:border-primary/30 group"
              onClick={() => setSelectedItem(item)}
            >
              <div className="flex items-center gap-2 mb-3">
                {item.impact === "high" && <AlertTriangle className="h-3.5 w-3.5 text-warning" />}
                <Badge variant={item.impact === "high" ? "destructive" : "secondary"} className="text-[10px]">
                  {item.impact.toUpperCase()} IMPACT
                </Badge>
                <Badge variant="outline" className="text-[10px]">{item.category}</Badge>
                <span className="ml-auto text-xs text-muted-foreground">{item.date}</span>
              </div>
              <h3 className="font-heading text-sm font-semibold leading-snug">{item.title}</h3>
              <p className="mt-2 text-xs text-muted-foreground leading-relaxed line-clamp-3">{item.summary}</p>
              <div className="mt-3 flex items-center justify-between">
                <div className="flex gap-1.5">
                  {item.tags.slice(0, 3).map((t) => (
                    <Badge key={t} variant="outline" className="text-[9px]">{t}</Badge>
                  ))}
                </div>
                <span className="flex items-center gap-1 text-xs text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                  Read details <ChevronRight className="h-3 w-3" />
                </span>
              </div>
              <div className="mt-2 flex items-center gap-1 text-[10px] text-muted-foreground">
                <ExternalLink className="h-2.5 w-2.5" />
                {item.source}
              </div>
            </div>
          ))}
        </div>
      </div>

      <Footer />
    </div>
  );
}
