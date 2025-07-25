import logging
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from utils.validation import validate_forecast_request
from utils.preprocessing import preprocess_input_data
from app import forecast_model

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Rate limiting storage (simple in-memory for demo)
request_counts = {}
RATE_LIMIT = 100  # requests per hour per IP

def check_rate_limit(ip_address):
    """Simple rate limiting check"""
    current_time = datetime.now()
    hour_key = current_time.strftime('%Y-%m-%d-%H')
    key = f"{ip_address}:{hour_key}"
    
    if key not in request_counts:
        request_counts[key] = 0
    
    request_counts[key] += 1
    
    # Cleanup old entries
    for old_key in list(request_counts.keys()):
        if old_key.split(':')[1] != hour_key:
            del request_counts[old_key]
    
    return request_counts[key] <= RATE_LIMIT

@api_bp.before_request
def before_request():
    """Check rate limits before processing requests"""
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    
    if not check_rate_limit(client_ip):
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': f'Maximum {RATE_LIMIT} requests per hour allowed',
            'status': 429
        }), 429

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        model_info = forecast_model.get_model_info()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'model_status': 'trained' if model_info['is_trained'] else 'not_trained',
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@api_bp.route('/model/info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    try:
        info = forecast_model.get_model_info()
        return jsonify({
            'success': True,
            'data': info,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'status': 500
        }), 500

@api_bp.route('/forecast', methods=['POST'])
def generate_forecast():
    """Generate forecast predictions"""
    try:
        # Check if request has JSON data
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json',
                'status': 400
            }), 400
        
        # Get JSON data
        data = request.get_json()
        if data is None:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data',
                'status': 400
            }), 400
        
        # Validate request
        validation_result = validate_forecast_request(data)
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'details': validation_result['errors'],
                'status': 400
            }), 400
        
        # Extract parameters
        target_weight = data.get('target_weight')
        sequence = data.get('sequence')
        
        # Preprocess input
        processed_data = preprocess_input_data(data)
        
        # Generate predictions until target weight is reached
        result = forecast_model.predict_until_target(
            sequences=processed_data['sequences'],
            target_weight=processed_data['target_weight']
        )
        
        return jsonify({
            'success': True,
            'data': {
                'predictions': result['predictions'],
                'summary': result['summary'],
                'metadata': {
                    'model_type': 'Fish Growth Forecast',
                    'generated_at': datetime.now().isoformat(),
                    'input_data': {
                        'target_weight': target_weight,
                        'sequence_length': len(sequence),
                        'sequences_shape': processed_data['sequences'].shape,
                        'feature_columns': processed_data['feature_columns']
                    },
                    'model_info': result['model_info']
                }
            }
        })
        
    except ValueError as e:
        logger.warning(f"Validation error in forecast: {e}")
        return jsonify({
            'success': False,
            'error': 'Invalid input parameters',
            'message': str(e),
            'status': 400
        }), 400
        
    except Exception as e:
        logger.error(f"Error generating forecast: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'Failed to generate forecast predictions',
            'status': 500
        }), 500

@api_bp.route('/forecast/batch', methods=['POST'])
def batch_forecast():
    """Generate multiple forecasts in batch"""
    try:
        # Check if request has JSON data
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json',
                'status': 400
            }), 400
        
        # Get JSON data
        data = request.get_json()
        if data is None:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data',
                'status': 400
            }), 400
        
        if not isinstance(data, dict) or 'requests' not in data:
            return jsonify({
                'success': False,
                'error': 'Invalid batch request format',
                'message': 'Expected {"requests": [list_of_forecast_requests]}',
                'status': 400
            }), 400
        
        requests_list = data['requests']
        if len(requests_list) > 10:  # Limit batch size
            return jsonify({
                'success': False,
                'error': 'Batch size too large',
                'message': 'Maximum 10 requests per batch allowed',
                'status': 400
            }), 400
        
        results = []
        for i, req in enumerate(requests_list):
            try:
                # Validate individual request
                validation_result = validate_forecast_request(req)
                if not validation_result['valid']:
                    results.append({
                        'request_id': i,
                        'success': False,
                        'error': 'Validation failed',
                        'details': validation_result['errors']
                    })
                    continue
                
                # Process request
                processed_data = preprocess_input_data(req)
                result = forecast_model.predict_until_target(
                    sequences=processed_data['sequences'],
                    target_weight=processed_data['target_weight']
                )
                
                results.append({
                    'request_id': i,
                    'success': True,
                    'data': result
                })
                
            except Exception as e:
                logger.error(f"Error in batch request {i}: {e}")
                results.append({
                    'request_id': i,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'data': {
                'results': results,
                'total_requests': len(requests_list),
                'successful_requests': sum(1 for r in results if r['success']),
                'generated_at': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Error in batch forecast: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500
