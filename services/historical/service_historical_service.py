"""
Service Company Historical Service

Implementation of historical financial calculations for service companies.
This handles service-specific metrics, assumptions, and calculations.
"""

from typing import Dict, Any, List, Optional
from .base_historical_service import BaseHistoricalService
import datetime
import math


class ServiceHistoricalService(BaseHistoricalService):
    """
    Historical service implementation for service companies.
    
    This handles service-specific calculations, metrics, and assumptions
    for businesses that provide services rather than physical products.
    """
    
    def __init__(self):
        """Initialize service historical service."""
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
            'employee_productivity'
        ]
    
    def _get_required_fields(self) -> List[str]:
        """Get required fields for service companies."""
        return [
            'revenue',
            'operating_expenses',
            'employee_count',
            'billable_hours',
            'service_delivery_costs',
            'client_count',
            'average_project_value'
        ]
    
    def _get_company_description(self) -> str:
        """Get description of service companies."""
        return "Service companies provide intangible services to clients. Key metrics include utilization rates, billable hours, and service delivery efficiency."
    
    def get_company_type_info(self) -> Dict[str, Any]:
        """Get information about service company type."""
        return {
            'name': 'Service Company',
            'description': self._get_company_description(),
            'supported_metrics': self._get_supported_metrics(),
            'required_fields': self._get_required_fields()
        }
    
    def validate_historical_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate historical data for service companies.
        
        Args:
            data: Historical data to validate
            
        Returns:
            Validation result with any errors or warnings
        """
        errors = []
        warnings = []
        
        # Check for required fields
        historical_data = data.get('historicalServices', [])
        
        if not historical_data:
            errors.append("Historical services data is required")
        
        # Service-specific validations
        for year_idx, year_data in enumerate(historical_data):
            if 'services' not in year_data:
                errors.append(f"Missing services data for year {year_idx + 1}")
                continue
                
            for service_idx, service in enumerate(year_data['services']):
                revenue = float(service.get('historicalRevenue', 0))
                if revenue < 0:
                    errors.append(f"Revenue cannot be negative in year {year_idx + 1}, service {service_idx + 1}")
                
                cost = float(service.get('cost', 0))
                if cost < 0:
                    errors.append(f"Cost cannot be negative in year {year_idx + 1}, service {service_idx + 1}")
        
        # Check growth rates
        revenue_growth = float(data.get('revenueGrowthRate', 0))
        if revenue_growth > 100:
            warnings.append("Revenue growth rate seems unusually high")
        
        expense_growth = float(data.get('expenseGrowthRate', 0))
        if expense_growth > 100:
            warnings.append("Expense growth rate seems unusually high")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def process_historical_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process historical data for service companies.
        
        Args:
            data: Raw historical data
            
        Returns:
            Processed historical data
        """
        # Add service-specific processing here if needed
        return data
    
    def calculate_company_specific_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate service-specific metrics and KPIs using advanced service business model inputs.
        
        Args:
            data: Historical and projected data
            
        Returns:
            Service-specific metrics and KPIs
        """
        metrics = {}
        
        # Get service business model inputs (with safe defaults)
        service_business_model = data.get('serviceBusinessModel', {})
        
        # Extract all service business metrics
        client_retention_rate = float(service_business_model.get('clientRetentionRate', 85))
        churn_rate = float(service_business_model.get('churnRate', 15))
        cac = float(service_business_model.get('clientAcquisitionCost', 0))
        clv = float(service_business_model.get('customerLifetimeValue', 0))
        recurring_revenue_percent = float(service_business_model.get('recurringRevenuePercent', 60))
        expansion_revenue_percent = float(service_business_model.get('expansionRevenuePercent', 25))
        seasonality_factor = float(service_business_model.get('seasonalityFactor', 20))
        utilization_rate = float(service_business_model.get('utilizationRate', 75))
        team_size = float(service_business_model.get('teamSize', 10))
        team_growth_rate = float(service_business_model.get('teamGrowthRate', 20))
        avg_project_duration = float(service_business_model.get('averageProjectDuration', 90))
        
        # Store all metrics
        metrics['client_retention_rate'] = client_retention_rate
        metrics['churn_rate'] = churn_rate
        metrics['utilization_rate'] = utilization_rate
        metrics['team_size'] = team_size
        metrics['team_growth_rate'] = team_growth_rate
        metrics['seasonality_factor'] = seasonality_factor
        metrics['recurring_revenue_percent'] = recurring_revenue_percent
        metrics['expansion_revenue_percent'] = expansion_revenue_percent
        metrics['avg_project_duration'] = avg_project_duration
        
        # Calculate derived metrics
        if cac > 0 and clv > 0:
            metrics['cac_efficiency'] = clv / cac
            metrics['cac_payback_months'] = (cac / (clv / 12)) if clv > 0 else 0
        else:
            metrics['cac_efficiency'] = 0
            metrics['cac_payback_months'] = 0
        
        # Calculate revenue per employee
        if 'historicalServices' in data and team_size > 0:
            total_revenue = 0
            for year_data in data['historicalServices']:
                for service in year_data.get('services', []):
                    total_revenue += float(service.get('historicalRevenue', 0))
            
            metrics['revenue_per_employee'] = total_revenue / team_size if team_size > 0 else 0
        else:
            metrics['revenue_per_employee'] = 0
        
        # Calculate customer metrics
        if 'historicalServices' in data:
            total_customers = 0
            for year_data in data['historicalServices']:
                for service in year_data.get('services', []):
                    total_customers += float(service.get('historicalClients', 0))
            
            if total_customers > 0:
                metrics['avg_revenue_per_customer'] = (total_revenue / total_customers) if total_customers > 0 else 0
                metrics['customer_concentration_risk'] = 1 / total_customers if total_customers > 0 else 1
            else:
                metrics['avg_revenue_per_customer'] = 0
                metrics['customer_concentration_risk'] = 1
        
        # Calculate capacity metrics
        if utilization_rate > 0 and team_size > 0:
            # Estimate capacity utilization efficiency
            metrics['capacity_efficiency'] = utilization_rate / 100
            metrics['team_productivity_score'] = (utilization_rate * team_growth_rate) / 100
        else:
            metrics['capacity_efficiency'] = 0
            metrics['team_productivity_score'] = 0
        
        # Calculate business model health score
        health_factors = []
        if client_retention_rate > 0:
            health_factors.append(min(client_retention_rate / 85, 1.2))  # 85% is good baseline
        if metrics['cac_efficiency'] > 0:
            health_factors.append(min(metrics['cac_efficiency'] / 3, 1.5))  # 3x is good baseline
        if recurring_revenue_percent > 0:
            health_factors.append(min(recurring_revenue_percent / 60, 1.2))  # 60% is good baseline
        if utilization_rate > 0:
            health_factors.append(min(utilization_rate / 75, 1.2))  # 75% is good baseline
        
        if health_factors:
            metrics['business_model_health_score'] = sum(health_factors) / len(health_factors)
        else:
            metrics['business_model_health_score'] = 0.5  # Neutral score
        
        return metrics
    
    def apply_company_specific_assumptions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply service-specific assumptions and adjustments.
        
        Args:
            data: Financial data
            
        Returns:
            Data with service-specific assumptions applied
        """
        # Add service-specific assumptions here if needed
        return data
    
    def _process_numeric_data(self, data: List) -> List[float]:
        """Process numeric data safely."""
        processed = []
        for item in data:
            try:
                processed.append(float(item))
            except (ValueError, TypeError):
                processed.append(0.0)
        return processed
    
    def _safe_float(self, value, default=0.0):
        """Safely convert value to float."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def _calculate_revenue_per_employee(self, data: Dict[str, Any]) -> List[float]:
        """Calculate revenue per employee."""
        # Implementation would calculate revenue per employee for each year
        return [0.0]  # Placeholder
    
    def _calculate_utilization_rate(self, data: Dict[str, Any]) -> List[float]:
        """Calculate utilization rate."""
        # Implementation would calculate utilization rate for each year
        return [0.0]  # Placeholder
    
    def _calculate_profit_margin(self, data: Dict[str, Any]) -> List[float]:
        """Calculate profit margin."""
        # Implementation would calculate profit margin for each year
        return [0.0]  # Placeholder
    
    def _calculate_operating_margin(self, data: Dict[str, Any]) -> List[float]:
        """Calculate operating margin."""
        # Implementation would calculate operating margin for each year
        return [0.0]  # Placeholder
    
    def _calculate_ebitda_margin(self, data: Dict[str, Any]) -> List[float]:
        """Calculate EBITDA margin."""
        # Implementation would calculate EBITDA margin for each year
        return [0.0]  # Placeholder
    
    def _calculate_revenue_growth_rate(self, data: Dict[str, Any]) -> List[float]:
        """Calculate revenue growth rate."""
        # Implementation would calculate revenue growth rate for each year
        return [0.0]  # Placeholder
    
    def _calculate_employee_productivity(self, data: Dict[str, Any]) -> List[float]:
        """Calculate employee productivity."""
        # Implementation would calculate employee productivity for each year
        return [0.0]  # Placeholder
    
    def _calculate_service_delivery_efficiency(self, data: Dict[str, Any]) -> List[float]:
        """Calculate service delivery efficiency."""
        # Implementation would calculate service delivery efficiency for each year
        return [0.0]  # Placeholder
    
    def _calculate_client_retention_rate(self, data: Dict[str, Any]) -> List[float]:
        """Calculate client retention rate."""
        # Implementation would calculate client retention rate for each year
        return [0.0]  # Placeholder
    
    def _calculate_average_project_size(self, data: Dict[str, Any]) -> List[float]:
        """Calculate average project size."""
        # Implementation would calculate average project size for each year
        return [0.0]  # Placeholder
    
    def _apply_efficiency_target(self, data: Dict[str, Any], target: float) -> Dict[str, Any]:
        """Apply efficiency target."""
        # Implementation would apply efficiency target
        return data
    
    def _apply_utilization_target(self, data: Dict[str, Any], target: float) -> Dict[str, Any]:
        """Apply utilization target."""
        # Implementation would apply utilization target
        return data
    
    def _apply_productivity_target(self, data: Dict[str, Any], target: float) -> Dict[str, Any]:
        """Apply productivity target."""
        # Implementation would apply productivity target
        return data
