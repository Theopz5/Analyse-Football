# %% [markdown]
# Antoine Kaczmarek, Etudiant en Master 1 IEAP 
# 
# Fonction principales pour l'analyse

# %%
# Composition des équipes 

import requests
import matplotlib.pyplot as plt
from matplotlib import rcParams

from mplsoccer import Pitch, VerticalPitch, FontManager, Sbopen
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.colors import LinearSegmentedColormap

from collections import Counter


reponse = requests.get("https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/events/16073.json")
if reponse.status_code == 200:
  data= reponse.json()
  print(len(list(data)), "eAenements")
  
for action in data:
  if action["team"]["name"]=="Atlético Madrid" and "tactics" in action:
      compo= action["tactics"]["formation"]
      equipe= action["team"]["name"]
      lineup= action["tactics"]["lineup"]
      
      print(f"Equipe : {equipe}")
      print(f"composition : {compo}")
      print("-"*30)
      
      for joueurs in lineup:
        nom = joueurs["player"]["name"]
        numero = joueurs.get("jersey_number")
        poste= joueurs["position"]["name"]
        
        print(f"{nom}")
        print(f"Poste : {poste}")
        print(f"N°: {numero}")
        print("-"*30)

        print("="*30)    
        
      break
     
  for action in data:
    if action["team"]["name"]=="Barcelona" and "tactics" in action:
      compo= action["tactics"]["formation"]
      equipe= action["team"]["name"]
      lineup= action["tactics"]["lineup"]
      
      print(f"Equipe : {equipe}")
      print(f"composition : {compo}")
      print("-"*30)
      
      for joueurs in lineup:
        nom = joueurs["player"]["name"]
        numero = joueurs.get("jersey_number")
        poste= joueurs["position"]["name"]
        
        print(f"{nom}")
        print(f"Poste : {poste}")
        print(f"N°: {numero}")
        print("-"*30) 
      
      break

# %% [markdown]
# Passes des joueurs

# %%
passesatl = 0
passesatlR = 0
passesbarcelone = 0
passesbarceloneR = 0


for action in data:
    if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Atlético Madrid":
        passesatl += 1
    elif action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Barcelona":
        passesbarcelone += 1


for action in data:
    if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Atlético Madrid":
        if action.get("pass", {}).get("outcome", {}).get("name") == "Incomplete":
            passesatlR += 1
    elif action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Barcelona":
        if action.get("pass", {}).get("outcome", {}).get("name") == "Incomplete":
            passesbarceloneR += 1


passesatl_success = passesatl - passesatlR
passesbarcelone_success = passesbarcelone - passesbarceloneR


pourcentage_atl = round((passesatl_success * 100 / passesatl), 1) if passesatl > 0 else 0
pourcentage_bar = round((passesbarcelone_success * 100 / passesbarcelone), 1) if passesbarcelone > 0 else 0


print("Nombre de passes total Barcelone :", passesbarcelone)
print("Nombre de passes réussies Barcelone :", passesbarcelone_success)
print("Nombre de passes total Atlético Madrid :", passesatl)
print("Nombre de passes réussies Atlético Madrid :", passesatl_success)
print("Pourcentage de réussite Barcelone :", pourcentage_bar, "%")
print("Pourcentage de réussite Atlético Madrid :", pourcentage_atl, "%")


# passes des joueurs
Playername = [
    "Jan Oblak"]


passeReussigc = 0
passerateGC = 0


passes_successGC1 = []  
passes_failedGC1 = [] 


for action in data:
    if (
        action.get("type", {}).get("name") == "Pass" and 
        action.get("player", {}).get("name") in Playername and
        action.get("period", {}) == 1
    ):
        start_location = action.get("location", [None, None])
        end_location = action.get("pass", {}).get("end_location", [None, None])
        
        if start_location and end_location:
            if action.get("pass", {}).get("outcome", {}).get("name") == "Incomplete":
                passes_failedGC1.append((start_location, end_location))
            else:
                passes_successGC1.append((start_location, end_location))


pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
fig, ax = pitch.draw(figsize=(10, 8))
fig.set_facecolor('#22312b')

for start, end in passes_successGC1:
    pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='green', ax=ax)

for start, end in passes_failedGC1:
    pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='red', ax=ax)

plt.title("Passes du gardien ATL en 1ère mi-temps (vert : réussies, rouge : incomplètes)", fontsize=16, color='white')
plt.show()


passerateGC2 = []  
passes_failedGC2 = [] 

for action in data:
    if (
        action.get("type", {}).get("name") == "Pass" and 
        action.get("player", {}).get("name") in Playername and
        action.get("period", {}) == 2
    ):
        start_location = action.get("location", [None, None])
        end_location = action.get("pass", {}).get("end_location", [None, None])
        
        if start_location and end_location:
            if action.get("pass", {}).get("outcome", {}).get("name") == "Incomplete":
                passes_failedGC2.append((start_location, end_location))
            else:
                passerateGC2.append((start_location, end_location))

pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
fig, ax = pitch.draw(figsize=(10, 8))
fig.set_facecolor('#22312b')

for start, end in passerateGC2:
    pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='green', ax=ax)

for start, end in passes_failedGC2:
    pitch.arrows(start[0], start[1], end[0], end[1], width=2, headwidth=5, headlength=5, color='red', ax=ax)

plt.title("Passes du gardien ATL en 2ème mi-temps (vert : réussies, rouge : incomplètes)", fontsize=16, color='white')
plt.show()

# %% [markdown]
# Flux et Heatmap des passes 

# %%
# Milieux de terrain de l'Atlético Madrid
midfielders_atletico = [
    "Jorge Resurrección Merodio", "Rodrigo Hernández Cascante", "Saúl Ñíguez Esclapez", "Thomas Lemar"
]

# Tout le match
for midfielder in midfielders_atletico:
    passes_xB = []
    passes_yB = []
    end_xB = []
    end_yB = []

    for action in data:
        if action.get("type", {}).get("name") == "Pass" and action.get("team", {}).get("name") == "Atlético Madrid":
            passer = action.get("player", {}).get("name")
            if passer == midfielder:
                start_loc = action.get("location", [None, None])
                end_loc = action.get("pass", {}).get("end_location", [None, None])
                if start_loc and end_loc:
                    passes_xB.append(start_loc[0])
                    passes_yB.append(start_loc[1])
                    end_xB.append(end_loc[0])
                    end_yB.append(end_loc[1])

    # Création de la carte
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
    fig, ax = pitch.draw(figsize=(10, 8))
    fig.set_facecolor('#22312b')

    bins = (6, 4)
    heatmap = pitch.bin_statistic(passes_xB, passes_yB, statistic='count', bins=bins)
    pitch.heatmap(heatmap, ax=ax, cmap='Blues', edgecolors='#22312b')

    pitch.flow(passes_xB, passes_yB, end_xB, end_yB, color='black', arrow_type='same', bins=bins, ax=ax, arrow_length=5)

    plt.title(f"Carte de flux et heatmap des passes de {midfielder}", fontsize=16, color='white')
    plt.show()

# %% [markdown]
# Heat map

# %%
position_x_filipe = []
position_y_filipe = []

for action in data:
    player = action.get("player", {}).get("name")
    loc = action.get("location", [None, None])
    
    if player == "Filipe Luís Kasmirski" and loc:
        position_x_filipe.append(loc[0])
        position_y_filipe.append(loc[1])

pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='white')
fig, ax = pitch.draw(figsize=(12, 8))
fig.set_facecolor('#22312b')

heatmap_cmap = LinearSegmentedColormap.from_list("heatmap_cmap", ["yellow", "red"])

pitch.kdeplot(position_x_filipe, position_y_filipe, ax=ax, shade=True, levels=100, cmap=heatmap_cmap)

plt.title("Carte de chaleur - Filipe Luís Kasmirski", fontsize=16, color='white')
plt.show()

# %% [markdown]
# Xg

# %%
xgAtlético_Madrid = []
xgbarcelone = []

xg_cumsum_Atlético_Madrid = {minute: 0 for minute in range(1, 121)} 
xg_cumsum_barcelone = {minute: 0 for minute in range(1, 121)}  
    
for action in data:
        if action.get("type", {}).get("name") == "Shot":
            team_name = action.get("team", {}).get("name")
            xg = action.get("shot", {}).get("statsbomb_xg", 0)
            minute = action.get("minute", 0)

            
            if team_name == "Atlético Madrid" and 1 <= minute <= 120:
                xg_cumsum_Atlético_Madrid[minute] += xg
            elif team_name == "Barcelona" and 1 <= minute <= 120:
                xg_cumsum_barcelone[minute] += xg

    
cumsum_Atlético_Madrid = np.cumsum(list(xg_cumsum_Atlético_Madrid.values()))[:-1]  
cumsum_barcelone = np.cumsum(list(xg_cumsum_barcelone.values()))[:-1]  

plt.figure(figsize=(12, 6))

Atlético_Madrid_line, = plt.plot(
        list(xg_cumsum_Atlético_Madrid.keys())[:-1],  cumsum_Atlético_Madrid,label="Atlético Madrid", color="blue", linewidth=2)
    
    
barcelone_line, = plt.plot(
        list(xg_cumsum_barcelone.keys())[:-1],  cumsum_barcelone,  label="Barcelona",  color="red",  linewidth=2)

for i in range(0, 120, 10): 
        if i < len(cumsum_Atlético_Madrid):  
            plt.text(i, cumsum_Atlético_Madrid[i], f"{cumsum_Atlético_Madrid[i]:.2f}", fontsize=10, color='black', ha='center')
        if i < len(cumsum_barcelone): 
            plt.text(i, cumsum_barcelone[i], f"{cumsum_barcelone[i]:.2f}", fontsize=10, color='red', ha='center')

    
plt.title("Expected Goals cumulés : Atlético Madrid (bleu) vs. Barcelone (rouge)", fontsize=16)
plt.xlabel("Minute", fontsize=12)
plt.ylabel("xG cumulés", fontsize=12)
plt.legend(title="Équipes", loc="upper left", fontsize=12)
plt.grid(color="white", linestyle="--", linewidth=0.5)
plt.show()


