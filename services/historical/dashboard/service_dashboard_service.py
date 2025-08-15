"""
Service Company Dashboard Service

Implementation of dashboard calculations for service companies.
This handles service-specific metrics, KPIs, and visualizations.
"""

from typing import Dict, Any, List, Optional
from .base_dashboard_service import BaseDashboardService
import datetime
import math
from services.dcf_calculation import calculate_sensitivity_analysis, calculate_tornado_data


class ServiceDashboardService(BaseDashboardService):
    """
    Dashboard service implementation for service companies.
    
    This handles service-specific dashboard calculations, metrics, and visualizations
    for businesses that provide services rather than physical products.
    """
    
    def __init__(self):
        """Initialize service dashboard service."""
        super().__init__("service")
    
    def _get_supported_metrics(self) -> List[str]:
        """Get metrics supported by service companies."""
        return [
            'revenue_per_employee',
            'profit_margin',
            'operating_margin',
            'ebitda_margin',
            'revenue_growth_rate',
            'customer_acquisition_cost',
            'customer_lifetime_value',
            'recurring_revenue_ratio',
            'service_delivery_efficiency',
            'utilization_rate',
            'billable_hours',
            'average_project_size',
            'client_retention_rate',
            'service_quality_score',
            'employee_productivity',
            'client_satisfaction_score',
            'project_completion_rate',
            'service_delivery_time',
            'cost_per_service_hour',
            'revenue_per_service_hour'
        ]
    
    def _get_required_fields(self) -> List[str]:
        """Get required fields for service companies."""
        return [
            'total revenue',  # These match the actual line item labels from financial statements
            'total operating expenses',
            'net income'
        ]
    
    def _get_company_description(self) -> str:
        """Get description of service companies."""
        return "Service companies provide intangible services to clients. Key metrics include utilization rates, billable hours, and service delivery efficiency."
    
    def _calculate_company_specific_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate service-specific metrics and comprehensive dashboard KPIs."""
        income_statement = data.get('income_statement', {})
        balance_sheet = data.get('balance_sheet', {})
        cash_flow = data.get('cash_flow', {})
        
        # Extract service-specific data from the original input data
        service_data = data.get('service_data', {})
        original_data = data.get('original_data', {})
        
        # Calculate comprehensive dashboard KPIs
        dashboard_kpis = self._calculate_comprehensive_dashboard_kpis(
            income_statement, balance_sheet, cash_flow, original_data
        )
        
        return {
            'operational': self._calculate_operational_metrics(income_statement, service_data),
            'efficiency': self._calculate_efficiency_metrics(income_statement, service_data),
            'client_metrics': self._calculate_client_metrics(service_data),
            'employee_metrics': self._calculate_employee_metrics(income_statement, service_data),
            'service_quality': self._calculate_service_quality_metrics(service_data),
            'dashboard_kpis': dashboard_kpis  # Add comprehensive KPIs
        }
    
    def _calculate_operational_metrics(self, income_statement: Dict[str, Any], service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate operational metrics for service companies."""
        revenue = self._get_value_from_statement(income_statement, 'Revenue', 0)
        operating_expenses = self._get_value_from_statement(income_statement, 'Operating Expenses', 0)
        net_income = self._get_value_from_statement(income_statement, 'Net Income', 0)
        
        # Service-specific operational metrics
        employee_count = service_data.get('employee_count', 1)
        billable_hours = service_data.get('billable_hours', 0)
        total_hours = service_data.get('total_hours', billable_hours)
        
        return {
            'revenue_per_employee': revenue / employee_count if employee_count > 0 else 0,
            'profit_per_employee': net_income / employee_count if employee_count > 0 else 0,
            'utilization_rate': (billable_hours / total_hours * 100) if total_hours > 0 else 0,
            'billable_hours_per_employee': billable_hours / employee_count if employee_count > 0 else 0,
            'operating_margin': (net_income / revenue * 100) if revenue > 0 else 0,
            'cost_per_hour': operating_expenses / billable_hours if billable_hours > 0 else 0
        }
    
    def _calculate_efficiency_metrics(self, income_statement: Dict[str, Any], service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate efficiency metrics for service companies."""
        revenue = self._get_value_from_statement(income_statement, 'Revenue', 0)
        operating_expenses = self._get_value_from_statement(income_statement, 'Operating Expenses', 0)
        
        # Service delivery efficiency
        service_delivery_costs = service_data.get('service_delivery_costs', 0)
        total_projects = service_data.get('total_projects', 1)
        completed_projects = service_data.get('completed_projects', 0)
        
        return {
            'service_delivery_efficiency': (revenue / service_delivery_costs) if service_delivery_costs > 0 else 0,
            'project_completion_rate': (completed_projects / total_projects * 100) if total_projects > 0 else 0,
            'revenue_per_project': revenue / total_projects if total_projects > 0 else 0,
            'cost_per_project': service_delivery_costs / total_projects if total_projects > 0 else 0,
            'efficiency_ratio': (revenue / operating_expenses) if operating_expenses > 0 else 0
        }
    
    def _calculate_client_metrics(self, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate client-related metrics."""
        total_clients = service_data.get('total_clients', 0)
        new_clients = service_data.get('new_clients', 0)
        retained_clients = service_data.get('retained_clients', 0)
        average_project_value = service_data.get('average_project_value', 0)
        client_satisfaction = service_data.get('client_satisfaction_score', 0)
        
        return {
            'client_retention_rate': (retained_clients / total_clients * 100) if total_clients > 0 else 0,
            'client_acquisition_rate': (new_clients / total_clients * 100) if total_clients > 0 else 0,
            'average_project_size': average_project_value,
            'client_satisfaction_score': client_satisfaction,
            'clients_per_employee': total_clients / service_data.get('employee_count', 1) if service_data.get('employee_count', 1) > 0 else 0
        }
    
    def _calculate_employee_metrics(self, income_statement: Dict[str, Any], service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate employee-related metrics."""
        revenue = self._get_value_from_statement(income_statement, 'Revenue', 0)
        employee_count = service_data.get('employee_count', 1)
        billable_hours = service_data.get('billable_hours', 0)
        total_hours = service_data.get('total_hours', billable_hours)
        
        return {
            'revenue_per_employee': revenue / employee_count if employee_count > 0 else 0,
            'billable_hours_per_employee': billable_hours / employee_count if employee_count > 0 else 0,
            'utilization_per_employee': (billable_hours / total_hours * 100) if total_hours > 0 else 0,
            'employee_productivity': revenue / billable_hours if billable_hours > 0 else 0
        }
    
    def _calculate_service_quality_metrics(self, service_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate service quality metrics."""
        total_projects = service_data.get('total_projects', 0)
        completed_projects = service_data.get('completed_projects', 0)
        on_time_deliveries = service_data.get('on_time_deliveries', 0)
        client_satisfaction = service_data.get('client_satisfaction_score', 0)
        service_delivery_time = service_data.get('average_delivery_time', 0)
        
        return {
            'project_completion_rate': (completed_projects / total_projects * 100) if total_projects > 0 else 0,
            'on_time_delivery_rate': (on_time_deliveries / completed_projects * 100) if completed_projects > 0 else 0,
            'service_quality_score': client_satisfaction,
            'average_delivery_time': service_delivery_time,
            'quality_efficiency': (completed_projects / total_projects * client_satisfaction / 100) if total_projects > 0 else 0
        }
    
    def _generate_revenue_breakdown_chart(self, income_statement: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate service-specific revenue breakdown chart data."""
        # Get service breakdown from additional data
        service_data = income_statement.get('service_breakdown', {})
        
        if not service_data:
            # Fallback to basic revenue breakdown
            return super()._generate_revenue_breakdown_chart(income_statement)
        
        chart_data = []
        for service_type, revenue in service_data.items():
            chart_data.append({
                'name': service_type,
                'value': revenue,
                'percentage': 0  # Will be calculated by frontend
            })
        
        return chart_data
    
    def _generate_expense_breakdown_chart(self, income_statement: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate service-specific expense breakdown chart data."""
        # Get expense breakdown from additional data
        expense_data = income_statement.get('expense_breakdown', {})
        
        if not expense_data:
            # Fallback to basic expense breakdown
            return super()._generate_expense_breakdown_chart(income_statement)
        
        chart_data = []
        for expense_category, amount in expense_data.items():
            chart_data.append({
                'name': expense_category,
                'value': amount,
                'percentage': 0  # Will be calculated by frontend
            })
        
        return chart_data
    
    def _generate_service_specific_charts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate service-specific chart data."""
        service_data = data.get('service_data', {})
        
        return {
            'utilization_trend': self._generate_utilization_trend_chart(service_data),
            'client_growth': self._generate_client_growth_chart(service_data),
            'project_efficiency': self._generate_project_efficiency_chart(service_data),
            'employee_productivity': self._generate_employee_productivity_chart(service_data)
        }
    
    def _generate_utilization_trend_chart(self, service_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate utilization trend chart data."""
        years = service_data.get('years', [])
        utilization_rates = service_data.get('utilization_rates', [])
        
        chart_data = []
        for i, year in enumerate(years):
            chart_data.append({
                'year': year,
                'utilization_rate': utilization_rates[i] if i < len(utilization_rates) else 0,
                'target_rate': 80  # Industry standard
            })
        
        return chart_data
    
    def _generate_client_growth_chart(self, service_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate client growth chart data."""
        years = service_data.get('years', [])
        total_clients = service_data.get('total_clients_by_year', [])
        new_clients = service_data.get('new_clients_by_year', [])
        
        chart_data = []
        for i, year in enumerate(years):
            chart_data.append({
                'year': year,
                'total_clients': total_clients[i] if i < len(total_clients) else 0,
                'new_clients': new_clients[i] if i < len(new_clients) else 0
            })
        
        return chart_data
    
    def _generate_project_efficiency_chart(self, service_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate project efficiency chart data."""
        years = service_data.get('years', [])
        completion_rates = service_data.get('project_completion_rates', [])
        on_time_rates = service_data.get('on_time_delivery_rates', [])
        
        chart_data = []
        for i, year in enumerate(years):
            chart_data.append({
                'year': year,
                'completion_rate': completion_rates[i] if i < len(completion_rates) else 0,
                'on_time_rate': on_time_rates[i] if i < len(on_time_rates) else 0
            })
        
        return chart_data
    
    def _generate_employee_productivity_chart(self, service_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate employee productivity chart data."""
        years = service_data.get('years', [])
        revenue_per_employee = service_data.get('revenue_per_employee', [])
        billable_hours_per_employee = service_data.get('billable_hours_per_employee', [])
        
        chart_data = []
        for i, year in enumerate(years):
            chart_data.append({
                'year': year,
                'revenue_per_employee': revenue_per_employee[i] if i < len(revenue_per_employee) else 0,
                'billable_hours_per_employee': billable_hours_per_employee[i] if i < len(billable_hours_per_employee) else 0
            })
        
        return chart_data
    
    def _generate_insights(self, data: Dict[str, Any], common_metrics: Dict[str, Any], company_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate service-specific insights."""
        insights = super()._generate_insights(data, common_metrics, company_metrics)
        
        # Add service-specific insights
        operational_metrics = company_metrics.get('operational', {})
        efficiency_metrics = company_metrics.get('efficiency', {})
        client_metrics = company_metrics.get('client_metrics', {})
        
        # Utilization insights
        utilization_rate = operational_metrics.get('utilization_rate', 0)
        if utilization_rate < 60:
            insights['performance_insights'].append("Low utilization rate - consider improving resource allocation")
        elif utilization_rate > 90:
            insights['performance_insights'].append("High utilization rate - may need to hire additional staff")
        
        # Client retention insights
        client_retention = client_metrics.get('client_retention_rate', 0)
        if client_retention < 80:
            insights['performance_insights'].append("Low client retention rate - focus on customer satisfaction")
        elif client_retention > 95:
            insights['performance_insights'].append("Excellent client retention - strong customer relationships")
        
        # Project efficiency insights
        completion_rate = efficiency_metrics.get('project_completion_rate', 0)
        if completion_rate < 85:
            insights['performance_insights'].append("Low project completion rate - review project management processes")
        
        # Employee productivity insights
        revenue_per_employee = operational_metrics.get('revenue_per_employee', 0)
        if revenue_per_employee < 100000:  # $100k per employee threshold
            insights['recommendations'].append("Consider training programs to improve employee productivity")
        
        return insights
    
    def _calculate_comprehensive_dashboard_kpis(self, income_statement: Dict[str, Any], 
                                              balance_sheet: Dict[str, Any], 
                                              cash_flow: Dict[str, Any],
                                              original_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive dashboard KPIs using data from financial statements.
        This replaces the dashboard KPI calculation that was in base_historical_service.
        """
        from .dashboard_calculator import DashboardCalculator
        
        # Extract years for calculations
        years = income_statement.get('years', [])
        total_years = len(years)
        
        if total_years == 0:
            return {}
        
        # Get line items from statements
        income_line_items = income_statement.get('line_items', [])
        balance_line_items = balance_sheet.get('line_items', [])
        
        # Helper function to find values from line items
        def find_line_item_values(line_items, label_keywords):
            # First pass: Try exact matches (prioritize exact matches)
            for item in line_items:
                label = item.get('label', '').strip()
                for keyword in label_keywords:
                    if label == keyword:  # Exact match
                        return item.get('values', [])
            
            # Second pass: Try case-insensitive contains matches
            for item in line_items:
                label = item.get('label', '').strip()
                for keyword in label_keywords:
                    if keyword.lower() in label.lower():  # Contains match
                        return item.get('values', [])
            
            return [0] * total_years
        
        # Extract key financial data - use exact case-insensitive matching
        revenue_values = find_line_item_values(income_line_items, ['TOTAL REVENUE', 'total revenue', 'revenue'])
        net_income_values = find_line_item_values(income_line_items, ['NET INCOME', 'net income'])
        ebitda_values = find_line_item_values(income_line_items, ['EBITDA', 'ebitda'])
        operating_expenses_values = find_line_item_values(income_line_items, ['TOTAL OPERATING EXPENSES', 'total operating expenses', 'operating expenses'])
        
        # Balance sheet items - use exact case-insensitive matching
        total_assets_values = find_line_item_values(balance_line_items, ['TOTAL ASSETS', 'total assets'])
        total_liabilities_values = find_line_item_values(balance_line_items, ['TOTAL LIABILITIES', 'total liabilities'])
        total_equity_values = find_line_item_values(balance_line_items, ['TOTAL EQUITY', 'total equity'])
        current_assets_values = find_line_item_values(balance_line_items, ['Total Current Assets', 'total current assets', 'current assets'])
        current_liabilities_values = find_line_item_values(balance_line_items, ['Total Current Liabilities', 'total current liabilities', 'current liabilities'])
        
        # Calculate KPIs using the base year data (current year, not forecast)
        # Base year is the last historical year (years_in_business - 1 index)
        years_in_business = int(original_data.get('yearsInBusiness', 2))
        base_year_idx = years_in_business - 1  # Index of the base year (current year)
        
        # Validate base year index
        if base_year_idx >= len(years) or base_year_idx < 0:
            base_year_idx = 0  # Fallback to first year if index is invalid
        
        # Basic financial metrics - use base year (current year) data
        total_revenue = revenue_values[base_year_idx] if revenue_values and base_year_idx < len(revenue_values) else 0
        total_expenses = operating_expenses_values[base_year_idx] if operating_expenses_values and base_year_idx < len(operating_expenses_values) else 0
        net_income = net_income_values[base_year_idx] if net_income_values and base_year_idx < len(net_income_values) else 0
        ebitda = ebitda_values[base_year_idx] if ebitda_values and base_year_idx < len(ebitda_values) else 0
        
        total_assets = total_assets_values[base_year_idx] if total_assets_values and base_year_idx < len(total_assets_values) else 0
        total_liabilities = total_liabilities_values[base_year_idx] if total_liabilities_values and base_year_idx < len(total_liabilities_values) else 0
        total_equity = total_equity_values[base_year_idx] if total_equity_values and base_year_idx < len(total_equity_values) else 0
        current_assets = current_assets_values[base_year_idx] if current_assets_values and base_year_idx < len(current_assets_values) else 0
        current_liabilities = current_liabilities_values[base_year_idx] if current_liabilities_values and base_year_idx < len(current_liabilities_values) else 0
        
        # Calculate ratios
        profit_margin = (net_income / total_revenue * 100) if total_revenue != 0 else 0
        ebitda_margin = (ebitda / total_revenue * 100) if total_revenue != 0 else 0
        roe = (net_income / total_equity * 100) if total_equity != 0 else 0
        asset_turnover = (total_revenue / total_assets) if total_assets != 0 else 0
        current_ratio = (current_assets / current_liabilities) if current_liabilities != 0 else 0
        debt_to_equity = (total_liabilities / total_equity) if total_equity != 0 else 0
        
        # Calculate growth rates
        revenue_growth = DashboardCalculator.calculate_growth_rate(revenue_values) if len(revenue_values) > 1 else 0
        
        # Service-specific metrics from original data
        service_business_model = original_data.get('serviceBusinessModel', {})
        client_retention_rate = float(service_business_model.get('clientRetentionRate', 85))
        utilization_rate = float(service_business_model.get('utilizationRate', 75))
        clv = float(service_business_model.get('customerLifetimeValue', 25000))
        cac = float(service_business_model.get('clientAcquisitionCost', 1500))
        
        # Financial assumptions
        wacc = float(original_data.get('discountRate', 10))
        terminal_growth = float(original_data.get('terminalGrowth', 2))
        
        # Calculate Free Cash Flow (FCF) from cash flow statement
        fcf_values = self._calculate_free_cash_flow(cash_flow, income_statement, total_years)
        
        # Calculate terminal value (simplified DCF approach)
        if len(net_income_values) > 0:
            final_year_net_income = net_income_values[-1]
            terminal_value = (final_year_net_income * (1 + terminal_growth/100)) / ((wacc/100) - (terminal_growth/100))
        else:
            terminal_value = 0
        
        # Calculate comprehensive ratios using new organized approach
        base_ratios = self._calculate_base_ratios(
            total_revenue, total_expenses, net_income, ebitda,
            total_assets, total_equity, current_assets, current_liabilities, 
            total_liabilities, revenue_values
        )
        
        service_ratios = self._calculate_service_specific_ratios(original_data)
        
        # Calculate base case sensitivity analysis KPIs
        base_case_kpis = self._calculate_base_case_sensitivity_kpis(
            income_statement, balance_sheet, cash_flow, original_data
        )
        
        return {
            # Core financial metrics
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_income': net_income,
            'ebitda': ebitda,
            
            # Balance sheet metrics
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'total_equity': total_equity,
            'current_assets': current_assets,
            'current_liabilities': current_liabilities,
            
            # Base ratios (applicable to all company types)
            **base_ratios,
            
            # Service-specific ratios
            **service_ratios,
            
            # Legacy compatibility (these are now in base_ratios but kept for compatibility)
            'profit_margin': profit_margin,
            'ebitda_margin': ebitda_margin,
            'roe': roe,
            'asset_turnover': asset_turnover,
            'current_ratio': current_ratio,
            'debt_to_equity': debt_to_equity,
            'revenue_growth': revenue_growth,
            
            # Service-specific metrics
            'client_retention_rate': client_retention_rate,
            'utilization_rate': utilization_rate,
            'clv': clv,
            'cac': cac,
            
            # Valuation metrics
            'wacc': wacc,
            'terminal_growth': terminal_growth,
            'terminal_value': terminal_value,
            
            # Free Cash Flow metrics
            'free_cash_flow_all_years': fcf_values,
            'fcf_base_year': fcf_values[base_year_idx] if fcf_values and base_year_idx < len(fcf_values) else 0,
            
            # Revenue vs Expenses donut chart data (base year)
            'donut_chart_data': self._calculate_donut_chart_data(
                total_revenue, total_expenses, net_income, ebitda
            ),
            
            # Tornado chart data for sensitivity analysis
            'tornado_chart_data': self._calculate_tornado_chart_data(
                total_revenue, ebitda, net_income, fcf_values, original_data
            ),
            
            # Sensitivity heatmap data
            'sensitivity_heatmap_data': self._calculate_sensitivity_heatmap_data(
                total_revenue, ebitda, net_income, original_data
            ),
            
            # Vertical and horizontal analysis
            'vertical_analysis': self._calculate_vertical_analysis(income_statement, balance_sheet),
            'horizontal_analysis': self._calculate_horizontal_analysis(income_statement, balance_sheet),
            
            # Base case sensitivity analysis KPIs
            **base_case_kpis,
            
            # Chart data for all years (for revenue vs expense graph and FCF chart)
            'chart_data': {
                'years': years,
                'revenue_all_years': revenue_values,
                'expenses_all_years': operating_expenses_values,
                'net_income_all_years': net_income_values,
                'ebitda_all_years': ebitda_values,
                'free_cash_flow_all_years': fcf_values
            }
        }
    
    def _calculate_free_cash_flow(self, cash_flow: Dict[str, Any], income_statement: Dict[str, Any], total_years: int) -> List[float]:
        """
        Calculate Free Cash Flow (FCF) for all years.
        FCF = Net Cash from Operations - Capital Expenditures
        """
        fcf_values = [0] * total_years
        
        try:
            # Get cash flow line items
            cash_flow_line_items = cash_flow.get('line_items', [])
            
            # Helper function to find values from cash flow line items
            def find_cash_flow_values(label_keywords):
                for item in cash_flow_line_items:
                    label = item.get('label', '').strip()
                    for keyword in label_keywords:
                        if keyword.lower() in label.lower():
                            return item.get('values', [])
                return [0] * total_years
            
            # Get operating cash flow
            operating_cash_flow = find_cash_flow_values([
                'Net Cash from Operations', 
                'net cash from operations',
                'operating cash flow',
                'cash from operating activities'
            ])
            
            # Get capital expenditures (usually negative in cash flow)
            capital_expenditures = find_cash_flow_values([
                'Capital Expenditures', 
                'capital expenditures',
                'capex',
                'equipment purchases',
                'property plant equipment'
            ])
            
            # If we can't find specific line items, try to calculate from income statement
            if not operating_cash_flow or all(v == 0 for v in operating_cash_flow):
                print("Operating cash flow not found in cash flow statement, estimating from income statement")
                # Estimate operating cash flow as Net Income + Depreciation (simplified)
                income_line_items = income_statement.get('line_items', [])
                
                net_income_values = []
                depreciation_values = []
                
                for item in income_line_items:
                    label = item.get('label', '').strip().lower()
                    if 'net income' in label:
                        net_income_values = item.get('values', [])
                    elif 'depreciation' in label or 'amortization' in label:
                        depreciation_values = item.get('values', [])
                
                # Estimate operating cash flow
                if net_income_values:
                    operating_cash_flow = net_income_values[:]
                    if depreciation_values:
                        for i in range(min(len(operating_cash_flow), len(depreciation_values))):
                            operating_cash_flow[i] += abs(depreciation_values[i])  # Add back depreciation
            
            # Ensure arrays have correct length
            if len(operating_cash_flow) < total_years:
                operating_cash_flow.extend([0] * (total_years - len(operating_cash_flow)))
            if len(capital_expenditures) < total_years:
                capital_expenditures.extend([0] * (total_years - len(capital_expenditures)))
            
            # Calculate FCF = Operating Cash Flow - Capital Expenditures
            for i in range(total_years):
                operating_cf = operating_cash_flow[i] if i < len(operating_cash_flow) else 0
                capex = capital_expenditures[i] if i < len(capital_expenditures) else 0
                
                # Capital expenditures are usually negative in cash flow statements
                # If they're negative, we subtract the negative (which adds them)
                # If they're positive, we subtract them
                if capex < 0:
                    fcf_values[i] = operating_cf + capex  # capex is negative, so this subtracts
                else:
                    fcf_values[i] = operating_cf - capex  # capex is positive, so we subtract
            
            print(f"=== FCF CALCULATION DEBUG ===")
            print(f"Operating Cash Flow: {operating_cash_flow[:5]}...")  # First 5 values
            print(f"Capital Expenditures: {capital_expenditures[:5]}...")  # First 5 values
            print(f"Calculated FCF: {fcf_values[:5]}...")  # First 5 values
            
        except Exception as e:
            print(f"Error calculating Free Cash Flow: {str(e)}")
            # Return zeros if calculation fails
            fcf_values = [0] * total_years
        
        return fcf_values
    
    def _calculate_donut_chart_data(self, revenue: float, expenses: float, net_income: float, ebitda: float) -> Dict[str, Any]:
        """
        Calculate data for Revenue vs Expenses donut chart using base year data.
        Returns data with values and percentages for visualization.
        """
        try:
            # Ensure we have valid numbers
            revenue = float(revenue) if revenue else 0
            expenses = float(expenses) if expenses else 0
            net_income = float(net_income) if net_income else 0
            ebitda = float(ebitda) if ebitda else 0
            
            # If we have negative net income, adjust the calculation
            # Revenue = Expenses + Net Income (if net income is positive)
            # If net income is negative, then Expenses > Revenue
            
            # Calculate total for percentage calculation
            # For donut chart, we want to show: Revenue vs Expenses breakdown
            # Method 1: Show Revenue and Expenses as parts of total cash flow
            # Method 2: Show how revenue is split between expenses and profit
            
            # Simple Revenue vs Expenses donut chart (comparison view)
            if revenue > 0:
                # Calculate total for percentage calculation (Revenue + Expenses as comparison)
                total_comparison = revenue + expenses
                
                # Calculate percentages based on total comparison
                revenue_percentage = (revenue / total_comparison) * 100 if total_comparison > 0 else 0
                expense_percentage = (expenses / total_comparison) * 100 if total_comparison > 0 else 0
                
                donut_data = [
                    {
                        'name': 'Revenue',
                        'value': revenue,
                        'percentage': revenue_percentage,
                        'color': '#22c55e',  # Green color for revenue
                        'format': 'currency'
                    },
                    {
                        'name': 'Operating Expenses',
                        'value': expenses,
                        'percentage': expense_percentage,
                        'color': '#ef4444',  # Red color for expenses
                        'format': 'currency'
                    }
                ]
                
            else:
                # Edge case: No revenue data
                donut_data = [
                    {
                        'name': 'No Revenue Data',
                        'value': 0,
                        'percentage': 0,
                        'color': '#9ca3af',
                        'format': 'currency'
                    }
                ]
            
            # Calculate summary metrics
            profit_margin = (net_income / revenue * 100) if revenue > 0 else 0
            expense_ratio = (expenses / revenue * 100) if revenue > 0 else 0
            
            return {
                'chart_data': donut_data,
                'summary': {
                    'total_revenue': revenue,
                    'total_expenses': expenses,
                    'net_income': net_income,
                    'ebitda': ebitda,
                    'profit_margin': profit_margin,
                    'expense_ratio': expense_ratio,
                    'is_profitable': net_income > 0
                },
                'base_year_metrics': {
                    'revenue_per_dollar': 1.0,  # Base metric
                    'expense_per_dollar': (expenses / revenue) if revenue > 0 else 0,
                    'profit_per_dollar': (net_income / revenue) if revenue > 0 else 0
                }
            }
            
        except Exception as e:
            print(f"Error calculating donut chart data: {str(e)}")
            return {
                'chart_data': [],
                'summary': {
                    'total_revenue': 0,
                    'total_expenses': 0,
                    'net_income': 0,
                    'ebitda': 0,
                    'profit_margin': 0,
                    'expense_ratio': 0,
                    'is_profitable': False
                },
                'base_year_metrics': {
                    'revenue_per_dollar': 0,
                    'expense_per_dollar': 0,
                    'profit_per_dollar': 0
                }
            }

    def _calculate_tornado_chart_data(self, revenue: float, ebitda: float, net_income: float, fcf_values: List[float], original_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Calculate tornado chart data using real DCF sensitivity analysis with user's actual assumptions.
        Shows actual DCF valuation impact from key variable changes.
        """
        try:
            revenue = float(revenue) if revenue else 0
            ebitda = float(ebitda) if ebitda else 0
            net_income = float(net_income) if net_income else 0
            
            # Use actual FCF values from cash flow statement
            if not fcf_values or len(fcf_values) == 0:
                # Fallback: estimate FCF from net income if no cash flow data
                fcf_values = [net_income * 0.8]  # Assume 80% of net income converts to FCF
            
            # Extract user's actual assumptions from original_data
            user_wacc = original_data.get('discount_rate', 0.12) if original_data else 0.12
            user_terminal_growth = original_data.get('terminal_growth_rate', 0.03) if original_data else 0.03
            user_revenue_growth = original_data.get('revenue_growth_rate', 0.10) if original_data else 0.10
            
            # Define sensitivity ranges centered around user's actual assumptions
            sensitivity_ranges = {
                'revenue_growth': {'low': -0.15, 'high': 0.25, 'type': 'fcf'},  # -15% to +25%
                'operating_margin': {'low': -0.10, 'high': 0.15, 'type': 'fcf'},  # -10% to +15%
                'wacc': {'low': max(0.05, user_wacc - 0.04), 'high': min(0.20, user_wacc + 0.04), 'type': 'wacc'},  # ±4% around user's WACC
                'terminal_growth': {'low': max(0.005, user_terminal_growth - 0.02), 'high': min(0.08, user_terminal_growth + 0.02), 'type': 'growth'}  # ±2% around user's terminal growth
            }
            
            # Use user's actual assumptions as base values
            base_discount_rate = user_wacc
            base_terminal_growth = user_terminal_growth
            
            # Terminal value calculation function
            def terminal_value_func(last_fcf: float, growth_rate: float, discount_rate: float) -> float:
                if discount_rate <= growth_rate:
                    return last_fcf * 20  # High multiple for low discount rate
                return last_fcf * (1 + growth_rate) / (discount_rate - growth_rate)
            
            # Use real DCF sensitivity analysis with user's assumptions
            tornado_data = calculate_tornado_data(
                fcf_values, 
                base_discount_rate, 
                base_terminal_growth, 
                sensitivity_ranges, 
                terminal_value_func
            )
            
            print(f"=== REAL DCF TORNADO CHART CALCULATION (USER ASSUMPTIONS) ===")
            print(f"User WACC: {user_wacc}")
            print(f"User Terminal Growth: {user_terminal_growth}")
            print(f"User Revenue Growth: {user_revenue_growth}")
            print(f"FCF values: {fcf_values}")
            print(f"Base discount rate: {base_discount_rate}")
            print(f"Base terminal growth: {base_terminal_growth}")
            print(f"Tornado data points: {len(tornado_data)}")
            for item in tornado_data:
                print(f"{item['variable']}: Low={item['low']:.0f}, High={item['high']:.0f}")
            
            return tornado_data
            
        except Exception as e:
            print(f"Error calculating tornado chart data: {str(e)}")
            # Fallback to simplified calculation if DCF fails
            return self._calculate_simplified_tornado_data(revenue, ebitda, net_income, fcf_values, original_data)
    
    def _calculate_simplified_tornado_data(self, revenue: float, ebitda: float, net_income: float, fcf_values: List[float], original_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fallback simplified tornado chart calculation if DCF analysis fails.
        """
        try:
            revenue = float(revenue) if revenue else 0
            ebitda = float(ebitda) if ebitda else 0
            net_income = float(net_income) if net_income else 0
            
            # Base FCF for calculations (use latest year if available)
            base_fcf = fcf_values[-1] if fcf_values else 0
            
            # Base DCF valuation (simplified calculation: FCF * 10 as a multiple)
            base_dcf = base_fcf * 10 if base_fcf else revenue * 2  # Fallback to revenue multiple
            
            tornado_data = []
            
            # Revenue Growth Rate impact - use user's actual growth rate as reference
            user_revenue_growth = original_data.get('revenue_growth_rate', 0.10) if original_data else 0.10
            revenue_low = base_dcf * 0.75  # -25% impact on valuation
            revenue_high = base_dcf * 1.35  # +35% impact on valuation
            tornado_data.append({
                'variable': f'Revenue Growth ({user_revenue_growth*100:.1f}%)',
                'low': revenue_low,
                'high': revenue_high,
                'base': base_dcf
            })
            
            # EBITDA Margin impact - use user's actual margin as reference
            user_ebitda_margin = original_data.get('ebitda_margin', 0.15) if original_data else 0.15
            ebitda_low = base_dcf * 0.70  # -30% impact on valuation
            ebitda_high = base_dcf * 1.40  # +40% impact on valuation
            tornado_data.append({
                'variable': f'EBITDA Margin ({user_ebitda_margin*100:.1f}%)',
                'low': ebitda_low,
                'high': ebitda_high,
                'base': base_dcf
            })
            
            # WACC (Cost of Capital) impact - use user's actual WACC as reference
            user_wacc = original_data.get('discount_rate', 0.12) if original_data else 0.12
            wacc_low = base_dcf * 1.25  # Lower WACC = Higher valuation
            wacc_high = base_dcf * 0.80  # Higher WACC = Lower valuation
            tornado_data.append({
                'variable': f'WACC ({user_wacc*100:.1f}%)',
                'low': wacc_high,  # Note: reversed because higher WACC = lower value
                'high': wacc_low,
                'base': base_dcf
            })
            
            # Terminal Growth Rate impact - use user's actual terminal growth as reference
            user_terminal_growth = original_data.get('terminal_growth_rate', 0.03) if original_data else 0.03
            terminal_low = base_dcf * 0.85  # -15% impact
            terminal_high = base_dcf * 1.20  # +20% impact
            tornado_data.append({
                'variable': f'Terminal Growth ({user_terminal_growth*100:.1f}%)',
                'low': terminal_low,
                'high': terminal_high,
                'base': base_dcf
            })
            
            # Exit Multiple impact - use user's actual assumptions as reference
            user_exit_multiple = original_data.get('exit_multiple', 8.0) if original_data else 8.0
            exit_low = base_dcf * 0.65  # -35% impact
            exit_high = base_dcf * 1.45  # +45% impact
            tornado_data.append({
                'variable': f'Exit Multiple ({user_exit_multiple:.1f}x)',
                'low': exit_low,
                'high': exit_high,
                'base': base_dcf
            })
            
            print(f"=== SIMPLIFIED TORNADO CHART CALCULATION (USER ASSUMPTIONS) ===")
            print(f"User WACC: {original_data.get('discount_rate', 0.12) if original_data else 0.12}")
            print(f"User Terminal Growth: {original_data.get('terminal_growth_rate', 0.03) if original_data else 0.03}")
            print(f"User Revenue Growth: {original_data.get('revenue_growth_rate', 0.10) if original_data else 0.10}")
            print(f"Base DCF: {base_dcf}")
            print(f"Tornado data points: {len(tornado_data)}")
            for item in tornado_data:
                print(f"{item['variable']}: Low={item['low']:.0f}, High={item['high']:.0f}")
            
            return tornado_data
            
        except Exception as e:
            print(f"Error in simplified tornado calculation: {str(e)}")
            return []

    def _calculate_sensitivity_heatmap_data(self, revenue: float, ebitda: float, net_income: float, original_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Calculate sensitivity heatmap data using real DCF analysis with user's actual assumptions.
        Creates a matrix of WACC vs Terminal Growth Rate scenarios.
        """
        try:
            revenue = float(revenue) if revenue else 0
            ebitda = float(ebitda) if ebitda else 0
            net_income = float(net_income) if net_income else 0
            
            # Extract user's actual assumptions from original_data
            user_wacc = original_data.get('discount_rate', 0.12) if original_data else 0.12
            user_terminal_growth = original_data.get('terminal_growth_rate', 0.03) if original_data else 0.03
            user_revenue_growth = original_data.get('revenue_growth_rate', 0.10) if original_data else 0.10
            
            # Estimate FCF from net income if no cash flow data available
            estimated_fcf = net_income * 0.8  # Assume 80% of net income converts to FCF
            
            # Use real DCF sensitivity analysis with user's actual assumptions
            sensitivity_ranges = {
                'revenue_growth': {'low': -0.15, 'high': 0.25, 'type': 'fcf'},  # -15% to +25%
                'operating_margin': {'low': -0.10, 'high': 0.15, 'type': 'fcf'},  # -10% to +15%
                'wacc': {'low': max(0.05, user_wacc - 0.04), 'high': min(0.20, user_wacc + 0.04), 'type': 'wacc'},  # ±4% around user's WACC
                'terminal_growth': {'low': max(0.005, user_terminal_growth - 0.02), 'high': min(0.08, user_terminal_growth + 0.02), 'type': 'growth'}  # ±2% around user's terminal growth
            }
            
            # Use user's actual assumptions as base values
            base_discount_rate = user_wacc
            base_terminal_growth = user_terminal_growth
            
            # Terminal value calculation function
            def terminal_value_func(last_fcf: float, growth_rate: float, discount_rate: float) -> float:
                if discount_rate <= growth_rate:
                    return last_fcf * 20  # High multiple for low discount rate
                return last_fcf * (1 + growth_rate) / (discount_rate - growth_rate)
            
            # Use real DCF sensitivity analysis with user's assumptions
            sensitivity_results = calculate_sensitivity_analysis(
                [{'free_cash_flow': estimated_fcf}],  # Single year forecast
                sensitivity_ranges,
                base_discount_rate,
                base_terminal_growth
            )
            
            # Extract sensitivity matrix from results
            sensitivity_matrix = sensitivity_results.get('sensitivity_matrix', [])
            
            if sensitivity_matrix:
                print(f"=== REAL DCF SENSITIVITY HEATMAP CALCULATION (USER ASSUMPTIONS) ===")
                print(f"User WACC: {user_wacc}")
                print(f"User Terminal Growth: {user_terminal_growth}")
                print(f"User Revenue Growth: {user_revenue_growth}")
                print(f"Estimated FCF: {estimated_fcf}")
                print(f"Base discount rate: {base_discount_rate}")
                print(f"Base terminal growth: {base_terminal_growth}")
                print(f"Heatmap rows: {len(sensitivity_matrix)}")
                return sensitivity_matrix
            else:
                # Fallback to simplified calculation if DCF fails
                return self._calculate_simplified_sensitivity_heatmap(revenue, ebitda, net_income, original_data)
            
        except Exception as e:
            print(f"Error calculating sensitivity heatmap data: {str(e)}")
            # Fallback to simplified calculation if DCF fails
            return self._calculate_simplified_sensitivity_heatmap(revenue, ebitda, net_income, original_data)
    
    def _calculate_simplified_sensitivity_heatmap(self, revenue: float, ebitda: float, net_income: float, original_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fallback simplified sensitivity heatmap calculation if DCF analysis fails.
        Uses user's actual assumptions instead of hardcoded values.
        """
        try:
            revenue = float(revenue) if revenue else 0
            ebitda = float(ebitda) if ebitda else 0
            net_income = float(net_income) if net_income else 0
            
            # Extract user's actual assumptions from original_data
            user_wacc = original_data.get('discount_rate', 0.12) if original_data else 0.12
            user_terminal_growth = original_data.get('terminal_growth_rate', 0.03) if original_data else 0.03
            
            # Base enterprise value estimation (simplified DCF)
            base_ev = revenue * 3 if revenue > 0 else 100000  # Fallback value
            
            # WACC scenarios centered around user's actual WACC (±2% range)
            wacc_range = 0.02  # ±2% range
            wacc_scenarios = [
                max(0.05, user_wacc - wacc_range),
                user_wacc - wacc_range/2,
                user_wacc,  # User's actual WACC
                user_wacc + wacc_range/2,
                min(0.20, user_wacc + wacc_range)
            ]
            
            # Terminal growth rate scenarios centered around user's actual terminal growth (±1% range)
            growth_range = 0.01  # ±1% range
            growth_scenarios = [
                max(0.005, user_terminal_growth - growth_range),
                user_terminal_growth - growth_range/2,
                user_terminal_growth,  # User's actual terminal growth
                user_terminal_growth + growth_range/2,
                min(0.08, user_terminal_growth + growth_range)
            ]
            
            heatmap_data = []
            
            for wacc in wacc_scenarios:
                row_data = {
                    'wacc': wacc,
                    'values': []
                }
                
                for growth in growth_scenarios:
                    # Simplified DCF calculation
                    # EV = FCF / (WACC - Growth Rate)
                    # Adjust base valuation based on WACC and growth assumptions
                    
                    if wacc <= growth:
                        # Handle edge case where WACC <= growth rate
                        dcf_value = base_ev * 2  # High valuation
                    else:
                        # Calculate valuation multiplier based on WACC and growth
                        wacc_impact = 1 / wacc  # Lower WACC = higher multiplier
                        growth_impact = 1 + growth * 10  # Higher growth = higher multiplier
                        
                        dcf_value = base_ev * wacc_impact * growth_impact
                    
                    row_data['values'].append({
                        'growth': growth,
                        'dcf': dcf_value
                    })
                
                heatmap_data.append(row_data)
            
            print(f"=== SIMPLIFIED SENSITIVITY HEATMAP CALCULATION (USER ASSUMPTIONS) ===")
            print(f"User WACC: {user_wacc}")
            print(f"User Terminal Growth: {user_terminal_growth}")
            print(f"Base EV: {base_ev}")
            print(f"WACC scenarios: {wacc_scenarios}")
            print(f"Growth scenarios: {growth_scenarios}")
            print(f"Heatmap rows: {len(heatmap_data)}")
            
            return heatmap_data
            
        except Exception as e:
            print(f"Error in simplified sensitivity heatmap calculation: {str(e)}")
            return []

    def _calculate_base_ratios(self, total_revenue: float, total_expenses: float, net_income: float, ebitda: float,
                              total_assets: float, total_equity: float, current_assets: float, 
                              current_liabilities: float, total_liabilities: float, revenue_values: List[float]) -> Dict[str, Any]:
        """
        Calculate base financial ratios applicable to all company types.
        These ratios are fundamental and work across service, retail, SaaS, etc.
        """
        try:
            from .dashboard_calculator import DashboardCalculator
            
            # PROFITABILITY RATIOS
            profit_margin = (net_income / total_revenue * 100) if total_revenue > 0 else None
            gross_margin = ((total_revenue - total_expenses) / total_revenue * 100) if total_revenue > 0 else None
            operating_margin = (ebitda / total_revenue * 100) if total_revenue > 0 else None
            
            # EFFICIENCY RATIOS
            asset_turnover = (total_revenue / total_assets) if total_assets > 0 else None
            roe = (net_income / total_equity * 100) if total_equity > 0 else None
            expense_ratio = (total_expenses / total_revenue * 100) if total_revenue > 0 else None
            ebitda_margin = (ebitda / total_revenue * 100) if total_revenue > 0 else None
            
            # LIQUIDITY RATIOS
            current_ratio = (current_assets / current_liabilities) if current_liabilities > 0 and current_assets > 0 else None
            quick_ratio = (current_assets / current_liabilities) if current_liabilities > 0 and current_assets > 0 else None
            
            # LEVERAGE RATIOS
            debt_to_equity = (total_liabilities / total_equity) if total_equity > 0 and total_liabilities >= 0 else None
            working_capital = (current_assets - current_liabilities) if current_assets > 0 and current_liabilities > 0 else None
            debt_ratio = (total_liabilities / total_assets * 100) if total_assets > 0 and total_liabilities >= 0 else None
            equity_ratio = (total_equity / total_assets * 100) if total_assets > 0 and total_equity >= 0 else None
            roa = (net_income / total_assets * 100) if total_assets > 0 else None
            
            # GROWTH RATIOS
            revenue_growth = DashboardCalculator.calculate_growth_rate(revenue_values) if len(revenue_values) > 1 else 0
            
            # VALUATION RATIOS (simplified)
            terminal_value = total_revenue * 2.5 if total_revenue > 0 else 0  # Simple revenue multiple
            wacc = 10.0  # Default WACC assumption (should be configurable)
            
            return {
                # Profitability
                'profit_margin': profit_margin,
                'gross_margin': gross_margin,
                'operating_margin': operating_margin,
                'ebitda_margin': ebitda_margin,
                'roa': roa,
                'roe': roe,
                
                # Efficiency  
                'asset_turnover': asset_turnover,
                'expense_ratio': expense_ratio,
                
                # Liquidity
                'current_ratio': current_ratio,
                'working_capital': working_capital,
                'quick_ratio': quick_ratio,
                
                # Leverage
                'debt_to_equity': debt_to_equity,
                'debt_ratio': debt_ratio,
                'equity_ratio': equity_ratio,
                
                # Growth & Valuation
                'revenue_growth': revenue_growth,
                'terminal_value': terminal_value,
                'wacc': wacc,
            }
            
        except Exception as e:
            print(f"Error calculating base ratios: {str(e)}")
            return {}
    
    def _calculate_service_specific_ratios(self, original_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate service-specific ratios and metrics.
        These are only applicable to service companies.
        """
        try:
            service_data = original_data.get('service_data', {})
            
            # Service business metrics
            client_retention_rate = service_data.get('client_retention_rate', 0)
            utilization_rate = service_data.get('utilization_rate', 0)
            clv = service_data.get('customer_lifetime_value', 0)
            cac = service_data.get('customer_acquisition_cost', 0)
            
            # Calculated service ratios
            clv_cac_ratio = (clv / cac) if cac > 0 else 0
            
            # Additional service metrics
            client_concentration_risk = service_data.get('client_concentration_risk', 0)
            
            return {
                'client_retention_rate': client_retention_rate,
                'utilization_rate': utilization_rate,
                'clv': clv,
                'cac': cac,
                'clv_cac_ratio': clv_cac_ratio,
                'client_concentration_risk': client_concentration_risk,
            }
            
        except Exception as e:
            print(f"Error calculating service-specific ratios: {str(e)}")
            return {}
    
    def _calculate_vertical_analysis(self, income_statement: Dict[str, Any], balance_sheet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate vertical analysis for both income statement and balance sheet.
        Vertical analysis shows each line item as a percentage of a base figure.
        - Income Statement: Each item as % of total revenue
        - Balance Sheet: Each item as % of total assets
        
        Uses proper year identification (historical vs forecasted) based on current year (2025).
        """
        try:
            vertical_data = {
                'income_statement': [],
                'balance_sheet': []
            }
            
            # Get line items and years
            income_line_items = income_statement.get('line_items', [])
            balance_line_items = balance_sheet.get('line_items', [])
            years = income_statement.get('years', [])
            
            # Determine current year (2025) and identify historical vs forecasted years
            import datetime
            current_year = datetime.datetime.now().year
            year_metadata = []
            for year_str in years:
                year_int = int(year_str)
                if year_int < current_year:
                    year_metadata.append({'year': year_str, 'type': 'historical'})
                elif year_int == current_year:
                    year_metadata.append({'year': year_str, 'type': 'current'})
                else:
                    year_metadata.append({'year': year_str, 'type': 'forecasted'})
            
            # Find base items for percentage calculations
            # Income Statement: Use same logic as find_line_item_values to get Total Revenue
            revenue_base_item = None
            
            # Prioritize TOTAL REVENUE, then fall back to others (same as find_line_item_values)
            revenue_keywords = ['TOTAL REVENUE', 'total revenue', 'revenue']
            
            # First pass: Try exact matches (prioritize exact matches)
            for keyword in revenue_keywords:
                for i, item in enumerate(income_line_items):
                    label = item.get('label', '').strip()
                    if label == keyword:  # Exact match
                        values = item.get('values', [])
                        if sum(values) > 0:  # Only use items with non-zero values
                            revenue_base_item = item
                            break
                if revenue_base_item:
                    break
            
            # Second pass: Try case-insensitive contains matches
            if not revenue_base_item:
                for keyword in revenue_keywords:
                    for i, item in enumerate(income_line_items):
                        label = item.get('label', '').strip()
                        if keyword.lower() in label.lower():  # Contains match
                            values = item.get('values', [])
                            if sum(values) > 0:  # Only use items with non-zero values
                                revenue_base_item = item
                                break
                    if revenue_base_item:
                        break
            
            # Balance Sheet: Use same logic to find Total Assets
            assets_base_item = None
            
            # Prioritize different asset items - more comprehensive search
            assets_keywords = [
                'TOTAL ASSETS', 'total assets', 
                'Total Current Assets', 'total current assets',
                'ASSETS', 'assets'
            ]
            
            # First pass: Try exact matches
            for keyword in assets_keywords:
                for i, item in enumerate(balance_line_items):
                    label = item.get('label', '').strip()
                    if label == keyword:  # Exact match
                        values = item.get('values', [])
                        # Use items with any non-zero values (positive or negative)
                        if any(abs(v) > 0 for v in values):
                            assets_base_item = item
                            break
                if assets_base_item:
                    break
            
            # Second pass: Try case-insensitive contains matches
            if not assets_base_item:
                for keyword in assets_keywords:
                    for i, item in enumerate(balance_line_items):
                        label = item.get('label', '').strip()
                        if keyword.lower() in label.lower():  # Contains match
                            values = item.get('values', [])
                            # Use items with any non-zero values (positive or negative)
                            if any(abs(v) > 0 for v in values):
                                assets_base_item = item
                                break
                    if assets_base_item:
                        break
            
            # Calculate Income Statement vertical analysis
            if revenue_base_item:
                revenue_base_values = revenue_base_item.get('values', [])
                
                for item in income_line_items:
                    if item.get('is_spacer'):
                        continue
                        
                    item_values = item.get('values', [])
                    percentages = []
                    
                    for i, value in enumerate(item_values):
                        if i < len(revenue_base_values) and revenue_base_values[i] != 0:
                            percentage = (value / abs(revenue_base_values[i])) * 100
                        else:
                            percentage = 0
                        percentages.append(round(percentage, 2))
                    
                    vertical_data['income_statement'].append({
                        'name': item.get('label', ''),
                        'values': item_values,
                        'percentages': percentages,
                        'isHeader': item.get('is_header', False),
                        'isSubItem': item.get('is_sub_item', False),
                        'isTotal': item.get('is_total', False)
                    })
            
            # Calculate Balance Sheet vertical analysis
            if assets_base_item:
                assets_base_values = assets_base_item.get('values', [])
                
                for i, item in enumerate(balance_line_items):
                    if item.get('is_spacer'):
                        continue
                        
                    item_values = item.get('values', [])
                    percentages = []
                    
                    for j, value in enumerate(item_values):
                        if j < len(assets_base_values) and abs(assets_base_values[j]) > 0.01:  # Avoid division by very small numbers
                            # For balance sheet, use absolute value of base for percentage calculation
                            percentage = (value / abs(assets_base_values[j])) * 100
                        else:
                            percentage = 0
                        percentages.append(round(percentage, 2))
                    
                    vertical_data['balance_sheet'].append({
                        'name': item.get('label', ''),
                        'values': item_values,
                        'percentages': percentages,
                        'isHeader': item.get('is_header', False),
                        'isSubItem': item.get('is_sub_item', False),
                        'isTotal': item.get('is_total', False)
                    })
            
            # Add year metadata to help frontend understand historical vs forecasted years
            vertical_data['year_metadata'] = year_metadata
            vertical_data['years'] = years
            
            return vertical_data
            
        except Exception as e:
            print(f"Error calculating vertical analysis: {str(e)}")
            return {'income_statement': [], 'balance_sheet': []}
    
    def _calculate_horizontal_analysis(self, income_statement: Dict[str, Any], balance_sheet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate horizontal analysis for both income statement and balance sheet.
        Horizontal analysis shows year-over-year growth percentages.
        
        Uses proper year identification (historical vs forecasted) based on current year (2025).
        """
        try:
            horizontal_data = {
                'income_statement': []
            }
            
            # Get line items and years
            income_line_items = income_statement.get('line_items', [])
            years = income_statement.get('years', [])
            
            # Determine current year (2025) and identify historical vs forecasted years
            import datetime
            current_year = datetime.datetime.now().year
            year_metadata = []
            for year_str in years:
                year_int = int(year_str)
                if year_int < current_year:
                    year_metadata.append({'year': year_str, 'type': 'historical'})
                elif year_int == current_year:
                    year_metadata.append({'year': year_str, 'type': 'current'})
                else:
                    year_metadata.append({'year': year_str, 'type': 'forecasted'})
            
            # Calculate horizontal analysis for Income Statement
            for item in income_line_items:
                if item.get('is_spacer'):
                    continue
                    
                item_values = item.get('values', [])
                growth_percentages = [None]  # First year has no previous year
                
                # Calculate year-over-year growth
                for i in range(1, len(item_values)):
                    if item_values[i-1] != 0:
                        growth = ((item_values[i] - item_values[i-1]) / abs(item_values[i-1])) * 100
                        growth_percentages.append(round(growth, 2))
                    else:
                        growth_percentages.append(None)
                
                horizontal_data['income_statement'].append({
                    'name': item.get('label', ''),
                    'values': item_values,
                    'growth': growth_percentages,
                    'isHeader': item.get('is_header', False),
                    'isSubItem': item.get('is_sub_item', False),
                    'isTotal': item.get('is_total', False)
                })
            
            # Add year metadata to help frontend understand historical vs forecasted years
            horizontal_data['year_metadata'] = year_metadata
            horizontal_data['years'] = years
            
            return horizontal_data
            
        except Exception as e:
            print(f"Error calculating horizontal analysis: {str(e)}")
            return {'income_statement': []}
    
    def _calculate_base_case_sensitivity_kpis(self, income_statement: Dict[str, Any], 
                                           balance_sheet: Dict[str, Any], 
                                           cash_flow: Dict[str, Any], 
                                           original_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate base case KPIs for sensitivity analysis using original user assumptions.
        
        This method calculates key valuation and financial metrics that will be used
        as the base case in sensitivity analysis scenarios.
        """
        try:
            from .dashboard_calculator import DashboardCalculator
            
            # Extract user assumptions from original data
            discount_rate = float(original_data.get('discountRate', 10)) / 100  # WACC
            terminal_growth = float(original_data.get('terminalGrowth', 2)) / 100
            tax_rate = float(original_data.get('taxRate', 25)) / 100
            
            # Extract growth rates and other key assumptions
            revenue_growth_rate = float(original_data.get('revenueGrowthRate', 10)) / 100
            expense_growth_rate = float(original_data.get('expenseGrowthRate', 5)) / 100
            
            # Service business model assumptions
            service_business_model = original_data.get('serviceBusinessModel', {})
            client_retention_rate = float(service_business_model.get('clientRetentionRate', 85)) / 100
            utilization_rate = float(service_business_model.get('utilizationRate', 75)) / 100
            
            # Extract financial data from statements
            years = income_statement.get('years', [])
            total_years = len(years)
            
            # Get line items for calculations
            income_line_items = income_statement.get('line_items', [])
            balance_line_items = balance_sheet.get('line_items', [])
            
            # Helper function to find values from line items (reuse existing logic)
            def find_line_item_values(line_items, label_keywords):
                for keyword in label_keywords:
                    for item in line_items:
                        label = item.get('label', '').strip()
                        if label == keyword:  # Exact match
                            return item.get('values', [])
                
                for keyword in label_keywords:
                    for item in line_items:
                        label = item.get('label', '').strip()
                        if keyword.lower() in label.lower():  # Contains match
                            return item.get('values', [])
                
                return [0] * total_years
            
            # Extract key financial metrics
            revenue_values = find_line_item_values(income_line_items, ['TOTAL REVENUE', 'total revenue', 'revenue'])
            net_income_values = find_line_item_values(income_line_items, ['NET INCOME', 'net income'])
            ebitda_values = find_line_item_values(income_line_items, ['EBITDA', 'ebitda'])
            
            # Calculate Free Cash Flow for valuation
            fcf_values = self._calculate_free_cash_flow(cash_flow, income_statement, total_years)
            
            # Current year metrics (base year for valuation)
            current_revenue = revenue_values[-1] if revenue_values else 0
            current_net_income = net_income_values[-1] if net_income_values else 0
            current_ebitda = ebitda_values[-1] if ebitda_values else 0
            current_fcf = fcf_values[-1] if fcf_values else 0
            
            # Calculate Enterprise Value using DCF approach
            # Project FCF for next 5-10 years and calculate terminal value
            projection_years = 5
            projected_fcf = []
            
            # Simple FCF projection based on revenue growth and margin assumptions
            base_fcf = current_fcf if current_fcf > 0 else current_net_income
            fcf_growth_rate = revenue_growth_rate * 0.8  # FCF typically grows slower than revenue
            
            for year in range(1, projection_years + 1):
                projected_year_fcf = base_fcf * ((1 + fcf_growth_rate) ** year)
                projected_fcf.append(projected_year_fcf)
            
            # Calculate terminal value
            terminal_fcf = projected_fcf[-1] * (1 + terminal_growth)
            terminal_value = terminal_fcf / (discount_rate - terminal_growth) if discount_rate > terminal_growth else 0
            
            # Calculate NPV (Net Present Value)
            npv = 0
            for i, fcf in enumerate(projected_fcf):
                npv += fcf / ((1 + discount_rate) ** (i + 1))
            
            # Add discounted terminal value
            npv += terminal_value / ((1 + discount_rate) ** projection_years)
            
            # Enterprise Value = NPV
            enterprise_value = npv
            
            # Calculate Equity Value (assuming minimal debt for simplicity)
            # In a full model, we'd subtract net debt
            net_debt = 0  # Simplified - could extract from balance sheet
            equity_value = enterprise_value - net_debt
            
            # Calculate IRR (simplified calculation)
            # For simplicity, estimate IRR based on FCF growth and terminal value
            total_return = (terminal_fcf + sum(projected_fcf)) / base_fcf if base_fcf > 0 else 0
            irr = (total_return ** (1/projection_years)) - 1 if total_return > 0 else 0
            
            # Calculate additional metrics
            revenue_multiple = enterprise_value / current_revenue if current_revenue > 0 else 0
            ebitda_multiple = enterprise_value / current_ebitda if current_ebitda > 0 else 0
            
            # Payback period (simplified)
            cumulative_fcf = 0
            payback_period = 0
            for i, fcf in enumerate(projected_fcf):
                cumulative_fcf += fcf
                if cumulative_fcf >= abs(base_fcf) and payback_period == 0:
                    payback_period = i + 1
                    break
            
            return {
                'base_case_enterprise_value': enterprise_value,
                'base_case_equity_value': equity_value,
                'base_case_npv': npv,
                'base_case_irr': irr,
                'base_case_revenue_multiple': revenue_multiple,
                'base_case_ebitda_multiple': ebitda_multiple,
                'base_case_payback_period': payback_period,
                'base_case_terminal_value': terminal_value,
                'base_case_assumptions': {
                    'discount_rate': discount_rate,
                    'terminal_growth_rate': terminal_growth,
                    'revenue_growth_rate': revenue_growth_rate,
                    'expense_growth_rate': expense_growth_rate,
                    'client_retention_rate': client_retention_rate,
                    'utilization_rate': utilization_rate,
                    'tax_rate': tax_rate
                },
                'base_case_projections': {
                    'projected_fcf': projected_fcf,
                    'projection_years': projection_years
                }
            }
            
        except Exception as e:
            print(f"Error calculating base case sensitivity KPIs: {str(e)}")
            return {
                'base_case_enterprise_value': 0,
                'base_case_equity_value': 0,
                'base_case_npv': 0,
                'base_case_irr': 0,
                'base_case_revenue_multiple': 0,
                'base_case_ebitda_multiple': 0,
                'base_case_payback_period': 0,
                'base_case_terminal_value': 0,
                'base_case_assumptions': {},
                'base_case_projections': {}
        }

