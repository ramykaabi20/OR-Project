import { Routes } from '@angular/router';
import { ShortestPathComponent } from './shortest-path/shortest-path.component';
import { TspComponent } from './tsp/tsp.component';

export const routes: Routes = [
  { path: '', redirectTo: '/shortest-path', pathMatch: 'full' },
  { path: 'shortest-path', component: ShortestPathComponent },
  { path: 'tsp', component: TspComponent }
];
