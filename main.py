from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import tempfile
import os
from weasyprint import HTML
import logging
import traceback

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="HTML to PDF Micro SaaS", description="Convert HTML to PDF using FastAPI")

class PDFRequest(BaseModel):
    title: str
    html: str

@app.post("/html2pdf")
async def convert_html_to_pdf(request: PDFRequest):
    """
    Convert HTML string to PDF
    """
    html = request.html
    title = request.title
    logging.info(f"Received HTML length: {len(html)}")
    try:
        # Generate PDF directly from HTML string
        logging.info("Generating PDF...")
        pdf_bytes = HTML(string=html).write_pdf()

        # Write bytes to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            temp_pdf.write(pdf_bytes)
            pdf_path = temp_pdf.name

        logging.info(f"PDF generated at {pdf_path}")

        # Return PDF file
        filename = f"{title}.pdf" if title else "output.pdf"
        return FileResponse(pdf_path, media_type='application/pdf', filename=filename)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error converting HTML to PDF: {str(e)}")

@app.get("/")
async def root():
    return {"message": "HTML to PDF Micro SaaS API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)