/**
 * cashFlowCalculator.ts
 * ============================================================================
 * Production-Ready Cash Flow & Runway Calculation Engine
 * 
 * Implements standard financial statement accounting principles:
 * 1. Net Cash Flow = Operating CF + Investing CF + Financing CF
 * 2. Ending Cash = Beginning Cash + Net Cash Flow
 * 3. Period-over-period compounding & running cumulative balances
 * 4. Exact runway exhaustion & average burn rate modeling
 * 5. Break-even month detection & contribution margin requirement
 * 6. Real-time sensitivity scenarios (+/- 10%)
 * ============================================================================
 */

export interface CashFlowInputs {
  startingCash: number;            // Opening bank balance
  monthlyRevenue: number;          // Base month 1 revenue
  revenueGrowthRatePct: number;    // % monthly compound growth
  fixedCosts: number;              // Monthly rent, payroll, SaaS, insurance
  variableCostPct: number;         // % of revenue (direct COGS)
  oneTimeCapex: number;            // One-time capital expenditure / equipment
  capexMonth: number;              // 1-indexed month CapEx occurs
  fundingInflows: number;          // Equity / angel / grant injections
  fundingMonth: number;            // 1-indexed month funding lands
  loanRepayments: number;          // Monthly debt service (principal + interest)
  projectionMonths: 12 | 24 | 36;  // Horizon length
  startDate?: Date;                // Base date for period labeling
}

export interface PeriodRecord {
  periodIndex: number;
  periodLabel: string;
  
  // 1. Operating Cash Flow (OCF)
  revenue: number;
  fixedCosts: number;
  variableCosts: number;
  totalOperatingCosts: number;
  operatingCf: number;
  
  // 2. Investing Cash Flow (ICF)
  capex: number;
  investingCf: number;
  
  // 3. Financing Cash Flow (FCF)
  fundingInflow: number;
  loanRepayment: number;
  financingCf: number;
  
  // 4. Net Change & Balances
  netCashFlow: number;
  beginningCash: number;
  endingCash: number;
  isCashExhausted: boolean;
  isOperatingBreakeven: boolean;
  isNetPositive: boolean;
}

export interface ModelSummary {
  startingCash: number;
  endingCash: number;
  minCashBalance: number;
  minCashMonth: string;
  runwayMonths: number | null;     // null indicates infinite/perpetual runway
  isRunwayInfinite: boolean;
  averageMonthlyBurn: number;
  averageMonthlyNet: number;
  breakevenMonth: number | null;
  breakevenLabel: string | null;
  breakevenRevenueNeeded: number;
  totalRevenueProjected: number;
  totalOperatingCf: number;
  totalNetCf: number;
}

export interface SensitivityResults {
  base: { records: PeriodRecord[]; summary: ModelSummary };
  conservative: { records: PeriodRecord[]; summary: ModelSummary };
  optimistic: { records: PeriodRecord[]; summary: ModelSummary };
}

/**
 * Pure calculation function for monthly cash flow modeling.
 * Fully deterministic with zero side-effects (<1ms execution time).
 */
export function calculateMonthlyCashFlow(inputs: CashFlowInputs): {
  records: PeriodRecord[];
  summary: ModelSummary;
} {
  const baseDate = inputs.startDate || new Date();
  const months = Math.max(1, Math.min(120, inputs.projectionMonths));
  
  const growthMultiplier = 1.0 + inputs.revenueGrowthRatePct / 100.0;
  const varCostRate = Math.max(0.0, Math.min(1.0, inputs.variableCostPct / 100.0));
  
  const records: PeriodRecord[] = [];
  let currentCash = inputs.startingCash;
  
  const burnAmounts: number[] = [];
  let breakevenMonthIdx: number | null = null;
  let breakevenLabel: string | null = null;
  let exhaustionMonth: number | null = null;
  
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  
  for (let m = 1; m <= months; m++) {
    const periodDate = new Date(baseDate.getFullYear(), baseDate.getMonth() + (m - 1), 1);
    const periodLabel = `${monthNames[periodDate.getMonth()]} ${periodDate.getFullYear()}`;
    
    // 1. Operating Cash Flow
    const rev = Number((inputs.monthlyRevenue * Math.pow(growthMultiplier, m - 1)).toFixed(2));
    const fixed = Number(inputs.fixedCosts.toFixed(2));
    const varCosts = Number((rev * varCostRate).toFixed(2));
    const totalOps = Number((fixed + varCosts).toFixed(2));
    const ocf = Number((rev - totalOps).toFixed(2));
    
    // 2. Investing Cash Flow
    const capex = m === inputs.capexMonth ? Number(inputs.oneTimeCapex.toFixed(2)) : 0.0;
    const icf = -capex;
    
    // 3. Financing Cash Flow
    const funding = m === inputs.fundingMonth ? Number(inputs.fundingInflows.toFixed(2)) : 0.0;
    const loanPmt = Number(inputs.loanRepayments.toFixed(2));
    const fcf = Number((funding - loanPmt).toFixed(2));
    
    // 4. Net Change & Balances (Strict Accounting Invariant)
    const netCf = Number((ocf + icf + fcf).toFixed(2));
    const beginningCash = Number(currentCash.toFixed(2));
    const endingCash = Number((beginningCash + netCf).toFixed(2));
    currentCash = endingCash;
    
    const isExhausted = endingCash <= 0;
    if (isExhausted && exhaustionMonth === null) {
      exhaustionMonth = m;
    }
    
    const isOpBe = ocf >= 0;
    const isNetPos = netCf >= 0;
    
    if (isOpBe && isNetPos && breakevenMonthIdx === null) {
      breakevenMonthIdx = m;
      breakevenLabel = `Month ${m} (${periodLabel})`;
    }
    
    if (netCf < 0) {
      burnAmounts.push(Math.abs(netCf));
    }
    
    records.push({
      periodIndex: m,
      periodLabel,
      revenue: Number(rev.toFixed(2)),
      fixedCosts: Number(fixed.toFixed(2)),
      variableCosts: Number(varCosts.toFixed(2)),
      totalOperatingCosts: Number(totalOps.toFixed(2)),
      operatingCf: Number(ocf.toFixed(2)),
      capex: Number(capex.toFixed(2)),
      investingCf: Number(icf.toFixed(2)),
      fundingInflow: Number(funding.toFixed(2)),
      loanRepayment: Number(loanPmt.toFixed(2)),
      financingCf: Number(fcf.toFixed(2)),
      netCashFlow: Number(netCf.toFixed(2)),
      beginningCash: Number(beginningCash.toFixed(2)),
      endingCash: Number(endingCash.toFixed(2)),
      isCashExhausted: isExhausted,
      isOperatingBreakeven: isOpBe,
      isNetPositive: isNetPos
    });
  }
  
  // Summary Metrics
  const endingCashAll = records[records.length - 1].endingCash;
  let minRec = records[0];
  for (const r of records) {
    if (r.endingCash < minRec.endingCash) minRec = r;
  }
  
  const avgBurn = burnAmounts.length > 0 ? burnAmounts.reduce((a, b) => a + b, 0) / burnAmounts.length : 0.0;
  const totalNet = records.reduce((sum, r) => sum + r.netCashFlow, 0);
  const avgNet = totalNet / records.length;
  
  let runwayMonths: number | null = null;
  let isRunwayInfinite = false;
  
  if (exhaustionMonth !== null) {
    runwayMonths = exhaustionMonth;
    isRunwayInfinite = false;
  } else if (avgBurn > 0 && avgNet < 0) {
    runwayMonths = Math.floor(inputs.startingCash / avgBurn);
    isRunwayInfinite = false;
  } else {
    runwayMonths = null;
    isRunwayInfinite = true;
  }
  
  const contributionMarginRatio = 1.0 - varCostRate;
  const beRevenueNeeded = contributionMarginRatio > 0 ? inputs.fixedCosts / contributionMarginRatio : 0.0;
  
  const summary: ModelSummary = {
    startingCash: inputs.startingCash,
    endingCash: endingCashAll,
    minCashBalance: minRec.endingCash,
    minCashMonth: minRec.periodLabel,
    runwayMonths,
    isRunwayInfinite,
    averageMonthlyBurn: Number(avgBurn.toFixed(2)),
    averageMonthlyNet: Number(avgNet.toFixed(2)),
    breakevenMonth: breakevenMonthIdx,
    breakevenLabel,
    breakevenRevenueNeeded: Number(beRevenueNeeded.toFixed(2)),
    totalRevenueProjected: Number(records.reduce((sum, r) => sum + r.revenue, 0).toFixed(2)),
    totalOperatingCf: Number(records.reduce((sum, r) => sum + r.operatingCf, 0).toFixed(2)),
    totalNetCf: Number(totalNet.toFixed(2))
  };
  
  return { records, summary };
}

/**
 * Aggregates monthly projections into Quarterly or Annual views.
 */
export function aggregateCashFlow(
  records: PeriodRecord[],
  frequency: "monthly" | "quarterly" | "yearly"
) {
  if (frequency === "monthly" || records.length === 0) return records;
  
  const chunkSize = frequency === "quarterly" ? 3 : 12;
  const aggregated = [];
  
  for (let i = 0; i < records.length; i += chunkSize) {
    const chunk = records.slice(i, i + chunkSize);
    if (chunk.length === 0) continue;
    
    const groupNum = Math.floor(i / chunkSize) + 1;
    const label = frequency === "quarterly"
      ? `Q${groupNum} (${chunk[0].periodLabel.slice(0, 3)} - ${chunk[chunk.length - 1].periodLabel})`
      : `Year ${groupNum} (${chunk[0].periodLabel} - ${chunk[chunk.length - 1].periodLabel})`;
      
    const begCash = chunk[0].beginningCash;
    const endCash = chunk[chunk.length - 1].endingCash;
    const totRev = chunk.reduce((s, r) => s + r.revenue, 0);
    const totFixed = chunk.reduce((s, r) => s + r.fixedCosts, 0);
    const totVar = chunk.reduce((s, r) => s + r.variableCosts, 0);
    const totOcf = chunk.reduce((s, r) => s + r.operatingCf, 0);
    const totCapex = chunk.reduce((s, r) => s + r.capex, 0);
    const totIcf = chunk.reduce((s, r) => s + r.investingCf, 0);
    const totFunding = chunk.reduce((s, r) => s + r.fundingInflow, 0);
    const totDebt = chunk.reduce((s, r) => s + r.loanRepayment, 0);
    const totFcf = chunk.reduce((s, r) => s + r.financingCf, 0);
    const totNet = chunk.reduce((s, r) => s + r.netCashFlow, 0);
    
    aggregated.push({
      periodLabel: label,
      revenue: Number(totRev.toFixed(2)),
      fixedCosts: Number(totFixed.toFixed(2)),
      variableCosts: Number(totVar.toFixed(2)),
      operatingCf: Number(totOcf.toFixed(2)),
      capex: Number(totCapex.toFixed(2)),
      investingCf: Number(totIcf.toFixed(2)),
      fundingInflow: Number(totFunding.toFixed(2)),
      loanRepayment: Number(totDebt.toFixed(2)),
      financingCf: Number(totFcf.toFixed(2)),
      netCashFlow: Number(totNet.toFixed(2)),
      beginningCash: Number(begCash.toFixed(2)),
      endingCash: Number(endCash.toFixed(2)),
      isCashExhausted: endCash <= 0
    });
  }
  
  return aggregated;
}

/**
 * Runs What-If sensitivity scenarios (+/- 10% Revenue & Costs).
 */
export function runSensitivityAnalysis(baseInputs: CashFlowInputs): SensitivityResults {
  const base = calculateMonthlyCashFlow(baseInputs);
  
  const consInputs: CashFlowInputs = {
    ...baseInputs,
    monthlyRevenue: baseInputs.monthlyRevenue * 0.90,
    revenueGrowthRatePct: Math.max(0, baseInputs.revenueGrowthRatePct - 2),
    fixedCosts: baseInputs.fixedCosts * 1.10,
    variableCostPct: Math.min(95, baseInputs.variableCostPct * 1.10),
    oneTimeCapex: baseInputs.oneTimeCapex * 1.10
  };
  const conservative = calculateMonthlyCashFlow(consInputs);
  
  const optInputs: CashFlowInputs = {
    ...baseInputs,
    monthlyRevenue: baseInputs.monthlyRevenue * 1.10,
    revenueGrowthRatePct: baseInputs.revenueGrowthRatePct + 2,
    fixedCosts: baseInputs.fixedCosts * 0.90,
    variableCostPct: Math.max(5, baseInputs.variableCostPct * 0.90),
    oneTimeCapex: baseInputs.oneTimeCapex * 0.90
  };
  const optimistic = calculateMonthlyCashFlow(optInputs);
  
  return { base, conservative, optimistic };
}
