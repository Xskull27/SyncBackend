import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project_sync_backend.app.api.v1.endpoints.projects import router as projects_router
from project_sync_backend.app.api.v1.endpoints.auth import router as auth_router
from project_sync_backend.app.api.v1.endpoints.issues import router as issues_router
from project_sync_backend.app.api.v1.endpoints.dashboard import router as dashboard_router

from project_sync_backend.app.core.config import settings
from project_sync_backend.app.db.database import create_db_and_tables, test_database_connection

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Project Management System...")
    
    # Print environment settings (be careful not to log sensitive data in production)
    logger.info("Environment Settings Loaded")
    logger.info(f"Database URL configured: {bool(settings.APP_DATABASE_URL)}")
    
    # Database initialization with error handling
    try:
        logger.info("🔍 Testing database connection...")
        
        # First test the connection
        if test_database_connection():
            logger.info("✅ Database connection test successful")
            
            # If connection test passes, create tables
            logger.info("🔧 Creating database tables...")
            create_db_and_tables()
            logger.info("✅ Database tables created successfully")
            
        else:
            logger.warning("⚠️ Database connection failed")
            
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        logger.error("This is likely due to:")
        logger.error("1. Network connectivity issues")
        logger.error("2. Neon database is sleeping/inactive")
        logger.error("3. Incorrect database credentials")
        logger.error("4. Firewall blocking the connection")
        
        # For development, you might want to continue without database
        # For production, you might want to fail fast
        logger.warning("⚠️ Starting application without database initialization")
        logger.warning("Database operations will fail until connection is restored")
    
    logger.info("🎉 Application startup completed")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Project Management System...")
    # Add any cleanup code here if needed

app = FastAPI(
    title="Project Management System",
    description="A role-based project management system built with SQLModel",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bug-tracker-frontend-ochre.vercel.app",
        "http://localhost:3000", 
        "https://project-sync-sigma.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects_router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(issues_router, prefix="/api/v1/issues", tags=["issues"])
app.include_router(dashboard_router, prefix="/api/v1", tags=["dashboard"])

@app.get("/", tags=["root"])
@app.head("/", tags=["root"])
def read_root():
    return {
        "message": "Project Management System API", 
        "version": "1.0.0",
        "docs": "/docs",
        "health": "OK"
    }

@app.get("/health", tags=["health"])
def health_check():
    """Enhanced health check with database status"""
    try:
        db_status = test_database_connection()
        return {
            "status": "healthy" if db_status else "degraded",
            "database": "connected" if db_status else "disconnected",
            "version": "1.0.0",
            "message": "API is running" if db_status else "API running but database unavailable"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "error",
            "version": "1.0.0",
            "message": f"Health check failed: {str(e)}"
        }

@app.get("/db-status", tags=["health"])
def database_status():
    """Detailed database status endpoint"""
    try:
        db_connected = test_database_connection()
        return {
            "database_connected": db_connected,
            "database_url_configured": bool(settings.APP_DATABASE_URL),
            "status": "Database is accessible" if db_connected else "Database connection failed"
        }
    except Exception as e:
        return {
            "database_connected": False,
            "database_url_configured": bool(settings.APP_DATABASE_URL),
            "status": f"Database error: {str(e)}"
        }

# Only print sensitive settings in development
if os.getenv("ENVIRONMENT", "development") == "development":
    print("ENV SETTINGS:", {
        "SECRET_KEY": "***" if settings.SECRET_KEY else None,
        "ALGORITHM": settings.ALGORITHM,
        "ACCESS_TOKEN_EXPIRE_MINUTES": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "DATABASE_CONFIGURED": bool(settings.APP_DATABASE_URL)
    })

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
# import os
# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from project_sync_backend.app.api.v1.endpoints.projects import router as projects_router
# from project_sync_backend.app.api.v1.endpoints.auth import router as auth_router
# from project_sync_backend.app.api.v1.endpoints.issues import router as issues_router
# from project_sync_backend.app.api.v1.endpoints.dashboard import router as dashboard_router

# from project_sync_backend.app.core.config import settings
# from project_sync_backend.app.db.database import create_db_and_tables

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Create tables on startup
#     create_db_and_tables()
#     yield
#     # Cleanup on shutdown (if needed)

# app = FastAPI(
#     title="Project Management System",
#     description="A role-based project management system built with SQLModel",
#     version="1.0.0",
#     lifespan=lifespan
# )

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://bug-tracker-frontend-ochre.vercel.app","http://localhost:3000" , "https://projectsync-alpha.vercel.app"],  # In production, specify allowed origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include routers
# app.include_router(projects_router, prefix="/api/v1/projects", tags=["projects"])
# app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
# app.include_router(issues_router, prefix="/api/v1/issues", tags=["issues"])
# app.include_router(dashboard_router, prefix="/api/v1", tags=["dashboard"])

# @app.get("/", tags=["root"])
# @app.head("/", tags=["root"])
# def read_root():
#     return {
#         "message": "Project Management System API", 
#         "version": "1.0.0",
#         "docs": "/docs",
#         "health": "OK"
#     }

# @app.get("/health", tags=["health"])
# def health_check():
#     return {"status": "healthy"}

# print("ENV SETTINGS:", settings.dict())

# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.environ.get("PORT", 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port)

