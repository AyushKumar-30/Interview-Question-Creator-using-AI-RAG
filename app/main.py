# Import FastAPI core modules
from fastapi import FastAPI, Request, UploadFile, File

# Used to send back HTML responses (webpages)
from fastapi.responses import HTMLResponse
from pypdf import PdfReader

# Helps render HTML templates like index.html
from fastapi.templating import Jinja2Templates

# Utility modules
import shutil  # Used to copy uploaded file
import os      # Used to create folders like /uploads

# Create a FastAPI app instance
app = FastAPI()

# Tell FastAPI where to find the HTML templates
templates = Jinja2Templates(directory="app/templates")

# Define a folder where uploaded files will be saved
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

# This route shows the homepage with the upload form
@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    # It renders the 'index.html' page with the form
    return templates.TemplateResponse("index.html", {"request": request})

# This route is triggered when a user uploads a PDF
@app.post("/upload", response_class=HTMLResponse)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    # Save uploaded file to /uploads
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # ✅ Step: Extract text from the saved PDF
    reader = PdfReader(file_location)
    all_text = ""
    for page in reader.pages:
        all_text += page.extract_text()

    # (Optional) Save extracted text to a .txt file or print
    print(f"\nExtracted {len(all_text)} characters from {file.filename}\n")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "msg": f"✅ Uploaded and extracted {len(all_text)} characters from '{file.filename}'"
    })
