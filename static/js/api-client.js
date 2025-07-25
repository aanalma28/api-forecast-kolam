/**
 * API Client for ML Forecasting API
 * Handles all API interactions and UI updates
 */

class APIClient {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    /**
     * Make HTTP request with error handling
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`);
            }

            return data;
        } catch (error) {
            console.error(`API Request failed for ${endpoint}:`, error);
            throw error;
        }
    }

    /**
     * Get API health status
     */
    async getHealth() {
        const cacheKey = 'health';
        
        // Check cache first
        if (this.cache.has(cacheKey)) {
            const cached = this.cache.get(cacheKey);
            if (Date.now() - cached.timestamp < this.cacheTimeout) {
                return cached.data;
            }
        }

        try {
            const data = await this.request('/health');
            
            // Cache the result
            this.cache.set(cacheKey, {
                data: data,
                timestamp: Date.now()
            });
            
            return data;
        } catch (error) {
            return {
                status: 'unhealthy',
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Get model information
     */
    async getModelInfo() {
        return await this.request('/model/info');
    }

    /**
     * Generate forecast
     */
    async generateForecast(params = {}) {
        const defaultParams = {
            start_date: new Date().toISOString().split('T')[0],
            periods: 30,
            confidence_level: 0.95
        };

        const requestBody = { ...defaultParams, ...params };

        return await this.request('/forecast', {
            method: 'POST',
            body: JSON.stringify(requestBody)
        });
    }

    /**
     * Generate batch forecast
     */
    async generateBatchForecast(requests) {
        if (!Array.isArray(requests) || requests.length === 0) {
            throw new Error('Requests must be a non-empty array');
        }

        if (requests.length > 10) {
            throw new Error('Maximum 10 requests allowed per batch');
        }

        return await this.request('/forecast/batch', {
            method: 'POST',
            body: JSON.stringify({ requests })
        });
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }
}

// Create global API client instance
const apiClient = new APIClient();

/**
 * UI Helper Functions
 */

/**
 * Check and display API status
 */
async function checkAPIStatus() {
    const statusElement = document.getElementById('api-status');
    if (!statusElement) return;

    try {
        // Show loading state
        statusElement.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Checking status...</span>
                </div>
                <p class="mt-2 text-muted">Checking API status...</p>
            </div>
        `;

        const health = await apiClient.getHealth();
        
        if (health.status === 'healthy') {
            statusElement.innerHTML = `
                <div class="text-center">
                    <div class="status-indicator status-healthy"></div>
                    <span class="text-success fw-bold">API is healthy</span>
                    <div class="mt-2">
                        <small class="text-muted">Model Status: ${health.model_status || 'unknown'}</small><br>
                        <small class="text-muted">Version: ${health.version || '1.0.0'}</small><br>
                        <small class="text-muted">Last checked: ${new Date(health.timestamp).toLocaleTimeString()}</small>
                    </div>
                </div>
            `;
        } else {
            statusElement.innerHTML = `
                <div class="text-center">
                    <div class="status-indicator status-unhealthy"></div>
                    <span class="text-danger fw-bold">API is unhealthy</span>
                    <div class="mt-2">
                        <small class="text-muted">Error: ${health.error || 'Unknown error'}</small><br>
                        <small class="text-muted">Last checked: ${new Date(health.timestamp).toLocaleTimeString()}</small>
                    </div>
                    <button class="btn btn-sm btn-outline-primary mt-2" onclick="checkAPIStatus()">
                        <i data-feather="refresh-cw" class="me-1"></i>
                        Retry
                    </button>
                </div>
            `;
        }
        
        // Re-initialize feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
        
    } catch (error) {
        statusElement.innerHTML = `
            <div class="text-center">
                <div class="status-indicator status-unhealthy"></div>
                <span class="text-danger fw-bold">Connection failed</span>
                <div class="mt-2">
                    <small class="text-muted">Error: ${error.message}</small>
                    <button class="btn btn-sm btn-outline-primary mt-2 d-block mx-auto" onclick="checkAPIStatus()">
                        <i data-feather="refresh-cw" class="me-1"></i>
                        Retry
                    </button>
                </div>
            </div>
        `;
        
        // Re-initialize feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }
}

/**
 * Format JSON for display
 */
function formatJSON(obj) {
    return JSON.stringify(obj, null, 2)
        .replace(/(".*?"):/g, '<span class="json-key">$1</span>:')
        .replace(/: (".*?")/g, ': <span class="json-string">$1</span>')
        .replace(/: (\d+\.?\d*)/g, ': <span class="json-number">$1</span>')
        .replace(/: (true|false)/g, ': <span class="json-boolean">$1</span>');
}

/**
 * Show notification toast
 */
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '1050';
        document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toastId = `toast-${Date.now()}`;
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="true" data-bs-delay="5000">
            <div class="toast-header bg-${type} text-white">
                <i data-feather="info" class="me-2"></i>
                <strong class="me-auto">API Response</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Initialize and show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    // Re-initialize feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }

    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

/**
 * Handle errors gracefully
 */
function handleError(error, context = 'API operation') {
    console.error(`Error in ${context}:`, error);
    showToast(`${context} failed: ${error.message}`, 'danger');
}

/**
 * Utility function to generate sample forecast
 */
async function generateSampleForecast() {
    try {
        const result = await apiClient.generateForecast({
            start_date: new Date().toISOString().split('T')[0],
            periods: 7
        });
        
        if (result.success) {
            showToast(`Generated ${result.data.predictions.length} predictions successfully!`, 'success');
            return result;
        } else {
            throw new Error(result.error || 'Unknown error');
        }
    } catch (error) {
        handleError(error, 'Forecast generation');
        return null;
    }
}

/**
 * Copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success');
    } catch (error) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('Copied to clipboard!', 'success');
    }
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Format number for display
 */
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

/**
 * Initialize API client functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // Set up periodic health checks
    if (document.getElementById('api-status')) {
        // Check immediately
        checkAPIStatus();
        
        // Then check every 30 seconds
        setInterval(checkAPIStatus, 30000);
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // Ctrl/Cmd + / to focus search (if implemented)
        if ((event.ctrlKey || event.metaKey) && event.key === '/') {
            event.preventDefault();
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
    });
});

// Export API client for use in other scripts
window.apiClient = apiClient;
window.checkAPIStatus = checkAPIStatus;
window.formatJSON = formatJSON;
window.showToast = showToast;
window.handleError = handleError;
window.generateSampleForecast = generateSampleForecast;
