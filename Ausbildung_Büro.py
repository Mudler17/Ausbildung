# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
import textwrap
import html
import json
import streamlit as st
import streamlit.components.v1 as components

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

def daterange_str(d1: date, d2: date) -> str:
    if d1 == d2:
        return d1.strftime("%d.%m.%Y")
    return f"{d1.strftime('%d.%m.%Y')} – {d2.strftime('%d.%m.%Y')}"

def copy_button(text: str, key: str, label: str = "📋 In Zwischenablage"):
    """
    Robuster Copy-Button via components.html.
    Nutzt navigator.clipboard; fällt bei restriktiven Browsern auf Auswahl+Copy zurück.
    """
    # Für JS sicher serialisieren
    js_payload = json.dumps(text)
    btn_id = f"copybtn_{key}"
    html_code = f"""
    <div style="display:flex;gap:.5rem;align-items:center;">
      <button id="{btn_id}" style="padding:.5rem .75rem;border:1px solid #ddd;border-radius:.5rem;cursor:pointer;">
        {html.escape(label)}
      </button>
      <span id="{btn_id}_status" style="font-size:.9rem;color:#666;"></span>
    </div>
    <script>
      (function(){{
        const btn = document.getElementById("{btn_id}");
        const status = document.getElementById("{btn_id}_status");
        const text = {js_payload};
        async function copyText() {{
          try {{
            if (navigator.clipboard && window.isSecureContext) {{
              await navigator.clipboard.writeText(text);
            }} else {{
              const ta = document.createElement("textarea");
              ta.value = text;
              ta.style.position = "fixed";
              ta.style.left = "-9999px";
              document.body.appendChild(ta);
              ta.focus();
              ta.select();
              document.execCommand("copy");
              document.body.removeChild(ta);
            }}
            status.textContent = "Kopiert!";
            setTimeout(()=>{{status.textContent="";}}, 2000);
          }} catch(e) {{
            status.textContent = "Kopieren fehlgeschlagen";
            setTimeout(()=>{{status.textContent="";}}, 3000);
          }}
        }}
        btn.addEventListener("click", copyText);
      }})();
    </script>
    """
    components.html(html_code, height=40)

def dl_button(label: str, txt: str, filename: str):
    st.download_button(
        label=label,
        data=txt,
        file_name=filename,
        mime="text/plain"
    )

# ────────────────────────────────────────────────────────────────────────────────
# Sidebar: Modus & Zeitraum (von–bis)
# ────────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Einstellungen")
    modus = st.radio(
        "Modus",
        options=["Ausbildung (Büromanagement)", "Berufsvorbereitung"],
        index=0
    )

    # Standard-Zeitraum: Montag dieser Woche bis heute
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    date_from, date_to = st.date_input(
        "Zeitraum (von – bis)",
        value=(monday, today),
        format="DD.MM.YYYY"
    )
    # Abfangen einzelner Auswahl
    if isinstance(date_from, tuple) or isinstance(date_to, tuple):
        # Streamlit gibt bei Fehlbedienung manchmal Tupel zurück
        date_from = monday
        date_to = today
    if date_from > date_to:
        st.error("Das Startdatum liegt nach dem Enddatum. Bitte korrigieren.")
    st.markdown("---")
    st.markdown("**Export**: Unten Berichtsheft/Arbeitsauftrag/Prüfungsübungen generieren. Kopieren oder als TXT speichern.")

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
        f"**Zeitraum:** {daterange_str(date_from, date_to)}",
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
- Zeitraum: {daterange_str(date_from, date_to)}

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
    parts.append(f"Modus: {modus} · Zeitraum: {daterange_str(date_from, date_to)}")
    parts.append(section("Aufgabenpool (wähle 2–3)"))
    parts.append(bullet(PRUEFUNGSUEBUNGEN))
    parts.append(section("Kontext aus der Praxiswoche"))
    if lf:
        parts.append("**Schwerpunkte:**\n" + bullet(lf))
    if tools:
        parts.append("\n**Werkzeuge:**\n" + bullet(tools))
    if schule:
        parts.append("\n**Bezug Berufsschule:**\n" + bullet(schule))
    parts.append(section("Abgabe & Bewertung (Kurzrubrik)"))
    parts.append(bullet([
        "Vollständigkeit & Nachvollziehbarkeit",
        "Form & Layout (professionell, CI falls vorhanden)",
        "Korrektheit (fachlich, rechnerisch)",
        "Begründungen/Entscheidungen kurz erläutert",
        "Zeitmanagement eingehalten"
    ]))
    return "\n".join(parts).strip()

# ────────────────────────────────────────────────────────────────────────────────
# Ausgabe & Downloads + Copy-Buttons
# ────────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🧾 Berichtsheft", "🛠️ Arbeitsauftrag (Prompt)", "📝 Prüfungsübungen"])

with tab1:
    txt = gen_berichtsheft()
    st.markdown(txt)
    colA, colB = st.columns([1,1])
    with colA:
        dl_button("⬇️ Berichtsheft als TXT", txt, f"berichtsheft_bueromanagement_{datetime.now():%Y%m%d}.txt")
    with colB:
        copy_button(txt, key="berichtsheft")

with tab2:
    txt = gen_arbeitsauftrag()
    st.code(txt)
    colA, colB = st.columns([1,1])
    with colA:
        dl_button("⬇️ Arbeitsauftrag-Prompt als TXT", txt, f"arbeitsauftrag_prompt_{datetime.now():%Y%m%d}.txt")
    with colB:
        copy_button(txt, key="arbeitsauftrag")

with tab3:
    txt = gen_pruefung()
    st.markdown(txt)
    colA, colB = st.columns([1,1])
    with colA:
        dl_button("⬇️ Prüfungsübungen als TXT", txt, f"pruefung_uebungen_{datetime.now():%Y%m%d}.txt")
    with colB:
        copy_button(txt, key="pruefung")
