import { Link } from "react-router-dom";
import { Search, Eye, BarChart3, Shield, Briefcase, PieChart, ArrowRight, TrendingUp, Zap, Globe } from "lucide-react";
import { Button } from "@/components/ui/button";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { marketInsights } from "@/data/dummyData";

const features = [
  {
    icon: Search,
    title: "Financial Search",
    desc: "Search any company's financial reports, news, and data. AI-summarized insights with source verification.",
    to: "/search",
    color: "from-primary to-chart-blue",
  },
  {
    icon: Eye,
    title: "Smart Watchlist",
    desc: "Monitor companies you care about. Auto-aggregated news, reports, and price movements in one place.",
    to: "/watchlist",
    color: "from-chart-blue to-chart-purple",
  },
  {
    icon: BarChart3,
    title: "Market Insights",
    desc: "Bite-sized summaries of what's happening in financial markets, stock movements, and global trends.",
    to: "/insights",
    color: "from-chart-amber to-destructive",
  },
  {
    icon: Shield,
    title: "Regulatory Hub",
    desc: "RBI guidelines, SEBI regulations, budget insights, and policy changes — summarized and sourced.",
    to: "/regulatory",
    color: "from-primary to-chart-amber",
  },
  {
    icon: Briefcase,
    title: "Portfolio Analyzer",
    desc: "Upload your portfolio and get AI-driven insights, diversification strategies, and actionable recommendations.",
    to: "/portfolio",
    color: "from-chart-purple to-primary",
  },
  {
    icon: PieChart,
    title: "Investment Analyzer",
    desc: "Analyze investments across sectors — equities, mutual funds, gold, bonds — with AI-powered strategies.",
    to: "/investment-analyzer",
    color: "from-destructive to-chart-amber",
  },
];

export default function Index() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <TickerBar />

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 opacity-20">
          <div className="absolute left-1/4 top-1/4 h-96 w-96 rounded-full bg-primary/30 blur-[120px]" />
          <div className="absolute right-1/4 bottom-1/4 h-96 w-96 rounded-full bg-chart-blue/30 blur-[120px]" />
        </div>
        <div className="container relative mx-auto px-4 py-24 text-center lg:py-36">
          <div className="mx-auto inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-xs font-medium text-primary mb-6">
            <Zap className="h-3.5 w-3.5" />
            AI-Powered Financial Intelligence
          </div>
          <h1 className="font-heading text-4xl font-bold leading-tight tracking-tight sm:text-5xl lg:text-6xl">
            One Platform for{" "}
            <span className="gradient-text">Smarter</span>
            <br />
            Investment Decisions
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground">
            Aggregate financial data from multiple sources, get AI-powered summaries, 
            monitor your watchlist, and analyze portfolios — all in one unified platform.
          </p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <Link to="/search">
              <Button size="lg" className="gap-2 glow-green">
                <Search className="h-4 w-4" /> Start Searching
              </Button>
            </Link>
            <Link to="/portfolio">
              <Button size="lg" variant="outline" className="gap-2">
                <Briefcase className="h-4 w-4" /> Analyze Portfolio
              </Button>
            </Link>
          </div>

          {/* Stats */}
          <div className="mx-auto mt-16 grid max-w-3xl grid-cols-2 gap-4 md:grid-cols-4">
            {[
              { label: "Data Sources", value: "50+" },
              { label: "Companies", value: "5,000+" },
              { label: "Reports Analyzed", value: "1M+" },
              { label: "Active Users", value: "10K+" },
            ].map((s) => (
              <div key={s.label} className="glass-card p-4">
                <div className="font-heading text-2xl font-bold text-primary">{s.value}</div>
                <div className="text-xs text-muted-foreground">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-12">
          <h2 className="font-heading text-3xl font-bold">Everything You Need</h2>
          <p className="mt-2 text-muted-foreground">Comprehensive tools for individual investors and financial institutions</p>
        </div>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {features.map((f) => (
            <Link key={f.to} to={f.to} className="group">
              <div className="glass-card h-full p-6 transition-all hover:border-primary/50 hover:glow-green">
                <div className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${f.color} opacity-80`}>
                  <f.icon className="h-6 w-6 text-foreground" />
                </div>
                <h3 className="font-heading text-lg font-semibold">{f.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
                <div className="mt-4 flex items-center gap-1 text-sm font-medium text-primary opacity-0 transition-opacity group-hover:opacity-100">
                  Explore <ArrowRight className="h-3.5 w-3.5" />
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Quick Market Pulse */}
      <section className="container mx-auto px-4 py-16">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="font-heading text-2xl font-bold">Market Pulse</h2>
            <p className="text-sm text-muted-foreground">Latest from the markets</p>
          </div>
          <Link to="/insights">
            <Button variant="outline" size="sm" className="gap-1">
              View All <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </Link>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {marketInsights.slice(0, 3).map((item) => (
            <div key={item.id} className="glass-card p-5">
              <div className="flex items-center gap-2 mb-3">
                <span className={`inline-block h-2 w-2 rounded-full ${
                  item.sentiment === "positive" ? "bg-primary" : item.sentiment === "negative" ? "bg-destructive" : "bg-warning"
                }`} />
                <span className="text-xs text-muted-foreground">{item.category}</span>
                <span className="ml-auto text-xs text-muted-foreground">{item.date}</span>
              </div>
              <h3 className="font-heading text-sm font-semibold leading-snug">{item.title}</h3>
              <p className="mt-2 text-xs text-muted-foreground leading-relaxed">{item.summary}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="container mx-auto px-4 py-16">
        <div className="glass-card relative overflow-hidden p-10 text-center">
          <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-chart-blue/10" />
          <div className="relative">
            <Globe className="mx-auto mb-4 h-10 w-10 text-primary animate-float" />
            <h2 className="font-heading text-2xl font-bold">For Individual Investors & Financial Institutions</h2>
            <p className="mx-auto mt-3 max-w-xl text-sm text-muted-foreground">
              Whether you're tracking your personal portfolio or need institutional-grade regulatory intelligence, 
              SmartFinance has the tools you need.
            </p>
            <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
              <Link to="/search">
                <Button className="gap-2 glow-green">
                  <TrendingUp className="h-4 w-4" /> Get Started Free
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
