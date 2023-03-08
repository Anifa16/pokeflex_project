from flask import render_template,request
import requests
from . import main
from flask_login import login_required

@main.route('/')
def home():
   return render_template('home.html')

@main.route('/pokeflex', methods=['GET', 'POST'])
@login_required
def pokeflex():
    pokemon_names = ["bulbasaur", "charmander", "squirtle", "pikachu", "eevee"] # this is my list if my pokemons
    pokemon_data = {} # once I get them from my api url I will store them in pokemon data 
    name = None
    
    if request.method == 'POST':   # this is me checking if a user has enter something 
        name = request.form['name'].lower() 
        if name not in pokemon_names:
            # If the user searches for a pokemon that isn't in our list, display an error message
            print(f'Sorry, {name.capitalize()} is not in our list.')
        else:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
            if response.status_code == 200:
                pokemon_json = response.json()
                abilities = [ability['ability']['name'] for ability in pokemon_json['abilities']]
                sprite_url = pokemon_json['sprites']['front_shiny']
                base_experience = pokemon_json['base_experience']
                attack_base_stat = pokemon_json['stats'][1]['base_stat']
                hp_base_stat = pokemon_json['stats'][0]['base_stat']
                defense_base_stat = pokemon_json['stats'][2]['base_stat']
                
                # Store the data we retrieved for the pokemon the user searched for
                pokemon_data[name] = {
                    "abilities": abilities,
                    "sprite_url": sprite_url,
                    "base_experience": base_experience,
                    "attack_base_stat": attack_base_stat,
                    "hp_base_stat": hp_base_stat,
                    "defense_base_stat": defense_base_stat
                }
            else:
                # If the request was unsuccessful, display an error message
               error = 'That pokemon is not avaiable in our data'
               return render_template('pokeflex.html', error=error)
    
    return render_template('pokeflex.html', pokemon_data=pokemon_data, name=name)



