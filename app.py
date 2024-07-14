from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)


tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id= task_id_control, title=data.get('title'), description=data.get('description', ""))
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({
        "message": "Nova Tarefa criada com sucesso",
        "id": new_task.id
    })


@app.route('/tasks', methods=['GET'])
def list_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }
    return jsonify(output)


@app.route('/tasks/<int:id>', methods=['GET'])
def list_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({
        "message": "Não foi possível localizar"
    }), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
def edit_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    if task == None:
        return jsonify({
            "message": "Não foi possível localizar"
        }), 404
    data = request.get_json()
    task.title = data.get('title')
    task.description = data.get('description')
    task.completed = data.get('completed')
    print(task)
    return jsonify({
        "message": "Tarefa atualizada com sucesso"
    })


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    if task == None:
        return jsonify({
            "message": "Não foi possível localizar"
        }), 404
    tasks.remove(task)
    return jsonify({
            "message": "Tarefa deletada com sucesso"
        })

if __name__ == "__main__":
    app.run(debug=True)
