
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hello():
    return "hello"

print("app created")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
