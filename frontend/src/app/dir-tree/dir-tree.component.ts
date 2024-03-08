import { CollectionViewer, SelectionChange, DataSource } from '@angular/cdk/collections';
import { FlatTreeControl } from '@angular/cdk/tree';
import { Component, EventEmitter, Output } from '@angular/core';
import { BehaviorSubject, merge, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTreeModule } from '@angular/material/tree';
import { DirTreeService, DirTreeItem } from '../dir-tree.service';
import { CommonModule } from '@angular/common';


export class DynamicDataSource implements DataSource<DirTreeItem> {
    dataChange = new BehaviorSubject<DirTreeItem[]>([]);

    get data(): DirTreeItem[] {
        return this.dataChange.value;
    }
    set data(value: DirTreeItem[]) {
        this._treeControl.dataNodes = value;
        this.dataChange.next(value);
    }

    constructor(
        private _treeControl: FlatTreeControl<DirTreeItem>,
        private _database: DirTreeService,
    ) { }

    connect(collectionViewer: CollectionViewer): Observable<DirTreeItem[]> {
        this._treeControl.expansionModel.changed.subscribe(change => {
            if (change.added || change.removed)
                this.handleTreeControl(change);
        });
        return merge(collectionViewer.viewChange, this.dataChange).pipe(map(() => this.data));
    }

    disconnect(collectionViewer: CollectionViewer): void {
        // no-op
    }

    /** Handle expand/collapse behaviors */
    handleTreeControl(change: SelectionChange<DirTreeItem>) {
        if (change.added) {
            change.added.forEach(node => this.toggleNode(node, true));
        }
        if (change.removed) {
            change.removed
                .slice()
                .reverse()
                .forEach(node => this.toggleNode(node, false));
        }
    }

    /**
     * Toggle the node, remove from display list
     */
    toggleNode(node: DirTreeItem, expand: boolean) {
        node.isLoading = true;
        this._database.getChildren(node.path, node.level + 1).subscribe(children => {
            const index = this.data.indexOf(node);
            if (!children || index < 0) {
                // If no children, or cannot find the node, no op
                node.isLoading = false;
                return;
            }
            if (expand) {
                this.data.splice(index + 1, 0, ...children);
            } else {
                let count = 0;
                for (
                    let i = index + 1;
                    i < this.data.length && this.data[i].level > node.level;
                    i++, count++
                ) {
                    // Skip nodes with higher level than the current node.
                }
                this.data.splice(index + 1, count);
            }

            // notify the change
            this.dataChange.next(this.data);
            node.isLoading = false;
        });
    }
}

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
    dataSource: DynamicDataSource;

    constructor(database: DirTreeService) {
        this.treeControl = new FlatTreeControl<DirTreeItem>(this.getLevel, this.isExpandable);
        this.dataSource = new DynamicDataSource(this.treeControl, database);
        database.initialData().subscribe(data => this.dataSource.data = data);
    }

    getLevel = (node: DirTreeItem) => node.level;
    isExpandable = (node: DirTreeItem) => node.has_items;
    hasChild = (_: number, _nodeData: DirTreeItem) => _nodeData.has_items;

    openFile(node: DirTreeItem) {
        this.file.emit(node.path);
    }
    
}