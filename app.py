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

# ✅ Serve static files properly
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.post("/process-data/")
async def process_data(
    param1: str = Form(...), param2: int = Form(...), param3: float = Form(...)
):
    # Processing simulation
    processed_data = [
        {
            "Input1": param1,
            "Input2": param2,
            "Input3": param3,
            "Result": param2 * param3,
        }
    ]

    df = pd.DataFrame(processed_data)

    # Save to Excel
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "output.xlsx")
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename="ProcessedData.xlsx")
