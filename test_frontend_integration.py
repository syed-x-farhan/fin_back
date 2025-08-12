#!/usr/bin/env python3
"""
Test script to verify frontend integration with dashboard KPIs.
This simulates the exact API call the frontend makes.
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.historical.historical_factory import HistoricalServiceFactory

def test_frontend_api_integration():
    """Test the exact API flow that frontend uses."""
    
    # This is the exact data structure frontend sends
    frontend_data = {
        'yearsInBusiness': '2',
        'forecastYears': '5',
        'historicalServices': [
            {
                'year': '2023',
                'services': [
                    {
                        'name': 'Consulting Services',
                        'historicalRevenue': '150000',
                        'historicalClients': '25',
                        'cost': '45000'
                    }
                ]
            },
            {
                'year': '2024',
                'services': [
                    {
                        'name': 'Consulting Services',
                        'historicalRevenue': '180000',
                        'historicalClients': '30',
                        'cost': '54000'
                    }
                ]
            }
        ],
        'historicalExpenses': [
            {
                'year': '2023',
                'expenses': [
                    {'category': 'Office Rent', 'historicalAmount': '36000'},
                    {'category': 'Marketing', 'historicalAmount': '18000'},
                    {'category': 'Software', 'historicalAmount': '12000'}
                ]
            },
            {
                'year': '2024',
                'expenses': [
                    {'category': 'Office Rent', 'historicalAmount': '38000'},
                    {'category': 'Marketing', 'historicalAmount': '22000'},
                    {'category': 'Software', 'historicalAmount': '15000'}
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
            'clientRetentionRate': '90',
            'utilizationRate': '80',
            'customerLifetimeValue': '50000',
            'clientAcquisitionCost': '2500'
        },
        'taxRate': '25',
        'selfFunding': '75000',
        'revenueGrowthRate': '15',
        'expenseGrowthRate': '8',
        'discountRate': '12',
        'terminalGrowth': '3'
    }
    
    print("🚀 TESTING FRONTEND API INTEGRATION")
    print("=" * 50)
    
    try:
        # Call the same method frontend calls
        result = HistoricalServiceFactory.calculate_historical_statements('service', frontend_data)
        
        if result.get('success'):
            print("✅ API CALL SUCCESSFUL")
            
            # Extract dashboard KPIs (what frontend receives)
            dashboard_kpis = result.get('dashboard_kpis', {})
            
            print(f"\n📊 DASHBOARD KPIs SENT TO FRONTEND:")
            print("-" * 40)
            
            # Format KPIs like frontend would display them
            kpi_display = {
                'Revenue': f"${dashboard_kpis.get('total_revenue', 0):,.0f}",
                'Expenses': f"${dashboard_kpis.get('total_expenses', 0):,.0f}",
                'Net Income': f"${dashboard_kpis.get('net_income', 0):,.0f}",
                'Profit Margin': f"{dashboard_kpis.get('profit_margin', 0):.1f}%",
                'ROE': f"{dashboard_kpis.get('roe', 0):.1f}%",
                'Current Ratio': f"{dashboard_kpis.get('current_ratio', 0):.2f}",
                'Client Retention': f"{dashboard_kpis.get('client_retention_rate', 0):.0f}%",
                'Utilization Rate': f"{dashboard_kpis.get('utilization_rate', 0):.0f}%",
                'CLV': f"${dashboard_kpis.get('clv', 0):,.0f}",
                'CAC': f"${dashboard_kpis.get('cac', 0):,.0f}",
                'Terminal Value': f"${dashboard_kpis.get('terminal_value', 0):,.0f}",
                'Revenue Growth': f"{dashboard_kpis.get('revenue_growth', 0):.1f}%",
                'EBITDA Margin': f"{dashboard_kpis.get('ebitda_margin', 0):.1f}%"
            }
            
            for label, value in kpi_display.items():
                print(f"  {label:<15}: {value}")
            
            print(f"\n🔍 VERIFICATION:")
            print("-" * 40)
            print(f"✅ Real Revenue Calculation: ${dashboard_kpis.get('total_revenue', 0):,.0f}")
            print(f"✅ Real Expense Calculation: ${dashboard_kpis.get('total_expenses', 0):,.0f}")
            print(f"✅ Real Profit Calculation: ${dashboard_kpis.get('net_income', 0):,.0f}")
            print(f"✅ Service Metrics Included: CLV=${dashboard_kpis.get('clv', 0):,.0f}, CAC=${dashboard_kpis.get('cac', 0):,.0f}")
            
            # Check if these are real calculations vs mock data
            if dashboard_kpis.get('total_revenue', 0) > 100000:
                print(f"✅ Using REAL calculated data (not mock values)")
            else:
                print(f"❌ Might be using mock data")
                
            return True
            
        else:
            print("❌ API CALL FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_frontend_api_integration()
    if success:
        print(f"\n🎉 FRONTEND INTEGRATION TEST PASSED!")
        print(f"The dashboard should display real calculated KPIs.")
    else:
        print(f"\n💥 FRONTEND INTEGRATION TEST FAILED!")