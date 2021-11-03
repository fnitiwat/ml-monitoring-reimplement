import numpy as np
from fastapi import FastAPI

from monitoring import instrumentator


app = FastAPI()
instrumentator.instrument(app).expose(app)


@app.get("/")
async def root():
    return "helloworld"


@app.get("/predict")
async def predict():
    """
    mock classifier predict animal 
    """
    class_names = ["dog", "cat", "lion", "zebra"]
    pred_prob = np.random.rand(len(class_names)).tolist()
    pred_class_prob = np.max(pred_prob).item()
    pred_class = class_names[np.argmax(pred_prob)]
    
    prediction = {
        "pred_class": pred_class,
        "pred_class_prob": pred_class_prob,
        "pred_prob": pred_prob,
    }

    return prediction