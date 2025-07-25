import logging
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)

def validate_forecast_request(data):
    """Validate forecast request parameters"""
    errors = []
    
    if not isinstance(data, dict):
        return {
            'valid': False,
            'errors': ['Request data must be a JSON object']
        }
    
    # Validate start_date
    start_date = data.get('start_date')
    if start_date:
        if not isinstance(start_date, str):
            errors.append('start_date must be a string')
        else:
            # Check date format (YYYY-MM-DD)
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            if not re.match(date_pattern, start_date):
                errors.append('start_date must be in YYYY-MM-DD format')
            else:
                try:
                    parsed_date = datetime.strptime(start_date, '%Y-%m-%d')
                    # Check if date is not too far in the past or future
                    today = datetime.now()
                    if parsed_date < today - timedelta(days=365 * 5):
                        errors.append('start_date cannot be more than 5 years in the past')
                    elif parsed_date > today + timedelta(days=365 * 2):
                        errors.append('start_date cannot be more than 2 years in the future')
                except ValueError:
                    errors.append('start_date is not a valid date')
    
    # Validate periods
    periods = data.get('periods', 30)
    if not isinstance(periods, int):
        try:
            periods = int(periods)
        except (ValueError, TypeError):
            errors.append('periods must be an integer')
    else:
        if periods < 1:
            errors.append('periods must be at least 1')
        elif periods > 365:
            errors.append('periods cannot exceed 365 days')
    
    # Validate confidence_level if provided
    confidence_level = data.get('confidence_level')
    if confidence_level is not None:
        try:
            confidence_level = float(confidence_level)
            if confidence_level <= 0 or confidence_level >= 1:
                errors.append('confidence_level must be between 0 and 1')
        except (ValueError, TypeError):
            errors.append('confidence_level must be a number between 0 and 1')
    
    # Validate additional parameters
    if 'model_params' in data:
        model_params = data['model_params']
        if not isinstance(model_params, dict):
            errors.append('model_params must be a JSON object')
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_date_range(start_date, end_date):
    """Validate a date range"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start >= end:
            return False, "start_date must be before end_date"
        
        if (end - start).days > 365:
            return False, "Date range cannot exceed 365 days"
        
        return True, None
        
    except ValueError as e:
        return False, f"Invalid date format: {str(e)}"

def sanitize_input(data):
    """Sanitize input data to prevent injection attacks"""
    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            if isinstance(key, str) and key.isalnum():
                sanitized[key] = sanitize_input(value)
        return sanitized
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data[:100]]  # Limit list size
    elif isinstance(data, str):
        # Remove potentially dangerous characters
        return re.sub(r'[<>"\'\;]', '', data)[:1000]  # Limit string length
    elif isinstance(data, (int, float, bool)) or data is None:
        return data
    else:
        return str(data)[:1000]
