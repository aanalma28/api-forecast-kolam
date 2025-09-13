import logging
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)

# Maksimum bobot per jenis ikan (isi sesuai dataset kamu)
MAX_WEIGHT_PER_FISH = {
    "Nila Merah": 2.5,
    "Patin": 3.0,
    "Lele": 2.0,
    "Bawal": 1.5,
    "Gurame": 0.3
}

def validate_forecast_request(data):
    """Validate fish farming forecast request parameters"""
    errors = []
    
    if not isinstance(data, dict):
        return {
            'valid': False,
            'errors': ['Request data must be a JSON object']
        }
    
    # Validate target_weight     
    target_weight = data.get('target_weight')
    fish_type = data.get('fish_type')  # pastikan fish_type dikirim di request

    if target_weight is None:
        errors.append('target_weight is required')
    else:
        try:
            target_weight = float(target_weight)
            if target_weight <= 0:
                errors.append('target_weight must be greater than 0')
            elif fish_type in MAX_WEIGHT_PER_FISH:
                max_weight = MAX_WEIGHT_PER_FISH[fish_type]
                if target_weight > max_weight:
                    errors.append(f'target_weight for {fish_type} cannot exceed {max_weight}kg (max in dataset)')
            elif target_weight > 10:  # fallback limit
                errors.append('target_weight cannot exceed 10kg')
        except (ValueError, TypeError):
            errors.append('target_weight must be a number')
                
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }

def validate_sequence(data):
    errors = []
    # Validate sequence
    sequence = data.get('sequence')
    if not sequence:
        errors.append('sequence is required')
    elif not isinstance(sequence, list):
        errors.append('sequence must be an array')
    elif len(sequence) < 7:
        errors.append('sequence must contain at least 7 data points')
    elif len(sequence) > 100:  # Reasonable upper limit
        errors.append('sequence cannot exceed 100 data points')
    else:
        # Validate each sequence item
        # dynamical features
        valid_fish_types = [
            "Nila Merah", "Patin", "Lele", 
            "Bawal", "Gurame"
        ]
        
        for i, item in enumerate(sequence):
            if not isinstance(item, dict):
                errors.append(f'sequence[{i}] must be an object')
                continue
            
            # Validate required fields
            # dynamical features
            required_fields = [
                'date', 'fish_type',
                'start_weight', 'avg_weight', 'week_age'
            ]
            for field in required_fields:
                if field not in item:
                    errors.append(f'sequence[{i}] missing required field: {field}')
            
            # Validate date format
            if 'date' in item:
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, str(item['date'])):
                    errors.append(f'sequence[{i}].date must be in YYYY-MM-DD format')
                else:
                    try:
                        datetime.strptime(str(item['date']), '%Y-%m-%d')
                    except ValueError:
                        errors.append(f'sequence[{i}].date is not a valid date')
            
            # Validate fish_type (optional but must be valid if provided)
            if 'fish_type' in item and item['fish_type'] not in valid_fish_types:
                errors.append(f'sequence[{i}].fish_type must be one of: {valid_fish_types}')
            
            # Validate numeric fields
            numeric_fields = ['start_weight', 'avg_weight', 'week_age']
            for field in numeric_fields:
                if field in item:
                    try:
                        value = float(item[field])
                        if value < 0:
                            errors.append(f'sequence[{i}].{field} must be non-negative')
                        elif field in ['start_weight', 'avg_weight'] and value > 10:
                            errors.append(f'sequence[{i}].{field} cannot exceed 10kg')
                        elif field == 'week_age' and value > 100:
                            errors.append(f'sequence[{i}].{field} cannot exceed 100 weeks')
                    except (ValueError, TypeError):
                        errors.append(f'sequence[{i}].{field} must be a number')
    
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
