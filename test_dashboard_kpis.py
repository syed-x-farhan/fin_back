#!/usr/bin/env python3
"""
Test script to verify dashboard KPIs calculation is working correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.historical.historical_factory import HistoricalServiceFactory

def test_dashboard_kpis():
    """Test the dashboard KPIs calculation with sample data."""
    
    # Sample historical data (similar to what frontend sends)
    test_data = {
        'yearsInBusiness': '2',
        'forecastYears': '5',
        'historicalServices': [
            {
                'year': '2023',
                'services': [
                    {
                        'name': 'Consulting',
                        'historicalRevenue': '100000',
                        'historicalClients': '50',
                        'cost': '30000'
                    }
                ]
            },
            {
                'year': '2024',
                'services': [
                    {
                        'name': 'Consulting',
                        'historicalRevenue': '120000',
                        'historicalClients': '60',
                        'cost': '35000'
                    }
                ]
            }
        ],
        'historicalExpenses': [
            {
                'year': '2023',
                'expenses': [
                    {'category': 'Office Rent', 'historicalAmount': '24000'},
                    {'category': 'Marketing', 'historicalAmount': '12000'}
                ]
            },
            {
                'year': '2024',
                'expenses': [
                    {'category': 'Office Rent', 'historicalAmount': '26000'},
                    {'category': 'Marketing', 'historicalAmount': '15000'}
                ]
            }
        ],
        'historicalEquipment': [
            {'year': '2023', 'equipment': []},
            {'year': '2024', 'equipment': []}
        ],
        'historicalLoans': [
            {'year': '2023', 'loans': []},
            {'year': '2024', 'loans': []}
        ],
        'historicalOther': [
            {'year': '2023', 'other': []},
            {'year': '2024', 'other': []}
        ],
        'historicalInvestments': [
            {'year': '2023', 'investments': []},
            {'year': '2024', 'investments': []}
        ],
        'historicalShareholders': [
            {'year': '2023', 'shareholders': []},
            {'year': '2024', 'shareholders': []}
        ],
        'serviceBusinessModel': {
            'clientRetentionRate': '85',
            'utilizationRate': '75',
            'customerLifetimeValue': '25000',
            'clientAcquisitionCost': '1500'
        },
        'taxRate': '25',
        'selfFunding': '50000',
        'revenueGrowthRate': '10',
        'expenseGrowthRate': '5',
        'discountRate': '10',
        'terminalGrowth': '2'
    }
    
    print("=== TESTING DASHBOARD KPIs CALCULATION ===")
    print(f"Test data keys: {list(test_data.keys())}")
    
    try:
        # Test the calculation
        result = HistoricalServiceFactory.calculate_historical_statements('service', test_data)
        
        print(f"\n=== CALCULATION RESULT ===")
        print(f"Result success: {result.get('success', False)}")
        print(f"Result keys: {list(result.keys())}")
        
        # Check if dashboard_kpis exists
        if 'dashboard_kpis' in result:
            dashboard_kpis = result['dashboard_kpis']
            print(f"\n=== DASHBOARD KPIs ===")
            print(f"Dashboard KPIs keys: {list(dashboard_kpis.keys())}")
            
            # Print key KPIs
            key_kpis = [
                'total_revenue', 'total_expenses', 'net_income', 'profit_margin',
                'roe', 'asset_turnover', 'current_ratio', 'terminal_value'
            ]
            
            for kpi in key_kpis:
                value = dashboard_kpis.get(kpi, 'NOT FOUND')
                print(f"  {kpi}: {value}")
                
        else:
            print("ERROR: dashboard_kpis not found in result!")
            
        # Check income statement structure
        if 'income_statement' in result:
            income = result['income_statement']
            print(f"\n=== INCOME STATEMENT STRUCTURE ===")
            print(f"Years: {income.get('years', 'NOT FOUND')}")
            print(f"Line items count: {len(income.get('line_items', []))}")
            
            # Show first few line items
            line_items = income.get('line_items', [])[:5]
            for item in line_items:
                label = item.get('label', 'NO LABEL')
                values = item.get('values', [])
                print(f"  {label}: {values}")
        
        return result
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_dashboard_kpis()