export interface NewsItem {
  id: string;
  title: string;
  summary: string;
  fullContent: string;
  source: string;
  sourceUrl: string;
  category: string;
  date: string;
  sentiment: "positive" | "negative" | "neutral";
  relatedCompanies: string[];
  tags: string[];
}

export interface CompanyStock {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  sector: string;
  marketCap: string;
  pe: number;
  high52w: number;
  low52w: number;
  volume: string;
}

export interface WatchlistCompany {
  symbol: string;
  name: string;
  sector: string;
  news: NewsItem[];
  price: number;
  change: number;
  changePercent: number;
}

export interface PortfolioStock {
  symbol: string;
  name: string;
  quantity: number;
  avgPrice: number;
  currentPrice: number;
  sector: string;
}

export interface RegulatoryItem {
  id: string;
  title: string;
  summary: string;
  fullContent: string;
  source: string;
  sourceUrl: string;
  category: string;
  date: string;
  impact: "high" | "medium" | "low";
  tags: string[];
}

export const stockTicker: { symbol: string; price: number; change: number }[] = [
  { symbol: "RELIANCE", price: 2456.30, change: 1.2 },
  { symbol: "TCS", price: 3245.80, change: -0.8 },
  { symbol: "INFY", price: 1567.45, change: 2.1 },
  { symbol: "HDFCBANK", price: 1623.90, change: 0.5 },
  { symbol: "ICICIBANK", price: 987.60, change: -1.3 },
  { symbol: "WIPRO", price: 412.75, change: 1.8 },
  { symbol: "BHARTIARTL", price: 1345.20, change: 0.9 },
  { symbol: "ITC", price: 465.30, change: -0.4 },
  { symbol: "SBIN", price: 623.15, change: 2.5 },
  { symbol: "TATAMOTORS", price: 765.40, change: -1.7 },
  { symbol: "ADANIENT", price: 2890.50, change: 3.1 },
  { symbol: "BAJFINANCE", price: 6780.25, change: -0.6 },
];

export const newsData: NewsItem[] = [
  {
    id: "1",
    title: "Reliance Industries Reports Record Q3 Profits Driven by Retail and Jio",
    summary: "Reliance Industries posted a record quarterly profit of ₹18,540 crore in Q3 FY25, driven by strong growth in its retail and digital services arms. Jio added 12 million subscribers while retail revenue grew 18% YoY.",
    fullContent: "Reliance Industries Limited reported its highest-ever quarterly consolidated net profit of ₹18,540 crore for the quarter ended December 2024, marking a 12% year-on-year increase. The conglomerate's retail business, Reliance Retail, posted revenue of ₹75,000 crore, up 18% from the same quarter last year, driven by strong festive season demand and expansion of digital commerce channels.\n\nJio Platforms continued its growth trajectory, adding 12 million net subscribers during the quarter to reach a total base of 490 million. ARPU (Average Revenue Per User) increased to ₹195.5, up from ₹181.7 in the previous quarter, aided by the tariff hike implemented in July 2024.\n\nThe oil-to-chemicals (O2C) business saw flat growth due to muted refining margins globally, though the company's new energy initiatives showed promising early results with the commissioning of its first giga-factory for solar panels.",
    source: "Economic Times",
    sourceUrl: "https://economictimes.com",
    category: "Earnings",
    date: "2025-03-27",
    sentiment: "positive",
    relatedCompanies: ["RELIANCE"],
    tags: ["Earnings", "Q3 Results", "Retail", "Jio"],
  },
  {
    id: "2",
    title: "TCS Wins $2.5 Billion Deal from Major European Bank for Digital Transformation",
    summary: "Tata Consultancy Services has secured its largest-ever deal worth $2.5 billion from a leading European financial institution for a comprehensive digital transformation spanning 7 years.",
    fullContent: "Tata Consultancy Services (TCS), India's largest IT services company, announced the signing of a landmark $2.5 billion contract with one of Europe's top five banks. The deal, spanning seven years, involves a complete overhaul of the bank's legacy systems, migration to cloud-native architecture, and implementation of AI-powered customer service solutions.\n\nThis represents the single largest deal in TCS's history and underscores the growing demand for digital transformation in the banking sector. The engagement will involve over 15,000 TCS consultants across multiple geographies.\n\nAnalysts view this positively for TCS's revenue visibility and expect it to significantly boost the company's European revenue contribution from the current 32% to approximately 38% over the deal tenure.",
    source: "Moneycontrol",
    sourceUrl: "https://moneycontrol.com",
    category: "Deals",
    date: "2025-03-26",
    sentiment: "positive",
    relatedCompanies: ["TCS"],
    tags: ["IT Services", "Deal Win", "Digital Transformation"],
  },
  {
    id: "3",
    title: "HDFC Bank's NPA Rises Marginally; Management Attributes to Seasonal Factors",
    summary: "HDFC Bank reported a slight uptick in gross NPAs to 1.35% from 1.26% in the previous quarter. The bank's management cited seasonal agricultural stress and merger-related portfolio adjustments.",
    fullContent: "HDFC Bank, India's largest private sector lender, reported a marginal increase in its gross non-performing assets (GNPA) ratio to 1.35% for Q3 FY25, compared to 1.26% in the preceding quarter. The net NPA stood at 0.38%, up from 0.31%.\n\nManagement attributed the rise to seasonal factors affecting the agricultural loan portfolio and ongoing adjustments in the merged HDFC Limited's housing loan book. CEO Sashidhar Jagdishan stated that the bank sees this as a temporary blip and expects credit quality to normalize by Q1 FY26.\n\nDespite the NPA uptick, the bank's net interest income grew 8% YoY to ₹30,100 crore, and net profit rose 6% to ₹16,735 crore. The bank maintained its credit-deposit ratio target and guided for stable margins ahead.",
    source: "LiveMint",
    sourceUrl: "https://livemint.com",
    category: "Banking",
    date: "2025-03-25",
    sentiment: "negative",
    relatedCompanies: ["HDFCBANK"],
    tags: ["Banking", "NPA", "Credit Quality"],
  },
  {
    id: "4",
    title: "Infosys Raises FY25 Revenue Guidance on Strong Deal Pipeline",
    summary: "Infosys has revised its FY25 revenue growth guidance upward to 5.5-6% from the earlier 4-5%, citing robust demand in financial services and manufacturing verticals.",
    fullContent: "Infosys, India's second-largest IT services company, has raised its full-year revenue growth guidance for FY25 to 5.5-6% in constant currency terms, up from the previous range of 4-5%. The revision comes on the back of a strong deal pipeline worth $12.2 billion in total contract value (TCV) signed during Q3.\n\nCEO Salil Parekh highlighted that the company is seeing broad-based demand recovery across geographies, with particularly strong traction in financial services, manufacturing, and retail verticals. The company's AI and automation practice has also seen a 40% increase in deal inquiries.\n\nOperating margins expanded by 50 basis points to 21.3%, aided by operational efficiencies and a favorable currency mix. The company declared an interim dividend of ₹18 per share.",
    source: "Business Standard",
    sourceUrl: "https://business-standard.com",
    category: "Earnings",
    date: "2025-03-24",
    sentiment: "positive",
    relatedCompanies: ["INFY"],
    tags: ["IT Services", "Guidance", "Revenue Growth"],
  },
  {
    id: "5",
    title: "Adani Group Announces ₹80,000 Crore Investment in Green Hydrogen",
    summary: "Adani Green Energy has unveiled an ambitious plan to invest ₹80,000 crore over the next 5 years in green hydrogen production, targeting 1 million tonnes annual capacity by 2030.",
    fullContent: "Adani Green Energy Limited announced a massive ₹80,000 crore ($9.6 billion) investment plan for green hydrogen production facilities across India. The phased investment, spanning 2025-2030, aims to establish India as a global leader in the emerging green hydrogen economy.\n\nThe first phase, involving ₹20,000 crore, will see the construction of a 250,000-tonne-per-annum electrolyzer facility in Mundra, Gujarat, expected to be operational by early 2027. Subsequent phases will establish production units in Rajasthan and Tamil Nadu.\n\nChairman Gautam Adani stated that green hydrogen represents the next frontier in India's energy transition and that the group is committed to making India self-sufficient in clean energy. The company has already secured off-take agreements with two major European industrial conglomerates.",
    source: "CNBC-TV18",
    sourceUrl: "https://cnbctv18.com",
    category: "Energy",
    date: "2025-03-23",
    sentiment: "positive",
    relatedCompanies: ["ADANIENT"],
    tags: ["Green Energy", "Hydrogen", "Investment"],
  },
  {
    id: "6",
    title: "Wipro Faces Margin Pressure Amid Rising Attrition in Digital Services",
    summary: "Wipro's operating margins contracted by 80bps to 14.8% as the company grapples with rising attrition in its high-margin digital services unit, now at 19.2%.",
    fullContent: "Wipro Limited reported a contraction in its IT services operating margin to 14.8% for Q3 FY25, down 80 basis points sequentially and 120 basis points year-on-year. The decline was primarily driven by rising attrition in the company's digital and cloud transformation practice, which touched 19.2%.\n\nThe company reported Q3 revenue of ₹23,200 crore, a modest 3.2% YoY growth in constant currency. Deal bookings were encouraging at $3.8 billion TCV, but the execution was hampered by talent challenges.\n\nCEO Srini Pallia acknowledged the margin headwinds and outlined a multi-pronged strategy including enhanced retention packages, accelerated freshers onboarding, and greater use of AI tools to improve delivery efficiency. The company maintains its Q4 guidance of 1-3% sequential revenue growth.",
    source: "Financial Express",
    sourceUrl: "https://financialexpress.com",
    category: "Earnings",
    date: "2025-03-22",
    sentiment: "negative",
    relatedCompanies: ["WIPRO"],
    tags: ["IT Services", "Margins", "Attrition"],
  },
  {
    id: "7",
    title: "SBI Reports Highest-Ever Quarterly Profit; Asset Quality Improves Significantly",
    summary: "State Bank of India posted its best-ever quarterly profit of ₹19,200 crore with GNPA declining to 2.07%, the lowest in over a decade, reflecting strong recovery and prudent lending.",
    fullContent: "State Bank of India, the country's largest lender, reported a record net profit of ₹19,200 crore for Q3 FY25, surging 28% year-on-year. The stellar performance was driven by robust net interest income growth of 14% and significant improvement in asset quality.\n\nGross NPAs declined to 2.07% from 2.55% a year ago, marking the lowest level in over a decade. Net NPAs stood at a healthy 0.53%. The bank's provision coverage ratio improved to 93.5%.\n\nChairman Dinesh Khara attributed the strong results to disciplined lending practices, digital transformation initiatives, and improved recovery from legacy stressed accounts. The bank's YONO digital platform now serves over 70 million users, contributing to lower customer acquisition costs.",
    source: "Reuters India",
    sourceUrl: "https://reuters.com",
    category: "Banking",
    date: "2025-03-21",
    sentiment: "positive",
    relatedCompanies: ["SBIN"],
    tags: ["Banking", "Record Profit", "Asset Quality"],
  },
  {
    id: "8",
    title: "Tata Motors EV Sales Surge 145% as Nexon EV Dominates Market",
    summary: "Tata Motors' electric vehicle division recorded 145% YoY sales growth in Q3, with the Nexon EV commanding a 62% market share in the passenger EV segment.",
    fullContent: "Tata Motors reported a remarkable 145% year-on-year growth in its electric vehicle sales during Q3 FY25, selling over 65,000 EVs in the quarter. The Nexon EV continued to dominate the Indian passenger EV market with a commanding 62% market share.\n\nThe company also launched the Curvv EV during the quarter, which received over 30,000 bookings within the first month. The EV business, while still loss-making, has seen significant improvement in unit economics with losses narrowing to ₹1.5 lakh per vehicle from ₹3.2 lakh a year ago.\n\nManagement guided that the EV business is on track to achieve breakeven by H2 FY26, supported by scale benefits and declining battery costs. The company's Sanand plant, dedicated to EV production, is now operating at 85% capacity.",
    source: "Auto Economic Times",
    sourceUrl: "https://auto.economictimes.com",
    category: "Automobile",
    date: "2025-03-20",
    sentiment: "positive",
    relatedCompanies: ["TATAMOTORS"],
    tags: ["EV", "Auto Sales", "Market Share"],
  },
];

export const companyStocks: CompanyStock[] = [
  { symbol: "RELIANCE", name: "Reliance Industries", price: 2456.30, change: 29.50, changePercent: 1.2, sector: "Conglomerate", marketCap: "₹16.6L Cr", pe: 28.5, high52w: 2856.15, low52w: 2180.00, volume: "12.5M" },
  { symbol: "TCS", name: "Tata Consultancy Services", price: 3245.80, change: -26.40, changePercent: -0.8, sector: "IT", marketCap: "₹11.8L Cr", pe: 32.1, high52w: 3890.00, low52w: 3050.60, volume: "4.2M" },
  { symbol: "INFY", name: "Infosys", price: 1567.45, change: 32.80, changePercent: 2.1, sector: "IT", marketCap: "₹6.5L Cr", pe: 26.8, high52w: 1780.00, low52w: 1310.50, volume: "8.7M" },
  { symbol: "HDFCBANK", name: "HDFC Bank", price: 1623.90, change: 8.10, changePercent: 0.5, sector: "Banking", marketCap: "₹12.3L Cr", pe: 19.4, high52w: 1794.00, low52w: 1363.55, volume: "6.1M" },
  { symbol: "ICICIBANK", name: "ICICI Bank", price: 987.60, change: -12.80, changePercent: -1.3, sector: "Banking", marketCap: "₹6.9L Cr", pe: 17.2, high52w: 1120.00, low52w: 890.25, volume: "9.3M" },
  { symbol: "WIPRO", name: "Wipro", price: 412.75, change: 7.35, changePercent: 1.8, sector: "IT", marketCap: "₹2.2L Cr", pe: 22.6, high52w: 512.40, low52w: 370.15, volume: "5.8M" },
  { symbol: "BHARTIARTL", name: "Bharti Airtel", price: 1345.20, change: 12.10, changePercent: 0.9, sector: "Telecom", marketCap: "₹8.0L Cr", pe: 42.3, high52w: 1560.00, low52w: 1100.80, volume: "3.4M" },
  { symbol: "ITC", name: "ITC Limited", price: 465.30, change: -1.85, changePercent: -0.4, sector: "FMCG", marketCap: "₹5.8L Cr", pe: 24.1, high52w: 510.00, low52w: 398.20, volume: "7.2M" },
  { symbol: "SBIN", name: "State Bank of India", price: 623.15, change: 15.60, changePercent: 2.5, sector: "Banking", marketCap: "₹5.6L Cr", pe: 9.8, high52w: 710.00, low52w: 542.00, volume: "15.1M" },
  { symbol: "TATAMOTORS", name: "Tata Motors", price: 765.40, change: -13.20, changePercent: -1.7, sector: "Automobile", marketCap: "₹2.8L Cr", pe: 8.5, high52w: 920.00, low52w: 610.30, volume: "11.2M" },
  { symbol: "ADANIENT", name: "Adani Enterprises", price: 2890.50, change: 89.60, changePercent: 3.1, sector: "Conglomerate", marketCap: "₹3.3L Cr", pe: 78.2, high52w: 3480.00, low52w: 2140.00, volume: "6.9M" },
  { symbol: "BAJFINANCE", name: "Bajaj Finance", price: 6780.25, change: -40.70, changePercent: -0.6, sector: "NBFC", marketCap: "₹4.2L Cr", pe: 35.6, high52w: 7850.00, low52w: 5980.00, volume: "2.1M" },
  { symbol: "HCLTECH", name: "HCL Technologies", price: 1289.50, change: 18.30, changePercent: 1.4, sector: "IT", marketCap: "₹3.5L Cr", pe: 24.7, high52w: 1460.00, low52w: 1080.25, volume: "3.8M" },
  { symbol: "SUNPHARMA", name: "Sun Pharmaceutical", price: 1145.60, change: -8.90, changePercent: -0.8, sector: "Pharma", marketCap: "₹2.7L Cr", pe: 31.2, high52w: 1310.00, low52w: 945.00, volume: "4.5M" },
  { symbol: "LT", name: "Larsen & Toubro", price: 3456.70, change: 42.30, changePercent: 1.2, sector: "Infrastructure", marketCap: "₹4.7L Cr", pe: 33.8, high52w: 3800.00, low52w: 2890.40, volume: "2.8M" },
  { symbol: "HINDUNILVR", name: "Hindustan Unilever", price: 2567.80, change: -15.40, changePercent: -0.6, sector: "FMCG", marketCap: "₹6.0L Cr", pe: 58.3, high52w: 2890.00, low52w: 2210.00, volume: "1.9M" },
];

export const regulatoryData: RegulatoryItem[] = [
  {
    id: "r1",
    title: "RBI Keeps Repo Rate Unchanged at 6.5% for Eighth Consecutive Time",
    summary: "The Reserve Bank of India maintained its benchmark repo rate at 6.5% in its February 2025 monetary policy review, citing persistent food inflation concerns while acknowledging improving core inflation trends.",
    fullContent: "The six-member Monetary Policy Committee (MPC) of the Reserve Bank of India voted 4-2 to keep the repo rate unchanged at 6.5% for the eighth consecutive meeting. Governor Shaktikanta Das highlighted that while core inflation has moderated to 3.8%, food inflation remains elevated at 8.2%, driven by vegetable and pulse prices.\n\nThe MPC maintained its stance of 'withdrawal of accommodation' and revised its FY25 GDP growth projection upward to 7.2% from 7.0%, while keeping the inflation forecast at 4.5%. The central bank also announced measures to improve liquidity in the banking system through variable rate repo operations.\n\nKey regulatory announcements included:\n- Enhancement of UPI transaction limits for select categories\n- New guidelines for digital lending platforms\n- Framework for self-regulatory organizations in the fintech space\n- Revised norms for priority sector lending classification",
    source: "RBI Official",
    sourceUrl: "https://rbi.org.in",
    category: "Monetary Policy",
    date: "2025-03-15",
    impact: "high",
    tags: ["RBI", "Repo Rate", "Monetary Policy", "Inflation"],
  },
  {
    id: "r2",
    title: "SEBI Introduces New Regulations for Algorithmic Trading in Retail Segment",
    summary: "SEBI has issued comprehensive guidelines for algorithmic trading by retail investors, mandating registration, audit trails, and risk controls to ensure market integrity and investor protection.",
    fullContent: "The Securities and Exchange Board of India (SEBI) has released a circular introducing a framework for algorithmic trading in the retail segment. The new regulations, effective from April 1, 2025, aim to democratize algo trading while maintaining market stability.\n\nKey provisions include:\n1. All algorithmic orders must be tagged with a unique identifier\n2. Brokers must register each algorithm with the exchange\n3. Kill switch capability mandatory for all algo systems\n4. Maximum order rate limits of 10 orders per second per user\n5. Mandatory audit trail maintenance for 7 years\n6. Risk management framework including daily loss limits\n\nSEBI Chairman Madhabi Puri Buch stated that these regulations balance innovation with investor protection. Brokers have been given a 6-month transition period to comply with all requirements.",
    source: "SEBI",
    sourceUrl: "https://sebi.gov.in",
    category: "Market Regulation",
    date: "2025-03-12",
    impact: "high",
    tags: ["SEBI", "Algo Trading", "Regulation", "Market Structure"],
  },
  {
    id: "r3",
    title: "Union Budget 2025-26: Key Highlights for Financial Markets",
    summary: "The Union Budget introduced changes to capital gains taxation, expanded tax benefits for NPS, and announced a ₹10,000 crore fund for fintech innovation.",
    fullContent: "Finance Minister Nirmala Sitharaman presented the Union Budget 2025-26 with several provisions impacting financial markets:\n\n**Capital Gains Tax Changes:**\n- Long-term capital gains exemption limit increased from ₹1 lakh to ₹1.5 lakh\n- Short-term capital gains tax on listed securities reduced from 15% to 12.5%\n- Holding period for debt mutual funds reduced to 2 years for LTCG eligibility\n\n**Investment Incentives:**\n- NPS employer contribution deduction increased from 10% to 14% of salary\n- New tax-saving infrastructure bonds with ₹50,000 additional deduction\n- Sovereign Gold Bond program expanded with quarterly issuances\n\n**Fintech & Digital:**\n- ₹10,000 crore Digital Finance Innovation Fund announced\n- Tax holidays for fintech startups extended by 2 years\n- Regulatory sandbox framework enhanced for blockchain applications\n\n**Market Infrastructure:**\n- GIFT City incentives expanded to attract more financial services\n- Single-window clearance for FPI registrations\n- Enhanced framework for REITs and InvITs",
    source: "Ministry of Finance",
    sourceUrl: "https://finmin.nic.in",
    category: "Budget",
    date: "2025-02-01",
    impact: "high",
    tags: ["Budget", "Capital Gains", "Tax", "Fintech"],
  },
  {
    id: "r4",
    title: "RBI Releases Draft Guidelines on Expected Credit Loss Framework for Banks",
    summary: "RBI has proposed transitioning from the current incurred loss model to an expected credit loss (ECL) framework for loan provisioning, aligning Indian banks with global standards.",
    fullContent: "The Reserve Bank of India published draft guidelines on the implementation of the Expected Credit Loss (ECL) framework for all scheduled commercial banks, effective from April 2026. This transition from the current incurred loss model to ECL will align Indian banking practices with IFRS 9 and global best practices.\n\nKey highlights:\n- Banks must classify financial assets into three stages based on credit quality\n- Stage 1: 12-month ECL for performing assets\n- Stage 2: Lifetime ECL for assets with significant increase in credit risk\n- Stage 3: Lifetime ECL for credit-impaired assets\n- Advanced statistical models required for probability of default estimation\n- Parallel run period of one year before full implementation\n\nThe banking industry estimates this could require additional provisioning of ₹50,000-70,000 crore across the system. Large banks like SBI, HDFC Bank, and ICICI Bank have already started pilot implementations.",
    source: "RBI Official",
    sourceUrl: "https://rbi.org.in",
    category: "Banking Regulation",
    date: "2025-03-01",
    impact: "medium",
    tags: ["RBI", "ECL", "Banking", "Provisioning"],
  },
  {
    id: "r5",
    title: "IRDAI Revises Investment Guidelines for Insurance Companies",
    summary: "Insurance regulator IRDAI has liberalized investment norms, allowing insurers to invest up to 10% in alternative investment funds and increasing the equity allocation limit.",
    fullContent: "The Insurance Regulatory and Development Authority of India (IRDAI) has issued revised investment guidelines for life and general insurance companies, effective immediately. The key changes aim to provide insurers greater flexibility in portfolio construction.\n\nMajor changes:\n- Equity investment limit increased from 50% to 60% for unit-linked plans\n- Alternative Investment Fund (AIF) allocation permitted up to 10% of total assets\n- Infrastructure debt fund investments given priority sector treatment\n- Real estate investment through REITs allowed up to 5%\n- ESG-compliant investments to receive favorable risk weight treatment\n- Overseas investment limit increased from 10% to 15%\n\nThe revised norms are expected to channel an additional ₹2-3 lakh crore into equity markets over the next 3-5 years as insurance companies rebalance their portfolios.",
    source: "IRDAI",
    sourceUrl: "https://irdai.gov.in",
    category: "Insurance Regulation",
    date: "2025-02-20",
    impact: "medium",
    tags: ["IRDAI", "Insurance", "Investment Guidelines"],
  },
];

export interface MarketInsightItem {
  id: string;
  title: string;
  summary: string;
  fullContent: string;
  source: string;
  sourceUrl: string;
  category: string;
  date: string;
  sentiment: "positive" | "negative" | "neutral";
  tags: string[];
}

export const marketInsights: MarketInsightItem[] = [
  {
    id: "m1",
    title: "Nifty 50 Hits All-Time High; IT and Banking Lead Rally",
    summary: "The benchmark Nifty 50 index surged past 23,500 for the first time, driven by strong buying in IT and banking heavyweights. FII inflows of ₹12,000 crore in the past week fueled the rally.",
    fullContent: "The benchmark Nifty 50 index marked a historic milestone on Friday, surging past the 23,500 mark for the first time. The rally was primarily driven by strong buying interest in heavyweight IT and banking stocks following positive global cues.\n\nForeign Institutional Investors (FIIs) have been net buyers, infusing over ₹12,000 crore in the past week alone, signaling robust confidence in the Indian macroeconomic fundamentals. Analysts expect the momentum to continue as corporate earnings for the upcoming quarter look promising.",
    source: "Bloomberg Quint",
    sourceUrl: "https://bloombergquint.com",
    category: "Market Rally",
    date: "2025-03-28",
    sentiment: "positive",
    tags: ["Nifty 50", "Stock Market", "FII", "Banking"],
  },
  {
    id: "m2",
    title: "Crude Oil Drops Below $70; Positive for Indian Markets",
    summary: "Brent crude oil prices fell below $70 per barrel for the first time in 6 months, providing relief to India's import bill and expected to positively impact inflation and fiscal deficit targets.",
    fullContent: "Global Brent crude oil prices have fallen below the critical $70 per barrel mark for the first time in six months. This decline is largely attributed to weakening demand forecasts from major economies and increased production from non-OPEC countries.\n\nFor India, which imports over 80% of its crude oil requirements, this drop is a significant positive. It provides much-needed relief to the country's import bill, easing pressure on the current account deficit. Economists predict this will also have a favorable impact on domestic inflation, potentially giving the RBI more room to maneuver monetary policy.",
    source: "Reuters",
    sourceUrl: "https://reuters.com",
    category: "Commodities",
    date: "2025-03-27",
    sentiment: "positive",
    tags: ["Crude Oil", "Commodities", "Inflation", "Macro Economy"],
  },
  {
    id: "m3",
    title: "Small-Cap Index Corrects 8% from Peak; Analysts Advise Caution",
    summary: "The Nifty Small-Cap 250 index has corrected 8% from its recent peak, with valuations still stretched at 28x forward earnings. Analysts recommend selective stock-picking over broad allocation.",
    fullContent: "The Nifty Small-Cap 250 index has witnessed a correction of approximately 8% from its recent peak, indicating profit-booking by domestic institutional investors and retail participants. Despite the correction, the index is still trading at a stretched valuation of 28x forward earnings.\n\nMarket analysts and fund managers are advising caution, suggesting that investors should pivot towards selective stock-picking rather than maintaining a broad-based allocation in the small-cap space. Companies with strong balance sheets and clear earnings visibility are preferred in the current environment.",
    source: "Moneycontrol",
    sourceUrl: "https://moneycontrol.com",
    category: "Market Correction",
    date: "2025-03-26",
    sentiment: "negative",
    tags: ["Small Caps", "Correction", "Valuation", "Stock Market"],
  },
  {
    id: "m4",
    title: "Rupee Strengthens to 82.50 Against Dollar on FII Inflows",
    summary: "The Indian rupee appreciated to 82.50 against the US dollar, its strongest level in 3 months, supported by sustained FII equity inflows and a weakening dollar index.",
    fullContent: "The Indian rupee has shown significant strength, appreciating to 82.50 against the US dollar, marking its strongest level in the past three months. The appreciation is primarily supported by sustained foreign institutional investor (FII) inflows into Indian equities and debt markets.\n\nAdditionally, a weakening US dollar index in the global markets has provided further tailwinds for the domestic currency. A stronger rupee is expected to lower the cost of imported goods, further aiding in the containment of domestic inflation.",
    source: "LiveMint",
    sourceUrl: "https://livemint.com",
    category: "Currency",
    date: "2025-03-25",
    sentiment: "positive",
    tags: ["Currency", "INR", "USD", "FII"],
  },
  {
    id: "m5",
    title: "Gold Prices Surge Past ₹72,000 Per 10 Grams on Global Uncertainty",
    summary: "Domestic gold prices reached a new all-time high of ₹72,300 per 10 grams, driven by geopolitical tensions and central bank buying globally. Silver also rallied to ₹85,000 per kg.",
    fullContent: "Domestic gold prices have surged to a new all-time high, crossing the ₹72,000 mark to reach ₹72,300 per 10 grams in the retail market. This rally is largely driven by escalating geopolitical tensions in the Middle East and strong, continuous buying by central banks globally as a safe-haven asset.\n\nFollowing the trend in gold, silver prices have also seen a sharp rally, crossing ₹85,000 per kilogram. Market experts suggest that as long as global uncertainties persist, precious metals will continue to find strong support at lower levels.",
    source: "Economic Times",
    sourceUrl: "https://economictimes.com",
    category: "Commodities",
    date: "2025-03-24",
    sentiment: "neutral",
    tags: ["Gold", "Silver", "Commodities", "Safe Haven"],
  },
  {
    id: "m6",
    title: "FPI Net Buyers for Third Consecutive Month; Invest ₹35,000 Crore in March",
    summary: "Foreign Portfolio Investors remained net buyers in Indian equities for the third consecutive month, investing ₹35,000 crore in March so far, signaling renewed confidence in India's growth story.",
    fullContent: "Foreign Portfolio Investors (FPIs) have remained robust net buyers of Indian equities for the third consecutive month, injecting over ₹35,000 crore in March alone. This sustained inflow signals renewed and growing confidence in India's macroeconomic stability and growth narrative among global investors.\n\nThe inflows have been broad-based, with significant investments directed towards the financial services, capital goods, and automobile sectors. This strong FPI participation is a key factor supporting the current resilience and upward momentum of the benchmark indices.",
    source: "Business Standard",
    sourceUrl: "https://business-standard.com",
    category: "FII Activity",
    date: "2025-03-23",
    sentiment: "positive",
    tags: ["FPI", "FII", "Investment", "Equities"],
  },
];

export const samplePortfolio: PortfolioStock[] = [
  { symbol: "RELIANCE", name: "Reliance Industries", quantity: 25, avgPrice: 2200.00, currentPrice: 2456.30, sector: "Conglomerate" },
  { symbol: "TCS", name: "Tata Consultancy Services", quantity: 15, avgPrice: 3100.50, currentPrice: 3245.80, sector: "IT" },
  { symbol: "HDFCBANK", name: "HDFC Bank", quantity: 30, avgPrice: 1500.00, currentPrice: 1623.90, sector: "Banking" },
  { symbol: "INFY", name: "Infosys", quantity: 40, avgPrice: 1420.00, currentPrice: 1567.45, sector: "IT" },
  { symbol: "ITC", name: "ITC Limited", quantity: 100, avgPrice: 420.00, currentPrice: 465.30, sector: "FMCG" },
  { symbol: "SBIN", name: "State Bank of India", quantity: 50, avgPrice: 560.00, currentPrice: 623.15, sector: "Banking" },
  { symbol: "BHARTIARTL", name: "Bharti Airtel", quantity: 20, avgPrice: 1200.00, currentPrice: 1345.20, sector: "Telecom" },
  { symbol: "TATAMOTORS", name: "Tata Motors", quantity: 35, avgPrice: 700.00, currentPrice: 765.40, sector: "Automobile" },
];

export const candlestickData = [
  { date: "Mar 01", open: 2380, high: 2420, low: 2365, close: 2410 },
  { date: "Mar 04", open: 2410, high: 2445, low: 2395, close: 2430 },
  { date: "Mar 05", open: 2430, high: 2460, low: 2415, close: 2420 },
  { date: "Mar 06", open: 2420, high: 2455, low: 2400, close: 2450 },
  { date: "Mar 07", open: 2450, high: 2480, low: 2435, close: 2440 },
  { date: "Mar 10", open: 2440, high: 2470, low: 2420, close: 2465 },
  { date: "Mar 11", open: 2465, high: 2490, low: 2450, close: 2475 },
  { date: "Mar 12", open: 2475, high: 2500, low: 2460, close: 2485 },
  { date: "Mar 13", open: 2485, high: 2510, low: 2470, close: 2460 },
  { date: "Mar 14", open: 2460, high: 2480, low: 2440, close: 2470 },
  { date: "Mar 17", open: 2470, high: 2495, low: 2455, close: 2490 },
  { date: "Mar 18", open: 2490, high: 2520, low: 2475, close: 2505 },
  { date: "Mar 19", open: 2505, high: 2530, low: 2490, close: 2480 },
  { date: "Mar 20", open: 2480, high: 2500, low: 2460, close: 2495 },
  { date: "Mar 21", open: 2495, high: 2525, low: 2480, close: 2510 },
  { date: "Mar 24", open: 2510, high: 2540, low: 2495, close: 2530 },
  { date: "Mar 25", open: 2530, high: 2555, low: 2515, close: 2520 },
  { date: "Mar 26", open: 2520, high: 2550, low: 2505, close: 2545 },
  { date: "Mar 27", open: 2545, high: 2570, low: 2530, close: 2555 },
  { date: "Mar 28", open: 2555, high: 2580, low: 2540, close: 2456 },
];

export const sectorAllocation = [
  { name: "IT", value: 30, color: "hsl(var(--chart-blue))" },
  { name: "Banking", value: 25, color: "hsl(var(--chart-green))" },
  { name: "Conglomerate", value: 18, color: "hsl(var(--chart-amber))" },
  { name: "FMCG", value: 10, color: "hsl(var(--chart-purple))" },
  { name: "Telecom", value: 9, color: "hsl(var(--chart-red))" },
  { name: "Automobile", value: 8, color: "hsl(160, 60%, 50%)" },
];
