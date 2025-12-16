import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from services.results_analisis import analyze_results

# Read files
with open('test/data/Formato_Preguntas.xlsx', 'rb') as f:
    formato_bytes = f.read()

with open('test/data/Resultados prueba ecoems 2025.xlsx', 'rb') as f:
    resultados_bytes = f.read()

student_hashmap, performance_report = analyze_results(formato_bytes, resultados_bytes)

print("Student Hashmap:")
print(json.dumps(student_hashmap, indent=4, ensure_ascii=False))

print("\nPerformance Report:")
print(json.dumps(performance_report, indent=4, ensure_ascii=False))