#!/usr/bin/env python3
"""
Debug script to check what data is available for the chart and debt-to-equity bar.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.historical.historical_factory import HistoricalServiceFactory

def debug_chart_data():
    """Debug what data is available for charts."""
    
    # Test data
    test_data = {
        'yearsInBusiness': '2',
        'forecastYears': '5',
        'historicalServices': [
            {'year': '2023', 'services': [{'name': 'Test Service', 'historicalRevenue': '50000', 'historicalClients': '10', 'cost': '15000'}]},
            {'year': '2024', 'services': [{'name': 'Test Service', 'historicalRevenue': '60000', 'historicalClients': '12', 'cost': '18000'}]}
        ],
        'historicalExpenses': [
            {'year': '2023', 'expenses': [{'category': 'Office', 'historicalAmount': '12000'}]},
            {'year': '2024', 'expenses': [{'category': 'Office', 'historicalAmount': '15000'}]}
        ],
        'historicalEquipment': [{'year': '2023', 'equipment': []}, {'year': '2024', 'equipment': []}],
        'historicalLoans': [{'year': '2023', 'loans': []}, {'year': '2024', 'loans': []}],
        'historicalOther': [{'year': '2023', 'other': []}, {'year': '2024', 'other': []}],
        'historicalInvestments': [{'year': '2023', 'investments': []}, {'year': '2024', 'investments': []}],
        'historicalShareholders': [{'year': '2023', 'shareholders': []}, {'year': '2024', 'shareholders': []}],
        'serviceBusinessModel': {'clientRetentionRate': '85', 'utilizationRate': '75', 'customerLifetimeValue': '25000', 'clientAcquisitionCost': '1500'},
        'taxRate': '25', 'selfFunding': '50000', 'revenueGrowthRate': '10', 'expenseGrowthRate': '5', 'discountRate': '10', 'terminalGrowth': '2'
    }

    print("🔍 DEBUGGING CHART DATA")
    print("=" * 50)
    
    result = HistoricalServiceFactory.calculate_historical_statements('service', test_data)
    
    if result.get('success'):
        income_statement = result.get('income_statement', {})
        line_items = income_statement.get('line_items', [])
        years = income_statement.get('years', [])
        
        print(f"📅 Years: {years}")
        print(f"📊 Total line items: {len(line_items)}")
        
        print("\n=== INCOME STATEMENT LINE ITEMS ===")
        revenue_items = []
        expense_items = []
        
        for item in line_items:
            label = item.get('label', '')
            values = item.get('values', [])
            
            if any(keyword in label.lower() for keyword in ['revenue', 'income']):
                revenue_items.append((label, values))
                print(f"💰 REVENUE: {label}: {values}")
            elif any(keyword in label.lower() for keyword in ['expense', 'operating', 'cost']):
                expense_items.append((label, values))
                print(f"💸 EXPENSE: {label}: {values}")
        
        print(f"\n📈 Found {len(revenue_items)} revenue items")
        print(f"📉 Found {len(expense_items)} expense items")
        
        print("\n=== DASHBOARD KPIs ===")
        dashboard_kpis = result.get('dashboard_kpis', {})
        print(f"debt_to_equity: {dashboard_kpis.get('debt_to_equity', 'NOT FOUND')}")
        print(f"total_revenue: {dashboard_kpis.get('total_revenue', 'NOT FOUND')}")
        print(f"total_expenses: {dashboard_kpis.get('total_expenses', 'NOT FOUND')}")
        
        print("\n=== BALANCE SHEET ITEMS (for debt-to-equity) ===")
        balance_sheet = result.get('balance_sheet', {})
        balance_line_items = balance_sheet.get('line_items', [])
        
        for item in balance_line_items:
            label = item.get('label', '')
            values = item.get('values', [])
            
            if any(keyword in label.lower() for keyword in ['liabilities', 'equity', 'debt']):
                print(f"🏦 {label}: {values}")
        
        return True
    else:
        print("❌ Calculation failed:", result.get('error'))
        return False

if __name__ == "__main__":
    debug_chart_data()