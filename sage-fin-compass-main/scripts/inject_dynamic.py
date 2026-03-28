import sys

file_path = 'c:/Users/urvas/OneDrive/Desktop/CodeCrafters/CodeCrafter_Mango/sage-fin-compass-main/src/pages/Portfolio.tsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I need to insert derived state variables above the return statement.
# Let's find "const colors = ["
anchor_state = 'const colors = ["hsl(160,84%,39%)", "hsl(217,91%,60%)", "hsl(38,92%,50%)", "hsl(270,76%,55%)", "hsl(0,72%,51%)", "hsl(160,60%,50%)"];'

new_state = anchor_state + '''

  const sortedSectors = [...sectorData].sort((a,b) => b.value - a.value);
  const topSector = sortedSectors[0];
  const isConcentrated = topSector && topSector.value > 30;
  const hasDefensive = portfolio.some(p => p.sector === 'Banking' || p.sector === 'FMCG');
'''
content = content.replace(anchor_state, new_state)

# Replace the HTML block starting from `{activeTab === 'analysis' && (` up to `{activeTab === 'recommendations' && (`
start_marker = "{activeTab === 'analysis' && ("
end_marker = "{activeTab === 'recommendations' && ("

idx_start = content.find(start_marker)
idx_end = content.find(end_marker)

if idx_start == -1 or idx_end == -1:
    print("Error finding markers")
    sys.exit(1)

new_analysis_html = """{activeTab === 'analysis' && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-300">
            <div className="grid gap-6 md:grid-cols-2">
              <div className="glass-card p-6">
                 <h3 className="font-heading text-lg font-bold flex items-center gap-2 mb-6"><BarChart2 className="h-5 w-5 text-[#0f62fe]"/> Sector Allocation</h3>
                 <div className="space-y-5">
                   {sortedSectors.map(s => (
                     <div key={s.name}>
                       <div className="flex justify-between text-sm mb-2 font-medium">
                         <span className="text-muted-foreground">{s.name}</span>
                         <span className="text-[#0f62fe] font-bold">{s.value}%</span>
                       </div>
                       <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                         <div className="h-full bg-[#0f62fe] transition-all duration-500 rounded-full" style={{ width: `${s.value}%` }} />
                       </div>
                     </div>
                   ))}
                 </div>
              </div>
              <div className="glass-card p-6 relative overflow-hidden">
                 <div className={`absolute top-0 left-0 w-1.5 h-full ${isConcentrated ? 'bg-orange-400' : 'bg-green-400'} transition-colors`}/>
                 <h3 className="font-heading text-lg font-bold flex items-center gap-2 mb-6 ml-2"><AlertTriangle className={`h-5 w-5 ${isConcentrated ? 'text-orange-500' : 'text-green-500'}`}/> Risk Assessment</h3>
                 <div className="space-y-5 ml-2">
                   <div>
                     <p className="text-xs text-muted-foreground mb-1">Volatility</p>
                     <p className={`font-semibold text-sm ${hasDefensive ? 'text-green-600 dark:text-green-400' : 'text-slate-800 dark:text-slate-200'}`}>{hasDefensive ? 'Low-Moderate' : 'Moderate-High'}</p>
                   </div>
                   <div className="h-px bg-border/50" />
                   <div>
                     <p className="text-xs text-muted-foreground mb-1">Concentration</p>
                     <p className={`font-semibold text-sm flex items-center gap-2 ${isConcentrated ? 'text-orange-600 dark:text-orange-400' : 'text-green-600 dark:text-green-400'}`}>
                       {topSector ? (isConcentrated ? `High ${topSector.name} (${topSector.value}%)` : 'Optimally Balanced') : 'Normal'}
                     </p>
                   </div>
                   <div className="h-px bg-border/50" />
                   <div>
                     <p className="text-xs text-muted-foreground mb-1">Diversification Status</p>
                     <p className={`font-semibold text-sm ${isConcentrated ? 'text-orange-600 dark:text-orange-400' : 'text-green-600 dark:text-green-400'}`}>{isConcentrated ? 'Needs Improvement' : 'Excellent'}</p>
                   </div>
                   {isConcentrated ? (
                     <div className="rounded-lg bg-orange-50 dark:bg-orange-900/20 p-4 border border-orange-100 dark:border-orange-500/20">
                       <p className="text-xs text-orange-800 dark:text-orange-300"><span className="font-semibold">AI Recommendation:</span> Add defensive stocks from Banking/FMCG sectors to dilute IT concentration.</p>
                     </div>
                   ) : (
                     <div className="rounded-lg bg-green-50 dark:bg-green-900/20 p-4 border border-green-100 dark:border-green-500/20">
                       <p className="text-xs text-green-800 dark:text-green-300"><span className="font-semibold">AI Status:</span> Portfolio is currently maintaining optimal sector allocation ratios!</p>
                     </div>
                   )}
                 </div>
              </div>
            </div>

            <h3 className="font-heading text-lg font-bold flex items-center gap-2 mt-8 mb-4"><Zap className="h-5 w-5 text-amber-500"/> Investment Strategies & Recommendations</h3>
            <div className="grid gap-4 md:grid-cols-2">
               {recommendationsItems.slice(0,4).map((rec, i) => (
                 <div key={i} className={`p-5 rounded-xl border transition-colors duration-500 ${rec.applied ? 'bg-green-50/50 dark:bg-green-900/10 border-green-200 dark:border-green-900/50' : rec.bg + ' ' + rec.border} dark:bg-background/50`}>
                   <div className="flex justify-between items-start mb-2">
                     <h4 className="font-bold text-sm text-slate-800 dark:text-slate-200 flex items-center gap-2">{rec.title}</h4>
                     <Badge variant="outline" className={`text-[10px] bg-white dark:bg-slate-900 ${rec.applied ? 'text-green-600 border-green-200 dark:text-green-400 dark:border-green-900' : (rec.impact === 'High' ? 'text-red-600 border-red-200 dark:text-red-400 dark:border-red-900' : (rec.impact === 'Medium' ? 'text-yellow-600 border-yellow-200 dark:text-yellow-500 dark:border-yellow-900' : 'text-green-600 border-green-200 dark:text-green-400 dark:border-green-900'))}`}>{rec.applied ? 'Resolved ✓' : rec.impact}</Badge>
                   </div>
                   <p className="text-xs text-slate-600 dark:text-slate-400 mb-4 h-8">{rec.applied ? 'This strategic objective has been successfully executed.' : rec.reason}</p>
                   <div className="h-px bg-slate-200/50 dark:bg-slate-700/50 w-full mb-3" />
                   <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Status:</p>
                   <p className={`text-sm font-medium px-3 py-2 rounded-md border ${rec.applied ? 'text-green-700 bg-green-100/50 border-green-200 dark:text-green-400 dark:bg-green-900/20 dark:border-green-800' : 'text-slate-800 dark:text-slate-200 bg-white/50 dark:bg-slate-900/50 border-white dark:border-slate-800'}`}>
                     {rec.applied ? '✓ Monitoring Performance' : (rec.action === 'Monitor' ? rec.reason : `${rec.action} ${rec.symbol} position ${rec.action === 'Add' ? 'by' : 'sell'} ${rec.shares} shares`)}
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
                     <li className="flex items-start gap-2"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> Diversified across {sectorData.length} core holding sectors</li>
                     {hasDefensive && <li className="flex items-start gap-2 animate-in fade-in duration-500"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> Solid defensive backbone limits drawdown risks</li>}
                     {!isConcentrated && <li className="flex items-start gap-2 animate-in fade-in duration-500"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> Optimal sector allocation targets successfully met</li>}
                   </ul>
                 </div>
                 <div>
                   <h4 className="text-sm font-bold mb-4 flex items-center gap-2 text-slate-800 dark:text-slate-200"><TrendingDown className="h-4 w-4 text-orange-500"/> Areas to Improve</h4>
                   <ul className="space-y-3 text-sm text-muted-foreground">
                     {isConcentrated && <li className="flex items-start gap-2"><AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5 shrink-0"/> Tech sector concentration risks need monitoring</li>}
                     {!hasDefensive && <li className="flex items-start gap-2"><AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5 shrink-0"/> Consider adding defensive stocks for volatility protection</li>}
                     {(!isConcentrated && hasDefensive) ? (
                         <li className="flex items-start gap-2 text-green-600 dark:text-green-400 font-medium animate-in fade-in duration-500"><CheckCircle className="h-4 w-4 text-green-500 mt-0.5 shrink-0"/> All major structural portfolio risks mitigated!</li>
                     ) : (
                         <li className="flex items-start gap-2"><AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5 shrink-0"/> Regular rebalancing schedule should be established</li>
                     )}
                   </ul>
                 </div>
               </div>
            </div>

            <div className="bg-blue-50/70 dark:bg-blue-900/10 border border-blue-100 dark:border-blue-900/30 rounded-xl p-6 mt-6 shadow-sm">
              <h3 className="text-sm font-bold text-slate-800 dark:text-slate-200 mb-4">Next Steps</h3>
              <ol className="list-decimal list-outside ml-4 space-y-2.5 text-sm text-slate-600 dark:text-slate-400 font-medium font-sans">
                {isConcentrated ? <li>Execute recommended rebalancing actions</li> : <li><strike className="text-slate-400">Execute recommended rebalancing actions</strike> <span className="text-green-600 ml-1">✓ Done</span></li>}
                <li>Review quarterly earnings for top sector holdings</li>
                <li>Set up automated dividend reinvestment</li>
                <li>Schedule monthly portfolio review</li>
                <li>Monitor RBI and market regulatory changes</li>
              </ol>
            </div>
          </div>
        )}

        """

content = content[:idx_start] + new_analysis_html + content[idx_end:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Dynamic analysis injected.")
