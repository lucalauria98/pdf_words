# PDF Wort-Extraktor

Ein Python-Programm zum Extrahieren aller Wörter aus PDF-Dateien und Speichern in CSV-Format.

## Features

- ✅ Extrahiert alle Wörter aus PDF-Dateien
- ✅ Wandelt alle Wörter in Kleinbuchstaben um
- ✅ Entfernt Duplikate
- ✅ Optional: Zeigt Anzahl der Vorkommen jedes Wortes
- ✅ Unterstützt große PDFs (200+ Seiten)
- ✅ Schnell und effizient mit PyMuPDF

## Installation

1. Python 3.7 oder höher erforderlich
2. Bibliotheken installieren:

```bash
pip install -r requirements.txt
```

Oder nur PyMuPDF (empfohlen):
```bash
pip install pymupdf
```

## Verwendung

### Basis-Verwendung (nur eindeutige Wörter)
```bash
python pdf_wort_extractor.py dokument.pdf
```

### Mit Anzahl der Vorkommen
```bash
python pdf_wort_extractor.py dokument.pdf --counts
```

### Eigene Ausgabe-Datei
```bash
python pdf_wort_extractor.py dokument.pdf -o ausgabe.csv --counts
```

## Ausgabe

Die CSV-Datei wird standardmäßig als `<pdf_name>_woerter.csv` oder `<pdf_name>_woerter_mit_anzahl.csv` gespeichert.

**Format ohne Anzahl:**
```csv
Wort
apfel
banane
computer
...
```

**Format mit Anzahl:**
```csv
Wort;Anzahl
der;1523
die;1201
und;987
...
```

## Grenzen und Bottlenecks

### ✅ Was funktioniert gut:
- **200 Seiten**: Kein Problem, sollte in 1-5 Minuten verarbeitet werden
- **500 Seiten**: Funktioniert, benötigt mehr Zeit (5-15 Minuten)
- **Text-PDFs**: Sehr schnell

### ⚠️ Mögliche Probleme:
- **Sehr große PDFs (>1000 Seiten)**: 
  - Kann viel RAM benötigen (abhängig von Textmenge)
  - Verarbeitungszeit kann 30+ Minuten betragen
  
- **PDFs mit vielen Bildern**: 
  - Wenn Text aus Bildern extrahiert werden soll, benötigt man OCR
  - Aktuelles Programm extrahiert nur Text-Layer
  
- **Komplexe PDFs** (Formulare, Tabellen):
  - Text-Reihenfolge kann beeinträchtigt sein
  - pdfplumber ist hier präziser, aber langsamer

### Performance-Optimierungen:
1. **PyMuPDF verwenden** (3-5x schneller als pdfplumber)
2. **RAM**: Je mehr RAM, desto größere PDFs können verarbeitet werden
3. **SSD**: Schnellere Festplatte beschleunigt das Laden

### Geschätzter Speicherbedarf:
- **200 Seiten PDF**: ~50-200 MB RAM
- **1000 Seiten PDF**: ~250 MB - 1 GB RAM
- **CSV-Ausgabe**: Meist sehr klein (< 1 MB für typische Dokumente)

## Beispiel

```bash
# PDF mit 200 Seiten verarbeiten
python pdf_wort_extractor.py grosse_dokumentation.pdf --counts

# Ausgabe:
# PDF geöffnet: 200 Seiten gefunden
# Verarbeite Seite 10/200...
# Verarbeite Seite 20/200...
# ...
# Insgesamt 45230 Wörter extrahiert
# Eindeutige Wörter gefunden: 8234
# 
# Ergebnis gespeichert in: grosse_dokumentation_woerter_mit_anzahl.csv
# ✓ Fertig!
```

## Fehlerbehebung

**"Keine PDF-Bibliothek gefunden"**
- Lösung: `pip install pymupdf` ausführen

**"PDF-Datei nicht gefunden"**
- Prüfen Sie den Pfad zur PDF-Datei
- Verwenden Sie absolute Pfade wenn nötig

**Zu langsam**
- Stellen Sie sicher, dass PyMuPDF installiert ist (nicht pdfplumber)
- Prüfen Sie, ob die PDF viele Bilder enthält (kann langsam sein)

