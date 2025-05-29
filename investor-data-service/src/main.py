from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import investors, commitments

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow all origins (not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET"],  # Allows only GET method
    allow_headers=["*"],  # Allows all headers
)

app.include_router(investors.router)
app.include_router(commitments.router)
        
@app.get("/", status_code=200)
def healthcheck():
    return 'healthcheck'
