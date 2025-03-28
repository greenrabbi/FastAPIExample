from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory=".", html=True), name="static")


@app.post("/process-data/")
async def process_data(
    param1: str = Form(...), param2: int = Form(...), param3: float = Form(...)
):
    processed_data = []
    for i in range(1, 101):
        row = {
            "Input1": param1,
            "Input2": param2,
            "Input3": param3,
            "Result": (i * param2 * param3),
        }
        processed_data.append(row)

    df = pd.DataFrame(processed_data)

    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "output.xlsx")
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename="ProcessedData.xlsx")


@app.get("/")
async def root():
    return {"message": "Python Processing App is running!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
