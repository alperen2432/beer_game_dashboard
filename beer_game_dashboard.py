import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Titel des Dashboards mit Stil
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; color: #4CAF50; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">📊 Beer Game Analyse-Dashboard</p>', unsafe_allow_html=True)

# Datei-Upload für Spieldaten
datei = st.file_uploader("📂 Lade eine Beer Game CSV-Datei hoch", type=["csv"])

if datei is not None:
    df = pd.read_csv(datei)
    st.success("✅ Datei erfolgreich hochgeladen!")

    # Sidebar-Filter für Semester und Spiel-ID
    st.sidebar.subheader("📅 Semester auswählen")
    semester_auswahl = st.sidebar.multiselect("Semester:", df["Semester"].unique(), default=df["Semester"].unique())

    st.sidebar.subheader("📌 Spiel ID auswählen")
    spiel_auswahl = st.sidebar.multiselect("Spiel ID:", df["Spiel_ID"].unique(), default=df["Spiel_ID"].unique())

    df_filtered = df[(df["Semester"].isin(semester_auswahl)) & (df["Spiel_ID"].isin(spiel_auswahl))]

    # Tabs für verschiedene Analysen
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Lagerbestand", "📦 Bestellungen", "⏳ Backlog", "📉 Bullwhip-Effekt"])

    with tab1:
        st.subheader("📦 Lagerbestand pro Runde")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df_filtered, x="Runde", y="Lagerbestand", hue="Rolle", ax=ax)
        ax.set_title("Lagerbestand pro Runde")
        st.pyplot(fig)

    with tab2:
        st.subheader("📦 Bestellungen pro Runde")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df_filtered, x="Runde", y="Bestellung", hue="Rolle", ax=ax)
        ax.set_title("Bestellungen im Zeitverlauf")
        st.pyplot(fig)

    with tab3:
        st.subheader("⏳ Backlog (Rückstände) im Verlauf")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df_filtered, x="Runde", y="Backlog", hue="Rolle", ax=ax)
        ax.set_title("Entwicklung des Backlogs")
        st.pyplot(fig)

    with tab4:
        st.subheader("📉 Bullwhip-Effekt Analyse")
        bullwhip_data = df_filtered.groupby("Rolle")["Bestellung"].var().reset_index()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=bullwhip_data, x="Rolle", y="Bestellung", ax=ax)
        ax.set_title("Variabilität der Bestellungen pro Rolle (Bullwhip-Effekt)")
        st.pyplot(fig)

    # Vergleich zwischen Gruppen
    st.subheader("📊 Vergleich zwischen Gruppen")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df_filtered, x="Spiel_ID", y="Lagerbestand", hue="Rolle", ax=ax)
    ax.set_title("Lagerbestand Vergleich zwischen Gruppen")
    st.pyplot(fig)

    # Vorhersage von Engpässen
    st.subheader("⚠️ Engpass-Warnsystem")
    low_stock = df_filtered[df_filtered["Lagerbestand"] < 20]
    if not low_stock.empty:
        st.warning("🚨 Achtung! Niedrige Lagerbestände gefunden!")
        st.dataframe(low_stock)
    else:
        st.success("✅ Keine kritischen Lagerbestände")

    # Optimale Bestellstrategie
    st.subheader("🏆 Optimale Bestellstrategie")
    best_teams = df_filtered.groupby("Spiel_ID")["Lagerbestand"].mean().reset_index()
    best_teams = best_teams.sort_values(by="Lagerbestand", ascending=False).head(5)
    st.dataframe(best_teams)

    # Analyse der Lieferzeiten
    st.subheader("🚚 Lieferzeit-Analyse")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df_filtered["Backlog"], bins=20, kde=True, ax=ax)
    ax.set_title("Verteilung der Lieferverzögerungen")
    st.pyplot(fig)

    # Saisonale Unterschiede
    st.subheader("📆 Saisonale Unterschiede zwischen Semestern")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_filtered, x="Runde", y="Lagerbestand", hue="Semester", ax=ax)
    ax.set_title("Vergleich der Lagerbestände zwischen Semestern")
    st.pyplot(fig)

    # Durchschnittswerte pro Rolle
    st.subheader("📊 Durchschnittswerte pro Rolle")
    avg_data = df_filtered.groupby("Rolle")[["Lagerbestand", "Bestellung", "Backlog"]].mean().reset_index()
    st.dataframe(avg_data)

    # Export der gefilterten Daten
    st.download_button("📥 Gefilterte Daten als CSV exportieren", 
                       df_filtered.to_csv(index=False).encode('utf-8'),
                       "beer_game_filtered_data.csv",
                       "text/csv")

else:
    st.warning("⚠ Bitte lade eine Datei hoch, um die Analyse zu starten.")
