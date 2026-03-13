from fastapi import FastAPI

app = FastAPI()

# creating endpoint
@app.get("/")