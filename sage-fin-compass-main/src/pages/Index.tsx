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
<div className="relative mt-24 mb-24 px-4">
  {/* 1. Background Ambient Glow - Makes the section pop in Dark Mode */}
  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3/4 h-full bg-emerald-500/5 dark:bg-emerald-500/10 blur-[120px] rounded-full pointer-events-none -z-10" />

  {/* 2. The Glass Container */}
  <div className="max-w-5xl mx-auto py-10 px-8 rounded-[2rem] border border-slate-200/60 dark:border-white/5 bg-white/40 dark:bg-slate-900/40 backdrop-blur-xl shadow-[0_8px_32px_rgba(0,0,0,0.03)] dark:shadow-[0_20px_50px_rgba(0,0,0,0.2)]">
    
    {/* Section Label */}
    <div className="flex justify-center mb-10">
  <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full 
                   bg-emerald-50/50 dark:bg-emerald-500/10 
                   text-[11px] font-extrabold uppercase tracking-widest 
                   text-emerald-700 dark:text-emerald-400 
                   border border-emerald-200/50 dark:border-emerald-500/20 
                   shadow-sm backdrop-blur-sm">
    {/* Added a small static green dot for visual balance */}
    <span className="relative flex h-2 w-2">
      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
      <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
    </span>
    Live Market Connectivity
  </span>
</div>
    
    {/* Logo Grid */}
    <div className="flex flex-wrap justify-center items-center gap-10 md:gap-20 opacity-80 grayscale hover:grayscale-0 transition-all duration-700 ease-in-out">
      
      {/* NSE */}
     <a href="https://www.nseindia.com" target="_blank" rel="noopener noreferrer" 
         className="group cursor-pointer no-underline transform hover:scale-110 transition-all">
        <span className="text-xl font-bold tracking-tighter text-slate-800 dark:text-slate-100 group-hover:text-emerald-500 transition-colors">NSE</span>
      </a>

      {/* BSE */}
      <a href="https://www.bseindia.com" target="_blank" rel="noopener noreferrer" 
         className="group cursor-pointer no-underline transform hover:scale-110 transition-all">
        <span className="text-xl font-bold tracking-tighter text-slate-800 dark:text-slate-100 group-hover:text-blue-500 transition-colors">BSE</span>
      </a>

      {/* NASDAQ */}
      <a href="https://www.nasdaq.com" target="_blank" rel="noopener noreferrer" 
         className="group cursor-pointer no-underline transform hover:scale-110 transition-all">
        <span className="text-xl font-bold tracking-tighter text-slate-800 dark:text-slate-100 group-hover:text-emerald-400 transition-colors">NASDAQ</span>
      </a>

      {/* REUTERS */}
      <a href="https://www.reuters.com" target="_blank" rel="noopener noreferrer" 
         className="group cursor-pointer no-underline transform hover:scale-110 transition-all">
        <span className="text-xl font-bold tracking-tight text-slate-800 dark:text-slate-100 group-hover:text-orange-500 transition-colors">REUTERS</span>
      </a>

      {/* SEC */}
      <a href="https://www.sec.gov" target="_blank" rel="noopener noreferrer" 
         className="group cursor-pointer no-underline transform hover:scale-110 transition-all">
        <span className="text-xl font-bold tracking-tighter text-slate-800 dark:text-slate-100 group-hover:text-blue-400 transition-colors">SEC</span>
      </a>

    </div>
  </div>
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
              <div className="group relative glass-card h-full p-6 transition-all duration-500 ease-out 
                              hover:-translate-y-3 hover:scale-[1.02] 
                              hover:border-emerald-500/60 hover:shadow-[0_20px_50px_rgba(16,185,129,0.15)] 
                              hover:bg-white/[0.05] cursor-pointer overflow-hidden">
                
                {/* Hover Glow Effect: This adds a soft light behind the icon when you hover */}
                <div className="absolute -inset-px bg-gradient-to-r from-emerald-500/10 to-blue-500/10 opacity-0 transition-opacity duration-500 group-hover:opacity-100" />

                <div className={`relative z-10 mb-4 inline-flex h-14 w-14 items-center justify-center rounded-2xl 
                                bg-gradient-to-br ${f.color} shadow-lg transition-all duration-500 
                                group-hover:scale-110 group-hover:rotate-3 group-hover:shadow-emerald-500/20`}>
                  <f.icon className="h-7 w-7 text-white" />
                </div>

                <h3 className="relative z-10 font-heading text-xl font-bold tracking-tight transition-colors duration-300 group-hover:text-emerald-400">
                  {f.title}
                </h3>
                
                <p className="relative z-10 mt-2 text-sm text-muted-foreground leading-relaxed transition-colors duration-300 group-hover:text-foreground/90">
                  {f.desc}
                </p>

                {/* Explore Link: Now with a dramatic slide-in and arrow-bounce */}
                <div className="relative z-10 mt-6 flex items-center gap-2 text-sm font-bold text-emerald-500 
                                opacity-0 transition-all duration-500 transform translate-y-2 
                                group-hover:opacity-100 group-hover:translate-y-0">
                  <span className="uppercase tracking-wider">Explore</span>
                  <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
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
           <h2 className="font-heading text-2xl font-bold">Institutional Regulatory & Compliance Hub</h2>
              <p className="mx-auto mt-3 max-w-xl text-sm text-muted-foreground">
                Monitor real-time SEBI mandates, RBI circulars, and institutional policy shifts with our AI-summarized compliance engine.
              </p>
            <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
              <Link to="/regulatory">
                <Button className="gap-2 glow-green">
                  <TrendingUp className="h-4 w-4" /> Access Regulatory Terminal
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
