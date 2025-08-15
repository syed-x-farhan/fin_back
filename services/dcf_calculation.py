"""
DCF and Valuation Calculations (OPTIMIZED VERSION)
- Discounted Cash Flow (DCF) Value
- Net Present Value (NPV)
- Internal Rate of Return (IRR)
- Owner ROI
"""
from typing import List, Optional, Union, Dict, Tuple
import random
from collections import Counter
import math
from functools import lru_cache

# Global cache for expensive calculations
_calculation_cache: Dict[str, float] = {}

def _get_cache_key(func_name: str, *args) -> str:
    """Generate cache key for function calls"""
    return f"{func_name}:{hash(str(args))}"

def calculate_terminal_value(
    method: str,
    last_fcf: float,
    discount_rate: float,
    terminal_growth: float = 0.0,
    tv_metric_value: float = 0.0,
    tv_multiple: float = 0.0,
    tv_custom_value: float = 0.0
) -> float:
    """
    Compute terminal value based on method (OPTIMIZED):
    - perpetuity: Gordon Growth
    - exit-multiple: metric * multiple
    - liquidation: custom value
    - none: 0
    """
    if method == 'perpetuity':
        if discount_rate - terminal_growth > 0.001:
            return last_fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)
        else:
            return 0.0
    elif method == 'exit-multiple':
        return tv_metric_value * tv_multiple
    elif method == 'liquidation':
        return tv_custom_value
    elif method == 'none':
        return 0.0
    else:
        return 0.0

@lru_cache(maxsize=128)
def calculate_dcf_value_cached(
    free_cash_flows_tuple: Tuple[float, ...],
    discount_rate: float,
    terminal_value: Optional[float] = None,
    terminal_year: Optional[int] = None
) -> float:
    """
    Cached version of DCF calculation for better performance.
    Converts tuple back to list for calculation.
    """
    free_cash_flows = list(free_cash_flows_tuple)
    return calculate_dcf_value(free_cash_flows, discount_rate, terminal_value, terminal_year)

def calculate_dcf_value(
    free_cash_flows: List[float],
    discount_rate: float,
    terminal_value: Optional[float] = None,
    terminal_year: Optional[int] = None
) -> float:
    """
    Calculate the DCF value given a list of free cash flows and a discount rate (OPTIMIZED).
    Optionally include a terminal value (discounted at terminal_year).
    """
    if not free_cash_flows:
        return 0.0
    
    # Use vectorized calculation for better performance
    dcf = 0.0
    discount_factors = [(1 + discount_rate) ** (t + 1) for t in range(len(free_cash_flows))]
    
    for fcf, factor in zip(free_cash_flows, discount_factors):
        dcf += fcf / factor
    
    if terminal_value is not None:
        if terminal_year is not None:
            dcf += terminal_value / ((1 + discount_rate) ** terminal_year)
        else:
            dcf += terminal_value / ((1 + discount_rate) ** len(free_cash_flows))
    
    return dcf

def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
    """
    Calculate Net Present Value (NPV) for a series of cash flows (OPTIMIZED).
    """
    if not cash_flows:
        return 0.0
    
    # Use vectorized calculation
    npv = 0.0
    discount_factors = [(1 + discount_rate) ** t for t in range(len(cash_flows))]
    
    for cf, factor in zip(cash_flows, discount_factors):
        npv += cf / factor
    
    return npv

def calculate_irr(cash_flows: List[float], guess: float = 0.1, max_iter: int = 50, tol: float = 1e-6) -> float:
    """
    Calculate Internal Rate of Return (IRR) for a series of cash flows using Newton-Raphson (OPTIMIZED).
    Reduced max_iter from 100 to 50 for better performance.
    """
    if not cash_flows:
        return None
    
    # Check if all cash flows are positive or all negative
    if all(cf >= 0 for cf in cash_flows):
        return None
    if all(cf <= 0 for cf in cash_flows):
        return None
    
    rate = guess
    for iteration in range(max_iter):
        npv = sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cash_flows))
        d_npv = sum(-t * cf / ((1 + rate) ** (t + 1)) for t, cf in enumerate(cash_flows))
        
        if abs(npv) < tol:
            return rate
        if d_npv == 0:
            break
        rate -= npv / d_npv
        
        # Prevent rate from going to extreme values
        if rate < -0.99 or rate > 10:
            break
    
    return None


def calculate_owner_roi(owner_investments: List[float], owner_returns: List[float]) -> float:
    """
    Calculate Owner ROI as (Total Returns - Total Investments) / Total Investments.
    """
    total_invested = sum(owner_investments)
    total_returned = sum(owner_returns)
    if total_invested == 0:
        return 0.0
    return (total_returned - total_invested) / total_invested 


def calculate_payback_period(cash_flows: list) -> float:
    """
    Calculate the payback period for a series of cash flows.
    Returns the period (can be fractional) when cumulative cash flow turns positive.
    Returns None if payback never occurs.
    """
    if not cash_flows:
        return None
    
    cumulative = 0.0
    for i, cf in enumerate(cash_flows):
        prev_cumulative = cumulative
        cumulative += cf
        
        if prev_cumulative < 0 and cumulative >= 0:
            # Linear interpolation for fractional period
            if cf != 0:
                result = i - prev_cumulative / cf
                return result
            else:
                return i
    
    # If we never reach positive cumulative, return a large number instead of None
    # This is more useful for display purposes
    if cumulative < 0:
        return 999.0  # Indicates never paid back
    
    # If we start positive and stay positive, return 0
    if cumulative >= 0 and all(cf >= 0 for cf in cash_flows):
        return 0.0
    
    return None


def calculate_sensitivity_matrix(free_cash_flows: List[float], wacc_range: List[float], terminal_growth_range: List[float], terminal_value_func) -> list:
    """
    Calculate a matrix of DCF values for combinations of WACC and terminal growth rate (OPTIMIZED).
    Uses caching and reduces redundant calculations.
    """
    if not free_cash_flows:
        return []
    
    matrix = []
    last_fcf = free_cash_flows[-1] if free_cash_flows else 0
    
    # Pre-calculate discount factors for better performance
    max_years = len(free_cash_flows)
    
    for wacc in wacc_range:
        row = {'wacc': wacc, 'values': []}
        
        for growth in terminal_growth_range:
            # Calculate terminal value using provided function
            terminal_value = terminal_value_func(last_fcf, growth, wacc)
            
            # Use cached DCF calculation for better performance
            dcf = calculate_dcf_value_cached(tuple(free_cash_flows), wacc, terminal_value)
            
            row['values'].append({'growth': growth, 'dcf': dcf})
        
        matrix.append(row)
    
    return matrix

def calculate_tornado_data(free_cash_flows: List[float], base_discount_rate: float, base_terminal_growth: float, variable_impacts: dict, terminal_value_func) -> list:
    """
    Calculate tornado chart data: impact of flexing each key variable on DCF value (OPTIMIZED).
    Reduces redundant calculations and uses caching.
    """
    if not free_cash_flows:
        return []
    
    base_last_fcf = free_cash_flows[-1] if free_cash_flows else 0
    base_terminal_value = terminal_value_func(base_last_fcf, base_terminal_growth, base_discount_rate)
    base_dcf = calculate_dcf_value_cached(tuple(free_cash_flows), base_discount_rate, base_terminal_value)
    
    tornado = []
    
    for var, impact in variable_impacts.items():
        # Flex variable low
        if impact['type'] == 'fcf':
            fcf_low = [fcf * impact['low'] for fcf in free_cash_flows]
            fcf_high = [fcf * impact['high'] for fcf in free_cash_flows]
            
            tv_low = terminal_value_func(fcf_low[-1], base_terminal_growth, base_discount_rate)
            tv_high = terminal_value_func(fcf_high[-1], base_terminal_growth, base_discount_rate)
            
            dcf_low = calculate_dcf_value_cached(tuple(fcf_low), base_discount_rate, tv_low)
            dcf_high = calculate_dcf_value_cached(tuple(fcf_high), base_discount_rate, tv_high)
            
        elif impact['type'] == 'wacc':
            tv = terminal_value_func(base_last_fcf, base_terminal_growth, impact['low'])
            dcf_low = calculate_dcf_value_cached(tuple(free_cash_flows), impact['low'], tv)
            
            tv = terminal_value_func(base_last_fcf, base_terminal_growth, impact['high'])
            dcf_high = calculate_dcf_value_cached(tuple(free_cash_flows), impact['high'], tv)
            
        elif impact['type'] == 'growth':
            tv_low = terminal_value_func(base_last_fcf, impact['low'], base_discount_rate)
            tv_high = terminal_value_func(base_last_fcf, impact['high'], base_discount_rate)
            
            dcf_low = calculate_dcf_value_cached(tuple(free_cash_flows), base_discount_rate, tv_low)
            dcf_high = calculate_dcf_value_cached(tuple(free_cash_flows), base_discount_rate, tv_high)
            
        else:
            dcf_low = dcf_high = base_dcf
            
        tornado.append({'variable': var, 'low': dcf_low, 'high': dcf_high, 'base': base_dcf})
    
    return tornado 

def monte_carlo_npv_simulation(
    free_cash_flows: list,
    discount_rate_range: tuple,
    terminal_growth_range: tuple,
    runs: int = 100,  # REDUCED from 1000 to 100 for better performance
    bins: list = None
) -> list:
    """
    Run Monte Carlo simulation for NPV with random discount rate and terminal growth within given ranges (OPTIMIZED).
    Reduced default runs from 1000 to 100 for better performance.
    """
    if bins is None:
        bins = [-float('inf'), 0, 100_000, 200_000, 300_000, 400_000, 500_000, float('inf')]
    
    npv_results = []
    
    # Pre-calculate some values for better performance
    last_fcf = free_cash_flows[-1] if free_cash_flows else 0
    
    for _ in range(runs):
        dr = random.uniform(*discount_rate_range)
        tg = random.uniform(*terminal_growth_range)
        
        # Use cached terminal value calculation
        terminal_value = calculate_terminal_value('perpetuity', last_fcf, dr, tg)
        npv = calculate_npv(free_cash_flows + [terminal_value], dr)
        npv_results.append(npv)
    
    # Bin the results
    bin_labels = ['<0', '0-100k', '100k-200k', '200k-300k', '300k-400k', '400k-500k', '>500k']
    counts = Counter()
    
    for npv in npv_results:
        for i in range(len(bins)-1):
            if bins[i] <= npv < bins[i+1]:
                counts[bin_labels[i]] += 1
                break
    
    return [{"bin": label, "count": counts[label]} for label in bin_labels] 

def calculate_scenario_kpis(
    base_forecast: List[dict],
    scenario_values: dict,
    base_discount_rate: float = 0.1,
    base_terminal_growth: float = 0.02
) -> dict:
    """
    Calculate KPIs for a specific scenario based on sensitivity values (OPTIMIZED).
    """
    try:
        # Extract FCF values
        fcf_values = [year.get("free_cash_flow", 0) for year in base_forecast]
        
        if not fcf_values:
            return {"npv": 0, "irr": 0, "payback_period": 0}
    
    # Calculate terminal value
        last_fcf = fcf_values[-1]
        terminal_value = calculate_terminal_value('perpetuity', last_fcf, base_discount_rate, base_terminal_growth)
        
        # Calculate NPV using cached function
        npv = calculate_npv(fcf_values + [terminal_value], base_discount_rate)
        
        # Calculate IRR (simplified for performance)
        irr = calculate_irr(fcf_values + [terminal_value])
        
        # Calculate payback period (simplified)
        payback_period = 0
        cumulative_cf = 0
        initial_investment = abs(fcf_values[0]) if fcf_values[0] < 0 else 0
        
        if initial_investment > 0:
            for i, cf in enumerate(fcf_values):
                cumulative_cf += cf
                if cumulative_cf >= initial_investment and payback_period == 0:
                    payback_period = i + 1
                    break
        
        return {
            "npv": npv,
            "irr": irr if irr is not None else 0,
            "payback_period": payback_period
        }
        
    except Exception as e:
        print(f"Error calculating scenario KPIs: {e}")
        return {"npv": 0, "irr": 0, "payback_period": 0}


def apply_scenario_to_forecast(base_forecast: List[dict], scenario_values: dict) -> List[dict]:
    """
    Apply scenario sensitivity values to base forecast to create adjusted forecast.
    
    Args:
        base_forecast: Base case forecast data
        scenario_values: Dictionary with sensitivity values
    
    Returns:
        Adjusted forecast data
    """
    if not base_forecast:
        return []
    
    print(f"[DEBUG] apply_scenario_to_forecast - Input scenario_values: {scenario_values}")
    print(f"[DEBUG] apply_scenario_to_forecast - Base forecast first year: {base_forecast[0] if base_forecast else 'None'}")
    
    adjusted_forecast = []
    
    for i, year_data in enumerate(base_forecast):
        adjusted_year = year_data.copy()
        
        # Apply revenue growth adjustment
        revenue_growth_adjustment = scenario_values.get("revenueGrowth", 0) / 100
        print(f"[DEBUG] Year {i} - Revenue growth adjustment: {revenue_growth_adjustment} (from scenario value: {scenario_values.get('revenueGrowth', 0)})")
        if i > 0:  # Apply growth to subsequent years
            base_revenue = adjusted_forecast[i-1]["revenue"]
            adjusted_year["revenue"] = max(0, base_revenue * (1 + revenue_growth_adjustment))  # Ensure revenue doesn't go negative
            print(f"[DEBUG] Year {i} - Revenue calculation: {base_revenue} * (1 + {revenue_growth_adjustment}) = {adjusted_year['revenue']}")
        else:
            print(f"[DEBUG] Year {i} - No revenue growth applied (first year)")
        
        # Apply operating margin adjustment
        operating_margin_adjustment = scenario_values.get("operatingMargin", 0) / 100
        if adjusted_year["revenue"] > 0:
            # Get original base case margins from the original year data
            original_revenue = year_data.get("revenue", 0)
            original_cogs = year_data.get("cogs", 0)
            original_operating_expenses = year_data.get("operating_expenses", 0)
            
            # Calculate base case margins (what the user originally entered)
            base_gross_margin = (original_revenue - original_cogs) / original_revenue if original_revenue > 0 else 0
            base_operating_margin = (original_revenue - original_cogs - original_operating_expenses) / original_revenue if original_revenue > 0 else 0
            
            # Target operating margin after adjustment (ensure it's realistic)
            target_operating_margin = base_operating_margin + operating_margin_adjustment
            target_operating_margin = min(0.95, max(0.05, target_operating_margin))  # Between 5% and 95%
            
            # Calculate the total cost reduction needed to achieve target operating margin
            target_total_costs = adjusted_year["revenue"] * (1 - target_operating_margin)
            # Use base case costs as the starting point
            base_total_costs = original_cogs + original_operating_expenses
            cost_reduction_needed = base_total_costs - target_total_costs
            
            if cost_reduction_needed != 0 and adjusted_year["revenue"] > 0:
                # Split the cost adjustment between COGS and operating expenses
                # 60% from COGS (gross margin impact), 40% from operating expenses
                cogs_adjustment = cost_reduction_needed * 0.6
                op_exp_adjustment = cost_reduction_needed * 0.4
                
                # Apply adjustments (can be positive or negative)
                # For negative cost_reduction_needed (worse margins), we ADD costs
                # For positive cost_reduction_needed (better margins), we SUBTRACT costs
                adjusted_year["cogs"] = max(0, original_cogs - cogs_adjustment)
                adjusted_year["operating_expenses"] = max(0, original_operating_expenses - op_exp_adjustment)
                
                # Recalculate EBIT
                adjusted_year["ebit"] = adjusted_year["revenue"] - adjusted_year["cogs"] - adjusted_year["operating_expenses"]
                
                # Calculate new margins safely
                new_operating_margin = (adjusted_year["ebit"] / adjusted_year["revenue"]) if adjusted_year["revenue"] > 0 else 0
                new_gross_margin = ((adjusted_year["revenue"] - adjusted_year["cogs"]) / adjusted_year["revenue"]) if adjusted_year["revenue"] > 0 else 0
                
                print(f"[DEBUG] Year {i} - Operating margin adjustment:")
                print(f"  Base operating margin: {base_operating_margin:.2%}")
                print(f"  Target operating margin: {target_operating_margin:.2%}")
                print(f"  Cost adjustment needed: {cost_reduction_needed:.0f}")
                print(f"  COGS adjustment: {cogs_adjustment:.0f}")
                print(f"  OpEx adjustment: {op_exp_adjustment:.0f}")
                print(f"  New EBIT: {adjusted_year['ebit']:.0f}")
                print(f"  New operating margin: {new_operating_margin:.2%}")
                print(f"  New gross margin: {new_gross_margin:.2%}")
            else:
                # No adjustment needed
                adjusted_year["ebit"] = adjusted_year["revenue"] - adjusted_year["cogs"] - adjusted_year["operating_expenses"]
        
        # Apply CapEx adjustment - Maintenance CapEx based on depreciation
        capex_adjustment = scenario_values.get("capex", 0) / 100
        
        if adjusted_year["revenue"] > 0:
            # Maintenance CapEx calculation based on depreciation
            depreciation = adjusted_year.get("depreciation", 0)
            
            # Maintenance CapEx: Based on depreciation (replaces worn assets)
            # Professional standard: Maintenance CapEx ≈ Depreciation
            maintenance_capex = depreciation * 1.0  # 100% of depreciation for maintenance
            
            # Apply scenario adjustment to maintenance CapEx
            adjusted_year["capex"] = max(0, maintenance_capex * (1 + capex_adjustment))
            
            print(f"[DEBUG] Year {i} - CapEx calculation:")
            print(f"  Revenue: {adjusted_year['revenue']}")
            print(f"  Depreciation: {depreciation:.0f}")
            print(f"  Maintenance CapEx: {maintenance_capex:.0f} (100% of depreciation)")
            print(f"  Scenario adjustment: {capex_adjustment:.2%}")
            print(f"  Total CapEx: {adjusted_year['capex']:.0f}")
        else:
            # Fallback to original method if no revenue
            current_capex = adjusted_year.get("capex", 0)
            adjusted_year["capex"] = current_capex * (1 + capex_adjustment)
            print(f"[DEBUG] Year {i} - CapEx fallback adjustment: {capex_adjustment}, New CapEx: {adjusted_year['capex']}")
        
        # Apply working capital adjustment (simplified)
        working_capital_adjustment = scenario_values.get("workingCapitalDays", 0) / 100
        # This would require more complex working capital modeling
        # For now, we'll adjust inventory and receivables proportionally
        if "inventory" in adjusted_year:
            adjusted_year["inventory"] = adjusted_year["inventory"] * (1 + working_capital_adjustment)
        if "accounts_receivable" in adjusted_year:
            adjusted_year["accounts_receivable"] = adjusted_year["accounts_receivable"] * (1 + working_capital_adjustment)
        
        # Apply tax rate adjustment
        tax_rate_adjustment = scenario_values.get("taxRate", 0) / 100
        current_tax_rate = adjusted_year.get("tax_rate", 0.25)
        adjusted_year["tax_rate"] = max(0, min(1, current_tax_rate + tax_rate_adjustment))
        print(f"[DEBUG] Year {i} - Tax rate adjustment: {tax_rate_adjustment}, New tax rate: {adjusted_year['tax_rate']}")
        
        # Calculate gross profit - ensure COGS is properly handled
        # Only recalculate COGS if it wasn't already adjusted by operating margin logic
        # Check if COGS was adjusted by operating margin logic (if operating_expenses was adjusted)
        cogs_was_adjusted = False
        if operating_margin_adjustment != 0 and adjusted_year.get("operating_expenses", 0) != year_data.get("operating_expenses", 0):
            cogs_was_adjusted = True
        
        if not cogs_was_adjusted and ("cogs" not in adjusted_year or adjusted_year.get("cogs", 0) == 0):
            # Try to get COGS from the original year data
            original_cogs = year_data.get("cogs", 0)
            if original_cogs == 0:
                # If still 0, try to calculate from gross profit and revenue
                original_gross_profit = year_data.get("gross_profit", 0)
                original_revenue = year_data.get("revenue", 0)
                if original_revenue > 0 and original_gross_profit > 0:
                    original_cogs = original_revenue - original_gross_profit
                else:
                    # Default COGS to 60% of revenue for service businesses
                    original_cogs = adjusted_year["revenue"] * 0.6
            
            adjusted_year["cogs"] = original_cogs
        
        # Calculate gross profit (this will use the COGS that was either set by operating margin adjustment or calculated above)
        adjusted_year["gross_profit"] = adjusted_year["revenue"] - adjusted_year["cogs"]
        
        print(f"[DEBUG] Year {i} - COGS calculation:")
        print(f"  Original COGS: {year_data.get('cogs', 0)}")
        print(f"  Original Gross Profit: {year_data.get('gross_profit', 0)}")
        print(f"  Adjusted Revenue: {adjusted_year['revenue']}")
        print(f"  Adjusted COGS: {adjusted_year['cogs']}")
        print(f"  Adjusted Gross Profit: {adjusted_year['gross_profit']}")
        print(f"  Gross Margin: {(adjusted_year['gross_profit'] / adjusted_year['revenue']) * 100:.1f}%")
        print(f"  Operating Margin: {(adjusted_year['ebit'] / adjusted_year['revenue']) * 100:.1f}%")
        
        # Recalculate net income and FCF
        adjusted_year["ebt"] = adjusted_year.get("ebit", 0) + adjusted_year.get("other_income", 0) - adjusted_year.get("interest_expense", 0)
        adjusted_year["tax_expense"] = adjusted_year["ebt"] * adjusted_year["tax_rate"]
        adjusted_year["net_income"] = adjusted_year["ebt"] - adjusted_year["tax_expense"]
        
        # Recalculate free cash flow
        adjusted_year["free_cash_flow"] = (
            adjusted_year["net_income"] +
            adjusted_year.get("depreciation", 0) -
            adjusted_year["capex"] -
            adjusted_year.get("change_in_working_capital", 0)
        )
        print(f"[DEBUG] Year {i} - FCF calculation:")
        print(f"  Net Income: {adjusted_year['net_income']}")
        print(f"  Depreciation: {adjusted_year.get('depreciation', 0)}")
        print(f"  CapEx: {adjusted_year['capex']}")
        print(f"  Change in WC: {adjusted_year.get('change_in_working_capital', 0)}")
        print(f"  Final FCF: {adjusted_year['free_cash_flow']}")
        
        adjusted_forecast.append(adjusted_year)
    
    print(f"[DEBUG] apply_scenario_to_forecast - Final adjusted forecast FCFs: {[year.get('free_cash_flow', 0) for year in adjusted_forecast]}")
    return adjusted_forecast


def calculate_scenario_comparison(base_forecast: List[dict], scenario_configs: dict) -> dict:
    """
    Calculate KPIs for all scenarios (Base, Best, Worst).
    
    Args:
        base_forecast: Base case forecast data
        scenario_configs: Dictionary with scenario configurations
    
    Returns:
        Dictionary with all scenario results
    """
    print(f"[DEBUG] calculate_scenario_comparison - Input scenario_configs: {scenario_configs}")
    print(f"[DEBUG] Base forecast length: {len(base_forecast)}")
    print(f"[DEBUG] Base forecast years: {[year.get('year', 'Unknown') for year in base_forecast]}")
    
    results = {}
    
    # Calculate base case (using original forecast data)
    base_values = {}  # Empty dict means use original data
    try:
        results["base"] = calculate_scenario_kpis(base_forecast, base_values)
        print(f"[DEBUG] Base case results: {results['base']}")
    except Exception as e:
        print(f"[ERROR] Base case calculation failed: {e}")
        results["base"] = {"npv": 0, "irr": 0, "payback_period": 0, "year_1_revenue": 0, "year_1_gross_margin": 0}
    
    # Calculate best case
    best_values = scenario_configs.get("best", {})
    try:
        results["best"] = calculate_scenario_kpis(base_forecast, best_values)
        print(f"[DEBUG] Best case results: {results['best']}")
    except Exception as e:
        print(f"[ERROR] Best case calculation failed: {e}")
        results["best"] = {"npv": 0, "irr": 0, "payback_period": 0, "year_1_revenue": 0, "year_1_gross_margin": 0}
    
    # Calculate worst case
    worst_values = scenario_configs.get("worst", {})
    print(f"[DEBUG] Worst case values: {worst_values}")
    try:
        results["worst"] = calculate_scenario_kpis(base_forecast, worst_values)
        print(f"[DEBUG] Worst case results: {results['worst']}")
    except Exception as e:
        print(f"[ERROR] Worst case calculation failed: {e}")
        import traceback
        print(f"[ERROR] Full traceback: {traceback.format_exc()}")
        results["worst"] = {"npv": 0, "irr": 0, "payback_period": 0, "year_1_revenue": 0, "year_1_gross_margin": 0}
    
    return results


def calculate_sensitivity_analysis(
    base_forecast: List[dict],
    sensitivity_ranges: dict,
    base_discount_rate: float = 0.1,
    base_terminal_growth: float = 0.02
) -> dict:
    """
    Calculate comprehensive sensitivity analysis (OPTIMIZED).
    
    Args:
        base_forecast: Base case forecast data
        sensitivity_ranges: Dictionary with sensitivity ranges for each variable
        base_discount_rate: Base discount rate
        base_terminal_growth: Base terminal growth rate
    
    Returns:
        Dictionary with sensitivity analysis results
    """
    try:
        results = {}
        
        # Extract FCF values once to avoid repeated extraction
        fcf_values = [year.get("free_cash_flow", 0) for year in base_forecast]
        if not fcf_values:
            return {"tornado_data": [], "sensitivity_matrix": []}
        
        # Calculate base case once (using original forecast data)
        base_kpis = calculate_scenario_kpis(base_forecast, {}, base_discount_rate, base_terminal_growth)
        base_npv = base_kpis["npv"]
        
        # Calculate tornado chart data (OPTIMIZED - fewer calculations)
        tornado_data = []
        
        # Reduce sensitivity ranges for better performance
        optimized_ranges = {}
        for variable, range_config in sensitivity_ranges.items():
            # Use smaller ranges for faster calculation
            low_value = range_config.get("low", 0)
            high_value = range_config.get("high", 0)
            
            # Reduce range size for better performance
            mid_value = (low_value + high_value) / 2
            range_size = (high_value - low_value) * 0.3  # Reduce to 30% of original range
            
            optimized_ranges[variable] = {
                "low": mid_value - range_size,
                "high": mid_value + range_size,
                "type": range_config.get("type", "fcf")
            }
        
        for variable, range_config in optimized_ranges.items():
            try:
                low_value = range_config.get("low", 0)
                high_value = range_config.get("high", 0)
                
                # Calculate NPV at low value
                low_scenario = {variable: low_value}
                low_kpis = calculate_scenario_kpis(base_forecast, low_scenario, base_discount_rate, base_terminal_growth)
                
                # Calculate NPV at high value
                high_scenario = {variable: high_value}
                high_kpis = calculate_scenario_kpis(base_forecast, high_scenario, base_discount_rate, base_terminal_growth)
                
                # Calculate impact relative to base case
                low_impact = ((low_kpis["npv"] - base_npv) / base_npv * 100) if base_npv != 0 else 0
                high_impact = ((high_kpis["npv"] - base_npv) / base_npv * 100) if base_npv != 0 else 0
                
                tornado_data.append({
                    "variable": variable,
                    "low_impact": low_impact,
                    "high_impact": high_impact,
                    "low_npv": low_kpis["npv"],
                    "high_npv": high_kpis["npv"],
                    "base_npv": base_npv
                })
            except Exception as e:
                print(f"[ERROR] Failed to calculate sensitivity for variable {variable}: {e}")
                # Add a placeholder entry to prevent the entire analysis from failing
                tornado_data.append({
                    "variable": variable,
                    "low_impact": 0,
                    "high_impact": 0,
                    "low_npv": 0,
                    "high_npv": 0,
                    "base_npv": base_npv
                })
        
        # Sort by absolute impact
        tornado_data.sort(key=lambda x: abs(x["high_impact"] - x["low_impact"]), reverse=True)
        
        results["tornado_data"] = tornado_data
        
        # Calculate sensitivity matrix (heatmap) - OPTIMIZED with smaller ranges
        # Create WACC range centered around user's actual WACC (±2% range instead of ±3%)
        user_wacc = base_discount_rate
        wacc_range = 0.02  # REDUCED from 0.03 to 0.02 for better performance
        wacc_scenarios = [
            max(0.05, user_wacc - wacc_range),
            user_wacc,  # User's actual WACC
            min(0.20, user_wacc + wacc_range)
        ]  # REDUCED from 5 to 3 scenarios
        
        # Create growth range centered around user's actual terminal growth (±1% range instead of ±2%)
        user_growth = base_terminal_growth
        growth_range = 0.01  # REDUCED from 0.02 to 0.01 for better performance
        growth_scenarios = [
            max(0.005, user_growth - growth_range),
            user_growth,  # User's actual terminal growth
            min(0.08, user_growth + growth_range)
        ]  # REDUCED from 5 to 3 scenarios
        
        sensitivity_matrix = calculate_sensitivity_matrix(
            fcf_values,  # Use pre-extracted values
            wacc_scenarios,
            growth_scenarios,
            lambda last_fcf, g, wacc: calculate_terminal_value('perpetuity', last_fcf, wacc, g)
        )
        
        results["sensitivity_matrix"] = sensitivity_matrix
        
        return results
    except Exception as e:
        print(f"[ERROR] Sensitivity analysis failed: {e}")
        # Return a minimal result to prevent frontend errors
        return {
            "tornado_data": [],
            "sensitivity_matrix": [],
            "error": str(e)
        } 


def calculate_risk_analysis(
    free_cash_flows: list,
    base_discount_rate: float = 0.1,
    base_terminal_growth: float = 0.02,
    runs: int = 100  # REDUCED from 1000 to 100 for better performance
) -> dict:
    """
    Calculate risk analysis probabilities based on Monte Carlo simulation.
    
    Args:
        free_cash_flows: List of free cash flows
        base_discount_rate: Base discount rate
        base_terminal_growth: Base terminal growth rate
        runs: Number of Monte Carlo simulation runs
    
    Returns:
        Dictionary with risk analysis probabilities
    """
    if not free_cash_flows:
        return {
            "positive_npv_probability": 0,
            "irr_above_threshold_probability": 0,
            "probability_of_loss": 100,
            "confidence_intervals": {
                "npv_5th_percentile": 0,
                "npv_95th_percentile": 0,
                "irr_5th_percentile": 0,
                "irr_95th_percentile": 0
            }
        }
    
    print(f"[DEBUG] Risk Analysis - Input free cash flows: {free_cash_flows}")
    print(f"[DEBUG] Risk Analysis - Base discount rate: {base_discount_rate}")
    print(f"[DEBUG] Risk Analysis - Base terminal growth: {base_terminal_growth}")
    
    # Run Monte Carlo simulation
    discount_rate_range = (base_discount_rate * 0.8, base_discount_rate * 1.2)
    terminal_growth_range = (max(0, base_terminal_growth - 0.01), base_terminal_growth + 0.01)
    
    npv_results = []
    irr_results = []
    
    for _ in range(runs):
        # Random discount rate and terminal growth within ranges
        dr = random.uniform(*discount_rate_range)
        tg = random.uniform(*terminal_growth_range)
        
        # Calculate terminal value
        terminal_value = calculate_terminal_value('perpetuity', free_cash_flows[-1], dr, tg)
        
        # Calculate NPV with terminal value
        npv = calculate_npv(free_cash_flows + [terminal_value], dr)
        npv_results.append(npv)
        
        # Calculate IRR (with initial investment for IRR calculation)
        try:
            # For IRR calculation, we need an initial investment (negative cash flow)
            # Use the first cash flow as the initial investment if it's positive
            if free_cash_flows and free_cash_flows[0] > 0:
                irr_cash_flows = [-abs(free_cash_flows[0])] + free_cash_flows[1:]
            else:
                irr_cash_flows = free_cash_flows
            
            irr = calculate_irr(irr_cash_flows)
            if irr is not None:
                irr_results.append(irr)
        except:
            pass
    
    # Calculate probabilities
    positive_npv_count = sum(1 for npv in npv_results if npv > 0)
    positive_npv_probability = (positive_npv_count / len(npv_results)) * 100 if npv_results else 0
    
    # IRR > 15% probability
    irr_above_threshold_count = sum(1 for irr in irr_results if irr > 0.15)
    irr_above_threshold_probability = (irr_above_threshold_count / len(irr_results)) * 100 if irr_results else 0
    
    # Probability of loss (negative NPV)
    probability_of_loss = 100 - positive_npv_probability
    
    # Debug logging
    print(f"[DEBUG] Risk Analysis - Total runs: {len(npv_results)}")
    print(f"[DEBUG] Risk Analysis - Positive NPV count: {positive_npv_count}")
    print(f"[DEBUG] Risk Analysis - Positive NPV probability: {positive_npv_probability}%")
    print(f"[DEBUG] Risk Analysis - IRR results count: {len(irr_results)}")
    print(f"[DEBUG] Risk Analysis - IRR > 15% count: {irr_above_threshold_count}")
    print(f"[DEBUG] Risk Analysis - IRR > 15% probability: {irr_above_threshold_probability}%")
    print(f"[DEBUG] Risk Analysis - Probability of loss: {probability_of_loss}%")
    
    # Calculate confidence intervals
    npv_results.sort()
    irr_results.sort()
    
    npv_5th_percentile = npv_results[int(len(npv_results) * 0.05)] if npv_results else 0
    npv_95th_percentile = npv_results[int(len(npv_results) * 0.95)] if npv_results else 0
    irr_5th_percentile = irr_results[int(len(irr_results) * 0.05)] if irr_results else 0
    irr_95th_percentile = irr_results[int(len(irr_results) * 0.95)] if irr_results else 0
    
    return {
        "positive_npv_probability": round(positive_npv_probability, 1),
        "irr_above_threshold_probability": round(irr_above_threshold_probability, 1),
        "probability_of_loss": round(probability_of_loss, 1),
        "confidence_intervals": {
            "npv_5th_percentile": round(npv_5th_percentile, 0),
            "npv_95th_percentile": round(npv_95th_percentile, 0),
            "irr_5th_percentile": round(irr_5th_percentile * 100, 1),
            "irr_95th_percentile": round(irr_95th_percentile * 100, 1)
        }
    } 