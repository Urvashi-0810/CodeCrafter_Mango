import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { TrendingUp, Search, Eye, BarChart3, Shield, Briefcase, PieChart, Menu, X, Sun, Moon, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useTheme } from "@/hooks/useTheme";

const navLinks = [
  { to: "/search", label: "Search", icon: Search },
  { to: "/watchlist", label: "Watchlist", icon: Eye },
  { to: "/insights", label: "Market Insights", icon: BarChart3 },
  { to: "/regulatory", label: "Regulatory", icon: Shield },
  { to: "/portfolio", label: "Portfolio", icon: Briefcase },
  { to: "/investment-analyzer", label: "Investment Analyzer", icon: PieChart },
  { to: "/learn", label: "Learn", icon: BookOpen },
];

export default function Navbar() {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const { isDark, toggle } = useTheme();

  return (
    <nav className="sticky top-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-xl">
      <div className="w-full flex h-16 items-center justify-between px-6 lg:px-12 xl:px-16">
        <Link to="/" className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary">
            <TrendingUp className="h-5 w-5 text-primary-foreground" />
          </div>
          <span className="font-heading text-lg font-bold tracking-tight">
            Smart<span className="text-primary">Finance</span>
          </span>
        </Link>

        {/* Desktop */}
        <div className="hidden items-center gap-1 lg:flex">
          {navLinks.map((l) => {
            const active = location.pathname === l.to;
            return (
              <Link key={l.to} to={l.to}>
                <Button
                  variant={active ? "default" : "ghost"}
                  size="sm"
                  className="gap-1.5 text-xs"
                >
                  <l.icon className="h-3.5 w-3.5" />
                  {l.label}
                </Button>
              </Link>
            );
          })}
          <Button variant="ghost" size="icon" onClick={toggle} className="ml-1">
            {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>
        </div>

        {/* Mobile toggle */}
        <Button
          variant="ghost"
          size="icon"
          className="lg:hidden"
          onClick={() => setMobileOpen(!mobileOpen)}
        >
          {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </Button>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="border-t border-border/50 bg-background/95 backdrop-blur-xl lg:hidden">
          <div className="container mx-auto flex flex-col gap-1 px-4 py-3">
            {navLinks.map((l) => {
              const active = location.pathname === l.to;
              return (
                <Link key={l.to} to={l.to} onClick={() => setMobileOpen(false)}>
                  <Button
                    variant={active ? "default" : "ghost"}
                    size="sm"
                    className="w-full justify-start gap-2"
                  >
                    <l.icon className="h-4 w-4" />
                    {l.label}
                  </Button>
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </nav>
  );
}
