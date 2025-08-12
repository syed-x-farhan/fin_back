"""
Base Dashboard Service

Abstract base class for historical dashboard calculations.
This provides the foundation for company-specific dashboard services.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import datetime
import math


class BaseDashboardService(ABC):
    """
    Abstract base class for historical dashboard calculations.
    
    This class provides the foundation for company-specific dashboard services,
    handling common dashboard calculations and providing hooks for company-specific metrics.
    """
    
    def __init__(self, company_type: str):
        """Initialize base dashboard service."""
        self.company_type = company_type
        self.supported_metrics = self._get_supported_metrics()
        self.required_fields = self._get_required_fields()
    
    @abstractmethod
    def _get_supported_metrics(self) -> List[str]:
        """Get metrics supported by this company type."""
        pass
    
    @abstractmethod
    def _get_required_fields(self) -> List[str]:
        """Get required fields for this company type."""
        pass
    
    @abstractmethod
    def _get_company_description(self) -> str:
        """Get description of this company type."""
        pass
    
    def get_company_type_info(self) -> Dict[str, Any]:
        """Get information about this company type."""
        return {
            'type': self.company_type,
            'description': self._get_company_description(),
            'supported_metrics': self.supported_metrics,
            'required_fields': self.required_fields
        }
    
    def calculate_dashboard_metrics(self, statements_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive dashboard metrics for historical data.
        
        Args:
            statements_data: Historical financial statements data
            
        Returns:
            Dictionary containing all dashboard metrics and chart data
        """
        try:
            # Validate input data
            validation_result = self._validate_dashboard_data(statements_data)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': validation_result['errors'],
                    'data': None
                }
            
            # Calculate common metrics
            common_metrics = self._calculate_common_metrics(statements_data)
            
            # Calculate company-specific metrics
            company_metrics = self._calculate_company_specific_metrics(statements_data)
            
            # Generate chart data
            chart_data = self._generate_chart_data(statements_data)
            
            # Generate KPI cards data
            kpi_cards = self._generate_kpi_cards(statements_data, common_metrics, company_metrics)
            
            # Generate insights and trends
            insights = self._generate_insights(statements_data, common_metrics, company_metrics)
            
            return {
                'success': True,
                'data': {
                    'overview': common_metrics['overview'],
                    'kpi_cards': kpi_cards,
                    'company_metrics': company_metrics,
                    'chart_data': chart_data,
                    'insights': insights,
                    'trends': common_metrics['trends'],
                    'comparisons': common_metrics['comparisons'],
                    # Include dashboard KPIs at the top level for easy access
                    'dashboard_kpis': company_metrics.get('dashboard_kpis', {})
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Dashboard calculation failed: {str(e)}",
                'data': None
            }
    
    def _validate_dashboard_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate dashboard input data."""
        errors = []
        
        # Check for required statements
        if not data.get('income_statement'):
            errors.append("Income statement data is required")
        if not data.get('balance_sheet'):
            errors.append("Balance sheet data is required")
        
        # Check for required fields
        for field in self.required_fields:
            if not self._has_field(data, field):
                errors.append(f"Required field '{field}' is missing")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _has_field(self, data: Dict[str, Any], field: str) -> bool:
        """Check if a field exists in the data structure."""
        # Check in income statement
        if data.get('income_statement'):
            if self._find_in_line_items(data['income_statement'], field):
                return True
        
        # Check in balance sheet
        if data.get('balance_sheet'):
            if self._find_in_line_items(data['balance_sheet'], field):
                return True
        
        # Check in cash flow
        if data.get('cash_flow'):
            if self._find_in_line_items(data['cash_flow'], field):
                return True
        
        return False
    
    def _find_in_line_items(self, statement: Dict[str, Any], field: str) -> bool:
        """Find a field in statement line items."""
        if not statement.get('line_items'):
            return False
        
        for item in statement['line_items']:
            if field.lower() in item.get('label', '').lower():
                return True
        
        return False
    
    def _calculate_common_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate common metrics across all company types."""
        income_statement = data.get('income_statement', {})
        balance_sheet = data.get('balance_sheet', {})
        cash_flow = data.get('cash_flow', {})
        
        # Extract values from statements
        overview = self._extract_overview_metrics(income_statement, balance_sheet)
        trends = self._calculate_trends(income_statement, balance_sheet)
        comparisons = self._calculate_comparisons(income_statement, balance_sheet)
        
        return {
            'overview': overview,
            'trends': trends,
            'comparisons': comparisons
        }
    
    def _extract_overview_metrics(self, income_statement: Dict[str, Any], balance_sheet: Dict[str, Any]) -> Dict[str, Any]:
        """Extract overview metrics from statements."""
        # Get first year data for overview
        revenue = self._get_value_from_statement(income_statement, 'Revenue', 0)
        expenses = self._get_value_from_statement(income_statement, 'Operating Expenses', 0)
        net_income = self._get_value_from_statement(income_statement, 'Net Income', 0)
        total_assets = self._get_value_from_statement(balance_sheet, 'Total Assets', 0)
        total_equity = self._get_value_from_statement(balance_sheet, 'Total Equity', 0)
        
        return {
            'total_revenue': revenue,
            'total_expenses': expenses,
            'net_income': net_income,
            'total_assets': total_assets,
            'total_equity': total_equity,
            'profit_margin': (net_income / revenue * 100) if revenue > 0 else 0,
            'asset_turnover': (revenue / total_assets) if total_assets > 0 else 0,
            'roe': (net_income / total_equity * 100) if total_equity > 0 else 0
        }
    
    def _get_value_from_statement(self, statement: Dict[str, Any], label: str, year_index: int = 0) -> float:
        """Get a specific value from statement line items."""
        if not statement.get('line_items'):
            return 0.0
        
        for item in statement['line_items']:
            if label.lower() in item.get('label', '').lower():
                values = item.get('values', [])
                if len(values) > year_index:
                    return float(values[year_index])
        
        return 0.0
    
    def _calculate_trends(self, income_statement: Dict[str, Any], balance_sheet: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate trends over time."""
        trends = {}
        
        # Revenue trend
        revenue_trend = self._calculate_trend_from_statement(income_statement, 'Revenue')
        if revenue_trend:
            trends['revenue_growth'] = revenue_trend['growth_rate']
            trends['revenue_trend'] = revenue_trend['values']
        
        # Net income trend
        net_income_trend = self._calculate_trend_from_statement(income_statement, 'Net Income')
        if net_income_trend:
            trends['net_income_growth'] = net_income_trend['growth_rate']
            trends['net_income_trend'] = net_income_trend['values']
        
        return trends
    
    def _calculate_trend_from_statement(self, statement: Dict[str, Any], label: str) -> Optional[Dict[str, Any]]:
        """Calculate trend for a specific line item."""
        if not statement.get('line_items'):
            return None
        
        for item in statement['line_items']:
            if label.lower() in item.get('label', '').lower():
                values = item.get('values', [])
                if len(values) < 2:
                    return None
                
                # Calculate growth rate
                if values[0] > 0:
                    growth_rate = ((values[-1] - values[0]) / values[0]) * 100
                else:
                    growth_rate = 0
                
                return {
                    'values': values,
                    'growth_rate': growth_rate
                }
        
        return None
    
    def _calculate_comparisons(self, income_statement: Dict[str, Any], balance_sheet: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate year-over-year comparisons."""
        comparisons = {}
        
        # Get multiple years of data
        years = income_statement.get('years', [])
        if len(years) >= 2:
            # Compare first and last year
            first_year_revenue = self._get_value_from_statement(income_statement, 'Revenue', 0)
            last_year_revenue = self._get_value_from_statement(income_statement, 'Revenue', -1)
            
            if first_year_revenue > 0:
                comparisons['revenue_yoy'] = ((last_year_revenue - first_year_revenue) / first_year_revenue) * 100
            else:
                comparisons['revenue_yoy'] = 0
        
        return comparisons
    
    @abstractmethod
    def _calculate_company_specific_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate company-specific metrics."""
        pass
    
    def _generate_chart_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate chart data for dashboard."""
        income_statement = data.get('income_statement', {})
        balance_sheet = data.get('balance_sheet', {})
        cash_flow = data.get('cash_flow', {})
        
        return {
            'revenue_vs_expenses': self._generate_revenue_vs_expenses_chart(income_statement),
            'revenue_breakdown': self._generate_revenue_breakdown_chart(income_statement),
            'expense_breakdown': self._generate_expense_breakdown_chart(income_statement),
            'cash_flow_analysis': self._generate_cash_flow_chart(cash_flow),
            'balance_sheet_trends': self._generate_balance_sheet_chart(balance_sheet)
        }
    
    def _generate_revenue_vs_expenses_chart(self, income_statement: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate revenue vs expenses chart data."""
        chart_data = []
        years = income_statement.get('years', [])
        
        for i, year in enumerate(years):
            revenue = self._get_value_from_statement(income_statement, 'Revenue', i)
            expenses = self._get_value_from_statement(income_statement, 'Operating Expenses', i)
            
            chart_data.append({
                'year': year,
                'revenue': revenue,
                'expenses': expenses,
                'net_income': revenue - expenses
            })
        
        return chart_data
    
    def _generate_revenue_breakdown_chart(self, income_statement: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate revenue breakdown chart data."""
        # This will be overridden by company-specific services
        return []
    
    def _generate_expense_breakdown_chart(self, income_statement: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate expense breakdown chart data."""
        # This will be overridden by company-specific services
        return []
    
    def _generate_cash_flow_chart(self, cash_flow: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate cash flow chart data."""
        chart_data = []
        years = cash_flow.get('years', [])
        
        for i, year in enumerate(years):
            operating = self._get_value_from_statement(cash_flow, 'Operating Cash Flow', i)
            investing = self._get_value_from_statement(cash_flow, 'Investing Cash Flow', i)
            financing = self._get_value_from_statement(cash_flow, 'Financing Cash Flow', i)
            
            chart_data.append({
                'year': year,
                'operating': operating,
                'investing': investing,
                'financing': financing
            })
        
        return chart_data
    
    def _generate_balance_sheet_chart(self, balance_sheet: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate balance sheet chart data."""
        chart_data = []
        years = balance_sheet.get('years', [])
        
        for i, year in enumerate(years):
            assets = self._get_value_from_statement(balance_sheet, 'Total Assets', i)
            liabilities = self._get_value_from_statement(balance_sheet, 'Total Liabilities', i)
            equity = self._get_value_from_statement(balance_sheet, 'Total Equity', i)
            
            chart_data.append({
                'year': year,
                'assets': assets,
                'liabilities': liabilities,
                'equity': equity
            })
        
        return chart_data
    
    def _generate_kpi_cards(self, data: Dict[str, Any], common_metrics: Dict[str, Any], company_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate KPI cards data."""
        overview = common_metrics['overview']
        
        return {
            'financial_performance': {
                'revenue': overview['total_revenue'],
                'net_income': overview['net_income'],
                'profit_margin': overview['profit_margin'],
                'roe': overview['roe']
            },
            'operational_metrics': company_metrics.get('operational', {}),
            'growth_metrics': common_metrics['trends'],
            'efficiency_metrics': company_metrics.get('efficiency', {})
        }
    
    def _generate_insights(self, data: Dict[str, Any], common_metrics: Dict[str, Any], company_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights and recommendations."""
        insights = {
            'performance_insights': [],
            'trend_insights': [],
            'recommendations': []
        }
        
        # Performance insights
        overview = common_metrics['overview']
        if overview['profit_margin'] > 20:
            insights['performance_insights'].append("Strong profitability with high profit margins")
        elif overview['profit_margin'] < 5:
            insights['performance_insights'].append("Low profit margins - consider cost optimization")
        
        # Trend insights
        trends = common_metrics['trends']
        if trends.get('revenue_growth', 0) > 10:
            insights['trend_insights'].append("Strong revenue growth trend")
        elif trends.get('revenue_growth', 0) < 0:
            insights['trend_insights'].append("Declining revenue - investigate market conditions")
        
        return insights

