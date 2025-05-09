from gurobipy import Model, GRB, quicksum

def solve_plne_test(capacites, couts_fixes, demandes, couts_transport):
    try:
        centres = list(capacites.keys())
        magasins = list(demandes.keys())

        model = Model("PLNE_test")
        model.setParam('OutputFlag', 0)  # Ne pas afficher les logs

        y = model.addVars(centres, vtype=GRB.BINARY, name="y")
        x = model.addVars(centres, magasins, vtype=GRB.CONTINUOUS, name="x")

        # Fonction objectif
        model.setObjective(
            quicksum(couts_fixes[i] * y[i] for i in centres) +
            quicksum(couts_transport[i, j] * x[i, j] for i in centres for j in magasins if (i, j) in couts_transport),
            GRB.MINIMIZE
        )

        # Contraintes
        for i in centres:
            model.addConstr(quicksum(x[i, j] for j in magasins if (i, j) in couts_transport) <= capacites[i] * y[i])

        for j in magasins:
            model.addConstr(quicksum(x[i, j] for i in centres if (i, j) in couts_transport) >= demandes[j])

        model.optimize()

        if model.status == GRB.OPTIMAL:
            print(f"✅ Coût total optimal : {model.objVal:.2f}")
            for i in centres:
                print(f"Centre {i} ouvert : {int(y[i].x)}")
                for j in magasins:
                    if (i, j) in couts_transport and x[i, j].x > 0:
                        print(f"  Livraison de {x[i, j].x:.2f} de {i} vers {j}")
        else:
            print("❌ Pas de solution optimale trouvée.")

    except Exception as e:
        print(f"Erreur : {str(e)}")

if __name__ == "__main__":
    # Exemple de test
    capacites = {"C1": 100, "C2": 150}
    couts_fixes = {"C1": 500, "C2": 600}
    demandes = {"M1": 80, "M2": 120}
    couts_transport = {
        ("C1", "M1"): 4,
        ("C1", "M2"): 5,
        ("C2", "M1"): 6,
        ("C2", "M2"): 3,
    }

    solve_plne_test(capacites, couts_fixes, demandes, couts_transport)
