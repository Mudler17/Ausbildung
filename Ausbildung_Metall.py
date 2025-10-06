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

# ---------------------- Defaults & Keys ----------------------
DEFAULTS = {
    "beruf": 0,  # Index in AUSBILDSBERUFE
    "jahr": 0,   # Index 0..3
    "lernort": 0,
    "aufgabentyp": 0,
    "output": ["Schritt-für-Schritt-Anleitung"],
    "sprache": 0,
    "ton": 1,
    "verfahren_ms": [], "verfahren_txt": "",
    "maschinen_ms": [], "maschinen_txt": "",
    "werkstoffe_ms": [], "werkstoffe_txt": "",
    "normen_ms": [], "normen_txt": "",
    "mess_ms": [], "mess_txt": "",
    "toleranzen": "",
    "didaktik": ["4-Stufen-Methode"],
    "lernziel": "",
    "zeit": 60,
    "materialien": "",
    "zeichnung": "",
    "kontext": "",
    "__RESET__": False,
}

def ensure_defaults():
    # Beim ersten Lauf Session-State initialisieren oder nach Reset überschreiben
    if not st.session_state:
        st.session_state.update(DEFAULTS)
    if st.session_state.get("__RESET__", False):
        st.session_state.update(DEFAULTS)
        st.session_state["__RESET__"] = False

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

# ---------------------- Init ----------------------
ensure_defaults()

# ---------------------- Layout ----------------------
colL, colR = st.columns([1, 1])

with colL:
    st.subheader("1) Rahmen & Rolle")
    beruf = st.selectbox("Ausbildungsberuf", AUSBILDSBERUFE, key="beruf", index=st.session_state.get("beruf", 0))
    ausbildungsjahr = st.selectbox("Ausbildungsjahr", ["1", "2", "3", "4"], key="jahr", index=st.session_state.get("jahr", 0))
    lernort = st.selectbox("Lernort", ["Betrieb", "ÜBA", "Berufsschule", "Prüfungsvorbereitung"], key="lernort", index=st.session_state.get("lernort", 0))
    aufgabentyp = st.selectbox("Aufgabentyp", AUFGABENTYP, key="aufgabentyp", index=st.session_state.get("aufgabentyp", 0))
    outputformat = st.multiselect("Gewünschtes Output-Format", OUTPUTFORMATE, default=st.session_state.get("output", ["Schritt-für-Schritt-Anleitung"]), key="output")
    sprache = st.selectbox("Sprache", SPRACHE, key="sprache", index=st.session_state.get("sprache", 0))
    ton = st.selectbox("Ton & Stil", TON, key="ton", index=st.session_state.get("ton", 1))

    st.subheader("2) Technik-Setup")
    verfahren = multiselect_with_free_text("Verfahren/Arbeitsgänge", VERFAHREN, "verfahren")
    maschinen = multiselect_with_free_text("Maschinen/Steuerungen", MASCHINEN, "maschinen")
    werkstoffe = multiselect_with_free_text("Werkstoffe", WERKSTOFFE, "werkstoffe")

with colR:
    st.subheader("3) Qualität & Sicherheit")
    normen = multiselect_with_free_text("Normen/Regeln", NORMEN, "normen")
    messmittel = multiselect_with_free_text("Messmittel/Prüfkriterien", MESSMITTEL, "mess")
    toleranzen = st.text_input("Maß-/Form-/Lagetoleranzen (z. B. Ø20 H7, Ra 1,6, Ⓜ⌀0,02)", key="toleranzen", value=st.session_state.get("toleranzen", ""))
    sicherheit = multiselect_with_free_text("Sicherheitsaspekte (PSA, Gefahren, Unterweisung)", [
        "PSA: Schutzbrille, Handschuhe", "Gefährdungsbeurteilung", "Sperrbereiche", "Brandgefahr",
        "Späne/Quetschstellen", "Schweißrauchabsaugung"
    ], "safety")

    st.subheader("4) Didaktik & Zeit")
    didaktik = st.multiselect("Didaktischer Ansatz", DIDAKTIK, default=st.session_state.get("didaktik", ["4-Stufen-Methode"]), key="didaktik")
    lernziel = st.text_area("Lernziel(e) (beobachtbar, SMART)", height=80, key="lernziel", value=st.session_state.get("lernziel", ""))
    zeit = st.number_input("Geplante Zeit (Minuten)", min_value=5, max_value=480, value=st.session_state.get("zeit", 60), step=5, key="zeit")

st.subheader("5) Materialien & Kontext")
materialien = st.text_area("Material-/Werkzeugliste (eine Position pro Zeile)", height=80, key="materialien", value=st.session_state.get("materialien", ""))
zeichnung = st.text_input("Link/Referenz: Zeichnung/Skizze/Foto (optional)", key="zeichnung", value=st.session_state.get("zeichnung", ""))
kontext = st.text_area("Kontext/Startlage (z. B. Werkstückbeschreibung, Ist-Stand, typische Fehler)", height=100, key="kontext", value=st.session_state.get("kontext", ""))

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
        "lernziel": st.session_state.get("lernziel", "").strip(),
        "verfahren": verfahren,
        "maschinen": maschinen,
        "werkstoffe": werkstoffe,
        "normen": normen,
        "messmittel": messmittel,
        "toleranzen": st.session_state.get("toleranzen", "").strip(),
        "sicherheit": sicherheit,
        "zeit_min": st.session_state.get("zeit", 60),
        "materialliste": [x.strip() for x in st.session_state.get("materialien", "").splitlines() if x.strip()],
        "zeichnung_ref": st.session_state.get("zeichnung", "").strip(),
        "kontext": st.session_state.get("kontext", "").strip(),
        "gewünschter_output": st.session_state.get("output", ["Schritt-für-Schritt-Anleitung"]),
        "meta": {"erstellt": now, "builder": "Promptbuilder Metall (Azubis)"}
    }

    prompt_text = textwrap.dedent(f"""Rolle & Ziel:\n{payload['rolle']} Sprich {('mich' if sprache=='Deutsch' else 'me')} im Stil: {ton}. Arbeite {('auf Deutsch' if sprache=='Deutsch' else 'in English')}. Ziel: {payload['ziel']}\n\nKontext:\n- Lernort: {lernort}\n- Aufgabentyp: {aufgabentyp}\n- Ausbildungsjahr: {ausbildungsjahr}\n- Verfahren/Arbeitsgänge: {', '.join(verfahren) or '-'}\n- Maschinen/Steuerungen: {', '.join(maschinen) or '-'}\n- Werkstoffe: {', '.join(werkstoffe) or '-'}\n- Normen/Regeln: {', '.join(normen) or '-'}\n- Messmittel/Prüfkriterien: {', '.join(messmittel) or '-'}\n- Toleranzen: {payload['toleranzen'] or '-'}\n- Sicherheitsaspekte: {', '.join(sicherheit) or '-'}\n- Zeitrahmen: {payload['zeit_min']} Minuten\n- Materialien/Werkzeuge: {', '.join(payload['materialliste']) or '-'}\n- Zeichnung/Referenz: {payload['zeichnung_ref'] or '-'}\n- Startlage/typische Fehler: {payload['kontext'] or '-'}\n- Didaktik: {', '.join(didaktik) or '-'}\n- Lernziel(e): {payload['lernziel'] or '-'}\n\nAufgaben an die KI:\n1) Erstelle die Ausgabe im/als: {', '.join(payload['gewünschter_output'])}.\n2) Nenne zuerst Sicherheits-Hinweise (DGUV-konform), dann Material/Setup, dann Vorgehen.\n3) Verwende Nummerierung und, wo sinnvoll, Tabellen.\n4) Mache Maße, Toleranzen, Werkstoff und Messmittel konkret; verweise auf Normstellen (z. B. DIN ISO 2768, ISO 1302) ohne zu erfinden.\n5) Baue Qualitätskriterien ein (z. B. Ø, Längen, Ra, Form-/Lagetoleranzen) und Hinweise zur Selbstkontrolle.\n6) Gib typische Fehlerbilder + Ursachen + Gegenmaßnahmen an (Fehlerkatalog).\n7) Schließe mit Reflexionsfragen fürs Berichtsheft.\n8) Wenn Informationen fehlen, frage gezielt nach (max. 3 Rückfragen).\n\nAusgabeformat (Beispielstruktur):\n- **Sicherheit**\n- **Material & Rüstung** (Tabelle)\n- **Arbeitsablauf** (Schritte 1..n)\n- **Qualitätsprüfung** (Toleranzen/Messmittel)\n- **Fehlerkatalog**\n- **Reflexion** (3–5 Fragen)""").strip()

    st.success("Prompt erzeugt. Unten kopieren oder als Datei speichern.")
    st.text_area("Generierter Prompt", prompt_text, height=320)
    st.download_button(label="⬇️ Prompt als .txt speichern", data=prompt_text, file_name=f"prompt_metall_azubis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", mime="text/plain", use_container_width=True)

    html_code = textwrap.dedent(f"""<div style='display:flex;gap:8px;align-items:center;margin-top:8px;'>
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
</script>""")
    components.html(html_code, height=60)

    with st.expander("Maschinenlesbare Prompt-Metadaten (JSON)"):
        st.code(json.dumps(payload, ensure_ascii=False, indent=2))

# ---------------------- Reset-Button am Ende ----------------------
if st.button("🔄 Alle Felder zurücksetzen und neu starten", use_container_width=True):
    st.session_state["__RESET__"] = True
    st.rerun()

# ---------------------- Footer ----------------------
st.markdown(
    """---
**Tipps:**
- Nutze präzise Toleranzen (z. B. *Ø20 H7*, *Ra 1,6*, *➍ Ⓜ⌀0,02*), sonst fragt die KI nach.
- Wähle *Output-Format* »Arbeitsplan/Rüstplan« für tabellarische Abläufe (Vorbereitung → Rüsten → Bearbeiten → Prüfen → Nacharbeit).
- Für CNC: Benenne Steuerung (z. B. *Sinumerik 840D*, *Heidenhain iTNC*). Bitte **keine realen NC-Programme** mit Betriebsdaten einfügen.
- Sicherheit geht vor: DGUV-konforme Hinweise zuerst.
"""
)
