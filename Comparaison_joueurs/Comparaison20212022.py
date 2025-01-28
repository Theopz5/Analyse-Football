import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Radar
import os


def load_data():
    file_path = "2021-2022 Football Player Stats.xlsx"
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
        return None


df = load_data()
df_min = df[df["Min"] >= 900]

#  postes
defenseurs_lateraux = ["DF", "MFDF", "DFMF"]
defenseurs_centraux = ["DF", "DFMF", "MFDF"]
milieux_defensifs = ["MF", "DFMF", "MFDF"]
milieux_offensifs = ["MFFW", "MFDF", "FW"]
ailiers = ["MFFW", "FWMF", "FW"]
attaquants = ["FW", "MFFW", "FWMF"]

#barre latérale des differents postes 
st.sidebar.header("Configuration")
poste = st.sidebar.radio(
    "Poste des joueurs à comparer",
    options=["Défenseur latéral", "Défenseur central", "Milieu défensif", "Milieu offensif", "Ailier", "Attaquant"],
)

# Variables selon les postes
if poste == "Défenseur latéral":
    colonnes = ["Tkl", "TklWon", "TklDri", "Crs", "PasTotCmp%", "PasTotAtt", "Assists", "AerWon%", "DriSucc%"]
    # signification Tkl : Number of players tackled/90 , TklWon : Tackles in which the tackler's team won possession of the ball, TklDri :Number of dribblers tackled, Crs : Crosses, PasTotCmp : Passes completed, PasTotAtt : Passes attempted , DriSucc% : Percentage of dribbles completed successfully, AerWon% : Percentage of aerials won, 
    df_poste = df_min[df_min["Pos"].isin(defenseurs_lateraux)]
elif poste == "Défenseur central":
    colonnes = ["Tkl", "TklWon", "Int", "Clr", "AerWon%", "Blocks", "Err", "Recov"]
    # signification : Number of players tackled/90 ; TklWon : Tackles in which the tackler's team won possession of the ball; Int : Interceptions/90; Clr : Clearances/90; AerWon% : Percentage of aerials won, Blocks : blocages/90, Err : Erreurs/90, Rec: Recupérations/90
    df_poste = df_min[df_min["Pos"].isin(defenseurs_centraux)]
elif poste == "Milieu défensif":
    colonnes = ["PasTotCmp%", "Assists", "Crs", "Tkl", "Int","Blocks", "Clr","TklWon", "DriSucc%"]
    #signifiacation : PasTotCmp : Passes completed, Assists : passes décisives /90, Crs: centres /90, Tkl : tacles glissés / 90 , Int: Interceptions/90, Clr : Clearances/90, AerWon% : Percentage of aerials won, Blocks : blocages/90, DriSucc% : Percentage of dribbles completed successfully, AerWon% : Percentage of aerials won
    df_poste = df_min[df_min["Pos"].isin(milieux_defensifs)]
elif poste == "Milieu offensif":
    colonnes = ["PasTotCmp%", "Assists", "Crs", "Tkl", "Int","DriSucc%", "GcaSh", "SCA", "GCA"]
    #signification : PasTotCmp% : Passes completed,  Assists : passes décisives /90, Crs : centres/90, Tkl: tacles/90, Int: interceptions /90, DriSucc% : pourcentage de dribbles reussis, GcaSh : GcaSh : Shots that lead to another goal-scoring shot, SCA: SCA : Shot-creating actions, GCA : Goal-creating actions
    df_poste = df_min[df_min["Pos"].isin(milieux_offensifs)]
elif poste == "Ailier":
    colonnes = ["Goals", "Shots", "SoT%", "Assists", "G/Sh", "GcaSh", "DriSucc%","Crs", "ScaFld", "SCA", "CPA"]
    #signification : Goals : buts/90, Shots : Tirs/90, SoT% : Shots on target percentage (Does not include penalty kicks), Assists : Passes décisives/90, G/Sh: Buts/tirs, ScaFld : Fouls drawn that lead to a shot attempt, SCA : Shot-creating actions
    df_poste = df_min[df_min["Pos"].isin(ailiers)]
else:  # Attaquant
    colonnes = ["Goals", "Shots", "SoT%", "Assists", "G/Sh", "GcaSh", "ScaSh", "ScaFld", "SCA"]
    #significations : Goals : buts/90, Shots : Tirs/90, SoT% : Shots on target percentage (Does not include penalty kicks), Assists : Passes décisives/90, G/Sh: Buts/tirs, GcaSh : Shots that lead to another goal-scoring shot, ScaSh : Shots that lead to another shot attempt, ScaFld : Fouls drawn that lead to a shot attempt, SCA : Shot-creating actions
    df_poste = df_min[df_min["Pos"].isin(attaquants)]

# Sélection des joueurs dans la barre latérale
joueur1 = st.sidebar.selectbox("Sélectionnez le joueur 1", sorted(df_poste["Player"].unique()))
joueur2 = st.sidebar.selectbox("Sélectionnez le joueur 2 (facultatif)", ["Aucun"] + sorted(df_poste["Player"].unique()))

# Filtrer les données des joueurs
df_joueur1 = df_poste[df_poste["Player"] == joueur1]
df_joueur2 = df_poste[df_poste["Player"] == joueur2] if joueur2 != "Aucun" else pd.DataFrame()


# Affichage des données des joueurs
st.write("Données du joueur 1 :", df_joueur1[colonnes])
if joueur2 != "Aucun":
    st.write("Données du joueur 2 :", df_joueur2[colonnes])


# Création du graphique
def create_radar_chart_two_players(columns, df_poste, joueur1, df_joueur1, joueur2=None, df_joueur2=None):
    minimums = df_poste[columns].min()
    maximums = df_poste[columns].max()

    radar = Radar(
        params=columns,
        min_range=minimums.values,
        max_range=maximums.values,
        num_rings=4,
        ring_width=1,
        center_circle_radius=1,
    )

    fig, ax = plt.subplots(figsize=(6, 6))  
    radar.setup_axis(ax=ax)

    # Tracer les stats du joueur 1 
    radar.draw_radar(df_joueur1[columns].iloc[0].values, ax=ax, kwargs_radar={'facecolor': '#f21118', 'alpha': 0.8}, kwargs_rings={'facecolor': '#ffa07a', 'alpha': 0.5})
    
    # Tracer les stats du joueur 2 
    if joueur2 and not df_joueur2.empty:
        radar.draw_radar(df_joueur2[columns].iloc[0].values, ax=ax, kwargs_radar={'facecolor': '#0b138a', 'alpha': 0.8}, kwargs_rings={'facecolor': '#add8e6', 'alpha': 0.5})

    radar.draw_range_labels(ax=ax, fontsize=12, zorder=2.5, color='#080561', alpha=0.3)  
    radar.draw_param_labels(ax=ax, fontsize=12, color='#040c0f', alpha=0.7)  
    radar.spoke(ax=ax, color='#040c0f', linestyle=':', zorder=2, alpha=0.2)

    # Légende avec les noms des joueurs
    label1 = f"{joueur1}"
    label2 = f"{joueur2}" if joueur2 != "Aucun" else "Moyennes"
    ax.legend([label1, label2], loc='upper right', fontsize=6, frameon=False, facecolor='white', edgecolor='none')

    return fig


st.header(f"Comparaison des joueurs : {joueur1}" + (f" vs {joueur2}" if joueur2 != "Aucun" else ""))
fig = create_radar_chart_two_players(colonnes, df_poste, joueur1, df_joueur1, joueur2, df_joueur2)
st.pyplot(fig)


# section pour expliquer les variables
st.subheader("Signification des variables")
explications = {
    "Défenseur latéral": {
        "Tkl": "Number of players tackled/90",
        "TklWon": "Tackles in which the tackler's team won possession of the ball",
        "TklDri": "Number of dribblers tackled",
        "Crs": "Crosses",
        "PasTotCmp%": "Passes completed (%)",
        "PasTotAtt": "Passes attempted",
        "Assists": "Assists",
        "AerWon%": "Percentage of aerials won",
        "DriSucc%": "Percentage of dribbles completed successfully",
    },
    "Défenseur central": {
        "Tkl": "Number of players tackled/90",
        "TklWon": "Tackles in which the tackler's team won possession of the ball",
        "Int": "Interceptions/90",
        "Clr": "Clearances/90",
        "AerWon%": "Percentage of aerials won",
        "Blocks": "Blocks/90",
        "Err": "Errors leading to opponent actions",
        "Recov": "Recoveries/90",
    },
    "Milieu défensif": {
        "PasTotCmp%": "Passes completed (%)",
        "Assists": "Assists/90",
        "Crs": "Crosses/90",
        "Tkl": "Tackles/90",
        "Int": "Interceptions/90",
        "Blocks": "Blocks/90",
        "Clr": "Clearances/90",
        "TklWon": "Tackles won possession",
        "DriSucc%": "Percentage of dribbles completed successfully",
    },
    "Milieu offensif": {
        "PasTotCmp%": "Passes completed (%)",
        "Assists": "Assists/90",
        "Crs": "Crosses/90",
        "Tkl": "Tackles/90",
        "Int": "Interceptions/90",
        "DriSucc%": "Percentage of dribbles completed successfully",
        "GcaSh": "Shots leading to goal-scoring shots",
        "SCA": "Shot-creating actions",
        "GCA": "Goal-creating actions",
    },
    "Ailier": {
        "Goals": "Goals/90",
        "Shots": "Shots/90",
        "SoT%": "Shots on target (%)",
        "Assists": "Assists/90",
        "G/Sh": "Goals per shot",
        "GcaSh": "Shots leading to goal-scoring shots",
        "DriSucc%": "Percentage of dribbles completed successfully",
        "Crs": "Crosses/90",
        "ScaFld": "Fouls drawn leading to shots",
        "SCA": "Shot-creating actions",
        "CPA": "Completed passes into attacking third",
    },
    "Attaquant": {
        "Goals": "Goals/90",
        "Shots": "Shots/90",
        "SoT%": "Shots on target (%)",
        "Assists": "Assists/90",
        "G/Sh": "Goals per shot",
        "GcaSh": "Shots leading to goal-scoring shots",
        "ScaSh": "Shots leading to another shot attempt",
        "ScaFld": "Fouls drawn leading to shots",
        "SCA": "Shot-creating actions",
    },
}

if poste in explications:
    for variable, description in explications[poste].items():
        st.markdown(f"**{variable}**: {description}")



#   streamlit run "/Users/Utilisateur/Documents/Comparaison_joueurs/Comparaison20212022.py"