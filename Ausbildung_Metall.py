# promptbuilder_metal.py
# Streamlit-App: Promptbuilder für Auszubildende im Metallhandwerk (inkl. Berufsvorbereitung)
# Hinweis: Keine personenbezogenen oder internen Unternehmensdaten eingeben.

import json
from datetime import datetime
import textwrap
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Promptbuilder · Metallhandwerk (Azubis/Berufsvorbereitung)", page_icon="🛠️", layout="wide")
st.title("🛠️ Promptbuilder für Auszubildende im Metallhandwerk")
st.caption("Hinweis: **Keine personenbezogenen Daten** oder **internen Unternehmensdaten** eingeben. Dieser Builder erzeugt strukturierte Prompts für KI-Hilfen im Ausbildungsalltag und in der Berufsvorbereitung.")

# ---------------------- Presets (erweitert) ----------------------
AUSBILDSBERUFE = [
    "Industriemechaniker:in", "Zerspanungsmechaniker:in", "Konstruktionsmechaniker:in",
    "Werkzeugmechaniker:in", "Metallbauer:in Konstruktionstechnik",
    "Feinwerkmechaniker:in", "Mechatroniker:in",
    "Fachkraft für Metalltechnik", "Maschinen- und Anlagenführer:in",
    "Technische:r Produktdesigner:in (Maschinenbau)"
]

BILDUNGSGANG = ["Duale Ausbildung", "Berufsvorbereitung (BvB/BF/BBW)"]

VERFAHREN = [
    # Grundfertigkeiten
    "Anreißen/Körnen", "Feilen", "Sägen (Hand/maschinell)", "Bohren", "Reiben", "Gewindeschneiden (Hand)",
    # Umformen/Trennen/Verbinden
    "Biegen", "Nieten", "Hartlöten", "Plasmaschneiden", "Autogenschneiden",
    # Zerspanung/CNC
    "Drehen", "Fräsen", "Schleifen", "CNC (Sinumerik)", "CNC (Heidenhain)", "CAM",
    # Schweißen/Metallbau
    "Schweißen MAG", "Schweißen WIG/TIG", "Punktschweißen",
    # Sonstiges
    "Montage", "Instandhaltung", "Messen/Prüfen"
]

MASCHINEN = [
    "Konventionelle Drehmaschine", "CNC-Drehmaschine", "Konventionelle Fräsmaschine",
    "CNC-Fräsmaschine", "Säulenbohrmaschine", "Bandsäge",
    "Schweißgerät MAG", "Schweißgerät WIG/TIG", "Punktschweißgerät",
    "Rohrbieger", "Plasmaschneider", "Autogenbrenner", "Flachschleifmaschine"
]

WERKSTOFFE = [
    "C15", "C45E", "42CrMo4", "S235JR", "S355",
    "1.4301 (V2A)", "1.4404 (V4A)", "9SMn28 (Automatenstahl)",
    "Al99,5", "AlCuMg1", "AlMg3", "Cu-ETP (Kupfer)", "CuZn (Messing)", "GG25"
]

MESSMITTEL = [
    "Messschieber 0–150 mm", "Tiefenmaß Messschieber", "Mikrometer 0–25 mm",
    "Höhenreißer + Anreißplatte", "Innenmessgerät", "Winkelmesser",
    "Rauheitsmessgerät", "Fühlerlehre", "Grenzlehrdorn", "Parallelendmaße"
]

NORMEN = [
    "DIN ISO 2768 (Allg. Toleranzen)", "DIN EN ISO 1101 (Form-/Lage)", "DIN EN ISO 1302 (Oberflächen)",
    "DIN 13 (Metrische Gewinde)", "DIN EN ISO 5817 (Schweißnahtbewertung)",
    "DIN EN ISO 9606-1 (Schweißerprüfung)", "EN ISO 4063 (Schweißprozess-Nr.)",
    "DGUV Vorschrift 1 (Sicherheit)", "Betriebs-/Maschinenanweisung"
]

DIDAKTIK = [
    "4-Stufen-Methode", "Leittextmethode", "Projektarbeit", "Lernaufgabe",
    "Peer-Learning", "Lernfeldorientiert", "Handlungsorientierte Unterweisung"
]

OUTPUTFORMATE = [
    "Schritt-für-Schritt-Anleitung", "Arbeitsplan/Rüstplan Tabelle", "Checkliste Sicherheit",
    "CNC-Beispiel (kommentiert)", "Quiz (10 Fragen, gemischt)", "Fehlerkatalog (Ursache→Maßnahme)",
    "Berichtsheft-Eintrag", "Bewertungsschema (Rubrik)", "Leittext/Lernaufgabe",
    "Kompetenzraster (Kurz)", "Unterweisungsblatt (4-Stufen)", "Mini-GBU (Gefährdungsbeurteilung)"
]

AUFGABENTYP = [
    "Arbeitsauftrag erstellen", "Grundfertigkeit üben (Feilen/Anreißen/Gewinde)",
    "CNC-Programm unterstützen", "Schweißaufgabe planen", "Werkstück fertigen",
    "Fehlersuche durchführen", "Qualitätsprüfung planen", "Wartung planen",
    "PAL-Prüfungsaufgabe trainieren", "Mini-Projekt (Berufsvorbereitung)"
]

SPRACHE = ["Deutsch", "Englisch"]
TON = ["klar & knapp", "instruktiv & geduldig", "prüfungsnah & formal", "kollegial & motivierend"]

# ---------------------- Utility ----------------------

def multiselect_with_free_text(label: str, options: list[str], key_prefix: str, height: int = 80):
    st.markdown(f"**{label}**")
    sel = st.multiselect(
        f"{label} · Vorschläge (Mehrfachauswahl möglich)", options=options, key=f"{key_prefix}_ms"
    )
    txt = st.text_area(
        f"{label} · Eigene Eingaben (eine pro Zeile)", key=f"{key_prefix}_txt", height=height
    )
    own = [x.strip("- ").strip() for x in txt.splitlines() if x.strip()]
    return [*sel, *own]

# ---------------------- Layout ----------------------
colL, colR = st.columns([1, 1])

with colL:
    st.subheader("1) Rahmen & Rolle")
    bildungsgang = st.selectbox("Bildungsgang", BILDUNGSGANG, key="bildungsgang")
    beruf = st.selectbox("Ausbildungsberuf / Zielberuf", AUSBILDSBERUFE, key="beruf")
    ausbildungsjahr = st.selectbox("Ausbildungsjahr (falls zutreffend)", ["1", "2", "3", "4"], key="jahr")
    lernort = st.selectbox("Lernort", ["Betrieb", "ÜBA", "Berufsschule", "Prüfungsvorbereitung", "Berufsvorbereitung"], key="lernort")
    aufgabentyp = st.selectbox("Aufgabentyp", AUFGABENTYP, key="aufgabentyp")
    outputformat = st.multiselect("Gewünschtes Output-Format", OUTPUTFORMATE, key="output")
    sprache = st.selectbox("Sprache", SPRACHE, key="sprache")
    ton = st.selectbox("Ton & Stil", TON, key="ton")

    st.subheader("2) Technik-Setup")
    verfahren = multiselect_with_free_text("Verfahren/Arbeitsgänge", VERFAHREN, "verfahren")
    maschinen = multiselect_with_free_text("Maschinen/Steuerungen", MASCHINEN, "maschinen")
    werkstoffe = multiselect_with_free_text("Werkstoffe", WERKSTOFFE, "werkstoffe")

with colR:
    st.subheader("3) Qualität & Sicherheit")
    normen = multiselect_with_free_text("Normen/Regeln", NORMEN, "normen")
    messmittel = multiselect_with_free_text("Messmittel/Prüfkriterien", MESSMITTEL, "mess")
    toleranzen = st.text_input("Maß-/Form-/Lagetoleranzen (z. B. Ø20 H7, Ra 1,6, Ⓜ⌀0,02)", key="toleranzen")
    sicherheit = multiselect_with_free_text("Sicherheitsaspekte (PSA, Gefahren, Unterweisung)", [
        "PSA: Schutzbrille, Handschuhe", "Gefährdungsbeurteilung", "Sperrbereiche", "Brandgefahr",
        "Späne/Quetschstellen", "Schweißrauchabsaugung"
    ], "safety")

    st.subheader("4) Didaktik & Zeit")
    didaktik = st.multiselect("Didaktischer Ansatz", DIDAKTIK, key="didaktik")
    lernziel = st.text_area("Lernziel(e) (beobachtbar, SMART)", height=80, key="lernziel")
    zeit = st.number_input("Geplante Zeit (Minuten)", min_value=5, max_value=480, step=5, key="zeit")

st.subheader("5) Materialien & Kontext")
materialien = st.text_area("Material-/Werkzeugliste (eine Position pro Zeile)", height=80, key="materialien")
zeichnung = st.text_input("Link/Referenz: Zeichnung/Skizze/Foto (optional)", key="zeichnung")
kontext = st.text_area("Kontext/Startlage (z. B. Werkstückbeschreibung, Ist-Stand, typische Fehler)", height=100, key="kontext")

# ---------------------- Prompt zusammensetzen ----------------------
if st.button("🔧 Prompt erzeugen", use_container_width=True):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "bildungsgang": st.session_state.get('bildungsgang', ''),
        "rolle": f"Du bist Ausbilder:in/Coach im Metallbereich für {st.session_state.get('beruf','')} (AJ {st.session_state.get('jahr','-')}).",
        "ziel": "Unterstütze die/den Lernende:n mit klaren, sicheren, normgerechten und prüfungsnahen Anweisungen (Niveau an Bildungsgang anpassen).",
        "lernort": st.session_state.get('lernort',''),
        "aufgabentyp": st.session_state.get('aufgabentyp',''),
        "sprache": st.session_state.get('sprache','Deutsch'),
        "ton": st.session_state.get('ton','instruktiv & geduldig'),
        "didaktik": st.session_state.get('didaktik',[]),
        "lernziel": st.session_state.get('lernziel','').strip(),
        "verfahren": verfahren,
        "maschinen": maschinen,
        "werkstoffe": werkstoffe,
        "normen": normen,
        "messmittel": messmittel,
        "toleranzen": st.session_state.get('toleranzen','').strip(),
        "sicherheit": sicherheit,
        "zeit_min": st.session_state.get('zeit',60),
        "materialliste": [x.strip() for x in st.session_state.get('materialien','').splitlines() if x.strip()],
        "zeichnung_ref": st.session_state.get('zeichnung','').strip(),
        "kontext": st.session_state.get('kontext','').strip(),
        "gewünschter_output": st.session_state.get('output',[]),
        "meta": {"erstellt": now, "builder": "Promptbuilder Metall (Azubis/Berufsvorbereitung)"}
    }

    prompt_text = textwrap.dedent(f"""Rolle & Ziel:\n{payload['rolle']} Bildungsgang: {payload['bildungsgang']}. Sprich {('mich' if payload['sprache']=='Deutsch' else 'me')} im Stil: {payload['ton']}. Arbeite {('auf Deutsch' if payload['sprache']=='Deutsch' else 'in English')}. Ziel: {payload['ziel']}\n\nKontext:\n- Lernort: {payload['lernort']}\n- Aufgabentyp: {payload['aufgabentyp']}\n- Ausbildungsjahr: {st.session_state.get('jahr','-')}\n- Verfahren/Arbeitsgänge: {', '.join(verfahren) or '-'}\n- Maschinen/Steuerungen: {', '.join(maschinen) or '-'}\n- Werkstoffe: {', '.join(werkstoffe) or '-'}\n- Normen/Regeln: {', '.join(normen) or '-'}\n- Messmittel/Prüfkriterien: {', '.join(messmittel) or '-'}\n- Toleranzen: {payload['toleranzen'] or '-'}\n- Sicherheitsaspekte: {', '.join(sicherheit) or '-'}\n- Zeitrahmen: {payload['zeit_min']} Minuten\n- Materialien/Werkzeuge: {', '.join(payload['materialliste']) or '-'}\n- Zeichnung/Referenz: {payload['zeichnung_ref'] or '-'}\n- Startlage/typische Fehler: {payload['kontext'] or '-'}\n- Didaktik: {', '.join(payload['didaktik']) or '-'}\n- Lernziel(e): {payload['lernziel'] or '-'}\n\nAufgaben an die KI:\n1) Erstelle die Ausgabe im/als: {', '.join(payload['gewünschter_output']) or '—'}.\n2) Passe Komplexität und Fachsprache an den Bildungsgang an (Berufsvorbereitung → mehr Bilder/Beispiele, einfache Sprache; Duale Ausbildung → fachlich präzise, normnah).\n3) Nenne zuerst Sicherheits-Hinweise (DGUV-konform), dann Material/Setup, dann Vorgehen.\n4) Verwende Nummerierung und, wo sinnvoll, Tabellen.\n5) Mache Maße, Toleranzen, Werkstoff und Messmittel konkret; verweise auf Normstellen (z. B. DIN ISO 2768, ISO 1302) ohne zu erfinden.\n6) Gib typische Fehlerbilder + Ursachen + Gegenmaßnahmen an (Fehlerkatalog).\n7) Schließe mit Reflexionsfragen; in der Berufsvorbereitung zusätzlich 1–2 Alltagsbezüge.\n8) Wenn Informationen fehlen, frage gezielt nach (max. 3 Rückfragen).\n\nAusgabeformat (Beispielstruktur):\n- **Sicherheit**\n- **Material & Rüstung** (Tabelle)\n- **Arbeitsablauf** (Schritte 1..n)\n- **Qualitätsprüfung** (Toleranzen/Messmittel)\n- **Fehlerkatalog**\n- **Reflexion** (3–5 Fragen)""").strip()

    st.success("Prompt erzeugt. Unten kopieren oder als Datei speichern.")
    st.text_area("Generierter Prompt", prompt_text, height=320)
    st.download_button(label="⬇️ Prompt als .txt speichern", data=prompt_text, file_name=f"prompt_metall_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", mime="text/plain", use_container_width=True)

    safe = prompt_text.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '&quot;').replace("'", "&#39;")
    components.html(textwrap.dedent(f"""
<div style='display:flex;gap:8px;align-items:center;margin-top:8px;'>
  <button id='copyBtn' style='padding:8px 12px;border-radius:10px;border:1px solid #ddd;cursor:pointer;'>📋 In Zwischenablage kopieren</button>
  <span id='copyInfo' style='opacity:0.8'></span>
</div>
<script>
  const text = "{safe}";
  const btn = document.getElementById('copyBtn');
  const info = document.getElementById('copyInfo');
  btn.addEventListener('click', async () => {{
    try {{ await navigator.clipboard.writeText(text); info.textContent = 'Kopiert!'; }}
    catch (e) {{ info.textContent = 'Kopieren nicht erlaubt. Markiere den Text und kopiere manuell (Ctrl/Cmd+C).'; }}
  }});
</script>
"""), height=60)

    with st.expander("Maschinenlesbare Prompt-Metadaten (JSON)"):
        st.code(json.dumps(payload, ensure_ascii=False, indent=2))

# ---------------------- Footer ----------------------
st.markdown(
    """---
**Tipps:**
- Passe die Sprachebene an: Berufsvorbereitung → einfache Sprache, Schrittbilder/Icons; Ausbildung → fachlich präzise, Normbezug.
- Nenne bei Gewinden *Nenndurchmesser, Steigung, Kernloch* (z. B. M6 × 1, Kernloch 5,0 mm, **DIN 13**).
- Für Schweißen: Qualität nach **ISO 5817**, Prozessnummern nach **ISO 4063**.
- Sicherheit geht vor: DGUV-Hinweise zuerst.
"""
)
