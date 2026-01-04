from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.api.v1.endpoints import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Todo API",
        description="Full-Stack Todo Web Application API",
        version="1.0.0",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Additional security headers
        allow_origin_regex="https://.*\.vercel\.app",  # Allow Vercel deployments
    )

    # Include API router
    app.include_router(api_router, prefix="/api")

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)