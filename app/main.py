from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import stocks

app = FastAPI(title="predictUs API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev ke liye sab allow, production mein specific URL dalna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router)

@app.get("/")
def read_root():
    return {"message": " congraturations! predictUs API is running 🚀"}


#uvicorn app.main:app --reload --port 8000 