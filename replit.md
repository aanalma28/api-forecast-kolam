# Fish Growth Forecasting API

## Overview

This is a Flask-based REST API service that provides specialized machine learning-powered fish growth forecasting capabilities. The application predicts fish growth timelines until target weight is reached, designed specifically for aquaculture and fish farming operations. It includes a web interface for documentation and API testing, along with comprehensive validation and preprocessing utilities for fish farming data.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular Flask architecture with clear separation of concerns:

- **Flask Application Core**: Main application setup with CORS enabled and proxy middleware
- **API Layer**: RESTful endpoints with rate limiting and validation
- **ML Model Layer**: Scikit-learn based forecasting model with automatic persistence
- **Utility Layer**: Input validation and data preprocessing modules
- **Frontend Layer**: HTML templates with Bootstrap for documentation and interface

## Key Components

### Backend Framework
- **Flask**: Lightweight WSGI web framework
- **Flask-CORS**: Cross-origin resource sharing support for API access
- **ProxyFix**: Handles reverse proxy headers for deployment

### Machine Learning
- **Fish Growth Model**: Placeholder implementation designed for user's custom model integration
- **Feature Engineering**: Date transformation (day, month, week, day_to), categorical encoding (fish_type, pool_type), and sequence processing
- **Data Preprocessing**: StandardScaler normalization, 7-window sequence creation with shape (batch_size, 7, 19)
- **Target-Based Prediction**: Predicts growth timeline until target weight is reached

### API Features
- **Fish-Specific Validation**: Validates fish farming data structure (target_weight, sequence with fish_type, weights, dates)
- **Rate Limiting**: In-memory rate limiting (100 requests/hour per IP)
- **Categorical Encoding**: Supports fish types (Nila, Mujair, Gurame) and pool types (A1-A10)
- **Sequence Processing**: Creates 7-day windows from time series data for model input
- **Error Handling**: Structured error responses with appropriate HTTP status codes

### Frontend Interface
- **Bootstrap 5**: Dark theme UI framework
- **Feather Icons**: Consistent iconography
- **Responsive Design**: Mobile-friendly documentation and interface
- **API Documentation**: Interactive documentation pages

## Data Flow

1. **Request Reception**: Flask receives API requests through CORS-enabled endpoints
2. **Rate Limiting**: Request count validation per IP address
3. **Input Validation**: Parameter validation using custom validation utilities
4. **Data Preprocessing**: Input normalization and type conversion
5. **Model Prediction**: Linear regression model generates forecasts
6. **Response Formatting**: JSON response with predictions and metadata
7. **Error Handling**: Structured error responses for validation or processing failures

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **Flask-CORS**: Cross-origin resource sharing
- **scikit-learn**: Machine learning model and preprocessing
- **pandas**: Data manipulation and time series handling
- **numpy**: Numerical computations
- **joblib**: Model serialization and persistence

### Frontend Dependencies
- **Bootstrap 5**: CSS framework from CDN
- **Feather Icons**: Icon library from CDN
- **Custom CSS**: Application-specific styling

### Runtime Dependencies
- **Werkzeug**: WSGI utilities and proxy handling
- **Python Standard Library**: datetime, logging, os, warnings

## Deployment Strategy

### Development Configuration
- **Debug Mode**: Enabled in main.py for development
- **Host Configuration**: Binds to 0.0.0.0:5000 for container compatibility
- **Session Secret**: Environment variable with fallback to development key

### Production Considerations
- **Proxy Support**: ProxyFix middleware for reverse proxy deployment
- **Environment Variables**: Session secret should be configured via environment
- **Model Persistence**: Models saved to data/ directory for persistence across deployments
- **Static Files**: CSS and JS served through Flask's static file handling

### Scalability Limitations
- **In-Memory Rate Limiting**: Current implementation uses local memory storage
- **Model Loading**: Single model instance loaded at startup
- **No Database**: Currently uses file-based model persistence

The application is designed for easy deployment on platforms like Replit, with built-in sample data generation and comprehensive error handling for robust operation.