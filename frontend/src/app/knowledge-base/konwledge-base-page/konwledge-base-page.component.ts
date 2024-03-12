import { Component } from '@angular/core';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTreeModule } from '@angular/material/tree';
import { DirectoryItem, KnowledgeBaseService } from '../knowledge-base.service';
import { FlatTreeControl } from '@angular/cdk/tree';
import { DynamicDataSource } from '../../utils/DynamicTree';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-konwledge-base-page',
  standalone: true,
  imports: [MatTreeModule, MatButtonModule, MatIconModule, MatProgressBarModule, CommonModule],
  templateUrl: './konwledge-base-page.component.html',
  styleUrl: './konwledge-base-page.component.css'
})
export class KonwledgeBasePageComponent {

    treeControl: FlatTreeControl<DirectoryItem>;
    dataSource: DynamicDataSource<DirectoryItem>;

    constructor(private service: KnowledgeBaseService) {
        this.treeControl = new FlatTreeControl<DirectoryItem>(
            node => node.level,
            node => !node.isLeaf
        );
        this.dataSource = new DynamicDataSource(this.treeControl, service.getChildren.bind(service));
        service.getChildren().subscribe(data => this.dataSource.data = data);
    }

    open(node: DirectoryItem) {
        console.log(node);
    }

}
