import { TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="border-t border-border/50 bg-card/50">
      <div className="container mx-auto px-4 py-10">
        <div className="grid gap-8 md:grid-cols-4">
          <div>
            <Link to="/" className="flex items-center gap-2 mb-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
                <TrendingUp className="h-4 w-4 text-primary-foreground" />
              </div>
              <span className="font-heading text-base font-bold">SmartFinance</span>
            </Link>
            <p className="text-sm text-muted-foreground">
              AI-powered financial intelligence for smarter investment decisions.
            </p>
          </div>
          <div>
            <h4 className="mb-3 font-heading text-sm font-semibold">Products</h4>
            <div className="flex flex-col gap-2 text-sm text-muted-foreground">
              <Link to="/search" className="hover:text-primary transition-colors">Financial Search</Link>
              <Link to="/watchlist" className="hover:text-primary transition-colors">Watchlist</Link>
              <Link to="/insights" className="hover:text-primary transition-colors">Market Insights</Link>
              <Link to="/portfolio" className="hover:text-primary transition-colors">Portfolio Analyzer</Link>
            </div>
          </div>
          <div>
            <h4 className="mb-3 font-heading text-sm font-semibold">For Institutions</h4>
            <div className="flex flex-col gap-2 text-sm text-muted-foreground">
              <Link to="/regulatory" className="hover:text-primary transition-colors">Regulatory Insights</Link>
              <Link to="/investment-analyzer" className="hover:text-primary transition-colors">Investment Analyzer</Link>
            </div>
          </div>
          <div>
            <h4 className="mb-3 font-heading text-sm font-semibold">Legal</h4>
            <div className="flex flex-col gap-2 text-sm text-muted-foreground">
              <span>Privacy Policy</span>
              <span>Terms of Service</span>
              <span>Disclaimer</span>
            </div>
          </div>
        </div>
        <div className="mt-8 border-t border-border/50 pt-6 text-center text-xs text-muted-foreground">
          © 2025 SmartFinance Solutions. All rights reserved. Not financial advice.
        </div>
      </div>
    </footer>
  );
}
