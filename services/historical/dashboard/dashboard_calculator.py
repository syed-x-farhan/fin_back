"""
Dashboard Calculator

Common calculation utilities and helper functions for dashboard services.
This provides shared functionality across different company types.
"""

from typing import Dict, Any, List, Optional, Tuple
import math
import statistics
from datetime import datetime, timedelta


class DashboardCalculator:
    """
    Common dashboard calculation utilities.
    
    This class provides shared calculation functions that can be used
    across different company-specific dashboard services.
    """
    
    @staticmethod
    def calculate_growth_rate(values: List[float]) -> float:
        """
        Calculate growth rate between first and last values.
        
        Args:
            values: List of numeric values
            
        Returns:
            Growth rate as percentage
        """
        if len(values) < 2:
            return 0.0
        
        first_value = values[0]
        last_value = values[-1]
        
        if first_value == 0:
            return 0.0
        
        return ((last_value - first_value) / first_value) * 100
    
    @staticmethod
    def calculate_compound_annual_growth_rate(values: List[float], years: int) -> float:
        """
        Calculate Compound Annual Growth Rate (CAGR).
        
        Args:
            values: List of numeric values
            years: Number of years
            
        Returns:
            CAGR as percentage
        """
        if len(values) < 2 or years <= 0:
            return 0.0
        
        first_value = values[0]
        last_value = values[-1]
        
        if first_value <= 0:
            return 0.0
        
        cagr = (math.pow(last_value / first_value, 1 / years) - 1) * 100
        return cagr
    
    @staticmethod
    def calculate_average(values: List[float]) -> float:
        """
        Calculate average of values.
        
        Args:
            values: List of numeric values
            
        Returns:
            Average value
        """
        if not values:
            return 0.0
        
        return sum(values) / len(values)
    
    @staticmethod
    def calculate_median(values: List[float]) -> float:
        """
        Calculate median of values.
        
        Args:
            values: List of numeric values
            
        Returns:
            Median value
        """
        if not values:
            return 0.0
        
        return statistics.median(values)
    
    @staticmethod
    def calculate_standard_deviation(values: List[float]) -> float:
        """
        Calculate standard deviation of values.
        
        Args:
            values: List of numeric values
            
        Returns:
            Standard deviation
        """
        if len(values) < 2:
            return 0.0
        
        return statistics.stdev(values)
    
    @staticmethod
    def calculate_percentile(values: List[float], percentile: float) -> float:
        """
        Calculate percentile of values.
        
        Args:
            values: List of numeric values
            percentile: Percentile to calculate (0-100)
            
        Returns:
            Percentile value
        """
        if not values:
            return 0.0
        
        return statistics.quantile(values, percentile / 100)
    
    @staticmethod
    def calculate_ratios(income_statement: Dict[str, Any], balance_sheet: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate common financial ratios.
        
        Args:
            income_statement: Income statement data
            balance_sheet: Balance sheet data
            
        Returns:
            Dictionary of financial ratios
        """
        ratios = {}
        
        # Extract values
        revenue = DashboardCalculator._get_value_from_statement(income_statement, 'Revenue', 0)
        net_income = DashboardCalculator._get_value_from_statement(income_statement, 'Net Income', 0)
        total_assets = DashboardCalculator._get_value_from_statement(balance_sheet, 'Total Assets', 0)
        total_equity = DashboardCalculator._get_value_from_statement(balance_sheet, 'Total Equity', 0)
        current_assets = DashboardCalculator._get_value_from_statement(balance_sheet, 'Total Current Assets', 0)
        current_liabilities = DashboardCalculator._get_value_from_statement(balance_sheet, 'Total Current Liabilities', 0)
        total_liabilities = DashboardCalculator._get_value_from_statement(balance_sheet, 'Total Liabilities', 0)
        
        # Calculate ratios
        if revenue > 0:
            ratios['net_margin'] = (net_income / revenue) * 100
        else:
            ratios['net_margin'] = 0.0
        
        if total_assets > 0:
            ratios['roa'] = (net_income / total_assets) * 100
            ratios['asset_turnover'] = revenue / total_assets
        else:
            ratios['roa'] = 0.0
            ratios['asset_turnover'] = 0.0
        
        if total_equity > 0:
            ratios['roe'] = (net_income / total_equity) * 100
        else:
            ratios['roe'] = 0.0
        
        if current_liabilities > 0:
            ratios['current_ratio'] = current_assets / current_liabilities
        else:
            ratios['current_ratio'] = 0.0
        
        if total_equity > 0:
            ratios['debt_to_equity'] = total_liabilities / total_equity
        else:
            ratios['debt_to_equity'] = 0.0
        
        return ratios
    
    @staticmethod
    def calculate_trend_analysis(values: List[float], years: List[str]) -> Dict[str, Any]:
        """
        Perform trend analysis on a series of values.
        
        Args:
            values: List of numeric values
            years: List of year labels
            
        Returns:
            Trend analysis results
        """
        if len(values) < 2:
            return {
                'trend': 'insufficient_data',
                'growth_rate': 0.0,
                'volatility': 0.0,
                'consistency': 0.0
            }
        
        # Calculate growth rate
        growth_rate = DashboardCalculator.calculate_growth_rate(values)
        
        # Calculate volatility (coefficient of variation)
        mean = DashboardCalculator.calculate_average(values)
        std_dev = DashboardCalculator.calculate_standard_deviation(values)
        volatility = (std_dev / mean * 100) if mean > 0 else 0.0
        
        # Calculate consistency (how steady the growth is)
        year_over_year_growth = []
        for i in range(1, len(values)):
            if values[i-1] > 0:
                yoy_growth = ((values[i] - values[i-1]) / values[i-1]) * 100
                year_over_year_growth.append(yoy_growth)
        
        consistency = 100 - DashboardCalculator.calculate_standard_deviation(year_over_year_growth) if year_over_year_growth else 0.0
        
        # Determine trend direction
        if growth_rate > 5:
            trend = 'strong_growth'
        elif growth_rate > 0:
            trend = 'moderate_growth'
        elif growth_rate > -5:
            trend = 'decline'
        else:
            trend = 'significant_decline'
        
        return {
            'trend': trend,
            'growth_rate': growth_rate,
            'volatility': volatility,
            'consistency': max(0, consistency),
            'year_over_year_growth': year_over_year_growth
        }
    
    @staticmethod
    def calculate_benchmark_comparison(actual_values: List[float], benchmark_values: List[float]) -> Dict[str, Any]:
        """
        Compare actual values against benchmark values.
        
        Args:
            actual_values: Actual performance values
            benchmark_values: Benchmark values for comparison
            
        Returns:
            Benchmark comparison results
        """
        if not actual_values or not benchmark_values:
            return {
                'performance_vs_benchmark': 0.0,
                'benchmark_percentile': 0.0,
                'performance_rating': 'insufficient_data'
            }
        
        # Calculate average performance vs benchmark
        actual_avg = DashboardCalculator.calculate_average(actual_values)
        benchmark_avg = DashboardCalculator.calculate_average(benchmark_values)
        
        if benchmark_avg > 0:
            performance_vs_benchmark = ((actual_avg - benchmark_avg) / benchmark_avg) * 100
        else:
            performance_vs_benchmark = 0.0
        
        # Calculate percentile ranking
        all_values = benchmark_values + [actual_avg]
        all_values.sort()
        percentile = (all_values.index(actual_avg) / len(all_values)) * 100
        
        # Determine performance rating
        if percentile >= 90:
            rating = 'excellent'
        elif percentile >= 75:
            rating = 'good'
        elif percentile >= 50:
            rating = 'average'
        elif percentile >= 25:
            rating = 'below_average'
        else:
            rating = 'poor'
        
        return {
            'performance_vs_benchmark': performance_vs_benchmark,
            'benchmark_percentile': percentile,
            'performance_rating': rating
        }
    
    @staticmethod
    def calculate_seasonality(values: List[float], periods_per_year: int = 12) -> Dict[str, Any]:
        """
        Calculate seasonality patterns in data.
        
        Args:
            values: List of numeric values
            periods_per_year: Number of periods per year (12 for monthly, 4 for quarterly)
            
        Returns:
            Seasonality analysis results
        """
        if len(values) < periods_per_year * 2:
            return {
                'seasonality_strength': 0.0,
                'seasonal_pattern': 'insufficient_data',
                'peak_period': None,
                'trough_period': None
            }
        
        # Calculate seasonal indices
        seasonal_indices = []
        for period in range(periods_per_year):
            period_values = values[period::periods_per_year]
            if period_values:
                seasonal_indices.append(DashboardCalculator.calculate_average(period_values))
        
        if not seasonal_indices:
            return {
                'seasonality_strength': 0.0,
                'seasonal_pattern': 'insufficient_data',
                'peak_period': None,
                'trough_period': None
            }
        
        # Calculate seasonality strength
        overall_mean = DashboardCalculator.calculate_average(seasonal_indices)
        if overall_mean > 0:
            seasonality_strength = (DashboardCalculator.calculate_standard_deviation(seasonal_indices) / overall_mean) * 100
        else:
            seasonality_strength = 0.0
        
        # Find peak and trough periods
        max_index = max(seasonal_indices)
        min_index = min(seasonal_indices)
        peak_period = seasonal_indices.index(max_index)
        trough_period = seasonal_indices.index(min_index)
        
        # Determine seasonal pattern
        if seasonality_strength > 20:
            pattern = 'strong_seasonality'
        elif seasonality_strength > 10:
            pattern = 'moderate_seasonality'
        else:
            pattern = 'minimal_seasonality'
        
        return {
            'seasonality_strength': seasonality_strength,
            'seasonal_pattern': pattern,
            'peak_period': peak_period,
            'trough_period': trough_period,
            'seasonal_indices': seasonal_indices
        }
    
    @staticmethod
    def calculate_forecast_accuracy(actual_values: List[float], forecast_values: List[float]) -> Dict[str, float]:
        """
        Calculate forecast accuracy metrics.
        
        Args:
            actual_values: Actual values
            forecast_values: Forecasted values
            
        Returns:
            Forecast accuracy metrics
        """
        if len(actual_values) != len(forecast_values) or not actual_values:
            return {
                'mape': 0.0,
                'mae': 0.0,
                'rmse': 0.0,
                'accuracy_score': 0.0
            }
        
        # Calculate Mean Absolute Percentage Error (MAPE)
        mape_errors = []
        for actual, forecast in zip(actual_values, forecast_values):
            if actual > 0:
                mape_errors.append(abs((actual - forecast) / actual) * 100)
        
        mape = DashboardCalculator.calculate_average(mape_errors) if mape_errors else 0.0
        
        # Calculate Mean Absolute Error (MAE)
        mae_errors = [abs(actual - forecast) for actual, forecast in zip(actual_values, forecast_values)]
        mae = DashboardCalculator.calculate_average(mae_errors)
        
        # Calculate Root Mean Square Error (RMSE)
        rmse_errors = [(actual - forecast) ** 2 for actual, forecast in zip(actual_values, forecast_values)]
        rmse = math.sqrt(DashboardCalculator.calculate_average(rmse_errors))
        
        # Calculate accuracy score (100 - MAPE)
        accuracy_score = max(0, 100 - mape)
        
        return {
            'mape': mape,
            'mae': mae,
            'rmse': rmse,
            'accuracy_score': accuracy_score
        }
    
    @staticmethod
    def _get_value_from_statement(statement: Dict[str, Any], label: str, year_index: int = 0) -> float:
        """Helper method to get value from statement line items."""
        if not statement.get('line_items'):
            return 0.0
        
        for item in statement['line_items']:
            if label.lower() in item.get('label', '').lower():
                values = item.get('values', [])
                if len(values) > year_index:
                    return float(values[year_index])
        
        return 0.0

