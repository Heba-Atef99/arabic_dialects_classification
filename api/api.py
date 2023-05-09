import pandas as pd
from fastapi import FastAPI
import joblib
from scipy.sparse import hstack
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

filename = 'char_word_model'
model = joblib.load(filename)
cv_char = joblib.load(filename+'_cv_char')
cv_word = joblib.load(filename+'_cv_word')


class Payload(BaseModel):
    text: str = ""


@app.get("/")
async def root():
    return {"message": "Welcome to the NLP Project, where we predict your dialect!"}

@app.post("/predict")
async def predict(payload: Payload):
    text = payload.text
    data = {'text': [text]}
    x_test = pd.DataFrame.from_dict(data)['text']
    x_test_char = cv_char.transform(x_test)
    x_test_word = cv_word.transform(x_test)
    x_test_full = hstack((x_test_char, x_test_word))
    prediction = model.predict(x_test_full)[0]
    return {"prediction": prediction}