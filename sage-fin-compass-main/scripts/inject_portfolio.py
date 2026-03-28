import sys

file_path = 'c:/Users/urvas/OneDrive/Desktop/CodeCrafters/CodeCrafter_Mango/sage-fin-compass-main/src/pages/Portfolio.tsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
import_lucide_old = '  Sparkles, AlertCircle, ArrowUpRight, ArrowDownRight, RefreshCw, FileText, Loader2\n} from "lucide-react";'
import_lucide_new = '  Sparkles, AlertCircle, ArrowUpRight, ArrowDownRight, RefreshCw, FileText, Loader2,\n  BarChart2, AlertTriangle, Zap, Info, CheckCircle, ChevronRight\n} from "lucide-react";'
content = content.replace(import_lucide_old, import_lucide_new)

if import_lucide_old not in content and import_lucide_new not in content:
    print("Warning: Failed to inject new imports.")

# 2. Insert new states
hook_anchor = 'const fileInputRef = useRef<HTMLInputElement>(null);'
new_hooks = '''const fileInputRef = useRef<HTMLInputElement>(null);

  const [activeTab, setActiveTab] = useState('overview');
  
  const [recommendationsItems, setRecommendationsItems] = useState([
    { id: 1, type: "diversification", title: "Risk Diversification", action: "Add", symbol: "HDFCBANK", shares: 20, reason: "Banking sector exposure for stability", applied: false, impact: "Medium", bg: "bg-yellow-50 dark:bg-yellow-900/10", border: "border-yellow-200 dark:border-yellow-700/50" },
    { id: 2, type: "dividend", title: "Dividend Optimization", action: "Add", symbol: "ITC", shares: 30, reason: "FMCG diversification and dividend income", applied: false, impact: "Medium", bg: "bg-yellow-50 dark:bg-yellow-900/10", border: "border-yellow-200 dark:border-yellow-700/50" },
    { id: 3, type: "rebalance", title: "Portfolio Rebalancing", action: "Reduce", symbol: "INFY", shares: 20, reason: "Trim IT overweight, lock in gains", applied: false, impact: "High", bg: "bg-red-50 dark:bg-red-900/10", border: "border-red-200 dark:border-red-700/50" },
    { id: 4, type: "tax", title: "Tax-Loss Harvesting Opportunity", action: "Monitor", symbol: "None", shares: 0, reason: "No current losses. Your portfolio is performing well.", applied: true, impact: "Low", bg: "bg-green-50 dark:bg-green-900/10", border: "border-green-200 dark:border-green-700/50" },
    { id: 5, type: "growth_2", title: "Real Estate Push", action: "Add", symbol: "DLF", shares: 15, reason: "Real estate sector bet on infrastructure push", applied: false, impact: "Low", bg: "bg-blue-50 dark:bg-blue-900/10", border: "border-blue-200 dark:border-blue-700/50" }
  ]);

  const applyRecommendation = (rec: any) => {
    if (rec.action === "Monitor") return;
    
    const stockInfo = companyStocks.find(s => s.symbol === rec.symbol);
    const currentPrice = stockInfo ? stockInfo.price : (rec.symbol === 'DLF' ? 850 : 1000);
    const sector = stockInfo ? stockInfo.sector : (rec.symbol === 'DLF' ? 'Real Estate' : 'Other');
    const name = stockInfo ? stockInfo.name : rec.symbol;

    if (rec.action === "Add") {
      const existing = portfolio.find(p => p.symbol === rec.symbol);
      let newPortfolio = [...portfolio];
      if (existing) {
        newPortfolio = newPortfolio.map(p => p.symbol === rec.symbol 
          ? { ...p, quantity: p.quantity + rec.shares, avgPrice: ((p.avgPrice * p.quantity) + (currentPrice * rec.shares))/(p.quantity + rec.shares) }
          : p
        );
      } else {
        newPortfolio.push({
          symbol: rec.symbol,
          name: name,
          quantity: rec.shares,
          avgPrice: currentPrice * 0.98,
          currentPrice: currentPrice,
          sector: sector
        });
      }
      setPortfolio(newPortfolio);
      toast.success(`Successfully added ${rec.shares} shares of ${rec.symbol}`);
    } else if (rec.action === "Reduce") {
      const existing = portfolio.find(p => p.symbol === rec.symbol);
      if (existing) {
        if (existing.quantity <= rec.shares) {
          setPortfolio(portfolio.filter(p => p.symbol !== rec.symbol));
        } else {
          setPortfolio(portfolio.map(p => p.symbol === rec.symbol 
            ? { ...p, quantity: p.quantity - rec.shares }
            : p
          ));
        }
        toast.success(`Successfully reduced ${rec.shares} shares of ${rec.symbol}`);
      }
    }

    setRecommendationsItems(recommendationsItems.map(r => r.id === rec.id ? { ...r, applied: true } : r));
  };
'''
if hook_anchor in content:
    content = content.replace(hook_anchor, new_hooks)
else:
    print("Warning: Failed to inject new hooks.")

# 3. Replace layout starting from Summary Cards
summary_cards_start = '        {/* Summary Cards */}'

tabs_and_overview = '''        {/* Tabs */}
        <div className="flex border-b mb-6 gap-6 w-full overflow-x-auto hide-scrollbar">
          {['Overview', 'Analysis', 'Recommendations'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab.toLowerCase())}
              className={`py-2 text-sm font-semibold transition-colors border-b-2 whitespace-nowrap ${
                activeTab === tab.toLowerCase() 
                ? 'border-[#0f62fe] text-[#0f62fe] dark:text-blue-400 dark:border-blue-400' 
                : 'border-transparent text-muted-foreground hover:text-foreground hover:border-muted'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {activeTab === 'overview' && (
          <div className="space-y-6 animate-in fade-in duration-300">
            {/* Summary Cards */}
'''

if summary_cards_start in content:
    content = content.replace(summary_cards_start, tabs_and_overview, 1)
else:
    print("Warning: Failed to find Summary Cards start.")

# we need to close the overview div before Footer.
# Find `<Footer />` marker
footer_index = content.rfind('      <Footer />')

if footer_index != -1 and tabs_and_overview in content:
    # Extract everything between overview start and footer.
    overview_content_end = content[content.find(tabs_and_overview) + len(tabs_and_overview) : footer_index]

    new_rest = '''
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-300">
            <div className="grid gap-6 md:grid-cols-2">
              <div className="glass-card p-6">
                 <h3 className="font-heading text-lg font-bold flex items-center gap-2 mb-6"><BarChart2 className="h-5 w-5 text-[#0f62fe]"/> Sector Allocation</h3>
                 <div className="space-y-5">
                   {sectorData.map(s => (
                     <div key={s.name}>
                       <div className="flex justify-between text-sm mb-2 font-medium">
                         <span className="text-muted-foreground">{s.name}</span>
                         <span className="text-[#0f62fe] font-bold">{s.value}%</span>
                       </div>
                       <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                         <div className="h-full bg-[#0f62fe] rounded-full" style={{ width: `${s.value}%` }} />
                       </div>
                     </div>
                   ))}
                 </div>
              </div>
              <div className="glass-card p-6">
                 <h3 className="font-heading text-lg font-bold flex items-center gap-2 mb-6"><AlertTriangle className="h-5 w-5 text-orange-500"/> Risk Assessment</h3>
                 <div className="space-y-5">
                   <div>
                     <p className="text-xs text-muted-foreground mb-1">Volatility</p>
                     <p className="font-semibold text-sm">Moderate</p>
                   </div>
                   <div className="h-px bg-border/50" />
                   <div>
                     <p className="text-xs text-muted-foreground mb-1">Concentration</p>
                     <p className="font-semibold text-sm flex items-center gap-2">
                       {sectorData[0]?.name && `High ${sectorData[0].name} (${sectorData[0].value}%)`}
                     </p>
                   </div>
                   <div className="h-px bg-border/50" />
                   <div>
                     <p className="text-xs text-muted-foreground mb-1">Diversification</p>
                     <p className="font-semibold text-sm text-orange-600 dark:text-orange-400">Needs Improvement</p>
                   </div>
                   <div className="rounded-lg bg-orange-50 dark:bg-orange-900/20 p-4 border border-orange-100 dark:border-orange-500/20">
                     <p className="text-xs text-orange-800 dark:text-orange-300"><span className="font-semibold">AI Recommendation:</span> Add 2-3 defensive stocks from Banking/Utility sectors.</p>
                   </div>
                 </div>
              </div>
            </div>

            <h3 className="font-heading text-lg font-bold flex items-center gap-2 mt-8 mb-4"><Zap className="h-5 w-5 text-amber-500"/> Investment Strategies & Recommendations</h3>
            <div className="grid gap-4 md:grid-cols-2">
               {recommendationsItems.slice(0,4).map((rec, i) => (
                 <div key={i} className={`p-5 rounded-xl border ${rec.border} ${rec.bg} dark:bg-background/50`}>
                   <div className="flex justify-between items-start mb-2">
                     <h4 className="font-bold text-sm text-slate-800 dark:text-slate-200 flex items-center gap-2">{rec.title}</h4>
                     <Badge variant="outline" className={`text-[10px] bg-white dark:bg-slate-900 ${rec.impact === 'High' ? 'text-red-600 border-red-200 dark:text-red-400 dark:border-red-900' : (rec.impact === 'Medium' ? 'text-yellow-600 border-yellow-200 dark:text-yellow-500 dark:border-yellow-900' : 'text-green-600 border-green-200 dark:text-green-400 dark:border-green-900')}`}>{rec.impact}</Badge>
                   </div>
                   <p className="text-xs text-slate-600 dark:text-slate-400 mb-4 h-8">{rec.reason}</p>
                   <div className="h-px bg-slate-200/50 dark:bg-slate-700/50 w-full mb-3" />
                   <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Suggested Action:</p>
                   <p className="text-sm font-medium text-slate-800 dark:text-slate-200 bg-white/50 dark:bg-slate-900/50 px-3 py-2 rounded-md border border-white dark:border-slate-800">
                     {rec.action === 'Monitor' ? rec.reason : `${rec.action} ${rec.symbol} position ${rec.action === 'Add' ? 'by' : 'sell'} ${rec.shares} shares`}
                   </p>
                 </div>
               ))}
            </div>
            
            <div className="glass-card p-6 mt-6">
               <h3 className="font-heading text-lg font-bold mb-6">Portfolio Analysis Summary</h3>
               <div className="grid gap-8 md:grid-cols-2">
                 <div>
                   <h4 className="text-sm font-bold mb-4 flex items-center gap-2 text-slate-800 dark:text-slate-200"><TrendingUp className="h-4 w-4 text-green-500"/> Strengths</h4>
                   <ul className="space-y-3 text-sm text-muted-foreground">
                     <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> Strong overall returns at {totalPnLPercent}% growth</li>
                     <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> Well-diversified across {sectorData.length} sectors</li>
                     <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> Adequate dividend yield for income generation</li>
                   </ul>
                 </div>
                 <div>
                   <h4 className="text-sm font-bold mb-4 flex items-center gap-2 text-slate-800 dark:text-slate-200"><TrendingDown className="h-4 w-4 text-orange-500"/> Areas to Improve</h4>
                   <ul className="space-y-3 text-sm text-muted-foreground">
                     <li className="flex items-start gap-2"><AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5 shrink-0"/> Tech sector concentration risks need monitoring</li>
                     <li className="flex items-start gap-2"><AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5 shrink-0"/> Consider adding defensive stocks for volatility protection</li>
                     <li className="flex items-start gap-2"><AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5 shrink-0"/> Regular rebalancing schedule should be established</li>
                   </ul>
                 </div>
               </div>
            </div>

            <div className="bg-blue-50/70 dark:bg-blue-900/10 border border-blue-100 dark:border-blue-900/30 rounded-xl p-6 mt-6 shadow-sm">
              <h3 className="text-sm font-bold text-slate-800 dark:text-slate-200 mb-4">Next Steps</h3>
              <ol className="list-decimal list-outside ml-4 space-y-2.5 text-sm text-slate-600 dark:text-slate-400 font-medium font-sans">
                <li>Review quarterly earnings for tech sector stocks</li>
                <li>Execute recommended rebalancing actions</li>
                <li>Set up automated dividend reinvestment</li>
                <li>Schedule monthly portfolio review</li>
                <li>Monitor RBI and market regulatory changes</li>
              </ol>
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div className="space-y-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
             <div className="flex flex-col sm:flex-row items-center sm:items-start gap-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-900/40 rounded-xl p-5 mb-6 shadow-sm">
               <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#0f62fe] text-white">
                 <Zap className="h-5 w-5" />
               </div>
               <div>
                  <h4 className="font-bold text-sm text-slate-800 dark:text-slate-200 text-center sm:text-left">AI-Powered Optimization</h4>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mt-1 text-center sm:text-left">Based on your current holdings, we recommend diversifying into defensive sectors and reducing IT concentration.</p>
               </div>
             </div>

             <div className="space-y-3">
               {recommendationsItems.filter(r => r.action !== 'Monitor').map(rec => (
                 <div key={rec.id} className="flex flex-col sm:flex-row items-start sm:items-center justify-between bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 hover:shadow-md transition-all">
                    <div className="mb-4 sm:mb-0">
                      <h4 className="font-bold text-[15px] flex items-center gap-2">
                        {rec.action} {rec.symbol} <span className="text-slate-400 font-normal">—</span> 
                        {rec.action === 'Reduce' ? 'sell' : ''} {rec.shares} shares
                      </h4>
                      <p className="text-sm text-muted-foreground mt-1">{rec.reason}</p>
                    </div>
                    <Button 
                      onClick={() => !rec.applied && applyRecommendation(rec)}
                      disabled={rec.applied}
                      className={`shrink-0 w-full sm:w-28 font-semibold ${rec.applied ? 'bg-blue-50 text-blue-400 hover:bg-blue-50 cursor-default border-none dark:bg-blue-900/20 dark:text-blue-500' : 'bg-[#0f62fe]/10 text-[#0f62fe] hover:bg-[#0f62fe]/20 dark:bg-blue-900/40 dark:text-blue-400'}`}
                      variant="secondary"
                    >
                      {rec.applied ? 'Applied' : 'Apply'}
                    </Button>
                 </div>
               ))}
             </div>
          </div>
        )}
      </div>

      <Footer />
'''

    content = content[:content.find(tabs_and_overview) + len(tabs_and_overview)] + overview_content_end + new_rest
else:
    print("Warning: Failed to find Footer.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Successfully rewritten Portfolio.tsx with massive analysis and recommendation UI injections!')
