import sys

file_path = 'c:/Users/urvas/OneDrive/Desktop/CodeCrafters/CodeCrafter_Mango/sage-fin-compass-main/src/pages/Portfolio.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will slice the content right at `{/* Tabs */}`
tabs_idx = content.find('{/* Tabs */}')
if tabs_idx == -1:
    print("Error: Could not find Tabs marker")
    sys.exit(1)

content_top = content[:tabs_idx]

content_bottom = """{/* Tabs */}
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
            <div className="grid gap-4 sm:grid-cols-4 mb-6">
              <div className="glass-card p-4">
                <span className="text-xs text-muted-foreground">Total Invested</span>
                <div className="font-heading text-xl font-bold mt-1">₹{totalInvested.toLocaleString(undefined, { maximumFractionDigits: 0 })}</div>
              </div>
              <div className="glass-card p-4">
                <span className="text-xs text-muted-foreground">Current Value</span>
                <div className="font-heading text-xl font-bold mt-1">₹{totalCurrent.toLocaleString(undefined, { maximumFractionDigits: 0 })}</div>
              </div>
              <div className="glass-card p-4">
                <span className="text-xs text-muted-foreground">P&L</span>
                <div className={`font-heading text-xl font-bold mt-1 flex items-center gap-1 ${totalPnL >= 0 ? "text-primary" : "text-destructive"}`}>
                  {totalPnL >= 0 ? <ArrowUpRight className="h-4 w-4" /> : <ArrowDownRight className="h-4 w-4" />}
                  ₹{Math.abs(totalPnL).toLocaleString(undefined, { maximumFractionDigits: 0 })}
                  <span className="text-sm">({totalPnLPercent}%)</span>
                </div>
              </div>
              <div className="glass-card p-4">
                <span className="text-xs text-muted-foreground">Stocks</span>
                <div className="font-heading text-xl font-bold mt-1">{portfolio.length}</div>
              </div>
            </div>

            <div className="grid gap-6 lg:grid-cols-3">
              {/* Holdings */}
              <div className="lg:col-span-2 space-y-3">
                <h2 className="font-heading text-lg font-semibold">Holdings</h2>
                <div className="space-y-2">
                  {portfolio.map((s) => {
                    const pnl = (s.currentPrice - s.avgPrice) * s.quantity;
                    const pnlPct = ((s.currentPrice - s.avgPrice) / s.avgPrice * 100).toFixed(2);
                    return (
                      <div key={s.symbol} className="glass-card p-4 flex items-center gap-4">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent font-heading text-xs font-bold shrink-0">
                          {s.symbol.slice(0, 2)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="font-heading text-sm font-semibold">{s.symbol}</span>
                            <Badge variant="outline" className="text-[10px]">{s.sector}</Badge>
                          </div>
                          <span className="text-xs text-muted-foreground">{s.name}</span>
                        </div>
                        <div className="text-right">
                          <div className="text-sm">Qty: <span className="font-medium">{s.quantity}</span></div>
                          <div className="text-xs text-muted-foreground">Avg: ₹{s.avgPrice.toLocaleString()}</div>
                        </div>
                        <div className="text-right min-w-[100px]">
                          <div className="text-sm font-medium">₹{(s.currentPrice * s.quantity).toLocaleString()}</div>
                          <div className={`flex items-center justify-end gap-0.5 text-xs ${pnl >= 0 ? "text-primary" : "text-destructive"}`}>
                            {pnl >= 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                            {pnl >= 0 ? "+" : ""}₹{Math.abs(pnl).toFixed(0)} ({pnlPct}%)
                          </div>
                        </div>
                        <Button variant="ghost" size="icon" className="h-8 w-8 shrink-0" onClick={() => removeStock(s.symbol)}>
                          <Trash2 className="h-3.5 w-3.5 text-muted-foreground hover:text-destructive" />
                        </Button>
                      </div>
                    );
                  })}
                </div>

                {/* Add Stock Button & Form */}
                {!showAddStock && (
                  <Button
                    variant="outline"
                    className="w-full mt-4 border-dashed border-2 py-6 text-muted-foreground hover:text-foreground hover:bg-accent/50 gap-2"
                    onClick={() => setShowAddStock(true)}
                  >
                    <Plus className="h-5 w-5" /> Add Stock
                  </Button>
                )}

                {showAddStock && (
                  <div className="glass-card mt-4 p-4 flex gap-3 items-end border border-primary/20 bg-background/50 shadow-sm relative">
                    <Button
                      variant="ghost"
                      size="icon"
                      className="absolute -top-3 -right-3 h-6 w-6 rounded-full bg-background border shadow-sm hover:bg-destructive hover:text-destructive-foreground z-10"
                      onClick={() => setShowAddStock(false)}
                    >
                      <Trash2 className="h-3 w-3" />
                    </Button>
                    <div className="flex-[3]">
                      <label className="text-xs text-muted-foreground font-medium mb-1.5 block">Symbol</label>
                      <Input
                        placeholder="e.g., SUNPHARMA"
                        value={newSymbol}
                        onChange={(e) => setNewSymbol(e.target.value.toUpperCase())}
                        className="bg-background h-10 w-full"
                      />
                    </div>
                    <div className="flex-1 min-w-[100px]">
                      <label className="text-xs text-muted-foreground font-medium mb-1.5 block">Quantity</label>
                      <Input
                        type="number"
                        placeholder="Qty"
                        value={newQty}
                        onChange={(e) => setNewQty(e.target.value)}
                        className="bg-background h-10 w-full"
                      />
                    </div>
                    <Button onClick={handleAddStock} className="glow-green h-10 px-6 text-sm font-medium">Add</Button>
                  </div>
                )}
              </div>

              {/* Sector Chart */}
              <div>
                <h2 className="font-heading text-lg font-semibold mb-3">Sector Allocation</h2>
                <div className="glass-card p-4">
                  <ResponsiveContainer width="100%" height={220}>
                    <PieChart>
                      <Pie data={sectorData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} innerRadius={50} strokeWidth={0}>
                        {sectorData.map((_, i) => (
                          <Cell key={i} fill={colors[i % colors.length]} />
                        ))}
                      </Pie>
                      <Tooltip
                        contentStyle={{ background: "hsl(222,47%,9%)", border: "1px solid hsl(217,33%,17%)", borderRadius: 8, fontSize: 12, color: "#fff" }}
                        itemStyle={{ color: "#fff" }}
                        formatter={(v: number) => [`${v}%`, "Allocation"]}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                  <div className="space-y-1.5 mt-2">
                    {sectorData.map((s, i) => (
                      <div key={s.name} className="flex items-center justify-between text-xs">
                        <div className="flex items-center gap-2">
                          <span className="h-2.5 w-2.5 rounded-full" style={{ background: colors[i % colors.length] }} />
                          <span>{s.name}</span>
                        </div>
                        <span className="font-medium">{s.value}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
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
                       {sectorData[0]?.name ? `High ${sectorData[0].name} (${sectorData[0].value}%)` : 'Normal'}
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
    </div>
  );
}
"""

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_top + content_bottom)

print("Fixed Portfolio UI!")
