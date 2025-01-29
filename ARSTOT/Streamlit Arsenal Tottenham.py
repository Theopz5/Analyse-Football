#Streamlit Arsenal Tottenham


import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch, FontManager,Pitch
import networkx as nx
from matplotlib.colors import LinearSegmentedColormap
from collections import Counter
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Analyse Football", page_icon="🏆", layout="wide")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/events/3754318.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Impossible de charger les données.")
        return []

data = load_data()


# polices pour les graphiques
robotto_regular = FontManager()

# visualisations des buts
def plot_goal(goal_action, goal_number):
    goal_freeze_frame = goal_action.get("shot", {}).get("freeze_frame", [])
    scorer_team = goal_action.get("team", {}).get("name")
    scorer_name = goal_action.get("player", {}).get("name")
    xg_value = goal_action.get("shot", {}).get("statsbomb_xg", 0)
    
    team_positions = []
    opponent_positions = []
    team_labels = []
    opponent_labels = []

    for player in goal_freeze_frame:
        position = player.get("location", [None, None])
        jersey_number = player.get("jersey_number", None)
        label = str(jersey_number) if jersey_number else "??"
        if position:
            if scorer_team == "Tottenham Hotspur":
                if player.get("teammate"):
                    team_positions.append(position)
                    team_labels.append(label)
                else:
                    opponent_positions.append(position)
                    opponent_labels.append(label)
            elif scorer_team == "Arsenal":
                if player.get("teammate"):
                    opponent_positions.append(position)
                    opponent_labels.append(label)
                else:
                    team_positions.append(position)
                    team_labels.append(label)

    pitch = VerticalPitch(half=True, goal_type='box', pad_bottom=-20)
    fig, axs = pitch.grid(figheight=8, endnote_height=0, title_height=0.1, title_space=0.02,
                          axis=False, grid_height=0.83)

    pitch.scatter(
        [pos[0] for pos in team_positions],
        [pos[1] for pos in team_positions],
        s=600,
        c='#1f77b4',
        label='Tottenham Player',
        ax=axs['pitch']
    )

    pitch.scatter(
        [pos[0] for pos in opponent_positions],
        [pos[1] for pos in opponent_positions],
        s=600,
        c='#d62728',
        label='Arsenal Player',
        ax=axs['pitch']
    )

    start_location = goal_action.get("location", [None, None])
    end_location = goal_action.get("shot", {}).get("end_location", [None, None])
    if start_location and end_location:
        pitch.scatter(start_location[0], start_location[1], marker='football', s=600,
                      ax=axs['pitch'], label='Shooter', zorder=1.2)
        pitch.lines(start_location[0], start_location[1], end_location[0], end_location[1],
                    comet=True, label='Shot', color='#cb5a4c', ax=axs['pitch'])
        pitch.goal_angle(start_location[0], start_location[1], ax=axs['pitch'],
                         alpha=0.2, zorder=1.1, color='#cb5a4c', goal='right')

    legend = axs['pitch'].legend(loc='upper left', labelspacing=1.5, fontsize=12)
    for text in legend.get_texts():
        text.set_fontproperties(robotto_regular.prop)

    axs['title'].text(
        0.5, 0.5,
        f"Goal #{goal_number}: {scorer_name}\n{scorer_team} vs Opponent",
        va='center', ha='center', color='black',
        fontproperties=robotto_regular.prop, fontsize=15
    )
    axs['title'].text(
        1.0, 0.5,
        f"xG: {xg_value:.2f}",
        va='center', ha='right', color='black',
        fontproperties=robotto_regular.prop, fontsize=12
    )

    return fig

#  statistiques globales de passes
passes_tot = 0
passes_totR = 0
passes_ars = 0
passes_arsR = 0

for action in data:
    if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Tottenham Hotspur":
        passes_tot += 1
        if action.get("pass", {}).get("outcome", {}).get("name") == "Incomplete":
            passes_totR += 1
    elif action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Arsenal":
        passes_ars += 1
        if action.get("pass", {}).get("outcome", {}).get("name") == "Incomplete":
            passes_arsR += 1

passes_tot_success = passes_tot - passes_totR
passes_ars_success = passes_ars - passes_arsR

pourcentage_Tot = round((passes_tot_success * 100 / passes_tot), 1) if passes_tot > 0 else 0
pourcentage_ars = round((passes_ars_success * 100 / passes_ars), 1) if passes_ars > 0 else 0

#  buts
buts = [action for action in data if action.get("type", {}).get("name") == "Shot" and action.get("shot", {}).get("outcome", {}).get("name") == "Goal"]

# Gestion des onglets 
menu = st.sidebar.radio("Résumé:", ["Match", "Tottenham Hotspur", "Arsenal", "Joueurs Stars"])
























if menu == "Tottenham Hotspur":
 
    st.header("Vue de Tottenham")
    
    # Statistiques
    st.subheader("Statistiques de passes - Tottenham")
    st.metric("Passes totales", passes_tot)
    st.metric("Passes réussies", passes_tot_success)
    st.metric("Taux de réussite", f"{pourcentage_Tot}%")
    
    # Affichage des buts
    st.subheader("Buts marqués par Tottenham")
    buts_tot = [but for but in buts if but.get("team", {}).get("name") == "Tottenham Hotspur"]
    if buts_tot:
        for i, but in enumerate(buts_tot):
            st.write(f"- **Minute {but['minute']}** : {but['player']['name']} avec un xG de {but['shot']['statsbomb_xg']:.2f}")
            fig = plot_goal(but, i + 1)
            st.pyplot(fig)
    else:
        st.write("Aucun but marqué par Totenham.")  
        
    # Statistiques spécifiques
    st.subheader("Statistiques de passes - Tottenham")
    st.metric("Passes totales", passes_tot)
    st.metric("Passes réussies", passes_tot_success)
    st.metric("Taux de réussite", f"{pourcentage_Tot}%")

    # Passes en première mi-temps
    st.subheader("Carte de flux et heatmap des passes de TOttenham en 1ère mi-temps")
    passes_xT1 = []
    passes_yT1 = []
    end_xT1 = []
    end_yT1 = []

    for action in data:
        if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Tottenham Hotspur" and action.get("period", {}) == 1:
            start_loc = action.get("location", [None, None])
            end_loc = action.get("pass", {}).get("end_location", [None, None])
            if start_loc and end_loc:
                passes_xT1.append(start_loc[0])
                passes_yT1.append(start_loc[1])
                end_xT1.append(end_loc[0])
                end_yT1.append(end_loc[1])

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 8))
    fig.set_facecolor('#22312b')

    bins = (6, 4)
    heatmap = pitch.bin_statistic(passes_xT1, passes_yT1, statistic='count', bins=bins)
    pitch.heatmap(heatmap, ax=ax, cmap='Blues', edgecolors='#22312b')

    pitch.flow(passes_xT1, passes_yT1, end_xT1, end_yT1, color='black', arrow_type='same', bins=bins, ax=ax, arrow_length=5)

    ax.set_title(f"Carte de flux et heatmap des passes de Tottenham en 1ère mi-temps", fontsize=16, color='white')
    st.pyplot(fig)

    # Passes en deuxième mi-temps
    st.subheader("Carte de flux et heatmap des passes de Tottenham en 2ème mi-temps")
    passes_xT2 = []
    passes_yT2 = []
    end_xT2 = []
    end_yT2 = []

    for action in data:
        if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Tottenham Hotspur" and action.get("period", {}) == 2:
            start_loc = action.get("location", [None, None])
            end_loc = action.get("pass", {}).get("end_location", [None, None])
            if start_loc and end_loc:
                passes_xT2.append(start_loc[0])
                passes_yT2.append(start_loc[1])
                end_xT2.append(end_loc[0])
                end_yT2.append(end_loc[1])

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 8))
    fig.set_facecolor('#22312b')

    bins = (6, 4)
    heatmap = pitch.bin_statistic(passes_xT2, passes_yT2, statistic='count', bins=bins)
    pitch.heatmap(heatmap, ax=ax, cmap='Blues', edgecolors='#22312b')

    pitch.flow(passes_xT2, passes_yT2, end_xT2, end_yT2, color='black', arrow_type='same', bins=bins, ax=ax, arrow_length=5)

    ax.set_title(f"Carte de flux et heatmap des passes de Tottenham en 2ème mi-temps", fontsize=16, color='white')
    st.pyplot(fig)

    # Passes match entier
    st.subheader("Carte de flux et heatmap des passes de Tottenham (Match Entier)")
    passes_xV = []
    passes_yT = []
    end_xV = []
    end_yT = []

    for action in data:
        if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Tottenham Hotspur":
            start_loc = action.get("location", [None, None])
            end_loc = action.get("pass", {}).get("end_location", [None, None])
            if start_loc and end_loc:
                passes_xV.append(start_loc[0])
                passes_yT.append(start_loc[1])
                end_xV.append(end_loc[0])
                end_yT.append(end_loc[1])

    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 8))
    fig.set_facecolor('#22312b')

    bins = (6, 4)
    heatmap = pitch.bin_statistic(passes_xV, passes_yT, statistic='count', bins=bins)
    pitch.heatmap(heatmap, ax=ax, cmap='Blues', edgecolors='#22312b')

    pitch.flow(passes_xV, passes_yT, end_xV, end_yT, color='black', arrow_type='same', bins=bins, ax=ax, arrow_length=5)

    ax.set_title(f"Carte de flux et heatmap des passes de Tottenham", fontsize=16, color='white')
    st.pyplot(fig)

    # numéros de maillot
    jersey_numbers = {}
    for action in data:
        if action["type"]["name"] == "Starting XI" and action["team"]["name"] == "Tottenham Hotspur":
            lineup = action["tactics"]["lineup"]
            for player in lineup:
                player_name = player["player"]["name"]
                jersey_number = player["jersey_number"]
                jersey_numbers[player_name] = jersey_number

    jersey_numbers["Heung-Min Son"] = 7
    jersey_numbers["Ryan Mason"] = 8
    jersey_numbers["Ben Davies"] = 33

    #  positions des joueurs et les passes
    player_positions = {}
    pass_counts = {}

    for action in data:
        if action["type"]["name"] == "Pass" and action["team"]["name"] == "Tottenham Hotspur":
            passer = action["player"]["name"]
            recipient = action.get("pass", {}).get("recipient", {}).get("name")
            start_loc = action.get("location")
            end_loc = action.get("pass").get("end_location")
            
            if recipient and end_loc:
                if passer not in player_positions:
                    player_positions[passer] = []
                player_positions[passer].append(start_loc)

                pair = (passer, recipient)
                if pair not in pass_counts:
                    pass_counts[pair] = 0
                pass_counts[pair] += 1

    # positions moyennes des joueurs
    average_positions = {
        player: np.mean(pos, axis=0) for player, pos in player_positions.items()
    }

    # graphe de passes
    G = nx.DiGraph()

    for (passer, recipient), count in pass_counts.items():
        G.add_edge(passer, recipient, weight=count)

    # dessiner le graphique
    def plot_pass_network():
      pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
      fig, ax = pitch.draw(figsize=(10, 8))
      fig.set_facecolor('#22312b')

    # Afficher les joueurs et leurs positions
      for player, pos in average_positions.items():
        jersey_number = jersey_numbers.get(player, "??")
        ax.scatter(pos[0], pos[1], s=500, c='blue', edgecolors='black', zorder=5)
        ax.text(pos[0], pos[1], str(jersey_number), fontsize=10, color='white', ha='center', zorder=6)

    # Tracer les passes
      for edge in G.edges(data=True):
        passer, recipient, attr = edge
        weight = attr['weight']

        
        if recipient in average_positions:
            start_pos = average_positions[passer]
            end_pos = average_positions[recipient]
            ax.plot(
                [start_pos[0], end_pos[0]],
                [start_pos[1], end_pos[1]],
                color='white',
                linewidth=weight,
                alpha=0.7,
            )

      ax.set_title("Réseau de passes de Tothenam (par numéro)", fontsize=16, color='white')
      return fig
  
  
    # Streamlit UI
    st.title("Réseau de passes de Tottenham")
    st.write("Position moyennes des joueurs et réseau de passes (remplacents inclus)")

    # Afficher le graphique
    fig = plot_pass_network()
    st.pyplot(fig)
    
    tot_players = []
    for action in data:
        if action["team"]["name"] == "Tottenham Hotspur" and "tactics" in action:
            for joueur in action["tactics"]["lineup"]:
                nom = joueur["player"]["name"]
                numero = joueur.get("jersey_number")
                poste = joueur["position"]["name"]
                tot_players.append({"name": nom, "number": numero, "position": poste})
                
    # Fonction pour afficher les statistiques du joueur sélectionné
    def display_player_stats(player):
        st.write(f"### Statistiques pour {player['name']}")
        st.write(f"**Poste :** {player['position']}")
        st.write(f"**Numéro de maillot :** {player['number']}")

        # heatmap
        st.subheader(f"**Heatmap de {player['name']} :**")
        plot_heatmap(player['name'])

        #  conduites de balle
        st.subheader(f"**Conduites de balle de {player['name']} :**")
        plot_ball_carries(player['name'])

    # générer la heatmap
    def plot_heatmap(player_name):
        heatmap_cmap = LinearSegmentedColormap.from_list("heatmap_cmap", ["yellow", "red"])
        
        # Récupère les positions du joueur
        player_positions_x = []
        player_positions_y = []
        
        for action in data:
            if action.get("player", {}).get("name") == player_name:
                if "location" in action:
                    player_positions_x.append(action["location"][0])
                    player_positions_y.append(action["location"][1])

        # Créer la carte
        pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 8))
        fig.set_facecolor('#22312b')
        
        pitch.kdeplot(player_positions_x, player_positions_y, ax=ax, shade=True, levels=100, cmap=heatmap_cmap)
        plt.title(f"Carte de chaleur de {player_name}", fontsize=16, color='white')

        # Affichage dans Streamlit
        st.pyplot(fig)
      
      
    def plot_heatmap(player_name):
        heatmap_cmap = LinearSegmentedColormap.from_list("heatmap_cmap", ["yellow", "red"])
        
        # Récupère les positions du joueur
        player_positions_x = []
        player_positions_y = []
        
        for action in data:
            if action.get("player", {}).get("name") == player_name:
                if "location" in action:
                    player_positions_x.append(action["location"][0])
                    player_positions_y.append(action["location"][1])

        # Créer la carte
        pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 8))
        fig.set_facecolor('#22312b')
        
        pitch.kdeplot(player_positions_x, player_positions_y, ax=ax, shade=True, levels=100, cmap=heatmap_cmap)
        plt.title(f"Carte de chaleur de {player_name}", fontsize=16, color='white')

        # Affichage dans Streamlit
        st.pyplot(fig)

    # Fonction pour afficher les conduites de balle
    def plot_ball_carries(player_name):
        carries_x_start = []
        carries_y_start = []
        carries_x_end = []
        carries_y_end = []

        for action in data:
            if action.get("type", {}).get("name") == "Carry" and action.get("player", {}).get("name") == player_name:
                start_loc = action.get("location", [None, None])
                end_loc = action.get("carry", {}).get("end_location", [None, None])
                if start_loc and end_loc:
                    carries_x_start.append(start_loc[0])
                    carries_y_start.append(start_loc[1])
                    carries_x_end.append(end_loc[0])
                    carries_y_end.append(end_loc[1])

        # Graphique des conduites de balle
        pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 8))
        fig.set_facecolor('#22312b')

        pitch.scatter(carries_x_start, carries_y_start, color='red', s=50, edgecolors='black', ax=ax, label='Départ')

        for i in range(len(carries_x_start)):
            pitch.lines(carries_x_start[i], carries_y_start[i],
                        carries_x_end[i], carries_y_end[i],
                        lw=2, color='blue', comet=True, ax=ax)

        plt.title(f"Conduites de balle de {player_name}", fontsize=16, color='white')
        
        # Affichage dans Streamlit
        st.pyplot(fig)
        
    #  déroulant pour choisir un joueur de tottenham
    selected_player_name = st.selectbox("Choisissez un joueur de Tottenham", [player["name"] for player in tot_players], key="totenham_player_select")

    # Trouver le joueur sélectionné dans la liste des joueurs
    selected_player = next(player for player in tot_players if player["name"] == selected_player_name)

    # Lorsque l'utilisateur sélectionne un joueur, afficher ses stats
    if selected_player:
        display_player_stats(selected_player)

    # Exemple de génération de statistiques pour les passes
    def plot_passes(player_name, passes_data):
        passes_success = []
        passes_failed = []
        
        for action in passes_data:
            if action.get("type", {}).get("name") == "Pass" and action.get("player", {}).get("name") == player_name:
                start_location = action.get("location", [None, None])
                end_location = action.get("pass", {}).get("end_location", [None, None])
                if start_location and end_location:
                    if action.get("pass", {}).get("outcome", {}).get("name") == "Incomplete":
                        passes_failed.append((start_location, end_location))
                    else:
                        passes_success.append((start_location, end_location))

        # Affichage sur le terrain
        pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 8))
        fig.set_facecolor('#22312b')

        for start, end in passes_success:
            pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='green', ax=ax)

        for start, end in passes_failed:
            pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='red', ax=ax)

        plt.title(f"Passes de {player_name} (vert : réussies, rouge : incomplètes)", fontsize=16, color='white')
        st.pyplot(fig)

    # Exemple d'affichage des passes pour un joueur
    plot_passes(selected_player_name, data)    
    
    

    passesT = []
    for action in data:
        if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Tottenham Hotspur":
            passer = action.get("player", {}).get("name")
            receiver = action.get("pass", {}).get("recipient", {}).get("name")
            if passer and receiver:
                passesT.append((passer, receiver))

    # Créer un DataFrame des passes
    df = pd.DataFrame([], columns=["passer", "receiver", "count"])
    compteur_passesT = Counter(passesT)
    for i, ((passer, receiver), count) in enumerate(compteur_passesT.most_common()):
      df.loc[i] = [passer, receiver, count]

  # Interface utilisateur Streamlit
    st.title("Analyse des passes des joueurs de Tottenham")


  # Filtrer les données pour le joueur sélectionné
    df_joueur = df[df["passer"] == selected_player_name]

  # Afficher les données des passes du joueur
    st.write(f"### Passes réalisées par **{selected_player_name}**")
    st.dataframe(df_joueur)

  # Fonction pour afficher les passes sur un terrain
    def plot_passes(player_name, passes_data):
      passes_success = []
      passes_failed = []

      for action in passes_data:
          if action.get("type", {}).get("name") == "Pass" and action.get("player", {}).get("name") == player_name:
              start_location = action.get("location", [None, None])
              end_location = action.get("pass", {}).get("end_location", [None, None])
              if start_location and end_location:
                  if action.get("pass", {}).get("outcome", {}).get("name") == "Incomplete":
                      passes_failed.append((start_location, end_location))
                  else:
                      passes_success.append((start_location, end_location))

      # Affichage des passes sur le terrain
      pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
      fig, ax = pitch.draw(figsize=(10, 8))
      fig.set_facecolor('#22312b')

      for start, end in passes_success:
          pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='green', ax=ax)

      for start, end in passes_failed:
          pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='red', ax=ax)

      plt.title(f"Passes de {player_name} (vert : réussies, rouge : incomplètes)", fontsize=16, color='white')
      st.pyplot(fig)

  # Afficher les passes sur le terrain pour le joueur sélectionné
    plot_passes(selected_player_name, data)

          




















if menu == "Arsenal":
  st.header("Vue d'Arsenal")
    
    # Statistiques spécifiques à Arsenal
  st.subheader("Statistiques de passes - Arsenal")
  st.metric("Passes totales", passes_ars)
  st.metric("Passes réussies", passes_ars_success)
  st.metric("Taux de réussite", f"{pourcentage_ars}%")
    
    # Affichage des buts d'Arsenal
  st.subheader("Buts marqués par Arsenal")
  buts_arsenal = [but for but in buts if but.get("team", {}).get("name") == "Arsenal"]
  if buts_arsenal:
      for i, but in enumerate(buts_arsenal):
            st.write(f"- **Minute {but['minute']}** : {but['player']['name']} avec un xG de {but['shot']['statsbomb_xg']:.2f}")
            fig = plot_goal(but, i + 1)
            st.pyplot(fig)
  else:
        st.write("Aucun but marqué par Arsenal.")
        
        

    # Statistiques spécifiques à Arsenal
  st.subheader("Statistiques de passes - Arsenal")
  st.metric("Passes totales", passes_tot)
  st.metric("Passes réussies", passes_tot_success)
  st.metric("Taux de réussite", f"{pourcentage_Tot}%")

    # Passes en première mi-temps
  st.subheader("Carte de flux et heatmap des passes d'Arsenal en 1ère mi-temps")
  passes_xT1 = []
  passes_yT1 = []
  end_xT1 = []
  end_yT1 = []

  for action in data:
      if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Arsenal" and action.get("period", {}) == 1:
            start_loc = action.get("location", [None, None])
            end_loc = action.get("pass", {}).get("end_location", [None, None])
            if start_loc and end_loc:
                passes_xT1.append(start_loc[0])
                passes_yT1.append(start_loc[1])
                end_xT1.append(end_loc[0])
                end_yT1.append(end_loc[1])

  pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
  fig, ax = pitch.draw(figsize=(10, 8))
  fig.set_facecolor('#22312b')

  bins = (6, 4)
  heatmap = pitch.bin_statistic(passes_xT1, passes_yT1, statistic='count', bins=bins)
  pitch.heatmap(heatmap, ax=ax, cmap='Reds', edgecolors='#22312b')

  pitch.flow(passes_xT1, passes_yT1, end_xT1, end_yT1, color='black', arrow_type='same', bins=bins, ax=ax, arrow_length=5)

  ax.set_title(f"Carte de flux et heatmap des passes d'Arsenal en 1ère mi-temps", fontsize=16, color='white')
  st.pyplot(fig)

    # Passes en deuxième mi-temps
  st.subheader("Carte de flux et heatmap des passes d'Arsenal en 2ème mi-temps")
  passes_xT2 = []
  passes_yT2 = []
  end_xT2 = []
  end_yT2 = []

  for action in data:
      if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Arsenal" and action.get("period", {}) == 2:
            start_loc = action.get("location", [None, None])
            end_loc = action.get("pass", {}).get("end_location", [None, None])
            if start_loc and end_loc:
                passes_xT2.append(start_loc[0])
                passes_yT2.append(start_loc[1])
                end_xT2.append(end_loc[0])
                end_yT2.append(end_loc[1])

  pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
  fig, ax = pitch.draw(figsize=(10, 8))
  fig.set_facecolor('#22312b')

  bins = (6, 4)
  heatmap = pitch.bin_statistic(passes_xT2, passes_yT2, statistic='count', bins=bins)
  pitch.heatmap(heatmap, ax=ax, cmap='Reds', edgecolors='#22312b')

  pitch.flow(passes_xT2, passes_yT2, end_xT2, end_yT2, color='black', arrow_type='same', bins=bins, ax=ax, arrow_length=5)

  ax.set_title(f"Carte de flux et heatmap des passes d'Arsenal en 2ème mi-temps", fontsize=16, color='white')
  st.pyplot(fig)

    # Passes globales
  st.subheader("Carte de flux et heatmap des passes d'Arsenal (Match Entier)")
  passes_xV = []
  passes_yT = []
  end_xV = []
  end_yT = []

  for action in data:
        if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Arsenal":
            start_loc = action.get("location", [None, None])
            end_loc = action.get("pass", {}).get("end_location", [None, None])
            if start_loc and end_loc:
                passes_xV.append(start_loc[0])
                passes_yT.append(start_loc[1])
                end_xV.append(end_loc[0])
                end_yT.append(end_loc[1])

  pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
  fig, ax = pitch.draw(figsize=(10, 8))
  fig.set_facecolor('#22312b')

  bins = (6, 4)
  heatmap = pitch.bin_statistic(passes_xV, passes_yT, statistic='count', bins=bins)
  pitch.heatmap(heatmap, ax=ax, cmap='Reds', edgecolors='#22312b')

  pitch.flow(passes_xV, passes_yT, end_xV, end_yT, color='black', arrow_type='same', bins=bins, ax=ax, arrow_length=5)

  ax.set_title(f"Carte de flux et heatmap des passes d'Arsenal", fontsize=16, color='white')
  st.pyplot(fig)

  
    # Extraire les numéros de maillot
  jersey_numbers = {}
  for action in data:
        if action["type"]["name"] == "Starting XI" and action["team"]["name"] == "Arsenal":
            lineup = action["tactics"]["lineup"]
            for player in lineup:
                player_name = player["player"]["name"]
                jersey_number = player["jersey_number"]
                jersey_numbers[player_name] = jersey_number

  jersey_numbers["Joel Nathaniel Campbell Samuels"] = 28
  jersey_numbers["Olivier Giroud"] = 12
  jersey_numbers["Matthieu Flamini"] = 20

    # Traiter les positions des joueurs et les passes
  player_positions = {}
  pass_counts = {}

  for action in data:
        if action["type"]["name"] == "Pass" and action["team"]["name"] == "Arsenal":
            passer = action["player"]["name"]
            recipient = action.get("pass", {}).get("recipient", {}).get("name")
            start_loc = action.get("location")
            end_loc = action.get("pass").get("end_location")
            
            if recipient and end_loc:
                if passer not in player_positions:
                    player_positions[passer] = []
                player_positions[passer].append(start_loc)

                pair = (passer, recipient)
                if pair not in pass_counts:
                    pass_counts[pair] = 0
                pass_counts[pair] += 1

    # Calculer les positions moyennes des joueurs
  average_positions = {
        player: np.mean(pos, axis=0) for player, pos in player_positions.items()
    }

    # Créer le graphe de passes
  G = nx.DiGraph()

  for (passer, recipient), count in pass_counts.items():
        G.add_edge(passer, recipient, weight=count)

    # Fonction pour dessiner le graphique
  
  def plot_pass_network():
      pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
      fig, ax = pitch.draw(figsize=(10, 8))
      fig.set_facecolor('#22312b')

    # Afficher les joueurs et leurs positions
      for player, pos in average_positions.items():
        jersey_number = jersey_numbers.get(player, "??")
        ax.scatter(pos[0], pos[1], s=500, c='red', edgecolors='black', zorder=5)
        ax.text(pos[0], pos[1], str(jersey_number), fontsize=10, color='white', ha='center', zorder=6)

    # Tracer les passes
      for edge in G.edges(data=True):
        passer, recipient, attr = edge
        weight = attr['weight']

        # Vérifier si le destinataire a une position dans average_positions
        if recipient in average_positions:
            start_pos = average_positions[passer]
            end_pos = average_positions[recipient]
            ax.plot(
                [start_pos[0], end_pos[0]],
                [start_pos[1], end_pos[1]],
                color='white',
                linewidth=weight,
                alpha=0.7,
            )

      ax.set_title("Réseau de passes d'Arsenal (par numéro)", fontsize=16, color='white')
      return fig

    # Streamlit UI
  st.title("Réseau de passes d'Arsenal")
  st.write("Position moyennes des joueurs et réseau de passes (remplacents inclus)")

    # Afficher le graphique
  fig = plot_pass_network()
  st.pyplot(fig)

    # Variables pour les tirs
  tirArsenalBut = 0
  tirArsenal = 0

  tir_success = []
  tir_failed = []

    # Filtrer les actions pour les tirs d'Arsenal
  for action in data:
        if (
            action.get("type", {}).get("name") == "Shot" and 
            action.get("team", {}).get("name") == "Arsenal"
        ):
            start_location = action.get("location", [None, None])
            end_location = action.get("shot", {}).get("end_location", [None, None])
            
            if start_location and end_location:
                if action.get("shot", {}).get("outcome", {}).get("name") == "Goal":
                    tir_success.append((start_location, end_location))
                    tirArsenalBut += 1
                else:
                    tir_failed.append((start_location, end_location))
                    tirArsenal += 1

    # Création du visuel du terrain
  st.title("Visualisation des tirs d'Arsenal")
  pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
  fig, ax = pitch.draw(figsize=(10, 8))
  fig.set_facecolor('#22312b')

    # Ajouter les flèches des tirs
  for start, end in tir_success:
        pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='green', ax=ax)

  for start, end in tir_failed:
        pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='red', ax=ax)

    # Ajouter le titre et afficher le graphique
  ax.set_title("Tirs d'Arsenal (vert : buts, rouge : échoués)", fontsize=16, color='white')
  st.pyplot(fig)

    # Affichage des statistiques
  st.subheader("Statistiques des tirs d'Arsenal")
  st.write(f"Nombre total de tirs : {tirArsenalBut + tirArsenal}")
  st.write(f"Tirs réussis (buts) : {tirArsenalBut}")
  st.write(f"Tirs échoués : {tirArsenal}")

  # Liste des joueurs d'Arsenal
  arsenal_players = []
  for action in data:
      if action["team"]["name"] == "Arsenal" and "tactics" in action:
          for joueur in action["tactics"]["lineup"]:
              nom = joueur["player"]["name"]
              numero = joueur.get("jersey_number")
              poste = joueur["position"]["name"]
              arsenal_players.append({"name": nom, "number": numero, "position": poste})
    
    

    # Fonction pour afficher les statistiques du joueur sélectionné
  def display_player_stats(player):
        st.write(f"### Statistiques pour {player['name']}")
        st.write(f"**Poste :** {player['position']}")
        st.write(f"**Numéro de maillot :** {player['number']}")

        # Affichage de la heatmap
        st.subheader(f"**Heatmap de {player['name']} :**")
        plot_heatmap(player['name'])

        # Affichage des conduites de balle
        st.subheader(f"**Conduites de balle de {player['name']} :**")
        plot_ball_carries(player['name'])

    # Fonction pour générer la heatmap
  def plot_heatmap(player_name):
        heatmap_cmap = LinearSegmentedColormap.from_list("heatmap_cmap", ["yellow", "red"])
        
        # Récupère les positions du joueur
        player_positions_x = []
        player_positions_y = []
        
        for action in data:
            if action.get("player", {}).get("name") == player_name:
                if "location" in action:
                    player_positions_x.append(action["location"][0])
                    player_positions_y.append(action["location"][1])

        # Créer la carte
        pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 8))
        fig.set_facecolor('#22312b')
        
        pitch.kdeplot(player_positions_x, player_positions_y, ax=ax, shade=True, levels=100, cmap=heatmap_cmap)
        plt.title(f"Carte de chaleur de {player_name}", fontsize=16, color='white')

        # Affichage dans Streamlit
        st.pyplot(fig)

    # Fonction pour afficher les conduites de balle
  def plot_ball_carries(player_name):
        carries_x_start = []
        carries_y_start = []
        carries_x_end = []
        carries_y_end = []

        for action in data:
            if action.get("type", {}).get("name") == "Carry" and action.get("player", {}).get("name") == player_name:
                start_loc = action.get("location", [None, None])
                end_loc = action.get("carry", {}).get("end_location", [None, None])
                if start_loc and end_loc:
                    carries_x_start.append(start_loc[0])
                    carries_y_start.append(start_loc[1])
                    carries_x_end.append(end_loc[0])
                    carries_y_end.append(end_loc[1])

        # Graphique des conduites de balle
        pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 8))
        fig.set_facecolor('#22312b')

        pitch.scatter(carries_x_start, carries_y_start, color='red', s=50, edgecolors='black', ax=ax, label='Départ')

        for i in range(len(carries_x_start)):
            pitch.lines(carries_x_start[i], carries_y_start[i],
                        carries_x_end[i], carries_y_end[i],
                        lw=2, color='blue', comet=True, ax=ax)

        plt.title(f"Conduites de balle de {player_name}", fontsize=16, color='white')
        
        # Affichage dans Streamlit
        st.pyplot(fig)
        

    # Créer un sélecteur déroulant pour choisir un joueur d'Arsenal
  selected_player_name = st.selectbox("Choisissez un joueur d'Arsenal", [player["name"] for player in arsenal_players], key="arsenal_player_select")

    # Trouver le joueur sélectionné dans la liste des joueurs
  selected_player = next(player for player in arsenal_players if player["name"] == selected_player_name)

    # Lorsque l'utilisateur sélectionne un joueur, afficher ses stats
  if selected_player:
        display_player_stats(selected_player)

    # Exemple de génération de statistiques pour les passes
  def plot_passes(player_name, passes_data):
        passes_success = []
        passes_failed = []
        
        for action in passes_data:
            if action.get("type", {}).get("name") == "Pass" and action.get("player", {}).get("name") == player_name:
                start_location = action.get("location", [None, None])
                end_location = action.get("pass", {}).get("end_location", [None, None])
                if start_location and end_location:
                    if action.get("pass", {}).get("outcome", {}).get("name") == "Incomplete":
                        passes_failed.append((start_location, end_location))
                    else:
                        passes_success.append((start_location, end_location))

        # Affichage sur le terrain
        pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
        fig, ax = pitch.draw(figsize=(10, 8))
        fig.set_facecolor('#22312b')

        for start, end in passes_success:
            pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='green', ax=ax)

        for start, end in passes_failed:
            pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='red', ax=ax)

        plt.title(f"Passes de {player_name} (vert : réussies, rouge : incomplètes)", fontsize=16, color='white')
        st.pyplot(fig)

    # Exemple d'affichage des passes pour un joueur
  plot_passes(selected_player_name, data)



  passesA = []
  for action in data:
        if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Arsenal":
            passer = action.get("player", {}).get("name")
            receiver = action.get("pass", {}).get("recipient", {}).get("name")
            if passer and receiver:
                passesA.append((passer, receiver))

    # Créer un DataFrame des passes
  df = pd.DataFrame([], columns=["passer", "receiver", "count"])
  compteur_passesA = Counter(passesA)
  for i, ((passer, receiver), count) in enumerate(compteur_passesA.most_common()):
      df.loc[i] = [passer, receiver, count]

  # Interface utilisateur Streamlit
  st.title("Analyse des passes des joueurs d'Arsenal")


  # Filtrer les données pour le joueur sélectionné
  df_joueur = df[df["passer"] == selected_player_name]

  # Afficher les données des passes du joueur
  st.write(f"### Passes réalisées par **{selected_player_name}**")
  st.dataframe(df_joueur)

  # Fonction pour afficher les passes sur un terrain
  def plot_passes(player_name, passes_data):
      passes_success = []
      passes_failed = []

      for action in passes_data:
          if action.get("type", {}).get("name") == "Pass" and action.get("player", {}).get("name") == player_name:
              start_location = action.get("location", [None, None])
              end_location = action.get("pass", {}).get("end_location", [None, None])
              if start_location and end_location:
                  if action.get("pass", {}).get("outcome", {}).get("name") == "Incomplete":
                      passes_failed.append((start_location, end_location))
                  else:
                      passes_success.append((start_location, end_location))

      # Affichage des passes sur le terrain
      pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
      fig, ax = pitch.draw(figsize=(10, 8))
      fig.set_facecolor('#22312b')

      for start, end in passes_success:
          pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='green', ax=ax)

      for start, end in passes_failed:
          pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='red', ax=ax)

      plt.title(f"Passes de {player_name} (vert : réussies, rouge : incomplètes)", fontsize=16, color='white')
      st.pyplot(fig)

  # Afficher les passes sur le terrain pour le joueur sélectionné
  plot_passes(selected_player_name, data)














if menu == "Match":
    st.header("Vue d'ensemble du match")
    
    # Statistiques de passes
    st.subheader("Statistiques de passes")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Passes totales - Arsenal", passes_ars)
        st.metric("Passes réussies - Arsenal", passes_ars_success)
        st.metric("Taux de réussite - Arsenal", f"{pourcentage_ars}%")
    with col2:
        st.metric("Passes totales - Tottenham", passes_tot)
        st.metric("Passes réussies - Tottenham", passes_tot_success)
        st.metric("Taux de réussite - Tottenham", f"{pourcentage_Tot}%")

    # Affichage des buts
    st.subheader("Buts marqués")
    if buts:
        for i, but in enumerate(buts):
            st.write(f"- **Minute {but['minute']}** : {but['player']['name']} ({but['team']['name']}) avec un xG de {but['shot']['statsbomb_xg']:.2f}")
            fig = plot_goal(but, i + 1)
            st.pyplot(fig)
    else:
        st.write("Aucun but marqué durant ce match.") 




















if menu == "Joueurs Stars": 


    # Configuration de l'interface Streamlit
    st.title("Analyse des performances des joueurs")
    st.sidebar.header("Options")
    players = st.sidebar.multiselect(
      "Sélectionnez les joueurs à analyser :", 
      ["Harry Kane", "Alexis Alejandro Sánchez Sánchez"],  
      default=["Harry Kane"]
    )

    # Initialisation des données
    positions = {player: {"x": [], "y": []} for player in players}
    key_passes = {player: {"start_x": [], "start_y": [], "end_x": [], "end_y": []} for player in players}
    shots = {player: {"x": [], "y": []} for player in players}
    goals = {player: {"x": [], "y": []} for player in players}

    # Analyse des données (remplacez "data" par vos données JSON)
    for action in data:  # Assurez-vous que "data" est défini
      player = action.get("player", {}).get("name")
      action_type = action.get("type", {}).get("name")
      location = action.get("location", [None, None])
      pass_data = action.get("pass", {})
      shot_data = action.get("shot", {})

      if player in players:
          if location[0] is not None and location[1] is not None:
              positions[player]["x"].append(location[0])
              positions[player]["y"].append(location[1])

          if action_type == "Pass" and (pass_data.get("goal_assist") or pass_data.get("assisted_shot_id")):
              key_passes[player]["start_x"].append(location[0])
              key_passes[player]["start_y"].append(location[1])
              key_passes[player]["end_x"].append(pass_data.get("end_location", [None, None])[0])
              key_passes[player]["end_y"].append(pass_data.get("end_location", [None, None])[1])

          if action_type == "Shot":
              shots[player]["x"].append(location[0])
              shots[player]["y"].append(location[1])
              if shot_data.get("goal"):
                  goals[player]["x"].append(location[0])
                  goals[player]["y"].append(location[1])

    # Visualisation Streamlit
    for player in players:
      st.subheader(f"Analyse pour {player}")

      # Création du terrain
      pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
      fig, ax = pitch.draw(figsize=(10, 6))

      # Carte de chaleur
      if positions[player]["x"] and positions[player]["y"]:
          pitch.kdeplot(
              positions[player]["x"], positions[player]["y"], ax=ax,
              shade=True, levels=50, cmap='Blues' if player == "Harry Kane" else 'Reds', alpha=0.7
          )

      # Passes clés
      if key_passes[player]["start_x"] and key_passes[player]["start_y"]:
          pitch.arrows(
              key_passes[player]["start_x"], key_passes[player]["start_y"],
              key_passes[player]["end_x"], key_passes[player]["end_y"],
              ax=ax, color='yellow', width=2, headwidth=10, headlength=10, label='Passes clés'
          )

      # Tirs
      if shots[player]["x"] and shots[player]["y"]:
          pitch.scatter(
              shots[player]["x"], shots[player]["y"], ax=ax, color='white', edgecolors='black',
              zorder=3, s=100, label='Tirs'
          )

      # Buts
      if goals[player]["x"] and goals[player]["y"]:
          pitch.scatter(
              goals[player]["x"], goals[player]["y"], ax=ax, color='gold', edgecolors='black',
              zorder=4, s=150, label='Buts', marker='*'
          )

      # Ajout de la légende et du titre
      ax.legend(loc='upper left', fontsize=9, frameon=False)
      ax.set_title(f"Carte de chaleur, passes clés, tirs et buts - {player}", fontsize=14, color='black')

      # Affichage dans Streamlit
      st.pyplot(fig)
      
  
  #   streamlit run "/Users/Utilisateur/Documents/ARSTOTStreamlit Arsenal Tottenham.py"