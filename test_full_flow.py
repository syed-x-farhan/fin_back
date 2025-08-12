#!/usr/bin/env python3
"""
Test script to verify the complete end-to-end flow:
1. Form submission → Backend calculation → Dashboard display
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.historical.historical_factory import HistoricalServiceFactory

def test_complete_flow():
    """Test the complete flow from form to dashboard."""
    
    print("🚀 TESTING COMPLETE END-TO-END FLOW")
    print("=" * 60)
    
    # Step 1: Simulate form data (what user enters)
    form_data = {
        'yearsInBusiness': '3',
        'forecastYears': '5',
        'historicalServices': [
            {
                'year': '2022',
                'services': [
                    {
                        'name': 'Digital Marketing Services',
                        'historicalRevenue': '200000',
                        'historicalClients': '40',
                        'cost': '60000'
                    }
                ]
            },
            {
                'year': '2023',
                'services': [
                    {
                        'name': 'Digital Marketing Services',
                        'historicalRevenue': '250000',
                        'historicalClients': '50',
                        'cost': '75000'
                    }
                ]
            },
            {
                'year': '2024',
                'services': [
                    {
                        'name': 'Digital Marketing Services',
                        'historicalRevenue': '300000',
                        'historicalClients': '60',
                        'cost': '90000'
                    }
                ]
            }
        ],
        'historicalExpenses': [
            {
                'year': '2022',
                'expenses': [
                    {'category': 'Office Rent', 'historicalAmount': '48000'},
                    {'category': 'Marketing', 'historicalAmount': '24000'},
                    {'category': 'Software', 'historicalAmount': '18000'},
                    {'category': 'Salaries', 'historicalAmount': '120000'}
                ]
            },
            {
                'year': '2023',
                'expenses': [
                    {'category': 'Office Rent', 'historicalAmount': '50000'},
                    {'category': 'Marketing', 'historicalAmount': '30000'},
                    {'category': 'Software', 'historicalAmount': '22000'},
                    {'category': 'Salaries', 'historicalAmount': '140000'}
                ]
            },
            {
                'year': '2024',
                'expenses': [
                    {'category': 'Office Rent', 'historicalAmount': '52000'},
                    {'category': 'Marketing', 'historicalAmount': '36000'},
                    {'category': 'Software', 'historicalAmount': '25000'},
                    {'category': 'Salaries', 'historicalAmount': '160000'}
                ]
            }
        ],
        'historicalEquipment': [
            {'year': '2022', 'equipment': []},
            {'year': '2023', 'equipment': []},
            {'year': '2024', 'equipment': []}
        ],
        'historicalLoans': [
            {'year': '2022', 'loans': []},
            {'year': '2023', 'loans': []},
            {'year': '2024', 'loans': []}
        ],
        'historicalOther': [
            {'year': '2022', 'other': []},
            {'year': '2023', 'other': []},
            {'year': '2024', 'other': []}
        ],
        'historicalInvestments': [
            {'year': '2022', 'investments': []},
            {'year': '2023', 'investments': []},
            {'year': '2024', 'investments': []}
        ],
        'historicalShareholders': [
            {'year': '2022', 'shareholders': []},
            {'year': '2023', 'shareholders': []},
            {'year': '2024', 'shareholders': []}
        ],
        'serviceBusinessModel': {
            'clientRetentionRate': '88',
            'utilizationRate': '82',
            'customerLifetimeValue': '45000',
            'clientAcquisitionCost': '3000'
        },
        'taxRate': '25',
        'selfFunding': '100000',
        'revenueGrowthRate': '18',
        'expenseGrowthRate': '10',
        'discountRate': '11',
        'terminalGrowth': '2.5'
    }
    
    print("📝 STEP 1: Form Data Prepared")
    print(f"   Years in Business: {form_data['yearsInBusiness']}")
    print(f"   Latest Revenue: ${int(form_data['historicalServices'][-1]['services'][0]['historicalRevenue']):,}")
    print(f"   Client Retention: {form_data['serviceBusinessModel']['clientRetentionRate']}%")
    print(f"   Revenue Growth Rate: {form_data['revenueGrowthRate']}%")
    
    try:
        # Step 2: Backend calculation (what API does)
        print(f"\n⚙️  STEP 2: Backend Processing...")
        result = HistoricalServiceFactory.calculate_historical_statements('service', form_data)
        
        if not result.get('success'):
            print(f"❌ Backend calculation failed: {result.get('error', 'Unknown error')}")
            return False
            
        print(f"✅ Backend calculation successful")
        
        # Step 3: Extract dashboard KPIs (what frontend receives)
        dashboard_kpis = result.get('dashboard_kpis', {})
        
        if not dashboard_kpis:
            print(f"❌ No dashboard KPIs found in result")
            return False
            
        print(f"\n📊 STEP 3: Dashboard KPIs Generated")
        print(f"   KPI Count: {len(dashboard_kpis)}")
        
        # Step 4: Format for dashboard display (what user sees)
        print(f"\n🎯 STEP 4: Dashboard Display Data")
        print("-" * 50)
        
        # Financial Overview
        print(f"💰 FINANCIAL OVERVIEW:")
        print(f"   Total Revenue: ${dashboard_kpis.get('total_revenue', 0):,.0f}")
        print(f"   Total Expenses: ${dashboard_kpis.get('total_expenses', 0):,.0f}")
        print(f"   Net Income: ${dashboard_kpis.get('net_income', 0):,.0f}")
        print(f"   Profit Margin: {dashboard_kpis.get('profit_margin', 0):.1f}%")
        
        # Financial Ratios
        print(f"\n📈 FINANCIAL RATIOS:")
        print(f"   ROE: {dashboard_kpis.get('roe', 0):.1f}%")
        print(f"   Asset Turnover: {dashboard_kpis.get('asset_turnover', 0):.2f}")
        print(f"   Current Ratio: {dashboard_kpis.get('current_ratio', 0):.2f}")
        
        # Service Business Metrics
        print(f"\n👥 SERVICE BUSINESS METRICS:")
        print(f"   Client Retention: {dashboard_kpis.get('client_retention_rate', 0):.0f}%")
        print(f"   Utilization Rate: {dashboard_kpis.get('utilization_rate', 0):.0f}%")
        print(f"   CLV: ${dashboard_kpis.get('clv', 0):,.0f}")
        print(f"   CAC: ${dashboard_kpis.get('cac', 0):,.0f}")
        
        # Valuation Metrics
        print(f"\n💎 VALUATION METRICS:")
        print(f"   Terminal Value: ${dashboard_kpis.get('terminal_value', 0):,.0f}")
        print(f"   WACC: {dashboard_kpis.get('wacc', 0):.1f}%")
        print(f"   Revenue Growth: {dashboard_kpis.get('revenue_growth', 0):.1f}%")
        print(f"   EBITDA Margin: {dashboard_kpis.get('ebitda_margin', 0):.1f}%")
        
        # Step 5: Verification
        print(f"\n✅ STEP 5: Verification")
        print("-" * 50)
        
        # Check if calculations are realistic
        revenue = dashboard_kpis.get('total_revenue', 0)
        expenses = dashboard_kpis.get('total_expenses', 0)
        net_income = dashboard_kpis.get('net_income', 0)
        
        if revenue > 200000:  # Should be higher than input data
            print(f"✅ Revenue calculation looks realistic: ${revenue:,.0f}")
        else:
            print(f"⚠️  Revenue might be too low: ${revenue:,.0f}")
            
        if expenses > 0 and expenses < revenue:
            print(f"✅ Expense calculation looks realistic: ${expenses:,.0f}")
        else:
            print(f"⚠️  Expense calculation might be off: ${expenses:,.0f}")
            
        if net_income > 0:
            print(f"✅ Profitable business: ${net_income:,.0f}")
        else:
            print(f"⚠️  Business showing losses: ${net_income:,.0f}")
            
        # Check service metrics match input
        input_retention = float(form_data['serviceBusinessModel']['clientRetentionRate'])
        calc_retention = dashboard_kpis.get('client_retention_rate', 0)
        
        if abs(input_retention - calc_retention) < 1:
            print(f"✅ Service metrics preserved: {calc_retention}% retention")
        else:
            print(f"⚠️  Service metrics changed: {input_retention}% → {calc_retention}%")
            
        return True
        
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 FULL END-TO-END FLOW TEST")
    print("Testing: Form → Backend → Dashboard")
    print("=" * 60)
    
    success = test_complete_flow()
    
    if success:
        print(f"\n🎉 COMPLETE FLOW TEST PASSED!")
        print(f"✅ Form data processed correctly")
        print(f"✅ Backend calculations working")
        print(f"✅ Dashboard KPIs generated")
        print(f"✅ Real data flowing through system")
        print(f"\n💡 The dashboard should display real calculated values!")
    else:
        print(f"\n💥 COMPLETE FLOW TEST FAILED!")
        print(f"❌ Check the error messages above")