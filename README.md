# BeratungsMatch - KI-gestützte Beratungsfirmen-Suche

Eine Webplattform, die Unternehmen hilft, die perfekte Beratungsfirma für ihre Bedürfnisse mithilfe von KI-Technologie zu finden.

## Funktionen

- Einfache formularbasierte Oberfläche für Unternehmen
- KI-gestützte Suche mit Perplexity API (inkl. Internetsuche)
- Fokus auf Münchner Beratungsfirmen
- Echtzeitempfehlungen mit Erklärungen

## Installation

1. Perplexity API Key einrichten:
   - Besuchen Sie [perplexity.ai](https://www.perplexity.ai) und erstellen Sie ein Konto
   - Generieren Sie einen API-Schlüssel
   - Kopieren Sie den API-Schlüssel in die `.env` Datei

2. Python-Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Anwendung starten:
```bash
python app.py
```

4. Öffnen Sie http://localhost:5000 im Browser

## Funktionsweise

1. Benutzer füllen ein Formular aus mit:
   - Geschäftlichen Anforderungen
   - Branche
   - Unternehmensgröße
   - Bevorzugter Standort (standardmäßig München)

2. Die KI analysiert die Anforderungen und sucht im Internet nach den am besten passenden Beratungsfirmen

3. Ergebnisse zeigen:
   - Firmenname
   - Website
   - Erklärung, warum die Firma gut passt

## Technologie-Stack

- Backend: Python/Flask
- Frontend: HTML/JavaScript mit Tailwind CSS
- KI: Perplexity API mit Online-Suche
- Umgebung: python-dotenv für Konfiguration

## Vorteile der Perplexity API

- Kostenlose API-Credits für neue Nutzer
- Integrierte Internetsuche für aktuelle Ergebnisse
- Speziell für Informationssuche optimiert
- Strukturierte JSON-Antworten