#!/usr/bin/env python3
"""Simple test to check balance sheet status only."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.historical.historical_factory import HistoricalServiceFactory

# Simple test data
test_data = {
    'yearsInBusiness': '2',
    'forecastYears': '3',
    'historicalServices': [
        {'year': '2023', 'services': [{'name': 'Service', 'historicalRevenue': '50000', 'historicalClients': '10', 'cost': '15000'}]},
        {'year': '2024', 'services': [{'name': 'Service', 'historicalRevenue': '60000', 'historicalClients': '12', 'cost': '18000'}]}
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

result = HistoricalServiceFactory.calculate_historical_statements('service', test_data)

if result.get('success'):
    print("✅ Calculation successful")
    dashboard_kpis = result.get('dashboard_kpis', {})
    print(f"debt_to_equity: {dashboard_kpis.get('debt_to_equity', 'NOT FOUND')}")
else:
    print("❌ Calculation failed")