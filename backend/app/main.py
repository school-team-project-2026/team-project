from fastapi import FastAPI

from app.routers.interest_items import router as interest_items_router

app = FastAPI(title="Team Project API")

app.include_router(interest_items_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
