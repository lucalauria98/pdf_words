#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Wort-Extraktor
Extrahiert alle Wörter aus einer PDF-Datei und speichert sie in einer CSV-Datei.
- Alle Wörter werden in Kleinbuchstaben umgewandelt
- Duplikate werden entfernt (oder mit Anzahl gespeichert)
- Unterstützt große PDFs (200+ Seiten)
"""

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import pymupdf  # PyMuPDF (fitz) - sehr schnell und effizient
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

if not HAS_PYMUPDF and not HAS_PDFPLUMBER:
    print("FEHLER: Keine PDF-Bibliothek gefunden!")
    print("Bitte installieren Sie eine der folgenden Bibliotheken:")
    print("  pip install pymupdf  (empfohlen - sehr schnell)")
    print("  pip install pdfplumber")
    sys.exit(1)


def extract_words_with_pymupdf(pdf_path):
    """
    Extrahiert Wörter aus PDF mit PyMuPDF (sehr schnell, gut für große PDFs).
    """
    words = []
    doc = pymupdf.open(pdf_path)
    
    print(f"PDF geöffnet: {len(doc)} Seiten gefunden")
    
    for page_num, page in enumerate(doc, start=1):
        if page_num % 10 == 0:
            print(f"Verarbeite Seite {page_num}/{len(doc)}...")
        
        text = page.get_text()
        # Wörter extrahieren: nur Buchstaben (inkl. Umlaute und Akzente)
        page_words = re.findall(r'\b[^\W\d_]+\b', text, re.UNICODE)
        words.extend(page_words)
    
    doc.close()
    return words


def extract_words_with_pdfplumber(pdf_path):
    """
    Extrahiert Wörter aus PDF mit pdfplumber (präziser, aber langsamer).
    """
    words = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"PDF geöffnet: {total_pages} Seiten gefunden")
        
        for page_num, page in enumerate(pdf.pages, start=1):
            if page_num % 10 == 0:
                print(f"Verarbeite Seite {page_num}/{total_pages}...")
            
            text = page.extract_text()
            if text:
                # Wörter extrahieren: nur Buchstaben (inkl. Umlaute und Akzente)
                page_words = re.findall(r'\b[^\W\d_]+\b', text, re.UNICODE)
                words.extend(page_words)
    
    return words


def normalize_word(word):
    """
    Normalisiert ein Wort: in Kleinbuchstaben umwandeln.
    """
    return word.lower()


def process_pdf(pdf_path, include_counts=False, output_path=None):
    """
    Verarbeitet eine PDF-Datei und extrahiert alle eindeutigen Wörter.
    
    Args:
        pdf_path: Pfad zur PDF-Datei
        include_counts: Wenn True, wird die Anzahl der Vorkommen gespeichert
        output_path: Pfad zur Ausgabe-CSV (optional)
    
    Returns:
        Liste von Tupeln (wort, anzahl) oder Liste von Wörtern
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF-Datei nicht gefunden: {pdf_path}")
    
    print(f"Starte Extraktion aus: {pdf_path.name}")
    
    # Wörter extrahieren (PyMuPDF bevorzugt, da schneller)
    if HAS_PYMUPDF:
        print("Verwende PyMuPDF (schnell)...")
        words = extract_words_with_pymupdf(pdf_path)
    else:
        print("Verwende pdfplumber...")
        words = extract_words_with_pdfplumber(pdf_path)
    
    print(f"Insgesamt {len(words)} Wörter extrahiert")
    
    # Wörter normalisieren (Kleinbuchstaben)
    normalized_words = [normalize_word(word) for word in words]
    
    if include_counts:
        # Zähle Vorkommen jedes Wortes
        word_counts = Counter(normalized_words)
        # Sortiere nach Häufigkeit (absteigend), dann alphabetisch
        result = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
        print(f"Eindeutige Wörter gefunden: {len(result)}")
        return result
    else:
        # Nur eindeutige Wörter, alphabetisch sortiert
        unique_words = sorted(set(normalized_words))
        print(f"Eindeutige Wörter gefunden: {len(unique_words)}")
        return unique_words


def save_to_csv(data, output_path, include_counts=False):
    """
    Speichert die extrahierten Wörter in eine CSV-Datei.
    
    Args:
        data: Liste von Wörtern oder Liste von Tupeln (wort, anzahl)
        output_path: Pfad zur Ausgabe-CSV
        include_counts: Ob Anzahl gespeichert werden soll
    """
    output_path = Path(output_path)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        if include_counts:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['Wort', 'Anzahl'])
            writer.writerows(data)
        else:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['Wort'])
            for word in data:
                writer.writerow([word])
    
    print(f"\nErgebnis gespeichert in: {output_path}")
    print(f"Dateigröße: {output_path.stat().st_size / 1024:.2f} KB")


def main():
    parser = argparse.ArgumentParser(
        description='Extrahiert alle Wörter aus einer PDF-Datei und speichert sie in CSV.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python pdf_wort_extractor.py dokument.pdf
  python pdf_wort_extractor.py dokument.pdf --counts
  python pdf_wort_extractor.py dokument.pdf -o ausgabe.csv --counts

Grenzen und Bottlenecks:
  - Speicher: Sehr große PDFs (>500 Seiten) können viel RAM benötigen
  - Geschwindigkeit: Abhängig von PDF-Komplexität (Text vs. Bilder)
  - PyMuPDF ist ca. 3-5x schneller als pdfplumber
  - 200 Seiten sollten kein Problem sein (ca. 1-5 Minuten je nach Komplexität)
        """
    )
    
    parser.add_argument(
        'pdf_file',
        help='Pfad zur PDF-Datei'
    )
    parser.add_argument(
        '-o', '--output',
        help='Ausgabe-CSV-Datei (Standard: <pdf_name>_woerter.csv)'
    )
    parser.add_argument(
        '--counts',
        action='store_true',
        help='Zeige Anzahl der Vorkommen jedes Wortes'
    )
    
    args = parser.parse_args()
    
    try:
        # Standard-Ausgabedatei wenn nicht angegeben
        if args.output:
            output_path = Path(args.output)
        else:
            pdf_path = Path(args.pdf_file)
            suffix = '_woerter_mit_anzahl' if args.counts else '_woerter'
            output_path = pdf_path.parent / f"{pdf_path.stem}{suffix}.csv"
        
        # PDF verarbeiten
        result = process_pdf(args.pdf_file, include_counts=args.counts)
        
        # In CSV speichern
        save_to_csv(result, output_path, include_counts=args.counts)
        
        print("\n✓ Fertig!")
        
    except FileNotFoundError as e:
        print(f"FEHLER: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"FEHLER: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

