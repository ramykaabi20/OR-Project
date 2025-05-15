import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="container mt-5">
      <div class="text-center mb-5">
        <h1 class="display-4">Projet de Recherche Opérationnelle</h1>
        <p class="lead">Année Universitaire 2024-2025 - GL3</p>
      </div>

      <div class="row justify-content-center mb-5">
        <div class="col-md-8">
          <div class="card">
            <div class="card-body">
              <h2 class="card-title text-center mb-4">À Propos du Projet</h2>
              <p class="card-text">
                Ce projet s'inscrit dans le cadre du cours de Recherche Opérationnelle pour la troisième année en Génie Logiciel. 
                Il implémente deux problèmes fondamentaux d'optimisation : le problème du voyageur de commerce (TSP) et le problème 
                du plus court chemin. Notre solution utilise des techniques de programmation linéaire en nombres entiers (PL/PLNE) 
                et propose une interface interactive pour la visualisation et la résolution de ces problèmes.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="row justify-content-center mb-5">
        <div class="col-md-8">
          <div class="card">
            <div class="card-body">
              <h2 class="card-title text-center mb-4">Contributeurs</h2>
              <div class="row text-center">
                <div class="col-md-4 mb-4">
                  <div class="contributor-card">
                    <div class="avatar-circle mb-3">
                      <img src="assets/contributors/rami.jpg" alt="Rami Kaabi" class="contributor-img">
                    </div>
                    <h5>Rami Kaabi</h5>
                    <p class="text-muted">Étudiant GL3</p>
                  </div>
                </div>
                <div class="col-md-4 mb-4">
                  <div class="contributor-card">
                    <div class="avatar-circle mb-3">
                      <img src="assets/contributors/ithar.jpg" alt="Ithar Hadj Amor" class="contributor-img">
                    </div>
                    <h5>Ithar Hadj Amor</h5>
                    <p class="text-muted">Étudiante GL3</p>
                  </div>
                </div>
                <div class="col-md-4 mb-4">
                  <div class="contributor-card">
                    <div class="avatar-circle mb-3">
                      <img src="assets/contributors/maryem.jpg" alt="Maryem Damak" class="contributor-img">
                    </div>
                    <h5>Maryem Damak</h5>
                    <p class="text-muted">Étudiante GL3</p>
                  </div>
                </div>
                <div class="col-md-4 mb-4">
                  <div class="contributor-card">
                    <div class="avatar-circle mb-3">
                      <img src="assets/contributors/mohamed.jpg" alt="Kmiha Mohamed" class="contributor-img">
                    </div>
                    <h5>Kmiha Mohamed</h5>
                    <p class="text-muted">Étudiant GL3</p>
                  </div>
                </div>
                <div class="col-md-4 mb-4">
                  <div class="contributor-card">
                    <div class="avatar-circle mb-3">
                      <img src="assets/contributors/amir.jpg" alt="Mallek Amir" class="contributor-img">
                    </div>
                    <h5>Mallek Amir</h5>
                    <p class="text-muted">Étudiant GL3</p>
                  </div>
                </div>
                <div class="col-md-4 mb-4">
                  <div class="contributor-card">
                    <div class="avatar-circle mb-3">
                      <img src="assets/contributors/moncef.jpg" alt="Moncef Koubaa" class="contributor-img">
                    </div>
                    <h5>Moncef Koubaa</h5>
                    <p class="text-muted">Étudiant GL3</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="d-flex justify-content-center gap-4">
            <a routerLink="/tsp" class="btn btn-primary btn-lg">
              Problème du Voyageur de Commerce
            </a>
            <a routerLink="/shortest-path" class="btn btn-success btn-lg">
              Problème du Plus Court Chemin
            </a>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .contributor-card {
      transition: transform 0.3s ease;
    }
    .contributor-card:hover {
      transform: translateY(-5px);
    }
    .avatar-circle {
      width: 150px;
      height: 150px;
      border-radius: 50%;
      overflow: hidden;
      margin: 0 auto;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .contributor-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  `]
})
export class HomeComponent {} 