import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { GraphVisualizerComponent } from '../graph-visualizer/graph-visualizer.component';

interface Result {
  status: string;
  data?: {
    path: [string, string][];
    adj_matrix: number[][];
    node_labels: string[];
    total_cost: number;
  }
}

@Component({
  selector: 'app-shortest-path',
  standalone: true,
  imports: [CommonModule, FormsModule, DecimalPipe, GraphVisualizerComponent],
  templateUrl: './shortest-path.component.html'
})
export class ShortestPathComponent implements OnInit {
  nodeInput: string = '';
  nodes: string[] = [];
  adjacencyMatrix: number[][] = [];
  source: string = '';
  target: string = '';
  result: Result | null = null;
  shortestPath: number[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {}

  addNode() {
    if (this.nodeInput && !this.nodes.includes(this.nodeInput)) {
      this.nodes.push(this.nodeInput);
      
      // Mettre à jour la matrice d'adjacence
      this.adjacencyMatrix.push(new Array(this.nodes.length).fill(0));
      for (let i = 0; i < this.adjacencyMatrix.length - 1; i++) {
        this.adjacencyMatrix[i].push(0);
      }
      
      this.nodeInput = '';
    }
  }

  removeNode(index: number) {
    this.nodes.splice(index, 1);
    
    // Mettre à jour la matrice d'adjacence
    this.adjacencyMatrix.splice(index, 1);
    for (let row of this.adjacencyMatrix) {
      row.splice(index, 1);
    }

    // Réinitialiser source et target si le nœud supprimé était sélectionné
    if (this.source === this.nodes[index]) this.source = '';
    if (this.target === this.nodes[index]) this.target = '';
  }

  updateMatrix(i: number, j: number, value: string) {
    const numValue = parseFloat(value);
    if (!isNaN(numValue) && numValue >= 0) {
      this.adjacencyMatrix[i][j] = numValue;
    }
  }

  generateRandom() {
    // Réinitialiser d'abord
    this.resetAll();

    // Générer un nombre aléatoire de nœuds (entre 4 et 8)
    const numNodes = Math.floor(Math.random() * 5) + 4;
    
    // Créer les nœuds avec des lettres
    for (let i = 0; i < numNodes; i++) {
      const nodeName = String.fromCharCode(65 + i); // A, B, C, ...
      this.nodes.push(nodeName);
      
      // Ajouter une nouvelle ligne à la matrice
      this.adjacencyMatrix.push(new Array(i + 1).fill(0));
      
      // Compléter les lignes précédentes avec une nouvelle colonne
      for (let j = 0; j < i; j++) {
        this.adjacencyMatrix[j].push(0);
      }
    }

    // Générer des arcs aléatoires (densité d'environ 40%)
    const numEdges = Math.floor((numNodes * (numNodes - 1) / 2) * 0.4);
    let edgesAdded = 0;

    while (edgesAdded < numEdges) {
      const i = Math.floor(Math.random() * numNodes);
      const j = Math.floor(Math.random() * numNodes);
      
      // Éviter les boucles et les arcs déjà existants
      if (i !== j && this.adjacencyMatrix[i][j] === 0) {
        // Générer un poids entre 1 et 10
        const weight = Math.floor(Math.random() * 10) + 1;
        this.adjacencyMatrix[i][j] = weight;
        edgesAdded++;
      }
    }

    // Sélectionner aléatoirement source et destination
    do {
      const sourceIndex = Math.floor(Math.random() * numNodes);
      const targetIndex = Math.floor(Math.random() * numNodes);
      if (sourceIndex !== targetIndex) {
        this.source = this.nodes[sourceIndex];
        this.target = this.nodes[targetIndex];
        break;
      }
    } while (true);
  }

  onSubmit() {
    const graph: { [key: string]: { [key: string]: number } } = {};

    // Convertir la matrice d'adjacence en format de graphe
    this.nodes.forEach((node, i) => {
      graph[node] = {};
      this.nodes.forEach((targetNode, j) => {
        if (this.adjacencyMatrix[i][j] > 0) {
          graph[node][targetNode] = this.adjacencyMatrix[i][j];
        }
      });
    });

    const data = {
      graph: graph,
      source: this.source,
      target: this.target
    };

    this.http.post<Result>('http://localhost:5000/api/solve', data)
      .subscribe({
        next: (response) => {
          console.log('Réponse du serveur:', response);
          this.result = response;
          if (response.status === 'success' && response.data) {
            this.shortestPath = response.data.path.map(p => this.nodes.indexOf(p[0]));
            if (response.data.path.length > 0) {
              this.shortestPath.push(this.nodes.indexOf(response.data.path[response.data.path.length - 1][1]));
            }
          }
        },
        error: (error) => {
          console.error('Erreur:', error);
          alert('Une erreur est survenue lors du calcul du plus court chemin');
        }
      });
  }

  resetAll() {
    this.nodeInput = '';
    this.nodes = [];
    this.adjacencyMatrix = [];
    this.source = '';
    this.target = '';
    this.result = null;
    this.shortestPath = [];
  }

  getPathDisplay(): string {
    if (!this.result?.data?.path || this.result.data.path.length === 0) {
      return '';
    }
    const path = this.result.data.path.map(p => p[0]);
    if (this.result.data.path.length > 0) {
      path.push(this.result.data.path[this.result.data.path.length - 1][1]);
    }
    return path.join(' → ');
  }
} 