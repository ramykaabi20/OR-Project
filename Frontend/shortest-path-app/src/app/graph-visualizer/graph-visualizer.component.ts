import { Component, OnInit, Input, ElementRef, ViewChild, OnChanges, SimpleChanges } from '@angular/core';
import { Network, DataSet, Node, Edge } from 'vis-network/standalone';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-graph-visualizer',
  standalone: true,
  imports: [CommonModule],
  template: `<div #graphContainer style="height: 400px; border: 1px solid lightgray;"></div>`
})
export class GraphVisualizerComponent implements OnInit, OnChanges {
  @ViewChild('graphContainer', { static: true }) graphContainer!: ElementRef;
  @Input() matrix: number[][] = [];
  @Input() shortestPath: number[] = [];
  @Input() tour: number[] = [];  // Pour le TSP
  @Input() labels: string[] = []; // Labels des nœuds

  private network: Network | null = null;
  private nodes: DataSet<Node> = new DataSet();
  private edges: DataSet<Edge> = new DataSet();

  ngOnInit() {
    const container = this.graphContainer.nativeElement;
    const options = {
      nodes: {
        shape: 'circle',
        size: 30,
        font: {
          size: 20
        }
      },
      edges: {
        arrows: {
          to: { enabled: true }
        },
        font: {
          align: 'middle'
        }
      },
      physics: {
        enabled: true,
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          gravitationalConstant: -50,
          centralGravity: 0.01,
          springLength: 200,
          springConstant: 0.08
        }
      }
    };

    this.network = new Network(container, { nodes: this.nodes, edges: this.edges }, options);
    this.updateGraph();
  }

  ngOnChanges(changes: SimpleChanges) {
    if ((changes['matrix'] || changes['shortestPath'] || changes['tour'] || changes['labels']) && this.network) {
      this.updateGraph();
    }
  }

  private updateGraph() {
    this.nodes.clear();
    this.edges.clear();

    // Add nodes
    for (let i = 0; i < this.matrix.length; i++) {
      this.nodes.add({
        id: i,
        label: this.labels[i] || String(i + 1),
        color: this.isNodeInPath(i) ? '#ff7f50' : '#97c2fc'
      });
    }

    // Add edges
    for (let i = 0; i < this.matrix.length; i++) {
      for (let j = 0; j < this.matrix[i].length; j++) {
        if (this.matrix[i][j] > 0) {
          const isInPath = this.isEdgeInPath(i, j);
          this.edges.add({
            from: i,
            to: j,
            label: String(this.matrix[i][j]),
            color: isInPath ? '#ff7f50' : '#848484',
            width: isInPath ? 3 : 1,
            arrows: this.tour.length > 0 ? 'to' : { to: true }  // Flèches pour TSP ou plus court chemin
          });
        }
      }
    }
  }

  private isNodeInPath(node: number): boolean {
    if (this.tour.length > 0) {
      return this.tour.includes(node);
    }
    return this.shortestPath.includes(node);
  }

  private isEdgeInPath(from: number, to: number): boolean {
    if (this.tour.length > 0) {
      // Pour le TSP
      for (let i = 0; i < this.tour.length - 1; i++) {
        if (this.tour[i] === from && this.tour[i + 1] === to) {
          return true;
        }
      }
    } else {
      // Pour le plus court chemin
      for (let i = 0; i < this.shortestPath.length - 1; i++) {
        if (this.shortestPath[i] === from && this.shortestPath[i + 1] === to) {
          return true;
        }
      }
    }
    return false;
  }
} 