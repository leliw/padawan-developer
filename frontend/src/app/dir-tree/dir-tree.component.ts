import { FlatTreeControl } from '@angular/cdk/tree';
import { Component, EventEmitter, Output } from '@angular/core';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTreeModule } from '@angular/material/tree';
import { DirTreeService, DirTreeItem } from '../dir-tree.service';
import { CommonModule } from '@angular/common';
import { DynamicDataSource } from '../utils/DynamicTree';


@Component({
    selector: 'app-dir-tree',
    standalone: true,
    imports: [MatTreeModule, MatButtonModule, MatIconModule, MatProgressBarModule, CommonModule],
    templateUrl: './dir-tree.component.html',
    styleUrl: './dir-tree.component.css'
})
export class DirTreeComponent {

    @Output() file = new EventEmitter<string>();
    
    treeControl: FlatTreeControl<DirTreeItem>;
    dataSource: DynamicDataSource<DirTreeItem>;

    constructor(service: DirTreeService) {
        this.treeControl = new FlatTreeControl<DirTreeItem>(
            node => node.level,
            node => node.hasChildren
        );
        this.dataSource = new DynamicDataSource(this.treeControl, service.getChildren.bind(service));
        service.initialData().subscribe(data => this.dataSource.data = data);
    }

    openFile(node: DirTreeItem) {
        this.file.emit(node.path);
    }
    
}