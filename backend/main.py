from fastapi import FastAPI


app = FastAPI(title="Smart Waste Management Portal API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}