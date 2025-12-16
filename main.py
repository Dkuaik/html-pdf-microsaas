from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import tempfile
import os
from weasyprint import HTML, CSS
import logging
import traceback
from services.results_analisis import analyze_results

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

@app.post("/html2pdf-long")
async def convert_html_to_long_pdf(request: PDFRequest):
    """
    Convert HTML string to a long PDF with variable height based on content
    """
    html = request.html
    title = request.title
    logging.info(f"Received HTML length: {len(html)} for long PDF")
    try:
        html_doc = HTML(string=html)
        document = html_doc.render()
        if document.pages:
            width = document.pages[0].width
            total_height = sum(page.height for page in document.pages)
            stylesheet = CSS(string=f'@page {{ size: {width}pt {total_height}pt; }}')
            pdf_bytes = html_doc.write_pdf(stylesheets=[stylesheet])
        else:
            # Fallback if no pages
            pdf_bytes = html_doc.write_pdf()

        # Write bytes to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
            temp_pdf.write(pdf_bytes)
            pdf_path = temp_pdf.name

        logging.info(f"Long PDF generated at {pdf_path}")

        # Return PDF file
        filename = f"{title}_long.pdf" if title else "output_long.pdf"
        return FileResponse(pdf_path, media_type='application/pdf', filename=filename)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error converting HTML to long PDF: {str(e)}")

@app.post("/analyze-results")
async def analyze_results_endpoint(
    formato: UploadFile = File(...),
    resultados: UploadFile = File(...)
):
    """
    Analyze student results and generate reports
    """
    try:
        formato_bytes = await formato.read()
        resultados_bytes = await resultados.read()

        student_hashmap, performance_report = analyze_results(formato_bytes, resultados_bytes)

        return JSONResponse({
            "student_hashmap": student_hashmap,
            "performance_report": performance_report
        })
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error analyzing results: {str(e)}")

@app.get("/")
async def root():
    return {"message": "HTML to PDF Micro SaaS API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)