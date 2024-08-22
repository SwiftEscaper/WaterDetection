from fastapi import FastAPI, Request
from pydantic import BaseModel

# HPC에서 돌릴 서버 코드 (이 코드만 HPC에서)
# uvicorn server:app --reload --host=0.0.0.0 --port=10000

app = FastAPI()

class SensorData(BaseModel):
    accident_type: int


@app.post("/water")
async def receive_data(data: SensorData):

    print(f"Received data: {data}")
    
    return {"status": "success", "received_data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
