import json
from datetime import datetime, date
import textwrap
import streamlit as st

# ────────────────────────────────────────────────────────────────────────────────
# Seiteneinstellungen
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ausbildung · Kaufmann/-frau für Büromanagement",
    page_icon="🗂️",
    layout="wide",
)
st.title("🗂️ Ausbildung · Kaufmann/-frau für Büromanagement")
st.caption("Hinweis: Keine personenbezogenen oder internen Unternehmensdaten eingeben.")

# ────────────────────────────────────────────────────────────────────────────────
# Hilfsfunktionen
# ────────────────────────────────────────────────────────────────────────────────
def combo_field(label: str, suggestions: list[str], key_text: str, key_multiselect: str):
    """
    Kombiniert Vorschlagsliste (Mehrfachauswahl) mit eigener Freitexteingabe (eine pro Zeile).
    Gibt eine zusammengeführte Liste zurück (ohne Leerzeilen).
    """
    st.markdown(f"**{label}**")
    chosen = st.multiselect(
        f"{label} · Vorschläge (Mehrfachauswahl möglich)",
        options=suggestions,
        key=key_multiselect
    )
    free = st.text_area(
        f"{label} · Eigene Eingaben (eine pro Zeile)",
        key=key_text,
        height=100,
        placeholder="Eigene Punkte je Zeile hinzufügen …"
    )
    own = [x.strip("- ").strip() for x in free.splitlines() if x.strip()]
    return [*chosen, *own]

def bullet(lines: list[str]) -> str:
    return "\n".join([f"- {x}" for x in lines if x.strip()])

def section(title: str) -> str:
    return f"\n## {title}\n"

def dl_button(label: str, txt: str, filename: str):
    st.download_button(
        label=label,
        data=txt,
        file_name=filename,
        mime="text/plain"
    )

# ────────────────────────────────────────────────────────────────────────────────
# Stammdaten & Modus
# ────────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Einstellungen")
    modus = st.radio(
        "Modus",
        options=["Ausbildung (Büromanagement)", "Berufsvorbereitung"],
        index=0
    )
    heute = date.today()
    meta_kw = st.text_input("Kalenderwoche / Zeitraum", value=f"KW {heute.isocalendar()[1]} · {heute:%d.%m.%Y}")
    meta_jahr = st.selectbox("Ausbildungsjahr", ["1. AJ", "2. AJ", "3. AJ", "—"], index=0)
    meta_betrieb = st.text_input("Ausbildungsbetrieb / Abteilung", value="")
    meta_ausbilder = st.text_input("Ausbilder:in", value="")
    meta_azubi = st.text_input("Azubi (Kürzel/Initialen)", value="")
    st.markdown("---")
    st.markdown("**Export**: Unten kannst du Berichtsheft/Arbeitsauftrag/Prüfungsübungen generieren und als TXT herunterladen.")

# ────────────────────────────────────────────────────────────────────────────────
# Vorschlagslisten
# ────────────────────────────────────────────────────────────────────────────────
LERNFELDER_BUERO = [
    "LF 1 Die eigene Rolle im Betrieb mitgestalten",
    "LF 2 Büroprozesse und Arbeitsorganisation",
    "LF 3 Informationsmanagement & Kommunikation",
    "LF 4 Auftragsbearbeitung & Beschaffung",
    "LF 5 Kundenorientierte Auftragsabwicklung",
    "LF 6 Personalwirtschaftliche Aufgaben unterstützen",
    "LF 7 Kaufmännische Steuerung & Kontrolle",
    "LF 8 Marketing & Veranstaltungsorganisation",
    "LF 9 Projekt- und Prozessmanagement",
    "LF 10 Qualitätsmanagement & Dokumentation",
]

TAETIGKEITEN = [
    "Posteingang/-ausgang bearbeiten",
    "Telefonate & Terminmanagement",
    "E-Mail-Korrespondenz",
    "Protokolle/Notizen erstellen",
    "Bestellungen/Angebote vergleichen",
    "Rechnungsprüfung/Vorkontierung",
    "Ablage/Dokumentenmanagement",
    "Datenpflege (CRM/Listen)",
    "Vorbereitung Besprechungen/Events",
    "Reisekosten vorbereiten/prüfen",
]

TOOLS = [
    "MS Word", "MS Excel", "MS PowerPoint", "MS Outlook", "MS Teams",
    "SharePoint/OneDrive", "SAP/ERP (allgemein)", "DATEV (allgemein)", "CRM-Tool (allgemein)",
]

KOMPETENZEN = [
    "Kommunikation (intern/extern)",
    "Selbstorganisation & Priorisierung",
    "Sorgfalt/Genauigkeit",
    "Kaufmännisches Grundverständnis",
    "Digitale Zusammenarbeit",
    "Dokumentation & Nachvollziehbarkeit",
    "Service- & Kundenorientierung",
]

NACHWEISE = [
    "Dokumente/Dateien (Ablage/Versionierung)",
    "E-Mails/Protokolle",
    "Checklisten/Formulare",
    "Belege/Rechnungen",
    "Auswertungen/Listen",
    "Screenshots (ohne personenbezogene Daten)",
]

PRUEFUNGSUEBUNGEN = [
    "Kaufmännische Fälle (Ein-/Ausgangsrechnungen, Skonto, Rabatt)",
    "Korrespondenz (Anfrage/Angebot/Reklamation)",
    "Termin- & Ressourcenplanung (Outlook/Teams)",
    "Informationsrecherche & -aufbereitung",
    "Kurzprojekt Organisation (Meeting/Event)",
]

BERUFSSCHULE = [
    "Deutsch/Wirtschaftskommunikation",
    "WiSo (Wirtschaft/Soziales)",
    "Rechnungswesen/Controlling",
    "Informationsverarbeitung (Text/Tabellen)",
    "Projektarbeit",
]

# ────────────────────────────────────────────────────────────────────────────────
# Eingaben: linke/rechte Spalte
# ────────────────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    if modus == "Ausbildung (Büromanagement)":
        lf = combo_field("Lernfelder/Schwerpunkte", LERNFELDER_BUERO, "lf_text", "lf_multi")
    else:
        lf = combo_field("Schwerpunkte (Berufsvorbereitung)", [
            "Grundlagen Bürokommunikation",
            "Arbeitsorganisation & Zeitmanagement",
            "Digitale Grundkompetenzen (Office/Cloud)",
            "Kaufmännische Basisprozesse",
            "Bewerbung/Profil/ProfilPass",
        ], "bv_text", "bv_multi")

    taetigkeiten = combo_field("Tätigkeiten/Aufgaben", TAETIGKEITEN, "task_text", "task_multi")
    tools = combo_field("Werkzeuge/Tools", TOOLS, "tools_text", "tools_multi")

with col2:
    kompetenzen = combo_field("Kompetenzen/Ziele", KOMPETENZEN, "skills_text", "skills_multi")
    nachweise = combo_field("Nachweise/Dokumente", NACHWEISE, "proof_text", "proof_multi")
    schule = combo_field("Berufsschule/Verknüpfung", BERUFSSCHULE, "school_text", "school_multi")

st.markdown("---")

# ────────────────────────────────────────────────────────────────────────────────
# Generatoren
# ────────────────────────────────────────────────────────────────────────────────
def build_header():
    hdr = [
        f"**Modus:** {modus}",
        f"**Zeitraum:** {meta_kw}",
        f"**Ausbildungsjahr:** {meta_jahr}",
        f"**Betrieb/Abteilung:** {meta_betrieb or '—'}",
        f"**Ausbilder:in:** {meta_ausbilder or '—'}",
        f"**Azubi:** {meta_azubi or '—'}",
    ]
    return "\n".join(hdr)

def gen_berichtsheft():
    parts = []
    parts.append(build_header())
    parts.append(section("Schwerpunkte"))
    parts.append(bullet(lf))
    parts.append(section("Tätigkeiten"))
    parts.append(bullet(taetigkeiten))
    parts.append(section("Eingesetzte Werkzeuge/Tools"))
    parts.append(bullet(tools))
    parts.append(section("Erworbene Kompetenzen"))
    parts.append(bullet(kompetenzen))
    parts.append(section("Nachweise/Belege"))
    parts.append(bullet(nachweise))
    if schule:
        parts.append(section("Verknüpfung zur Berufsschule"))
        parts.append(bullet(schule))
    return "\n".join(parts).strip()

def gen_arbeitsauftrag():
    prompt = f"""Rolle: Ausbilder:in
Auftrag: Detaillierten Arbeitsauftrag formulieren.

Rahmen:
- Modus: {modus}
- Zeitraum: {meta_kw}
- Ausbildungsjahr: {meta_jahr}
- Betrieb/Abteilung: {meta_betrieb or '—'}

Schwerpunkte:
{bullet(lf)}

Tätigkeiten:
{bullet(taetigkeiten)}

Werkzeuge:
{bullet(tools)}

Kompetenzen (Ziele):
{bullet(kompetenzen)}

Nachweise:
{bullet(nachweise)}

Bitte gib aus:
1) Ziel(e) in beobachtbaren Kriterien
2) Schritt-für-Schritt-Ablauf (mit Zeitindikationen, wo sinnvoll)
3) Qualitätskriterien & typische Fehler
4) Übergabe/Abnahme (inkl. Checkliste kurz)
5) Reflexionsfragen für den Azubi
Klar, prägnant, handlungsorientiert, max. 500 Wörter.
"""
    return textwrap.dedent(prompt).strip()

def gen_pruefung():
    parts = []
    parts.append("Rolle: Prüfer:in (Übungsaufgaben)")
    parts.append(f"Modus: {modus} · Zeitraum: {meta_kw} · AJ: {meta_jahr}")
    parts.append(section("Aufgabenpool (wähle 2–3)"))
    parts.append(bullet(PRUEFUNGSUEBUNGEN))
    parts.append(section("Konte
