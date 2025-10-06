# promptbuilder_metal.py
# Streamlit-App: Promptbuilder für Auszubildende im Metallhandwerk
# Hinweis: Keine personenbezogenen oder internen Unternehmensdaten eingeben.

import json
from datetime import datetime
import textwrap
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Promptbuilder · Metallhandwerk (Azubis)", page_icon="🛠️", layout="wide")
st.title("🛠️ Promptbuilder für Auszubildende im Metallhandwerk")
st.caption("Hinweis: **Keine personenbezogenen Daten** oder **internen Unternehmensdaten** eingeben. Dieser Builder erzeugt strukturierte Prompts für KI-Hilfen im Ausbildungsalltag.")

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

# ---------------------- Presets ----------------------
AUSBILDSBERUFE = [
    "Industriemechaniker:in", "Zerspanungsmechaniker:in", "Konstruktionsmechaniker:in",
    "Werkzeugmechaniker:in", "Metallbauer:in Fachr. Konstruktionstechnik",
    "Feinwerkmechaniker:in", "Mechatroniker:in"
]

VERFAHREN = [
    "Drehen", "Fräsen", "Bohren", "Schleifen", "Sägen", "Biegen", "Schweißen MAG", "Schweißen WIG/TIG",
    "CNC (Sinumerik)", "CNC (Heidenhain)", "CAM", "3D-Druck (Metall)", "Montage", "Instandhaltung"
]

MASCHINEN = [
    "Konventionelle Drehmaschine", "CNC-Drehmaschine", "Konventionelle Fräsmaschine",
    "CNC-Fräsmaschine", "Schweißgerät MAG", "Schweißgerät WIG/TIG", "Bandsäge", "Bohrmaschine Ständer",
    "Flachschleifmaschine"
]

WERKSTOFFE = [
    "C45E", "S235JR", "S355", "1.4301 (V2A)", "1.4404 (V4A)", "AlMg3", "GG25", "42CrMo4"
]

MESSMITTEL = [
    "Messschieber 0–150 mm", "Mikrometer 0–25 mm", "Höhenreißer", "Innenmessgerät", "Rauheitsmessgerät",
    "Winkelmesser", "Grenzlehrdorn", "Parallelendmaße"
]

NORMEN = [
    "DIN ISO 2768 (Toleranzen)", "DIN EN ISO 1101 (Form-/Lagetoleranzen)", "DIN EN ISO 1302 (Oberflächenangaben)",
    "DIN EN ISO 9606-1 (Schweißen – Prüfungen)", "DGUV Vorschrift 1 (Sicherheit)", "Betriebsanweisung Maschine"
]

DIDAKTIK = ["4-Stufen-Methode", "Leittextmethode", "Projektarbeit", "Lernaufgabe", "Peer-Learning"]

OUTPUTFORMATE = [
    "Schritt-für-Schritt-Anleitung", "Arbeitsplan/Rüstplan Tabelle", "Checkliste Sicherheit",
    "CNC-Beispiel (kommentiert)", "Quiz (10 Fragen, gemischt)", "Fehlerkatalog (Ursache→Maßnahme)",
    "Berichtsheft-Eintrag", "Bewertungsschema (Rubrik)"
]

AUFGABENTYP = [
    "Arbeitsauftrag erstellen", "CNC-Programm unterstützen", "Schweißaufgabe planen",
    "Werkstück fertigen", "Fehlersuche durchführen", "Qualitätsprüfung planen", "Wartung planen"
]

SPRACHE = ["Deutsch", "Englisch"]
TON = ["klar & knapp", "instruktiv & geduldig", "prüfungsnah & formal", "kollegial & motivierend"]

# ---------------------- Layout ----------------------
colL, colR = st.columns([1, 1])

with colL:
    st.subheader("1) Rahmen & Rolle")
    beruf = st.selectbox("Ausbildungsberuf", AUSBILDSBERUFE)
    ausbildungsjahr = st.selectbox("Ausbildungsjahr", ["1", "2", "3", "4"])
    lernort = st.selectbox("Lernort", ["Betrieb", "ÜBA", "Berufsschule", "Prüfungsvorbereitung"])
    aufgabentyp = st.selectbox("Aufgabentyp", AUFGABENTYP)
    outputformat = st.multiselect("Gewünschtes Output-Format", OUTPUTFORMATE, default=["Schritt-für-Schritt-Anleitung"])
    sprache = st.selectbox("Sprache", SPRACHE, index=0)
    ton = st.selectbox("Ton & Stil", TON, index=1)

    st.subheader("2) Technik-Setup")
    verfahren = multiselect_with_free_text("Verfahren/Arbeitsgänge", VERFAHREN, "verfahren")
    maschinen = multiselect_with_free_text("Maschinen/Steuerungen", MASCHINEN, "maschinen")
    werkstoffe = multiselect_with_free_text("Werkstoffe", WERKSTOFFE, "werkstoffe")

with colR:
    st.subheader("3) Qualität & Sicherheit")
    normen = multiselect_with_free_text("Normen/Regeln", NORMEN, "normen")
    messmittel = multiselect_with_free_text("Messmittel/Prüfkriterien", MESSMITTEL, "mess")
    toleranzen = st.text_input("Maß-/Form-/Lagetoleranzen (z. B. Ø20 H7, Ra 1,6, Ⓜ⌀0,02)")
    sicherheit = multiselect_with_free_text("Sicherheitsaspekte (PSA, Gefahren, Unterweisung)", [
        "PSA: Schutzbrille, Handschuhe", "Gefährdungsbeurteilung", "Sperrbereiche", "Brandgefahr",
        "Späne/Quetschstellen", "Schweißrauchabsaugung"
    ], "safety")

    st.subheader("4) Didaktik & Zeit")
    didaktik = st.multiselect("Didaktischer Ansatz", DIDAKTIK, default=["4-Stufen-Methode"])
    lernziel = st.text_area("Lernziel(e) (beobachtbar, SMART)", height=80)
    zeit = st.number_input("Geplante Zeit (Minuten)", min_value=5, max_value=480, value=60, step=5)

st.subheader("5) Materialien & Kontext")
materialien = st.text_area("Material-/Werkzeugliste (eine Position pro Zeile)", height=80)
zeichnung = st.text_input("Link/Referenz: Zeichnung/Skizze/Foto (optional)")
kontext = st.text_area("Kontext/Startlage (z. B. Werkstückbeschreibung, Ist-Stand, typische Fehler)", height=100)

# ---------------------- Prompt zusammensetzen ----------------------
if st.button("🔧 Prompt erzeugen", use_container_width=True):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    payload = {
        "rolle": f"Du bist Ausbilder:in/Coach im Metallhandwerk für {beruf} (AJ {ausbildungsjahr}).",
        "ziel": "Unterstütze die/den Auszubildende:n mit klaren, sicheren, normgerechten und prüfungsnahen Anweisungen.",
        "lernort": lernort,
        "aufgabentyp": aufgabentyp,
        "sprache": sprache,
        "ton": ton,
        "didaktik": didaktik,
        "lernziel": lernziel.strip(),
        "verfahren": verfahren,
        "maschinen": maschinen,
        "werkstoffe": werkstoffe,
        "normen": normen,
        "messmittel": messmittel,
        "toleranzen": toleranzen.strip(),
        "sicherheit": sicherheit,
        "zeit_min": zeit,
        "materialliste": [x.strip() for x in materialien.splitlines() if x.strip()],
        "zeichnung_ref": zeichnung.strip(),
        "kontext": kontext.strip(),
        "gewünschter_output": outputformat,
        "meta": {"erstellt": now, "builder": "Promptbuilder Metall (Azubis)"}
    }

    prompt_text = f"""
Rolle & Ziel:\n{payload['rolle']} Sprich {('mich' if sprache=='Deutsch' else 'me')} im Stil: {ton}. Arbeite {('auf Deutsch' if sprache=='Deutsch' else 'in English')}. Ziel: {payload['ziel']}

Kontext:\n- Lernort: {lernort}\n- Aufgabentyp: {aufgabentyp}\n- Ausbildungsjahr: {ausbildungsjahr}\n- Verfahren/Arbeitsgänge: {', '.join(verfahren) or '-'}\n- Maschinen/Steuerungen: {', '.join(maschinen) or '-'}\n- Werkstoffe: {', '.join(werkstoffe) or '-'}\n- Normen/Regeln: {', '.join(normen) or '-'}\n- Messmittel/Prüfkriterien: {', '.join(messmittel) or '-'}\n- Toleranzen: {payload['toleranzen'] or '-'}\n- Sicherheitsaspekte: {', '.join(sicherheit) or '-'}\n- Zeitrahmen: {zeit} Minuten\n- Materialien/Werkzeuge: {', '.join(payload['materialliste']) or '-'}\n- Zeichnung/Referenz: {payload['zeichnung_ref'] or '-'}\n- Startlage/typische Fehler: {payload['kontext'] or '-'}\n- Didaktik: {', '.join(didaktik) or '-'}\n- Lernziel(e): {payload['lernziel'] or '-'}

Aufgaben an die KI:\n1) Erstelle die Ausgabe im/als: {', '.join(outputformat)}.\n2) Nenne zuerst Sicherheits-Hinweise (DGUV-konform), dann Material/Setup, dann Vorgehen.\n3) Verwende Nummerierung und, wo sinnvoll, Tabellen.\n4) Mache Maße, Toleranzen, Werkstoff und Messmittel konkret; verweise auf Normstellen (z. B. DIN ISO 2768, ISO 1302) ohne zu erfinden.\n5) Baue Qualitätskriterien ein (z. B. Ø, Längen, Ra, Form-/Lagetoleranzen) und Hinweise zur Selbstkontrolle.\n6) Gib typische Fehlerbilder + Ursachen + Gegenmaßnahmen an (Fehlerkatalog).\n7) Schließe mit Reflexionsfragen fürs Berichtsheft.\n8) Wenn Informationen fehlen, frage gezielt nach (max. 3 Rückfragen).\n\nAusgabeformat (Beispielstruktur):\n- **Sicherheit**\n- **Material & Rüstung** (Tabelle)\n- **Arbeitsablauf** (Schritte 1..n)\n- **Qualitätsprüfung** (Toleranzen/Messmittel)\n- **Fehlerkatalog**\n- **Reflexion** (3–5 Fragen)
"""

    prompt_text = textwrap.dedent(prompt_text).strip()
    st.success("Prompt erzeugt. Unten kopieren oder als Datei speichern.")
    st.text_area("Generierter Prompt", prompt_text, height=320)
    st.download_button(label="⬇️ Prompt als .txt speichern", data=prompt_text, file_name=f"prompt_metall_azubis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", mime="text/plain", use_container_width=True)

    html_code = textwrap.dedent(f"""\
<div style='display:flex;gap:8px;align-items:center;margin-top:8px;'>
<button id='copyBtn' style='padding:8px 12px;border-radius:10px;border:1px solid #ddd;cursor:pointer;'>📋 In Zwischenablage kopieren</button>
<span id='copyInfo' style='opacity:0.8'></span>
</div>
<script>
const text = "{prompt_text.replace('\\','\\\\').replace('\n','\\n').replace('"','&quot;').replace("'", "&#39;")}";
const btn = document.getElementById('copyBtn');
const info = document.getElementById('copyInfo');
btn.addEventListener('click', async () => {{
try {{
await navigator.clipboard.writeText(text);
info.textContent = 'Kopiert!';
}} catch (e) {{
info.textContent = 'Kopieren nicht erlaubt. Markiere den Text und kopiere manuell (Ctrl/Cmd+C).';
}}
}});
</script>
""")
    components.html(html_code, height=60)

    with st.expander("Maschinenlesbare Prompt-Metadaten (JSON)"):
        st.code(json.dumps(payload, ensure_ascii=False, indent=2))

st.markdown(
    """
---
**Tipps:**
- Nutze präzise Toleranzen (z. B. *Ø20 H7*, *Ra 1,6*, *➍ Ⓜ⌀0,02*), sonst fragt die KI nach.
- Wähle *Output-Format* »Arbeitsplan/Rüstplan« für tabellarische Abläufe (Vorbereitung → Rüsten → Bearbeiten → Prüfen → Nacharbeit).
- Für CNC: Benenne Steuerung (z. B. *Sinumerik 840D*, *Heidenhain iTNC*). Bitte **keine realen NC-Programme** mit Betriebsdaten einfügen.
- Sicherheit geht vor: DGUV-konforme Hinweise zuerst.
"""
)
