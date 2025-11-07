#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vereinfachte Version - Interaktive Nutzung
Fragt nach PDF-Datei und speichert Ergebnisse automatisch.
"""

import sys
from pathlib import Path

# Hauptprogramm importieren
from pdf_wort_extractor import process_pdf, save_to_csv

def main():
    print("=" * 60)
    print("PDF Wort-Extraktor - Einfache Version")
    print("=" * 60)
    print()
    
    # PDF-Datei abfragen
    pdf_input = input("Pfad zur PDF-Datei: ").strip().strip('"')
    
    if not pdf_input:
        print("Keine Datei angegeben. Programm wird beendet.")
        sys.exit(1)
    
    pdf_path = Path(pdf_input)
    if not pdf_path.exists():
        print(f"FEHLER: Datei nicht gefunden: {pdf_path}")
        sys.exit(1)
    
    # Option: Mit Anzahl?
    print()
    counts_input = input("Anzahl der Vorkommen speichern? (j/n): ").strip().lower()
    include_counts = counts_input in ['j', 'ja', 'y', 'yes']
    
    # Verarbeitung
    print()
    print("Starte Verarbeitung...")
    print("-" * 60)
    
    try:
        # PDF verarbeiten
        result = process_pdf(pdf_path, include_counts=include_counts)
        
        # Ausgabe-Datei bestimmen
        suffix = '_woerter_mit_anzahl' if include_counts else '_woerter'
        output_path = pdf_path.parent / f"{pdf_path.stem}{suffix}.csv"
        
        # Speichern
        save_to_csv(result, output_path, include_counts=include_counts)
        
        print()
        print("=" * 60)
        print("✓ Erfolgreich abgeschlossen!")
        print(f"Ergebnis: {output_path}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nFEHLER: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

