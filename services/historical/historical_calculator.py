"""
Historical Data Calculator Service

This service handles calculations for established businesses with historical data.
It processes historical financial statements and projects future performance
based on historical trends and user inputs.
"""

import datetime
from typing import Dict, Any, List, Optional
import math

def calculate_historical_statements(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate financial statements for established businesses with historical data.
    
    Args:
        data: Dictionary containing historical data and projection parameters
        
    Returns:
        Dictionary containing calculated financial statements and projections
    """
    
    # --- Parse input data ---
    historical_years = int(data.get('historicalYears', 3))
    forecast_years = int(data.get('forecastYears', 5))
    business_type = data.get('businessType', 'service')  # service, retail, saas
    
    # Historical financial data
    historical_income = data.get('historicalIncome', [])
    historical_balance = data.get('historicalBalance', [])
    historical_cashflow = data.get('historicalCashflow', [])
    
    # Projection parameters
    revenue_growth = float(data.get('revenueGrowth', 0)) / 100
    expense_growth = float(data.get('expenseGrowth', 0)) / 100
    margin_improvement = float(data.get('marginImprovement', 0)) / 100
    
    # Working capital parameters
    ar_days = float(data.get('arDays', 30))
    ap_days = float(data.get('apDays', 30))
    inventory_days = float(data.get('inventoryDays', 60))
    
    # Capital structure
    target_debt_ratio = float(data.get('targetDebtRatio', 0.3))
    capex_ratio = float(data.get('capexRatio', 0.05))
    
    # Tax and other
    tax_rate = float(data.get('taxRate', 25)) / 100
    
    # Calculate base year (last historical year)
    current_date = datetime.datetime.today()
    base_year = current_date.year - 1
    total_years = historical_years + forecast_years
    years = [f"FY{base_year - historical_years + i + 1}" for i in range(total_years)]
    
    # --- Process Historical Data ---
    processed_historical = process_historical_data(
        historical_income, historical_balance, historical_cashflow,
        historical_years, base_year
    )
    
    # --- Project Future Performance ---
    projected_data = project_future_performance(
        processed_historical, forecast_years, revenue_growth,
        expense_growth, margin_improvement, business_type
    )
    
    # --- Calculate Working Capital ---
    working_capital = calculate_working_capital(
        projected_data, ar_days, ap_days, inventory_days
    )
    
    # --- Calculate Capital Structure ---
    capital_structure = calculate_capital_structure(
        projected_data, working_capital, target_debt_ratio, capex_ratio
    )
    
    # --- Generate Financial Statements ---
    income_statement = generate_income_statement(
        processed_historical, projected_data, years, tax_rate
    )
    
    balance_sheet = generate_balance_sheet(
        processed_historical, projected_data, working_capital,
        capital_structure, years
    )
    
    cash_flow = generate_cash_flow_statement(
        processed_historical, projected_data, working_capital,
        capital_structure, years
    )
    
    # --- Calculate KPIs and Metrics ---
    kpis = calculate_historical_kpis(
        processed_historical, projected_data, working_capital,
        capital_structure
    )
    
    return {
        'income_statement': income_statement,
        'balance_sheet': balance_sheet,
        'cash_flow': cash_flow,
        'kpis': kpis,
        'historical_data': processed_historical,
        'projections': projected_data,
        'years': years,
        'historical_years': historical_years,
        'forecast_years': forecast_years
    }

def process_historical_data(
    historical_income: List[Dict], 
    historical_balance: List[Dict], 
    historical_cashflow: List[Dict],
    historical_years: int,
    base_year: int
) -> Dict[str, Any]:
    """
    Process and validate historical financial data.
    """
    processed = {
        'revenue': [],
        'cogs': [],
        'operating_expenses': [],
        'ebitda': [],
        'depreciation': [],
        'ebit': [],
        'interest_expense': [],
        'ebt': [],
        'taxes': [],
        'net_income': [],
        'total_assets': [],
        'current_assets': [],
        'fixed_assets': [],
        'current_liabilities': [],
        'long_term_debt': [],
        'equity': [],
        'operating_cash_flow': [],
        'investing_cash_flow': [],
        'financing_cash_flow': [],
        'net_cash_flow': []
    }
    
    # Process income statement data
    for i in range(historical_years):
        year_data = historical_income[i] if i < len(historical_income) else {}
        processed['revenue'].append(float(year_data.get('revenue', 0)))
        processed['cogs'].append(float(year_data.get('cogs', 0)))
        processed['operating_expenses'].append(float(year_data.get('operatingExpenses', 0)))
        processed['ebitda'].append(float(year_data.get('ebitda', 0)))
        processed['depreciation'].append(float(year_data.get('depreciation', 0)))
        processed['ebit'].append(float(year_data.get('ebit', 0)))
        processed['interest_expense'].append(float(year_data.get('interestExpense', 0)))
        processed['ebt'].append(float(year_data.get('ebt', 0)))
        processed['taxes'].append(float(year_data.get('taxes', 0)))
        processed['net_income'].append(float(year_data.get('netIncome', 0)))
    
    # Process balance sheet data
    for i in range(historical_years):
        year_data = historical_balance[i] if i < len(historical_balance) else {}
        processed['total_assets'].append(float(year_data.get('totalAssets', 0)))
        processed['current_assets'].append(float(year_data.get('currentAssets', 0)))
        processed['fixed_assets'].append(float(year_data.get('fixedAssets', 0)))
        processed['current_liabilities'].append(float(year_data.get('currentLiabilities', 0)))
        processed['long_term_debt'].append(float(year_data.get('longTermDebt', 0)))
        processed['equity'].append(float(year_data.get('equity', 0)))
    
    # Process cash flow data
    for i in range(historical_years):
        year_data = historical_cashflow[i] if i < len(historical_cashflow) else {}
        processed['operating_cash_flow'].append(float(year_data.get('operatingCashFlow', 0)))
        processed['investing_cash_flow'].append(float(year_data.get('investingCashFlow', 0)))
        processed['financing_cash_flow'].append(float(year_data.get('financingCashFlow', 0)))
        processed['net_cash_flow'].append(float(year_data.get('netCashFlow', 0)))
    
    return processed

def project_future_performance(
    historical_data: Dict[str, Any],
    forecast_years: int,
    revenue_growth: float,
    expense_growth: float,
    margin_improvement: float,
    business_type: str
) -> Dict[str, Any]:
    """
    Project future financial performance based on historical trends and user inputs.
    """
    # Calculate historical averages and trends
    avg_revenue = sum(historical_data['revenue']) / len(historical_data['revenue'])
    avg_cogs_ratio = sum(historical_data['cogs']) / sum(historical_data['revenue']) if sum(historical_data['revenue']) > 0 else 0.6
    avg_opex_ratio = sum(historical_data['operating_expenses']) / sum(historical_data['revenue']) if sum(historical_data['revenue']) > 0 else 0.3
    
    # Calculate growth trends
    revenue_trend = calculate_growth_trend(historical_data['revenue'])
    expense_trend = calculate_growth_trend(historical_data['operating_expenses'])
    
    projected = {
        'revenue': [],
        'cogs': [],
        'operating_expenses': [],
        'ebitda': [],
        'depreciation': [],
        'ebit': [],
        'interest_expense': [],
        'ebt': [],
        'taxes': [],
        'net_income': []
    }
    
    # Project revenue
    last_revenue = historical_data['revenue'][-1] if historical_data['revenue'] else avg_revenue
    for i in range(forecast_years):
        growth_rate = revenue_growth + (revenue_trend * (1 - i/forecast_years))  # Decay trend over time
        projected_revenue = last_revenue * (1 + growth_rate) ** (i + 1)
        projected['revenue'].append(projected_revenue)
        last_revenue = projected_revenue
    
    # Project expenses
    for i in range(forecast_years):
        revenue = projected['revenue'][i]
        
        # COGS with margin improvement
        cogs_ratio = avg_cogs_ratio * (1 - margin_improvement)
        projected['cogs'].append(revenue * cogs_ratio)
        
        # Operating expenses
        opex_ratio = avg_opex_ratio * (1 - margin_improvement)
        projected['operating_expenses'].append(revenue * opex_ratio)
        
        # EBITDA
        ebitda = revenue - projected['cogs'][i] - projected['operating_expenses'][i]
        projected['ebitda'].append(ebitda)
        
        # Depreciation (assume 5% of revenue for simplicity)
        depreciation = revenue * 0.05
        projected['depreciation'].append(depreciation)
        
        # EBIT
        ebit = ebitda - depreciation
        projected['ebit'].append(ebit)
        
        # Interest (will be calculated based on capital structure)
        projected['interest_expense'].append(0)  # Placeholder
        
        # EBT
        ebt = ebit - projected['interest_expense'][i]
        projected['ebt'].append(ebt)
        
        # Taxes (will be calculated with actual tax rate)
        projected['taxes'].append(0)  # Placeholder
        
        # Net Income
        projected['net_income'].append(0)  # Placeholder
    
    return projected

def calculate_growth_trend(values: List[float]) -> float:
    """
    Calculate the average growth trend from historical data.
    """
    if len(values) < 2:
        return 0.0
    
    growth_rates = []
    for i in range(1, len(values)):
        if values[i-1] != 0:
            growth_rate = (values[i] - values[i-1]) / values[i-1]
            growth_rates.append(growth_rate)
    
    return sum(growth_rates) / len(growth_rates) if growth_rates else 0.0

def calculate_working_capital(
    projected_data: Dict[str, Any],
    ar_days: float,
    ap_days: float,
    inventory_days: float
) -> Dict[str, Any]:
    """
    Calculate working capital requirements based on projected revenue.
    """
    working_capital = {
        'accounts_receivable': [],
        'accounts_payable': [],
        'inventory': [],
        'net_working_capital': [],
        'change_in_nwc': []
    }
    
    prev_nwc = 0
    for i, revenue in enumerate(projected_data['revenue']):
        # Calculate working capital components
        ar = (revenue * ar_days) / 365
        ap = (projected_data['cogs'][i] * ap_days) / 365
        inventory = (projected_data['cogs'][i] * inventory_days) / 365
        
        nwc = ar + inventory - ap
        change_in_nwc = nwc - prev_nwc
        
        working_capital['accounts_receivable'].append(ar)
        working_capital['accounts_payable'].append(ap)
        working_capital['inventory'].append(inventory)
        working_capital['net_working_capital'].append(nwc)
        working_capital['change_in_nwc'].append(change_in_nwc)
        
        prev_nwc = nwc
    
    return working_capital

def calculate_capital_structure(
    projected_data: Dict[str, Any],
    working_capital: Dict[str, Any],
    target_debt_ratio: float,
    capex_ratio: float
) -> Dict[str, Any]:
    """
    Calculate optimal capital structure and financing needs.
    """
    capital_structure = {
        'total_assets': [],
        'debt': [],
        'equity': [],
        'capex': [],
        'free_cash_flow': []
    }
    
    for i, revenue in enumerate(projected_data['revenue']):
        # Calculate total assets (simplified)
        total_assets = revenue * 1.5  # Asset turnover ratio of 1.5
        
        # Calculate target debt
        target_debt = total_assets * target_debt_ratio
        
        # Calculate equity
        equity = total_assets - target_debt
        
        # Calculate CapEx
        capex = revenue * capex_ratio
        
        # Calculate Free Cash Flow
        ebitda = projected_data['ebitda'][i]
        taxes = projected_data['ebt'][i] * 0.25  # Assume 25% tax rate
        change_in_nwc = working_capital['change_in_nwc'][i]
        fcf = ebitda - taxes - capex - change_in_nwc
        
        capital_structure['total_assets'].append(total_assets)
        capital_structure['debt'].append(target_debt)
        capital_structure['equity'].append(equity)
        capital_structure['capex'].append(capex)
        capital_structure['free_cash_flow'].append(fcf)
    
    return capital_structure

def generate_income_statement(
    historical_data: Dict[str, Any],
    projected_data: Dict[str, Any],
    years: List[str],
    tax_rate: float
) -> Dict[str, Any]:
    """
    Generate complete income statement with historical and projected data.
    """
    income_statement = {
        'years': years,
        'line_items': []
    }
    
    # Combine historical and projected data
    all_revenue = historical_data['revenue'] + projected_data['revenue']
    all_cogs = historical_data['cogs'] + projected_data['cogs']
    all_operating_expenses = historical_data['operating_expenses'] + projected_data['operating_expenses']
    all_ebitda = historical_data['ebitda'] + projected_data['ebitda']
    all_depreciation = historical_data['depreciation'] + projected_data['depreciation']
    all_ebit = historical_data['ebit'] + projected_data['ebit']
    all_interest = historical_data['interest_expense'] + projected_data['interest_expense']
    all_ebt = historical_data['ebt'] + projected_data['ebt']
    all_taxes = historical_data['taxes'] + projected_data['taxes']
    all_net_income = historical_data['net_income'] + projected_data['net_income']
    
    # Create line items
    line_items = [
        {'label': 'Revenue', 'values': all_revenue},
        {'label': 'Cost of Goods Sold', 'values': all_cogs},
        {'label': 'Gross Profit', 'values': [r - c for r, c in zip(all_revenue, all_cogs)]},
        {'label': 'Operating Expenses', 'values': all_operating_expenses},
        {'label': 'EBITDA', 'values': all_ebitda},
        {'label': 'Depreciation & Amortization', 'values': all_depreciation},
        {'label': 'EBIT', 'values': all_ebit},
        {'label': 'Interest Expense', 'values': all_interest},
        {'label': 'EBT', 'values': all_ebt},
        {'label': 'Taxes', 'values': all_taxes},
        {'label': 'Net Income', 'values': all_net_income}
    ]
    
    income_statement['line_items'] = line_items
    return income_statement

def generate_balance_sheet(
    historical_data: Dict[str, Any],
    projected_data: Dict[str, Any],
    working_capital: Dict[str, Any],
    capital_structure: Dict[str, Any],
    years: List[str]
) -> Dict[str, Any]:
    """
    Generate complete balance sheet with historical and projected data.
    """
    balance_sheet = {
        'years': years,
        'line_items': []
    }
    
    # Calculate balance sheet items
    all_assets = historical_data['total_assets'] + capital_structure['total_assets']
    all_current_assets = historical_data['current_assets'] + [wc['net_working_capital'] for wc in working_capital.values()]
    all_fixed_assets = historical_data['fixed_assets'] + capital_structure['capex']
    all_current_liabilities = historical_data['current_liabilities'] + [wc['accounts_payable'] for wc in working_capital.values()]
    all_long_term_debt = historical_data['long_term_debt'] + capital_structure['debt']
    all_equity = historical_data['equity'] + capital_structure['equity']
    
    line_items = [
        {'label': 'Total Assets', 'values': all_assets},
        {'label': 'Current Assets', 'values': all_current_assets},
        {'label': 'Fixed Assets', 'values': all_fixed_assets},
        {'label': 'Total Liabilities', 'values': [c + l for c, l in zip(all_current_liabilities, all_long_term_debt)]},
        {'label': 'Current Liabilities', 'values': all_current_liabilities},
        {'label': 'Long-term Debt', 'values': all_long_term_debt},
        {'label': 'Total Equity', 'values': all_equity}
    ]
    
    balance_sheet['line_items'] = line_items
    return balance_sheet

def generate_cash_flow_statement(
    historical_data: Dict[str, Any],
    projected_data: Dict[str, Any],
    working_capital: Dict[str, Any],
    capital_structure: Dict[str, Any],
    years: List[str]
) -> List[Dict[str, Any]]:
    """
    Generate complete cash flow statement with historical and projected data.
    """
    cash_flow = []
    
    # Combine historical and projected data
    all_operating_cf = historical_data['operating_cash_flow'] + [fcf for fcf in capital_structure['free_cash_flow']]
    all_investing_cf = historical_data['investing_cash_flow'] + [-capex for capex in capital_structure['capex']]
    all_financing_cf = historical_data['financing_cash_flow'] + [0] * len(projected_data['revenue'])  # Placeholder
    
    for i, year in enumerate(years):
        period = {
            'year': year,
            'operating_activities': [
                ['Net Income', projected_data['net_income'][i] if i >= len(historical_data['net_income']) else historical_data['net_income'][i]],
                ['Depreciation', projected_data['depreciation'][i] if i >= len(historical_data['depreciation']) else historical_data['depreciation'][i]],
                ['Change in Working Capital', working_capital['change_in_nwc'][i] if i >= len(historical_data['net_income']) else 0]
            ],
            'investing_activities': [
                ['Capital Expenditure', -capital_structure['capex'][i] if i >= len(historical_data['net_income']) else 0]
            ],
            'financing_activities': [
                ['Debt Issuance/Repayment', 0],  # Placeholder
                ['Dividends', 0]  # Placeholder
            ],
            'net_cash_from_operating_activities': all_operating_cf[i],
            'net_cash_from_investing_activities': all_investing_cf[i],
            'net_cash_from_financing_activities': all_financing_cf[i],
            'net_change_in_cash': all_operating_cf[i] + all_investing_cf[i] + all_financing_cf[i],
            'opening_cash_balance': 0,  # Will be calculated
            'closing_cash_balance': 0   # Will be calculated
        }
        cash_flow.append(period)
    
    # Calculate opening and closing cash balances
    opening_cash = 0
    for period in cash_flow:
        period['opening_cash_balance'] = opening_cash
        period['closing_cash_balance'] = opening_cash + period['net_change_in_cash']
        opening_cash = period['closing_cash_balance']
    
    return cash_flow

def calculate_historical_kpis(
    historical_data: Dict[str, Any],
    projected_data: Dict[str, Any],
    working_capital: Dict[str, Any],
    capital_structure: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate key performance indicators for historical and projected data.
    """
    kpis = {
        'historical_metrics': {},
        'projected_metrics': {},
        'trends': {}
    }
    
    # Historical KPIs
    if historical_data['revenue']:
        kpis['historical_metrics'] = {
            'avg_revenue_growth': calculate_growth_trend(historical_data['revenue']),
            'avg_ebitda_margin': sum(historical_data['ebitda']) / sum(historical_data['revenue']) if sum(historical_data['revenue']) > 0 else 0,
            'avg_net_margin': sum(historical_data['net_income']) / sum(historical_data['revenue']) if sum(historical_data['revenue']) > 0 else 0,
            'avg_asset_turnover': sum(historical_data['revenue']) / sum(historical_data['total_assets']) if sum(historical_data['total_assets']) > 0 else 0
        }
    
    # Projected KPIs
    if projected_data['revenue']:
        kpis['projected_metrics'] = {
            'projected_revenue_growth': revenue_growth,
            'projected_ebitda_margin': sum(projected_data['ebitda']) / sum(projected_data['revenue']) if sum(projected_data['revenue']) > 0 else 0,
            'projected_net_margin': sum(projected_data['net_income']) / sum(projected_data['revenue']) if sum(projected_data['revenue']) > 0 else 0
        }
    
    return kpis 