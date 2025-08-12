"""
Dashboard Service Factory

Factory class for creating dashboard service instances based on company type.
This provides a unified interface for accessing different company-specific dashboard services.
"""

from typing import Dict, Any, Optional, Type, List
from .base_dashboard_service import BaseDashboardService
from .service_dashboard_service import ServiceDashboardService


class DashboardServiceFactory:
    """
    Factory for creating dashboard service instances.
    
    This class manages different company type implementations and provides
    a unified interface for creating dashboard services.
    """
    
    # Registry of available company types
    _service_registry: Dict[str, Type[BaseDashboardService]] = {
        'service': ServiceDashboardService,
        # Add more company types here as they are implemented
        # 'retail': RetailDashboardService,
        # 'saas': SaasDashboardService,
        # 'manufacturing': ManufacturingDashboardService,
    }
    
    @classmethod
    def get_available_company_types(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all available company types.
        
        Returns:
            Dictionary with company type information
        """
        company_types = {}
        
        for company_type, service_class in cls._service_registry.items():
            # Create a temporary instance to get company info
            temp_service = service_class()
            company_types[company_type] = temp_service.get_company_type_info()
        
        return company_types
    
    @classmethod
    def create_service(cls, company_type: str) -> BaseDashboardService:
        """
        Create a dashboard service instance for the specified company type.
        
        Args:
            company_type: Type of company (service, retail, saas, etc.)
            
        Returns:
            Dashboard service instance
            
        Raises:
            ValueError: If company type is not supported
        """
        if company_type not in cls._service_registry:
            available_types = list(cls._service_registry.keys())
            raise ValueError(
                f"Company type '{company_type}' is not supported. "
                f"Available types: {available_types}"
            )
        
        service_class = cls._service_registry[company_type]
        return service_class()
    
    @classmethod
    def register_company_type(cls, company_type: str, service_class: Type[BaseDashboardService]) -> None:
        """
        Register a new company type with its service implementation.
        
        Args:
            company_type: Name of the company type
            service_class: Service class implementation
        """
        cls._service_registry[company_type] = service_class
    
    @classmethod
    def is_company_type_supported(cls, company_type: str) -> bool:
        """
        Check if a company type is supported.
        
        Args:
            company_type: Type of company to check
            
        Returns:
            True if company type is supported, False otherwise
        """
        return company_type in cls._service_registry
    
    @classmethod
    def get_service_info(cls, company_type: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific company type service.
        
        Args:
            company_type: Type of company
            
        Returns:
            Company type information or None if not supported
        """
        if not cls.is_company_type_supported(company_type):
            return None
        
        service = cls.create_service(company_type)
        return service.get_company_type_info()
    
    @classmethod
    def calculate_dashboard_metrics(cls, company_type: str, statements_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate dashboard metrics for a specific company type.
        
        Args:
            company_type: Type of company
            statements_data: Historical statements data
            
        Returns:
            Dashboard calculation results
        """
        service = cls.create_service(company_type)
        return service.calculate_dashboard_metrics(statements_data)
    
    @classmethod
    def validate_dashboard_data(cls, company_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate dashboard data for a specific company type.
        
        Args:
            company_type: Type of company
            data: Dashboard data to validate
            
        Returns:
            Validation results
        """
        service = cls.create_service(company_type)
        return service._validate_dashboard_data(data)
    
    @classmethod
    def get_supported_metrics(cls, company_type: str) -> Optional[List[str]]:
        """
        Get supported metrics for a specific company type.
        
        Args:
            company_type: Type of company
            
        Returns:
            List of supported metrics or None if company type not supported
        """
        if not cls.is_company_type_supported(company_type):
            return None
        
        service = cls.create_service(company_type)
        return service.supported_metrics
    
    @classmethod
    def get_required_fields(cls, company_type: str) -> Optional[List[str]]:
        """
        Get required fields for a specific company type.
        
        Args:
            company_type: Type of company
            
        Returns:
            List of required fields or None if company type not supported
        """
        if not cls.is_company_type_supported(company_type):
            return None
        
        service = cls.create_service(company_type)
        return service.required_fields
    
    @classmethod
    def get_dashboard_chart_types(cls, company_type: str) -> Optional[List[str]]:
        """
        Get available chart types for a specific company type.
        
        Args:
            company_type: Type of company
            
        Returns:
            List of available chart types or None if company type not supported
        """
        if not cls.is_company_type_supported(company_type):
            return None
        
        # Define chart types for each company type
        chart_types = {
            'service': [
                'revenue_vs_expenses',
                'revenue_breakdown',
                'expense_breakdown',
                'cash_flow_analysis',
                'balance_sheet_trends',
                'utilization_trend',
                'client_growth',
                'project_efficiency',
                'employee_productivity'
            ],
            # Add more company types as they are implemented
            # 'retail': [...],
            # 'saas': [...],
        }
        
        return chart_types.get(company_type, [])
    
    @classmethod
    def get_kpi_categories(cls, company_type: str) -> Optional[List[str]]:
        """
        Get KPI categories for a specific company type.
        
        Args:
            company_type: Type of company
            
        Returns:
            List of KPI categories or None if company type not supported
        """
        if not cls.is_company_type_supported(company_type):
            return None
        
        # Define KPI categories for each company type
        kpi_categories = {
            'service': [
                'financial_performance',
                'operational_metrics',
                'efficiency_metrics',
                'client_metrics',
                'employee_metrics',
                'service_quality'
            ],
            # Add more company types as they are implemented
            # 'retail': [...],
            # 'saas': [...],
        }
        
        return kpi_categories.get(company_type, [])

