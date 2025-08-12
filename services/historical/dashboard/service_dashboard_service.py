"""
Service Company Dashboard Service

Implementation of dashboard calculations for service companies.
This handles service-specific metrics, KPIs, and visualizations.
"""

from typing import Dict, Any, List, Optional
from .base_dashboard_service import BaseDashboardService
import datetime
import math


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
            for item in line_items:
                label = item.get('label', '').strip()
                # Try exact match first, then case-insensitive contains
                for keyword in label_keywords:
                    if label == keyword or keyword.lower() in label.lower():
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
        profit_margin = (net_income / total_revenue * 100) if total_revenue > 0 else 0
        ebitda_margin = (ebitda / total_revenue * 100) if total_revenue > 0 else 0
        roe = (net_income / total_equity * 100) if total_equity > 0 else 0
        asset_turnover = (total_revenue / total_assets) if total_assets > 0 else 0
        current_ratio = (current_assets / current_liabilities) if current_liabilities > 0 else 0
        debt_to_equity = (total_liabilities / total_equity) if total_equity > 0 else 0
        
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
        
        # Calculate terminal value (simplified DCF approach)
        if len(net_income_values) > 0:
            final_year_net_income = net_income_values[-1]
            terminal_value = (final_year_net_income * (1 + terminal_growth/100)) / ((wacc/100) - (terminal_growth/100))
        else:
            terminal_value = 0
        
        return {
            # Core financial metrics
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_income': net_income,
            'profit_margin': profit_margin,
            'ebitda_margin': ebitda_margin,
            
            # Financial ratios
            'roe': roe,
            'asset_turnover': asset_turnover,
            'current_ratio': current_ratio,
            'debt_to_equity': debt_to_equity,
            
            # Growth metrics
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
            
            # Chart data for all years (for revenue vs expense graph)
            'chart_data': {
                'years': years,
                'revenue_all_years': revenue_values,
                'expenses_all_years': operating_expenses_values,
                'net_income_all_years': net_income_values,
                'ebitda_all_years': ebitda_values
            }
        }

