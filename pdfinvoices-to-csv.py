# Import libraries
import pdfplumber
import re
import csv


# General_var
invoices_file = 'Facturas.pdf'
num_factura_pattern = r'\d{3}\/2022'
fecha_factura_pattern = r'\d{1,2}\/\d{2}\/22'
invoices = []

for i in range(64):
    with pdfplumber.open(invoices_file) as pdf:
        page = pdf.pages[i]
        text = page.extract_text()

    for row in text.split("\n"):
        num_factura = re.search(num_factura_pattern, row)
        fecha_factura = re.search(fecha_factura_pattern, row)

        if num_factura:
            fc = num_factura.group()

        if fecha_factura:
            fecha = fecha_factura.group()

        if row.startswith("Concepto"):
            concepto = row

        if row.startswith("Base Imponible"):
            base_imponible = row.split()[2]
            currency = row.split()[3]

        if row.startswith("Total"):
            total = row.split()[1]
            currency = row.split()[2]

    comp_dict = [fc, fecha, concepto, base_imponible + currency, total + currency]
    invoices.append(comp_dict)

with open('invoices_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    for row in invoices:
        writer.writerow(row)

print('Todo exportado')
