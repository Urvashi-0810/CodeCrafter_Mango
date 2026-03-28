import { stockTicker } from "@/data/dummyData";

export default function TickerBar() {
  const items = [...stockTicker, ...stockTicker];
  return (
    <div className="overflow-hidden border-b border-border/30 bg-card/50 py-2">
      <div className="stock-ticker flex whitespace-nowrap">
        {items.map((s, i) => (
          <span key={i} className="mx-4 inline-flex items-center gap-2 text-xs">
            <span className="font-medium text-foreground">{s.symbol}</span>
            <span className="text-muted-foreground">₹{s.price.toLocaleString()}</span>
            <span className={s.change >= 0 ? "text-primary" : "text-destructive"}>
              {s.change >= 0 ? "▲" : "▼"} {Math.abs(s.change).toFixed(1)}%
            </span>
          </span>
        ))}
      </div>
    </div>
  );
}
