import { useState, useEffect, useCallback } from "react";
import { WatchlistCompany, newsData, companyStocks } from "@/data/dummyData";

const STORAGE_KEY = "smartfinance_watchlist";

export function useWatchlist() {
  const [watchlist, setWatchlist] = useState<WatchlistCompany[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        setWatchlist(JSON.parse(stored));
      } catch {
        setWatchlist([]);
      }
    }
  }, []);

  const persist = (list: WatchlistCompany[]) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    setWatchlist(list);
  };

  const addToWatchlist = useCallback(
    (symbol: string) => {
      if (watchlist.some((w) => w.symbol === symbol)) return;
      const stock = companyStocks.find((s) => s.symbol === symbol);
      if (!stock) return;
      const related = newsData.filter((n) =>
        n.relatedCompanies.includes(symbol)
      );
      const newItem: WatchlistCompany = {
        symbol: stock.symbol,
        name: stock.name,
        sector: stock.sector,
        news: related,
        price: stock.price,
        change: stock.change,
        changePercent: stock.changePercent,
      };
      persist([...watchlist, newItem]);
    },
    [watchlist]
  );

  const removeFromWatchlist = useCallback(
    (symbol: string) => {
      persist(watchlist.filter((w) => w.symbol !== symbol));
    },
    [watchlist]
  );

  const isInWatchlist = useCallback(
    (symbol: string) => watchlist.some((w) => w.symbol === symbol),
    [watchlist]
  );

  return { watchlist, addToWatchlist, removeFromWatchlist, isInWatchlist };
}
