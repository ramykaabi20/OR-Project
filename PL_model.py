from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from gurobipy import Model, GRB, quicksum

class PLWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Problème de Transport (PL)")
        self.setGeometry(100, 100, 600, 500)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QLabel { font-weight: bold; }
            QLineEdit, QTextEdit {
                background: #f0f0f0; padding: 5px; border-radius: 4px;
            }
            QPushButton {
                background: #2ecc71; color: white; padding: 6px; border-radius: 4px;
            }
            QPushButton:hover { background: #27ae60; }
        """)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Fournisseurs (ex: F1:100,F2:150)"))
        self.f_input = QLineEdit()
        layout.addWidget(self.f_input)

        layout.addWidget(QLabel("Clients (ex: C1:80,C2:170)"))
        self.c_input = QLineEdit()
        layout.addWidget(self.c_input)

        layout.addWidget(QLabel("Coûts (ex: F1-C1:4,F2-C2:3)"))
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
        ''' this function solves the transportation problem using Gurobi
        and displays the result in the QTextEdit widget.
        It reads the input from the QLineEdit widgets, constructs the model,
        and optimizes it. If a solution is found, it formats the output
        and sets it in the QTextEdit widget. If an error occurs, it displays
        the error message.
        The input format for suppliers, clients, and costs is:
        "F1:100,F2:150" for suppliers,
        "C1:80,C2:170" for clients,
        "F1-C1:4,F2-C2:3" for costs.
        The output format is:
        "Coût total: X.XX" followed by the variable assignments
        "x[i,j] = value" for each variable with a positive value.
        The function uses the Gurobi Python API to create a model,
        add variables, set the objective function, add constraints,
        and optimize the model. It handles exceptions and displays error messages
        in the result QTextEdit widget.
        '''
        try:
            fournisseurs = dict(x.split(":") for x in self.f_input.text().split(","))
            clients = dict(x.split(":") for x in self.c_input.text().split(","))
            couts = dict()
            for p in self.cost_input.text().split(","):
                k, v = p.split(":")
                i, j = k.split("-")
                couts[(i.strip(), j.strip())] = float(v)

            model = Model("PL")
            x = model.addVars(couts.keys(), name="x", vtype=GRB.CONTINUOUS)

            model.setObjective(quicksum(couts[i, j] * x[i, j] for (i, j) in couts), GRB.MINIMIZE)

            for i in fournisseurs:
                model.addConstr(quicksum(x[i, j] for j in clients if (i, j) in couts) <= float(fournisseurs[i]))

            for j in clients:
                model.addConstr(quicksum(x[i, j] for i in fournisseurs if (i, j) in couts) >= float(clients[j]))

            model.optimize()

            if model.status == GRB.OPTIMAL:
                output = f"Coût total: {model.objVal:.2f}\n\n"
                for var in x.values():
                    if var.x > 0:
                        output += f"{var.VarName} = {var.x:.2f}\n"
                self.result.setText(output)
            else:
                self.result.setText("Pas de solution optimale.")

        except Exception as e:
            self.result.setText(f"Erreur : {str(e)}")
