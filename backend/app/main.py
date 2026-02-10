"""PDF Toolbox FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import SecurityHeadersMiddleware
from app.api.v1.api import api_router

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description='Simple & Fast PDF Processing Tools'
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get('/')
async def root():
    """Root endpoint."""
    return {
        'message': 'PDF Toolbox API',
        'version': settings.VERSION,
        'docs': '/docs',
        'endpoints': {
            'tools': f'{settings.API_V1_STR}/tools',
            'files': f'{settings.API_V1_STR}/files',
            'jobs': f'{settings.API_V1_STR}/jobs'
        }
    }


@app.get('/health')
async def health_check():
    """Health check endpoint."""
    return {
        'status': 'healthy',
        'version': settings.VERSION,
        'processors': list(app.state.processors) if hasattr(app.state, 'processors') else []
    }


@app.on_event('startup')
async def startup_event():
    """Initialize services on startup."""
    # Import processors to register them
    from app.processors import merge, split, extract, watermark, remove_watermark, remove_watermark_image, pdf_to_images

    # Store registered processors in app state
    from app.processors.registry import registry
    app.state.processors = registry.get_all().keys()

    # Ensure storage directories exist
    from pathlib import Path
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.RESULT_DIR).mkdir(parents=True, exist_ok=True)


@app.on_event('shutdown')
async def shutdown_event():
    """Cleanup on shutdown."""
    # Cleanup temporary files if needed
    pass
