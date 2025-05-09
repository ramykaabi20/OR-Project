from gurobipy import Model, GRB, quicksum

def test_modele_transport():
    # Données
    fournisseurs = ['F1', 'F2']
    clients = ['C1', 'C2']
    offre = {'F1': 20, 'F2': 30}
    demande = {'C1': 10, 'C2': 40}
    couts = {
        ('F1', 'C1'): 2, ('F1', 'C2'): 4,
        ('F2', 'C1'): 5, ('F2', 'C2'): 1
    }

    model = Model("transport")
    model.setParam("OutputFlag", 0)

    x = model.addVars(fournisseurs, clients, name="x", lb=0)

    model.setObjective(quicksum(couts[i, j] * x[i, j] for i in fournisseurs for j in clients), GRB.MINIMIZE)

    # Contraintes
    for i in fournisseurs:
        model.addConstr(quicksum(x[i, j] for j in clients) <= offre[i], name=f"offre_{i}")
    for j in clients:
        model.addConstr(quicksum(x[i, j] for i in fournisseurs) >= demande[j], name=f"demande_{j}")

    model.optimize()

    if model.status == GRB.OPTIMAL:
        print("Solution optimale trouvée :")
        for i in fournisseurs:
            for j in clients:
                if x[i, j].X > 0:
                    print(f"Transport de {x[i, j].X} unités de {i} vers {j}")
        print(f"Coût total : {model.ObjVal}")
    else:
        print("Aucune solution optimale trouvée.")

if __name__ == "__main__":
    test_modele_transport()
