"""
Historical Service Factory

Factory class for creating historical service instances based on company type.
This provides a unified interface for accessing different company-specific historical services.
"""

from typing import Dict, Any, Optional, Type, List
from .base_historical_service import BaseHistoricalService
from .service_historical_service import ServiceHistoricalService


class HistoricalServiceFactory:
    """
    Factory for creating historical service instances.
    
    This class manages different company type implementations and provides
    a unified interface for creating historical services.
    """
    
    # Registry of available company types
    _service_registry: Dict[str, Type[BaseHistoricalService]] = {
        'service': ServiceHistoricalService,
        # Add more company types here as they are implemented
        # 'retail': RetailHistoricalService,
        # 'saas': SaasHistoricalService,
        # 'manufacturing': ManufacturingHistoricalService,
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
    def create_service(cls, company_type: str) -> BaseHistoricalService:
        """
        Create a historical service instance for the specified company type.
        
        Args:
            company_type: Type of company (service, retail, saas, etc.)
            
        Returns:
            Historical service instance
            
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
    def register_company_type(cls, company_type: str, service_class: Type[BaseHistoricalService]) -> None:
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
    def calculate_historical_statements(cls, company_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate historical statements for a specific company type.
        
        Args:
            company_type: Type of company
            data: Historical data and parameters
            
        Returns:
            Calculation results
        """
        service = cls.create_service(company_type)
        return service.calculate_historical_statements(data)
    
    @classmethod
    def validate_historical_data(cls, company_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate historical data for a specific company type.
        
        Args:
            company_type: Type of company
            data: Historical data to validate
            
        Returns:
            Validation results
        """
        service = cls.create_service(company_type)
        return service.validate_historical_data(data)
    
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
