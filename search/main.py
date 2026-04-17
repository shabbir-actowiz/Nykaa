from fastapi import FastAPI
from parser import *
app= FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to the Nykaa Search API!"}

@app.get("/search/{keyword}")
def search(keyword):
    return get_first_suggestion(keyword)

