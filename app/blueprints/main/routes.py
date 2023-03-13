from flask import render_template,request,jsonify
import requests
from . import main
from app.models import User
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required


@main.route('/')
@login_required
def home():
    users = User.query.all()
    if current_user.is_authenticated:
        following_set = set()

        for user in current_user.followed:
            following_set.add(user)

        for user in users:
            if user in following_set:
                user.isFollowing = True
        
    return render_template('home.html', users=users)

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



@main.route('/pokemon/catch', methods=['POST'])
@login_required
def catch_pokemon():
    user_id = get_current_user_id() # replace with code to get current user ID
    pokemon_name = request.form['pokemon_name'].lower()
    

    user = User.query.get(user_id)
    if len(user.pokemon_owned) >= 5:
        return jsonify({'message': 'You already have 5 Pokemon!'}), 400

    # Check if the user already has this Pokemon in their collection
    pokemon = PokemonCaptured.query.filter_by(name=pokemon_name).first()
    if pokemon:
        return jsonify({'message': 'You already have this Pokemon in your collection!'}), 400
    
    # If the user does not already have the Pokemon, create a new PokemonCaptured object
    new_pokemon = PokemonCaptured(name=pokemon_name)
    
    # Fetch the rest of the Pokemon's details from the PokeAPI
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
    response = requests.get(url)
    if not response.ok:
        error = 'That pokemon is not avaiable in our data'
        return render_template('pokeflex.html', error=error)
   
    data = response.json()
    new_pokemon.ability=data['abilities'][0]['ability']['name']
    new_pokemon.base_experience=data['base_experience']
    new_pokemon.sprite_url=data['sprites']['front_default']
    new_pokemon.attack_base_stat=data['stats'][1]['base_stat']
    new_pokemon.hp_base_stat=data['stats'][0]['base_stat']
    new_pokemon.defense_base_stat=data['stats'][2]['base_stat']
    # Save the new PokemonCaptured object to the database
    new_pokemon.save_to_db()
            
     # Add the new Pokemon to the user's collection
    user = User.query.get(user_id)
    user.pokemon_owned.append(new_pokemon)
    user.save_to_db()
            
    flash(f'You have caught a {pokemon_name}')
    return render_template('catch.html', pokemon=new_pokemon)

# to remove the pokemon from users list 
@main.route('/pokemon/remove', methods=['POST'])
@login_required
def remove_pokemon():
    pokemon_id = request.form['pokemon_id']
    pokemon = PokemonCaptured.query.get(pokemon_id)
    if not pokemon:
        return jsonify({'message': 'Pokemon not found!'}), 404

    user = User.query.get(get_current_user_id())
    if pokemon not in user.pokemon_owned:
        return jsonify({'message': 'You do not own this Pokemon!'}), 403

    user.pokemon_owned.remove(pokemon)
    pokemon.delete_from_db()
    return jsonify({'message': ' you removed successfully Pokemon!'})


@main.route('/users')
@login_required
def list_users():
    current_user = get_current_user_id() # replace with code to get current user ID
    users = User.query.filter(User.id != current_user).all()
    return render_template('users.html', users=users)



#The battle
@main.route('/users/<int:user_id>/battle', methods=['POST'])
@login_required
def battle_user(user_id):
    current_user = get_current_user_id() # replace with code to get current user ID
    user = User.query.get(user_id)
    if not user:
        abort(404)
    
    current_user_pokemon = PokemonCaptured.query.filter_by(user_id=current_user_id).all()
    user_pokemon = PokemonCaptured.query.filter_by(user_id=user_id).all()
   
    # Get the stats and images for each Pokemon
    if request.method == 'POST':
        # Get the user's selected pokemon from the form data
        pokemon_name = request.form['pokemon_name']
        current_user_pokemon_selected = PokemonCaptured.query
                # Get the stats and images for the user's selected pokemon
        url = f"https://pokeapi.co/api/v2/pokemon/{user_pokemon.name}/"
        response = requests.get(url)
        data = response.json()
        user_pokemon_data = {
            'name': user_pokemon.name,
            'ability': data['abilities'][0]['ability']['name'],
            'base_experience': data['base_experience'],
            'sprite_url': data['sprites']['front_default'],
            'attack_base_stat': data['stats'][1]['base_stat'],
            'hp_base_stat': data['stats'][0]['base_stat'],
            'defense_base_stat': data['stats'][2]['base_stat']
        }
        
        # Choose a random pokemon from the other user's collection
        other_user_pokemon = random.choice(user.pokemon_owned)
        
        # Get the stats and images for the other user's selected pokemon
        url = f"https://pokeapi.co/api/v2/pokemon/{other_user_pokemon.name}/"
        response = requests.get(url)
        data = response.json()
        other_user_pokemon_data = {
            'name': other_user_pokemon.name,
            'ability': data['abilities'][0]['ability']['name'],
            'base_experience': data['base_experience'],
            'sprite_url': data['sprites']['front_default'],
            'attack_base_stat': data['stats'][1]['base_stat'],
            'hp_base_stat': data['stats'][0]['base_stat'],
            'defense_base_stat': data['stats'][2]['base_stat']
        }
        
        # Determine the winner of the battle based on base experience
        if user_pokemon_data['base_experience'] > other_user_pokemon_data['base_experience']:
            winner = current_user
        else:
            winner = user
        
        return render_template('battle_results.html', 
                               user_pokemon=user_pokemon_data, 
                               other_user_pokemon=other_user_pokemon_data, 
                               winner=winner)

    else:
        # Get a list of the other user's pokemon for the user to choose from
        other_user_pokemon = user.pokemon_owned
        return render_template('battle.html', other_user_pokemon=other_user_pokemon)



