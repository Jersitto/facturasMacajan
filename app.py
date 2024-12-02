from flask import Flask, request, render_template, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

class FacturaPDF(FPDF):
    def header(self):
        self.set_font("Arial", size=12, style="B")
        self.cell(0, 10, "Cable Macaján - Factura de Servicio", align="C", ln=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", size=8)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

def generar_factura(nombre_cliente, valor_servicio):
    pdf = FacturaPDF()
    pdf.add_page()

   
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Cable Macaján", ln=True)
    pdf.cell(0, 10, "Macaján, Sucre", ln=True)
    pdf.cell(0, 10, "Teléfono: 3114206515", ln=True)

    pdf.ln(10)

   
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Datos del Cliente:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Nombre: {nombre_cliente}", ln=True)
    pdf.cell(0, 10, f"Servicio contratado: Cable TV", ln=True)
    pdf.cell(0, 10, f"Valor del servicio: ${valor_servicio:,.0f} Pesos", ln=True)
    pdf.ln(10)

    # Total a pagar
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Resumen:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Total a pagar: ${valor_servicio:,.0f} Pesos", ln=True)
    pdf.cell(0, 10, f"Cuenta de pago NEQUI: 3114206515", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", style="B",size=12)
    pdf.cell(0, 10, "Codigo QR de la cuenta NEQUI:", ln=True)
    pdf.image("templates/imagen.jpg", x=10, y=pdf.get_y(), w=50) 
    pdf.ln(40)  

    
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, "Gracias por confiar en Cable Macaján. Para cualquier consulta, contáctenos a nuestro soporte.")

    
    nombre_archivo = f"Factura_{nombre_cliente.replace(' ', '_')}.pdf"
    pdf.output(nombre_archivo)
    return nombre_archivo


# Rutas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    nombre_cliente = request.form['nombre_cliente']
    valor_servicio = float(request.form['valor_servicio'])
    archivo_pdf = generar_factura(nombre_cliente, valor_servicio)
    return send_file(archivo_pdf, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
