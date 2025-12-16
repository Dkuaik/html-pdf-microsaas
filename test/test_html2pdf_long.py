import requests
import os
from pathlib import Path

# Base URL of the API
BASE_URL = "http://localhost:8000"

# Data directory for storing PDFs
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Test HTML content (same as before)
HTML_CONTENT = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documento Simple para PDF</title>
    <style>
        /* Estilos básicos para impresión */
        body {
            font-family: Arial, sans-serif;
            margin: 2cm; /* Márgenes para simular una página impresa */
            color: #333;
        }
        h1 {
            color: #0056b3;
            border-bottom: 2px solid #0056b3;
            padding-bottom: 10px;
        }
        p {
            line-height: 1.6;
        }
        .seccion {
            margin-top: 20px;
            padding: 10px;
            border-left: 5px solid #ccc;
        }

        /* Oculta elementos que no quieres en el PDF, si los tuvieras */
        @media print {
            .no-imprimir {
                display: none;
            }
        }
    </style>
</head>
<body>

    <header>
        <h1>Título Principal del Documento</h1>
    </header>

    <div class="seccion">
        <h2>Subtítulo o Sección 1</h2>
        <p>Este es el contenido de la primera sección. Puedes incluir texto, listas o cualquier otro elemento HTML básico. La idea es que sea legible y simple para la conversión a PDF.</p>
        <ul>
            <li>Elemento de lista uno</li>
            <li>Elemento de lista dos</li>
            <li>Elemento de lista tres</li>
        </ul>
    </div>

    <div class="seccion">
        <h2>Sección 2: Conclusión</h2>
        <p>Asegúrate de que tu navegador tenga la opción "Imprimir a PDF" o "Guardar como PDF". Esto es lo que realizará la conversión. Mantener el CSS simple ayuda a una mejor compatibilidad con la impresión.</p>
        <p>Fecha de creación: <span id="fecha-actual"></span></p>
    </div>

    <script>
        // Opcional: añade la fecha actual con JavaScript
        document.getElementById('fecha-actual').textContent = new Date().toLocaleDateString('es-ES');
    </script>

</body>
</html>"""


def test_html2pdf_long():
    """Test the HTML to long PDF conversion endpoint"""
    print("Testing HTML to long PDF conversion...")

    # Send POST request with title and HTML in request body
    response = requests.post(
        f"{BASE_URL}/html2pdf-long",
        json={"title": "test_output_long", "html": HTML_CONTENT}
    )

    if response.status_code == 200:
        # Save the PDF to data directory
        output_path = DATA_DIR / "test_output_long.pdf"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✓ Long PDF saved successfully to: {output_path}")
        print(f"  File size: {len(response.content)} bytes")
        return True
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"  Response: {response.text}")
        return False


if __name__ == "__main__":
    test_html2pdf_long()