from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from gurobipy import Model, GRB, quicksum

app = Flask(__name__)
CORS(app)

def solve_tsp(distances):
    n = len(distances)
    model = Model("TSP")
    
    # Variables
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i,j] = model.addVar(vtype=GRB.BINARY, name=f'x_{i}_{j}')
    
    # Variable u pour MTZ
    u = model.addVars(n, lb=0, ub=n-1, vtype=GRB.INTEGER, name='u')
    
    # Objectif
    model.setObjective(
        quicksum(distances[i][j] * x[i,j] for i in range(n) for j in range(n) if i != j),
        GRB.MINIMIZE
    )
    
    # Contraintes
    # Chaque ville doit être visitée une fois
    for j in range(n):
        model.addConstr(quicksum(x[i,j] for i in range(n) if i != j) == 1)
    
    # Partir de chaque ville une fois
    for i in range(n):
        model.addConstr(quicksum(x[i,j] for j in range(n) if i != j) == 1)
    
    # Élimination des sous-tours (MTZ)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                model.addConstr(
                    u[i] - u[j] + n * x[i,j] <= n - 1
                )
    
    model.optimize()
    
    if model.status == GRB.OPTIMAL:
        # Reconstruction du tour
        tour = [0]  # Commencer par la ville 0
        current = 0
        while len(tour) < n:
            for j in range(n):
                if j != current and x[current,j].x > 0.5:
                    tour.append(j)
                    current = j
                    break
        
        return {
            "status": "success",
            "tour": tour,
            "total_distance": model.ObjVal
        }
    else:
        return {
            "status": "error",
            "message": "Pas de solution optimale trouvée"
        }

@app.route('/api/solve-tsp', methods=['POST'])
def api_solve_tsp():
    try:
        data = request.json
        distances = data['distances']
        result = solve_tsp(distances)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == '__main__':
    app.run(port=5001, debug=True) 