from flask import Flask, request, render_template

app = Flask(__name__)

# Base de datos ficticia de películas
movies = {
    '1': {'title': 'Titanic', 'image': 'https://images-na.ssl-images-amazon.com/images/S/pv-target-images/4721ec145e5bca07fe6a3719a290d053de2c245f26eda14be1ac25ed8476017f._RI_TTW_.jpg', 'description': 'Épica historia de amor y tragedia a bordo del Titanic, el majestuoso transatlántico que se hunde en su fatídico viaje inaugural'},
    '2': {'title': 'El séptimo continente', 'image': 'https://pics.filmaffinity.com/El_saeptimo_continente-231616411-mmed.jpg', 'description': 'Un inquietante retrato de la alienación y la desesperación en la vida moderna. Haneke explora la frialdad humana sin concesiones'},
    '3': {'title': 'Ese oscuro objeto del deseo', 'image': 'https://pics.filmaffinity.com/Ese_oscuro_objeto_del_deseo-767734797-large.jpg', 'description': 'Un enigmático juego de pasión y obsesión, donde el deseo se entrelaza con la locura en esta cautivadora película de Buñuel'},
    '4': {'title': 'Bad Boy Bubby', 'image': 'https://pics.filmaffinity.com/Bad_Boy_Bubby-978690686-large.jpg', 'description': 'Un viaje perturbador y provocativo hacia la redención de un hombre atrapado en un mundo de abuso y aislamiento'},
}

@app.route('/')
def index():
    return render_template('index.html', movies=movies)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    results = []
    for key, value in movies.items():
        if query.lower() in value['title'].lower():
            results.append({'title': value['title'], 'image': value['image']})

    return render_template('search.html', query=query, results=results)



if __name__ == '__main__':
    app.run(debug=True)
