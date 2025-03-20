import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import logger, console
from app.db.session import get_db, engine
from app.db.models import Base
from app.routers import auth, users, jobs

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS with specific configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # Use settings from config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include API routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(jobs.router, prefix=f"{settings.API_V1_STR}/jobs", tags=["jobs"])

@app.on_event("startup")
async def startup_event():
    """Initialize application at startup."""
    logger.info(f"[bold green]Starting {settings.PROJECT_NAME}[/bold green]")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Log level: {settings.LOG_LEVEL}")
    logger.info("Configuration loaded:")
    logger.info(f"  [cyan]SLURM Host:[/cyan] {settings.SLURM_HOST}")
    logger.info(f"  [cyan]SLURM User:[/cyan] {settings.SLURM_USER}")
    logger.info(f"  [cyan]Template Directory:[/cyan] {settings.TEMPLATE_DIR}")
    logger.info(f"  [cyan]Container Output Directory:[/cyan] {settings.CONTAINER_OUTPUT_DIR}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the SLURM Container Manager API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Create a first user if no users exist (useful for first run)
@app.on_event("startup")
async def create_first_user():
    from app.services.user import UserService
    from app.schemas.user import UserCreate
    
    logger.info("Checking for initial admin user...")
    db = next(get_db())
    user = UserService.get_by_username(db=db, username="admin")
    if not user:
        logger.info("Creating initial admin user...")
        user_in = UserCreate(
            username="admin",
            email="admin@example.com",
            password="adminpassword",
            first_name="Admin",
            last_name="User"
        )
        UserService.create(db=db, user_in=user_in)
        logger.info("[green]Admin user created successfully[/green]")
    else:
        logger.info("Admin user already exists")

if __name__ == "__main__":
    import uvicorn
    console.print("[bold green]Starting development server...[/bold green]")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )