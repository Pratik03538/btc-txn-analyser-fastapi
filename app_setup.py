from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def configure_app():
    """
    Creates and configures the FastAPI application instance, including middleware.
    """
    app = FastAPI(
        title="Bitcoin Dashboard API",
        description="API to serve data for the luxury Bitcoin dashboard.",
        version="1.0.0"
    )

    # --- Add CORS Middleware ---
    # This is crucial for allowing the frontend (HTML file opened in a browser)
    # to communicate with the backend API.
    origins = [
        "*" # Allows all origins for simplicity. For production, restrict this.
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"], # Allows all methods (GET, POST, etc.)
        allow_headers=["*"], # Allows all headers
    )

    return app

