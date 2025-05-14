from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
from gurobipy import Model, GRB, quicksum

app = Flask(__name__)
CORS(app)

def solve_shortest_path(graph_data, source, target):
    model = Model("PlusCourtChemin")
    nodes = list(graph_data.keys())
    arcs = [(i,j) for i in nodes for j in graph_data[i]]

    # Matrice d'adjacence
    adj = np.zeros((len(nodes), len(nodes)))
    for i in nodes:
        for j in graph_data[i]:
            adj[nodes.index(i)][nodes.index(j)] = graph_data[i][j]

    x = model.addVars(arcs, vtype=GRB.BINARY)

    # Objectif
    model.setObjective(quicksum(graph_data[i][j]*x[i,j] for (i,j) in arcs), GRB.MINIMIZE)

    # Contraintes
    model.addConstr(quicksum(x[source,j] for j in graph_data[source]) == 1)
    model.addConstr(quicksum(x[j,target] for j in nodes if target in graph_data[j]) == 1)

    for i in nodes:
        if i not in [source, target]:
            model.addConstr(
                quicksum(x[i,j] for j in graph_data[i]) -
                quicksum(x[j,i] for j in nodes if i in graph_data[j]) == 0
            )

    model.optimize()

    path = []
    if model.status == GRB.OPTIMAL:
        current = source
        while current != target:
            for j in graph_data[current]:
                if x[current,j].x > 0.5:
                    path.append((current, j))
                    current = j
                    break

    return {
        "path": path,
        "adj_matrix": adj.tolist(),
        "node_labels": nodes,
        "total_cost": model.ObjVal
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/solve', methods=['POST'])
def api_solve():
    data = request.json
    try:
        result = solve_shortest_path(
            data['graph'],
            data['source'],
            data['target']
        )
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
