import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';
import { GraphVisualizerComponent } from '../graph-visualizer/graph-visualizer.component';

interface TSPResult {
  status: string;
  tour: number[];
  total_distance: number;
  message?: string;
}

@Component({
  selector: 'app-tsp',
  standalone: true,
  imports: [CommonModule, FormsModule, DecimalPipe, GraphVisualizerComponent],
  templateUrl: './tsp.component.html'
})
export class TspComponent implements OnInit {
  cities: string[] = [];
  distances: number[][] = [];
  cityInput: string = '';
  result: TSPResult | null = null;
  loading: boolean = false;

  constructor(private http: HttpClient) {}

  ngOnInit() {}

  addCity() {
    if (this.cityInput.trim() && !this.cities.includes(this.cityInput.trim())) {
      this.cities.push(this.cityInput.trim());
      
      // Mettre à jour la matrice des distances
      if (!this.distances[this.cities.length - 1]) {
        this.distances[this.cities.length - 1] = new Array(this.cities.length).fill(0);
      }
      for (let i = 0; i < this.distances.length; i++) {
        if (!this.distances[i]) {
          this.distances[i] = new Array(this.cities.length).fill(0);
        }
        if (this.distances[i].length < this.cities.length) {
          this.distances[i].push(0);
        }
      }
      
      this.cityInput = '';
    }
  }

  removeCity(index: number) {
    this.cities.splice(index, 1);
    
    // Mettre à jour la matrice des distances
    this.distances.splice(index, 1);
    for (let row of this.distances) {
      row.splice(index, 1);
    }
    
    this.result = null;
  }

  updateDistance(i: number, j: number, value: string) {
    const distance = parseFloat(value);
    if (!isNaN(distance) && distance >= 0) {
      if (!this.distances[i]) {
        this.distances[i] = new Array(this.cities.length).fill(0);
      }
      if (!this.distances[j]) {
        this.distances[j] = new Array(this.cities.length).fill(0);
      }
      this.distances[i][j] = distance;
      this.distances[j][i] = distance; // La matrice est symétrique
      console.log('Matrice des distances mise à jour:', this.distances);
    }
  }

  generateRandomCities() {
    // Réinitialiser d'abord
    this.resetAll();

    // Générer un nombre aléatoire de villes (entre 4 et 8)
    const numCities = Math.floor(Math.random() * 5) + 4;
    
    // Créer les villes
    for (let i = 0; i < numCities; i++) {
      const cityName = String.fromCharCode(65 + i); // A, B, C, ...
      this.cities.push(cityName);
    }

    // Initialiser la matrice des distances
    this.distances = Array(numCities).fill(0).map(() => Array(numCities).fill(0));

    // Générer des distances aléatoires
    for (let i = 0; i < numCities; i++) {
      for (let j = 0; j < i; j++) {
        const distance = Math.floor(Math.random() * 20) + 1; // Distance entre 1 et 20
        this.distances[i][j] = distance;
        this.distances[j][i] = distance; // Matrice symétrique
      }
    }

    console.log('Villes générées:', this.cities);
    console.log('Matrice des distances générée:', this.distances);
  }

  solveTSP() {
    if (this.cities.length < 2) {
      alert('Il faut au moins 2 villes pour résoudre le TSP');
      return;
    }

    // Vérifier que toutes les distances sont remplies
    for (let i = 0; i < this.cities.length; i++) {
      for (let j = 0; j < this.cities.length; j++) {
        if (i !== j && (!this.distances[i] || !this.distances[i][j])) {
          alert('Veuillez remplir toutes les distances entre les villes');
          return;
        }
      }
    }

    this.loading = true;
    console.log('Envoi des données au serveur:', {
      distances: this.distances
    });

    this.http.post<TSPResult>('http://localhost:5001/api/solve-tsp', {
      distances: this.distances
    }).subscribe({
      next: (response) => {
        console.log('Réponse du serveur:', response);
        if (response.status === 'success') {
          this.result = response;
        } else {
          alert(response.message || 'Une erreur est survenue');
        }
        this.loading = false;
      },
      error: (error) => {
        console.error('Erreur:', error);
        alert('Une erreur est survenue lors de la résolution du problème');
        this.loading = false;
      }
    });
  }

  getTourPath(): string {
    if (!this.result || !this.result.tour || !Array.isArray(this.result.tour)) {
      return '';
    }
    // On prend toutes les villes sauf la dernière qui est identique à la première
    const path = this.result.tour.slice(0, -1).map(index => this.cities[index]);
    return path.join(' → ');
  }

  resetAll() {
    this.cities = [];
    this.distances = [];
    this.cityInput = '';
    this.result = null;
  }
} 