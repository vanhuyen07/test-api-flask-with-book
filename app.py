from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Book API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Danh sách các cuốn sách
books_list = [
    {'id': 0, 'author': 'chinua achebe', 'language': 'english', 'title': 'things fall apart'},
    {'id': 1, 'author': 'hans christian andersen', 'language': 'danish', 'title': 'fairy tales'},
    {'id': 2, 'author': 'samuel beckett', 'language': 'french,english', 'title': 'molloy,malone dies,the unnamable,the triology'},
    {'id': 3, 'author': 'giovanni boccaccio', 'language': 'italian', 'title': 'the decameron'},
    {'id': 5, 'author': 'emily bront', 'language': 'english', 'title': 'wuthering heights'},
    {'id': 6, 'author': 'jorge luis borges', 'language': 'spanish', 'title': 'ficciones'}
]

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'GET':
        if len(books_list) > 0:
            return jsonify(books_list)
        else:
            return jsonify({'message': 'Nothing found'}), 404

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        ID = books_list[-1]['id'] + 1
        new_obj = {'id': ID, 'author': new_author, 'language': new_lang, 'title': new_title}
        books_list.append(new_obj)
        return jsonify(books_list), 201

@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book)
        return jsonify({'message': 'Book not found'}), 404

    if request.method == 'PUT':
        for book in books_list:
            if book['id'] == id:
                book['author'] = request.form['author']
                book['language'] = request.form['language']
                book['title'] = request.form['title']
                update_book = {'id': id, 'author': book['author'], 'language': book['language'], 'title': book['title']}
                return jsonify(update_book)
        return jsonify({'message': 'Book not found'}), 404

    if request.method == 'DELETE':
        for index, book in enumerate(books_list):
            if book['id'] == id:
                books_list.pop(index)
                return jsonify({'message': 'Book deleted'}), 200
        return jsonify({'message': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port= 5000)
