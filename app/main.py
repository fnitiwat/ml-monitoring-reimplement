from fastapi import FastAPI

from monitoring import instrumentator


app = FastAPI()
instrumentator.instrument(app).expose(app)


@app.get("/")
async def root():
    return "helloworld"