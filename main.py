from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI on Render!"}

@app.post("/echo")
async def echo_message(request: Request):
    data = await request.json()
    return {"received": data}
