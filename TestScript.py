from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
import tempfile
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory=".", html=True), name="static")

# Optional: Add CORS if you want to connect from a web portal
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process-data/")
async def process_data(
    param1: str = Form(...),
    param2: int = Form(...),
    param3: float = Form(...)
):
    """
    Process data and return Excel file.
    """

    # Simulate heavy processing
    processed_data = []
    for i in range(1, 101):
        row = {
            "Input1": param1,
            "Input2": param2,
            "Input3": param3,
            "Result": (i * param2 * param3)
        }
        processed_data.append(row)

    df = pd.DataFrame(processed_data)

    # Save to temporary Excel file
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "output.xlsx")
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename="ProcessedData.xlsx")


@app.get("/")
async def root():
    return {"message": "Python Processing App is running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
