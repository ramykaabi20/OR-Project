import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { CommonModule } from '@angular/common';

import { AppComponent } from './app.component';
import { ShortestPathComponent } from './shortest-path/shortest-path.component';
import { TspComponent } from './tsp/tsp.component';
import { GraphVisualizerComponent } from './graph-visualizer/graph-visualizer.component';

const routes: Routes = [
  { path: '', redirectTo: '/shortest-path', pathMatch: 'full' },
  { path: 'shortest-path', component: ShortestPathComponent },
  { path: 'tsp', component: TspComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    ShortestPathComponent,
    TspComponent,
    GraphVisualizerComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { } 