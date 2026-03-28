import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import Index from "./pages/Index.tsx";
import SearchPage from "./pages/Search.tsx";
import WatchlistPage from "./pages/Watchlist.tsx";
import MarketInsightsPage from "./pages/MarketInsights.tsx";
import RegulatoryPage from "./pages/Regulatory.tsx";
import PortfolioPage from "./pages/Portfolio.tsx";
import InvestmentAnalyzerPage from "./pages/InvestmentAnalyzer.tsx";
import NotFound from "./pages/NotFound.tsx";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/watchlist" element={<WatchlistPage />} />
          <Route path="/insights" element={<MarketInsightsPage />} />
          <Route path="/regulatory" element={<RegulatoryPage />} />
          <Route path="/portfolio" element={<PortfolioPage />} />
          <Route path="/investment-analyzer" element={<InvestmentAnalyzerPage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
