from flask import Flask, request, jsonify
import json

app = Flask(__name__)

ARQUIVO = 'cursos.json'

def ler_dados():
    try:
        with open(ARQUIVO, 'r') as f:
            return json.load(f)
    except:
        return []

def salvar_dados(dados):
    with open(ARQUIVO, 'w') as f:
        json.dump(dados, f, indent=4)

@app.route('/cursos', methods=['POST'])
def criar_curso():
    dados = ler_dados()
    novo = request.json
    novo['id'] = len(dados) + 1
    dados.append(novo)
    salvar_dados(dados)
    return jsonify(novo), 201

@app.route('/cursos', methods=['GET'])
def listar_cursos():
    dados = ler_dados()
    return jsonify(dados)

@app.route('/cursos/<int:id>', methods=['GET'])
def buscar_curso(id):
    dados = ler_dados()
    for curso in dados:
        if curso['id'] == id:
            return jsonify(curso)
    return jsonify({"erro": "Curso não encontrado"}), 404

@app.route('/cursos/<int:id>', methods=['PUT'])
def atualizar_curso(id):
    dados = ler_dados()
    for curso in dados:
        if curso['id'] == id:
            curso.update(request.json)
            salvar_dados(dados)
            return jsonify(curso)
    return jsonify({"erro": "Curso não encontrado"}), 404

@app.route('/cursos/<int:id>', methods=['DELETE'])
def deletar_curso(id):
    dados = ler_dados()
    novos = [c for c in dados if c['id'] != id]
    if len(dados) == len(novos):
        return jsonify({"erro": "Curso não encontrado"}), 404
    salvar_dados(novos)
    return jsonify({"mensagem": "Curso removido com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
