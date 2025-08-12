# Historical Services Architecture

This directory contains the modular historical financial calculation services for the historical section of the application.

## Overview

The historical services are designed to be **reusable and extensible** for different company types (service, retail, SaaS, etc.). The architecture uses a **factory pattern** to manage different company type implementations.

## Structure

```
historical/
├── __init__.py                    # Package exports
├── base_historical_service.py     # Abstract base class
├── service_historical_service.py  # Service company implementation
├── retail_historical_service.py   # Retail company template
├── historical_factory.py          # Factory for creating services
├── historical_calculator.py       # Legacy calculator (for backward compatibility)
└── README.md                      # This documentation
```

## Architecture

### 1. BaseHistoricalService (Abstract Base Class)
- Defines the interface that all company-specific services must implement
- Provides common functionality for historical data processing
- Handles validation, processing, and calculation workflows

### 2. Company-Specific Services
Each company type has its own implementation that extends `BaseHistoricalService`:

- **ServiceHistoricalService**: For service companies (consulting, agencies, etc.)
- **RetailHistoricalService**: For retail companies (stores, e-commerce, etc.)
- **SaasHistoricalService**: For SaaS companies (software subscriptions, etc.)

### 3. HistoricalServiceFactory
- Manages the registry of available company types
- Provides unified interface for creating services
- Handles validation and routing to appropriate implementations

## Usage

### Basic Usage

```python
from services.historical import HistoricalServiceFactory

# Calculate historical statements for a service company
result = HistoricalServiceFactory.calculate_historical_statements(
    company_type='service',
    data={
        'companyType': 'service',
        'historicalData': {
            'revenue': [1000000, 1200000, 1400000],
            'operating_expenses': [800000, 900000, 1000000],
            'employee_count': [10, 12, 15],
            # ... other data
        },
        'assumptions': {
            'revenue_growth': 15,
            'utilization_rate_target': 0.75
        }
    }
)
```

### API Endpoints

The system provides several API endpoints:

- `POST /api/v1/models/historical/calculate` - Calculate historical statements
- `GET /api/v1/models/historical/company-types` - Get available company types
- `GET /api/v1/models/historical/company-types/{company_type}` - Get company type info
- `POST /api/v1/models/historical/validate` - Validate historical data

## Adding New Company Types

To add a new company type (e.g., manufacturing):

### 1. Create the Implementation

```python
# manufacturing_historical_service.py
from .base_historical_service import BaseHistoricalService

class ManufacturingHistoricalService(BaseHistoricalService):
    def __init__(self):
        super().__init__("manufacturing")
    
    def _get_supported_metrics(self) -> List[str]:
        return [
            'production_efficiency',
            'capacity_utilization',
            'inventory_turnover',
            'cost_per_unit',
            # ... other manufacturing metrics
        ]
    
    def _get_required_fields(self) -> List[str]:
        return [
            'revenue',
            'cost_of_goods_sold',
            'production_capacity',
            'inventory',
            # ... other required fields
        ]
    
    # Implement other required methods...
```

### 2. Register with Factory

```python
# In historical_factory.py
from .manufacturing_historical_service import ManufacturingHistoricalService

class HistoricalServiceFactory:
    _service_registry: Dict[str, Type[BaseHistoricalService]] = {
        'service': ServiceHistoricalService,
        'retail': RetailHistoricalService,
        'manufacturing': ManufacturingHistoricalService,  # Add this line
    }
```

### 3. Update Package Exports

```python
# In __init__.py
from .manufacturing_historical_service import ManufacturingHistoricalService

__all__ = [
    'calculate_historical_statements',
    'BaseHistoricalService', 
    'ServiceHistoricalService',
    'ManufacturingHistoricalService',  # Add this
    'HistoricalServiceFactory'
]
```

## Company Type Features

### Service Companies
- **Key Metrics**: Utilization rate, billable hours, revenue per employee
- **Required Fields**: Revenue, operating expenses, employee count, billable hours
- **Special Features**: Service delivery efficiency, client retention

### Retail Companies
- **Key Metrics**: Inventory turnover, revenue per square foot, same-store sales
- **Required Fields**: Revenue, COGS, inventory, store count, square footage
- **Special Features**: Store expansion, inventory management

### SaaS Companies (Template)
- **Key Metrics**: MRR, churn rate, CAC, LTV, ARPU
- **Required Fields**: Revenue, subscription data, customer metrics
- **Special Features**: Recurring revenue analysis, customer lifecycle

## Data Validation

Each company type has its own validation rules:

```python
# Example validation for service companies
def validate_historical_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
    errors = []
    warnings = []
    
    # Check required fields
    for field in self.required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Company-specific validations
    if 'billable_hours' in data and 'employee_count' in data:
        # Check for reasonable utilization rates
        pass
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }
```

## Metrics and KPIs

Each company type supports different metrics:

### Service Metrics
- Revenue per employee
- Utilization rate
- Service delivery efficiency
- Client retention rate
- Average project size

### Retail Metrics
- Revenue per square foot
- Inventory turnover
- Same-store sales growth
- Customer traffic
- Average transaction value

## Assumptions and Projections

Company-specific assumptions can be applied:

```python
# Service company assumptions
assumptions = {
    'utilization_rate_target': 0.75,
    'service_delivery_efficiency_target': 0.85,
    'employee_productivity_target': 150000  # Revenue per employee
}

# Retail company assumptions
assumptions = {
    'target_inventory_turnover': 6.0,
    'store_growth_rate': 0.10,
    'same_store_sales_growth_target': 0.05
}
```

## Error Handling

The system provides comprehensive error handling:

```python
try:
    result = HistoricalServiceFactory.calculate_historical_statements(
        company_type='service', 
        data=request_data
    )
except ValueError as e:
    # Handle unsupported company type
    return {"error": str(e)}
except Exception as e:
    # Handle calculation errors
    return {"error": f"Calculation failed: {str(e)}"}
```

## Testing

To test a new company type implementation:

```python
# Test validation
validation_result = HistoricalServiceFactory.validate_historical_data(
    company_type='manufacturing',
    data=test_data
)

# Test calculation
result = HistoricalServiceFactory.calculate_historical_statements(
    company_type='manufacturing',
    data=test_data
)

# Test metrics
metrics = HistoricalServiceFactory.get_supported_metrics('manufacturing')
```

## Migration from Legacy

The original `historical_calculator.py` is maintained for backward compatibility. New implementations should use the factory pattern for better modularity and extensibility.

## Future Enhancements

1. **More Company Types**: Add manufacturing, healthcare, real estate, etc.
2. **Advanced Metrics**: Industry-specific KPIs and benchmarks
3. **Machine Learning**: Predictive analytics for projections
4. **Data Import**: Support for more data formats and sources
5. **Reporting**: Enhanced visualization and reporting capabilities
