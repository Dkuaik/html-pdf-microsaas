from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import tempfile
import os
from weasyprint import HTML

app = FastAPI(title="HTML to PDF Micro SaaS", description="Convert HTML to PDF using FastAPI")

@app.post("/html2pdf")
async def convert_html_to_pdf(html: str):
    """
    Convert HTML string to PDF
    """
    try:
        # Create a temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_html:
            temp_html.write(html)
            temp_html_path = temp_html.name

        # Generate PDF
        pdf_path = temp_html_path.replace('.html', '.pdf')
        HTML(temp_html_path).write_pdf(pdf_path)

        # Clean up HTML file
        os.unlink(temp_html_path)

        # Return PDF file
        return FileResponse(pdf_path, media_type='application/pdf', filename='converted.pdf')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting HTML to PDF: {str(e)}")

@app.get("/")
async def root():
    return {"message": "HTML to PDF Micro SaaS API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)