from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.interest_items import router as interest_items_router

app = FastAPI(title="Team Project API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interest_items_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
