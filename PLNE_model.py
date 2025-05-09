# probleme_plne.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from gurobipy import Model, GRB, quicksum

class PLNEWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ouverture de Centres (PLNE)")
        self.setGeometry(100, 100, 600, 550)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QLabel { font-weight: bold; }
            QLineEdit, QTextEdit {
                background: #f5f5f5; padding: 6px; border-radius: 4px;
            }
            QPushButton {
                background: #3498db; color: white; padding: 7px; border-radius: 4px;
            }
            QPushButton:hover { background: #2980b9; }
        """)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Capacités des centres (C1:100,C2:150)"))
        self.cap_input = QLineEdit()
        layout.addWidget(self.cap_input)

        layout.addWidget(QLabel("Coûts fixes (C1:500,C2:600)"))
        self.fix_input = QLineEdit()
        layout.addWidget(self.fix_input)

        layout.addWidget(QLabel("Demandes des magasins (M1:80,M2:120)"))
        self.dem_input = QLineEdit()
        layout.addWidget(self.dem_input)

        layout.addWidget(QLabel("Coûts transport (C1-M1:4,C2-M2:3)"))
        self.cost_input = QLineEdit()
        layout.addWidget(self.cost_input)

        self.solve_btn = QPushButton("Résoudre")
        self.solve_btn.clicked.connect(self.solve_model)
        layout.addWidget(self.solve_btn)

        self.result = QTextEdit()
        self.result.setMinimumHeight(200)
        layout.addWidget(self.result)

        self.setLayout(layout)

    def solve_model(self):
        '''
        This function solves the facility location problem using Gurobi
        and displays the result in the QTextEdit widget.
        It reads the input from the QLineEdit widgets, constructs the model,
        and optimizes it. If a solution is found, it formats the output
        and sets it in the QTextEdit widget. If an error occurs, it displays
        the error message.
        The input format for capacities, fixed costs, demands, and transport costs is:
        "C1:100,C2:150" for capacities,
        "C1:500,C2:600" for fixed costs,
        "M1:80,M2:120" for demands,
        "C1-M1:4,C2-M2:3" for transport costs.
        The output format is:
        "Coût total: X.XX" followed by the variable assignments
        and whether each centre is open or not.
        The function uses Gurobi's Model, GRB.BINARY, and GRB.CONTINUOUS
        to define the decision variables and constraints.
        It also uses quicksum to define the objective function.
        The function handles exceptions and displays error messages in the QTextEdit widget.
        '''
        try:
            capacites = dict(x.split(":") for x in self.cap_input.text().split(","))
            couts_fixes = dict(x.split(":") for x in self.fix_input.text().split(","))
            demandes = dict(x.split(":") for x in self.dem_input.text().split(","))
            couts_transport = dict()
            for p in self.cost_input.text().split(","):
                k, v = p.split(":")
                i, j = k.split("-")
                couts_transport[(i.strip(), j.strip())] = float(v)

            centres = list(capacites.keys())
            magasins = list(demandes.keys())

            model = Model("PLNE")
            y = model.addVars(centres, vtype=GRB.BINARY, name="y")
            x = model.addVars(centres, magasins, vtype=GRB.CONTINUOUS, name="x")

            model.setObjective(
                quicksum(float(couts_fixes[i]) * y[i] for i in centres) +
                quicksum(couts_transport[i, j] * x[i, j] for i in centres for j in magasins),
                GRB.MINIMIZE
            )

            for i in centres:
                model.addConstr(quicksum(x[i, j] for j in magasins if (i, j) in couts_transport) <= float(capacites[i]) * y[i])
            for j in magasins:
                model.addConstr(quicksum(x[i, j] for i in centres if (i, j) in couts_transport) >= float(demandes[j]))

            model.optimize()

            if model.status == GRB.OPTIMAL:
                output = f"Coût total: {model.objVal:.2f}\n\n"
                for i in centres:
                    output += f"{i} ouvert: {int(y[i].x)}\n"
                    for j in magasins:
                        if (i, j) in couts_transport and x[i, j].x > 0:
                            output += f"  x[{i},{j}] = {x[i, j].x:.2f}\n"
                self.result.setText(output)
            else:
                self.result.setText("Pas de solution optimale.")

        except Exception as e:
            self.result.setText(f"Erreur : {str(e)}")
