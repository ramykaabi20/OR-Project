import { Routes } from '@angular/router';
import { ShortestPathComponent } from './shortest-path/shortest-path.component';
import { TspComponent } from './tsp/tsp.component';
import { HomeComponent } from './home/home.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'shortest-path', component: ShortestPathComponent },
  { path: 'tsp', component: TspComponent }
];
