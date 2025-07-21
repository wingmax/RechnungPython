#import readCSV as CSV
import os
import pandas as pd
from reportlab.lib.pagesizes import letter,A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


fileExcel = pd.read_excel("Verkaeufen.xlsx", engine='openpyxl')
fileExcel.to_csv("convertedCSVFile.csv", index=False,encoding="utf-8-sig")

path = "convertedCSVFile.csv"
fileCSV = pd.read_csv(path,encoding="utf-8-sig")

columns = fileCSV.columns
nData = fileCSV.shape[0]
for i in range(nData):
    [Rechnungsnummer,
                     Product,
                       Zusatzinfo,
                       Anzahl,
                       Einheit,
                       Preis,
                       Kaufsdatum,
                       Lieferungsdatum,
                       Rechnungsdatum,                       
                       Vorname,
                       Nachname,
                       Straße,
                       Hausnummer,
                       PLZ,
                       Ort] = fileCSV.iloc[i,:]
    
    dateiname = "Rechnung_"+str(Rechnungsnummer)+".pdf"
    pdf = canvas.Canvas(dateiname, pagesize=A4) #600*840
    pdf.setTitle("Verkaufsrechnung")
    pdfmetrics.registerFont(TTFont("Calibri", "Calibri.ttf"))
    pdfmetrics.registerFont(TTFont("CalibriBold", "Calibrib.ttf"))

    ##################### Kopfzeile #####################
    # Linksspalte: (LOGO, Mein Anschrift, Rechnungsanschrift)
    # Rechtsspalte: (Nummer, Datum usw.)

    # Linke Spalte LOGO+Mein Anschrift
    current_directory = os.path.dirname(os.path.abspath(__file__))
    logo_name = "Logo2.png" # The Logo File
    logoFilePath = os.path.join(current_directory, logo_name)
    pdf.drawImage(logoFilePath, x=55, y=725, width=140, height=45)
    pdf.setFont("Calibri", 7)
    meinAnschrift = "Wingman Electronics | Jakob-Sigle-Str 49 | 86842 Türkheim"
    x0 = 58
    y0 = 720
    pdf.drawString(x0, y0, meinAnschrift)

    # Linke Spalte Anschrift der Kunde
    pdf.setFont("CalibriBold", 10)
    pdf.drawString(x0, y0-15, Vorname+"  "+Nachname)
    pdf.setFont("Calibri", 8)
    pdf.drawString(x0, y0-25, Straße+" "+str(Hausnummer))
    pdf.drawString(x0, y0-33, str(PLZ)+" "+Ort)

    # Rechte Spalte- Die Name der Parametern:
    fontSize = 9
    pdf.setFont("CalibriBold", fontSize)
    x0 = 370
    y0 = 705
    pdf.drawString(x0, y0, "Rechnungsnummer:")
    pdf.drawString(x0, y0-fontSize, "Verkaufsdatum:")
    pdf.drawString(x0, y0-2*fontSize, "Lieferdatum:")
    pdf.drawString(x0, y0-3*fontSize, "Rechnungsdatum:")
    pdf.drawString(x0, y0-4*fontSize, "Ihr Ansprechpartner:")

    # Rechte Spalte- Die Parametern selbst:
    fontSize = 9
    pdf.setFont("Calibri", fontSize)
    x0 = 480
    y0 = 705
    pdf.drawString(x0, y0, str(Rechnungsnummer))
    pdf.drawString(x0, y0-fontSize, Kaufsdatum)
    pdf.drawString(x0, y0-2*fontSize, Lieferungsdatum)
    pdf.drawString(x0, y0-3*fontSize, Rechnungsdatum)
    pdf.drawString(x0, y0-4*fontSize, "Ahmet Akkoyunlu")   


      ##################### MITTEL #####################
    x0 = 58
    y0 = 500
    fontSize = 12
    space = 1
    pdf.setFont("Calibri", fontSize)
    bodyText1 = "           Vielen Dank für Ihren Antrag. Wie vereinbart stelle ich Ihnen folgende Produkte/Leistungen"
    bodyText2 = "und Lieferungen in Rechnung."
    pdf.drawString(x0, y0, bodyText1)
    pdf.drawString(x0, y0-space*fontSize, bodyText2)

    ###### TABLE ###
    products = []
    additionalInfos = []
    amounts = []
    unit =[]
    prices = []

    products.append(Product) 
    additionalInfos.append(Zusatzinfo) 
    amounts.append(Anzahl)
    unit.append(Einheit)
    prices.append(Preis)

    numberOfProducts = 1
    k=i+1
    
    total = float(str(Anzahl)) * float(str(Preis)) # Rechnungsbetrag

    if fileCSV.shape[0]!=i+1: # if not the last element of CSV is been processing
        while True:
            if fileCSV.iloc[k,0]!=fileCSV.iloc[i,0]:
                total = int(str(amounts)) * int(str(prices))
                break
            else:
                columnIndex_Product = fileCSV.columns.get_loc("Product")
                columnIndex_ZusatzInfo = fileCSV.columns.get_loc("Zusatzinfo")
                columnIndex_Anzahl = fileCSV.columns.get_loc("Anzahl")
                columnIndex_Einheit = fileCSV.columns.get_loc("Einheit")
                columnIndex_Preis = fileCSV.columns.get_loc("Preis")
                
                products.append(fileCSV.iloc[k,columnIndex_Product])
                additionalInfos.append(fileCSV.iloc[k,columnIndex_ZusatzInfo])
                amounts.append(fileCSV.iloc[k,columnIndex_Anzahl])
                unit.append(fileCSV.iloc[k,columnIndex_Einheit])
                prices.append(fileCSV.iloc[k,columnIndex_Preis])
            
                total =+ int(str(amounts(-1))) * int(str(prices(-1)))
                numberOfProducts = +1
                k= +1

    pdf.saveState()

    tableHeader = ["Pos."]
    tableHeader.append("Bezeichnung")
    tableHeader.append("ZusatzInfo")
    tableHeader.append("Menge")
    tableHeader.append("Einheit")
    tableHeader.append("E-Preis")
    
    pos = range(1,numberOfProducts+1)

    nRows = len(products)+1
    nColumns = len(tableHeader)

    data = [[0 for _ in range(nColumns)] for _ in range(nRows+1)]
    data [0][:] = tableHeader
    #index = numberOfProducts-1
    for i in range(numberOfProducts):
        data [i+1][:] = [pos[i], products[i],
                       additionalInfos[i],
                       amounts[i],
                        unit[i],
                        prices[i]]
        if i ==numberOfProducts-1:
            for j in range(4):
                data [i+2][j] = []
            data [i+2][4] = "Rechnungsbetrag"
            data [i+2][5] = str(total)+ " €"

    
    # Table styling
    colWidths=[10, 50, 50,10,20,100,100]
    table = Table(data, )  # Adjust column widths
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        #('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        #('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    table.setStyle(TableStyle([
    ('LINEABOVE', (0, -1), (-1, -1), 0, colors.white),  # No top border for last row
    ('LINEBELOW', (0, -1), (-1, -1), 0, colors.white),  # No bottom border for last row
    ('GRID', (0, -1), (-1, -1), 0, colors.white),
    ]))

    # Step 3: Place the table below the content
    x = 50  # Starting x-coordinate
    y = 400  # Starting y-coordinate (adjust based on your content's height)
    table.wrapOn(pdf, 0, 0)  # Necessary for sizing
    table.drawOn(pdf, x, y)  # Draw the table at the specified position

    # Save the final PDF
    pdf.restoreState()

    # Write Rechnungsbetrag:
    # fontSize = 14
    # pdf.setFont("CalibriBold", fontSize)
    # pdf.drawString(100, 300, "Rechnungsbetrag:")
    # pdf.drawString(130, 400, str(total)+ "€")

    # # Inhalt hinzufügen
    # pdf.setFont("Helvetica", 12)
    # pdf.drawString(50, 700, f"Kaufsdatum: {self.datum}")
    # pdf.drawString(50, 680, f"Ware: {self.ware}")
    # Nachname = self.anschrift["Nachname"]
    # Vorname  = self.anschrift["Vorname"]
    # Straße   = self.anschrift["Straße"]
    # Straßenummer = self.anschrift["Straße No"]
    # PLZ          = self.anschrift["PLZ"]
    # ort          = self.anschrift["Ort"]
    # land         = self.anschrift["Land"]

    # pdf.drawString(50, 660, "Gekauft von: "+Nachname+", "+Vorname)
    # pdf.drawString(120,640,Straße+" "+str(Straßenummer))
    # pdf.drawString(120,620,str(PLZ)+" "+ort+" "+land)
    # pdf.drawString(50, 600, f"Zahlungsmethode: {self.zahlung}")
    # pdf.drawString(50, 580, f"Zahlungsbetrag: {self.betrag} €")
    

    # Ohne Umsatzsteuer
    pdf.drawString(50, 245, "Rechnungsstellung erfolgt ohne Ausweis der Umsatzsteuer nach §19 UStG.")
    


    # Fußzeile
    fontSize = 12
    pdf.setFont("Calibri", fontSize)
    pdf.drawString(50, 185, "Mit freundlichen Grüßen")
    pdf.drawString(50, 170, "Ahmet Akkoyunlu")
    pdf.line(50,160,550,160)
    pdf.setFont("Calibri", 10)
    pdf.drawString(50, 150, "Wingman Electronics 2025")
    pdf.drawString(50, 130, "Ahmet Akkoyunlu | Finanzamt Memmingen-Mindelheim | Steuernummer: 138/200/32068")
    # pdf.drawString(50, 120, "USt-IdNr. | DE420650410")
    #pdf.drawString(50, 120, "Diese Beleg wurde durch das Automatisierunsprogramm der Wingman Electronics erstellt.")


    # PDF speichern
    pdf.save()
    print(f"PDF {dateiname} wurde erstellt.")





# import chardet

# with open("Verkaeufen.csv", "rb") as f:
#     result = chardet.detect(f.read())
#     print(result['encoding'])