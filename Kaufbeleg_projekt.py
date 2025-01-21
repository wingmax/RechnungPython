from reportlab.lib.pagesizes import letter,A4
from reportlab.pdfgen import canvas

class Kauf_Rechnung:
    def __init__(self,Datum,Anschrift,Ware,Kaufsort,Zahlungsmethode,Zahlungsbetrag):
        self.datum = Datum
        self.anschrift = Anschrift 
        self.ware = Ware 
        self.zahlung = Zahlungsmethode
        self.betrag = Zahlungsbetrag
        self.kaufsort = Kaufsort 

    def erstelle_pdf(self, dateiname):
        # Erstelle ein PDF-Dokument
        pdf = canvas.Canvas(dateiname, pagesize=A4) #600*840
        pdf.setTitle("Kauf Rechnung")

        # Kopfzeile
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(230, 750, "Kauf Rechnung")
        pdf.line(215,745,385,745)

        # Inhalt hinzufügen
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 700, f"Kaufsdatum: {self.datum}")
        pdf.drawString(50, 680, f"Ware: {self.ware}")
        Nachname = self.anschrift["Nachname"]
        Vorname  = self.anschrift["Vorname"]
        Straße   = self.anschrift["Straße"]
        Straßenummer = self.anschrift["Straße No"]
        PLZ          = self.anschrift["PLZ"]
        ort          = self.anschrift["Ort"]
        land         = self.anschrift["Land"]

        pdf.drawString(50, 660, "Gekauft von: "+Nachname+", "+Vorname)
        pdf.drawString(120,640,Straße+" "+str(Straßenummer))
        pdf.drawString(120,620,str(PLZ)+" "+ort+" "+land)
        pdf.drawString(50, 600, f"Zahlungsmethode: {self.zahlung}")
        pdf.drawString(50, 580, f"Zahlungsbetrag: {self.betrag} €")
        
        # Fußzeile
        pdf.line(50,160,550,160)
        pdf.setFont("Helvetica-Oblique", 10)
        pdf.drawString(50, 150, "Wingman Electronics 2024")
        pdf.drawString(50, 130, "Diese Beleg wurde durch das Automatisierunsprogramm der Wingman Electronics erstellt.")


        # PDF speichern
        pdf.save()
        print(f"PDF {dateiname} wurde erstellt.")


anschrift_keys = ["Vorname","Nachname","Straße","Straße No","PLZ","Ort","Land"]

Vorname = "Abuziddin"
Nachname = "Killibacak"
Straße = "Hansstraße"
Straßenummer = 12
PLZ = 34346
Ort = "Yozgat"
Land = "DE"
Datum = "23.11.2024"
Ware = "5 Stück DELL 130W Netzteil"
Zahlungsmethode = "PayPal"
Kaufsort = "Kleinanzeige"
Zahlungsbetrag = 39.5

Anschrift_values = [Vorname,Nachname, Straße, Straßenummer, PLZ, Ort,Land]
Anschrift = dict(zip(anschrift_keys,Anschrift_values))

kauf1 = Kauf_Rechnung(Datum,Anschrift,Ware,Kaufsort,Zahlungsmethode,Zahlungsbetrag)
kauf1.erstelle_pdf("Rechnung2.pdf")