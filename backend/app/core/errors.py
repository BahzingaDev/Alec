from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base API error class"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv

class ValidationError(APIError):
    """Validation error"""
    def __init__(self, message, payload=None):
        super().__init__(message, status_code=400, payload=payload)

class NotFoundError(APIError):
    """Resource not found error"""
    def __init__(self, message='Resource not found', payload=None):
        super().__init__(message, status_code=404, payload=payload)

class UnauthorizedError(APIError):
    """Unauthorized error"""
    def __init__(self, message='Unauthorized', payload=None):
        super().__init__(message, status_code=401, payload=payload)

class ForbiddenError(APIError):
    """Forbidden error"""
    def __init__(self, message='Forbidden', payload=None):
        super().__init__(message, status_code=403, payload=payload)

def register_error_handlers(app):
    """Register error handlers with Flask app"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        response = jsonify({
            'message': error.description,
            'status': 'error',
            'code': error.code
        })
        response.status_code = error.code
        return response
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        logger.error(f'Unhandled exception: {error}', exc_info=True)
        response = jsonify({
            'message': 'Internal server error',
            'status': 'error',
            'code': 500
        })
        response.status_code = 500
        return response