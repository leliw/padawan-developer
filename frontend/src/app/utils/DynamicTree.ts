import { DataSource, CollectionViewer, SelectionChange } from "@angular/cdk/collections";
import { FlatTreeControl } from "@angular/cdk/tree";
import { BehaviorSubject, Observable, merge, map } from "rxjs";



/**
 * Represents a tree item in a dynamic tree.
 */
export interface TreeItem {
    level: number;
    isLoading: boolean;
    hasChildren?: boolean;
    isLeaf?: boolean;
}

/**
 * Represents a dynamic data source for a tree component.
 * This class implements the `DataSource` interface and provides methods for connecting and disconnecting from a collection viewer.
 * It also handles expand/collapse behaviors and toggling nodes in the tree.
 *
 * @template T - The type of the tree items.
 */
export class DynamicDataSource<T extends TreeItem> implements DataSource<T> {
    dataChange = new BehaviorSubject<T[]>([]);

    get data(): T[] {
        return this.dataChange.value;
    }
    set data(value: T[]) {
        this._treeControl.dataNodes = value;
        this.dataChange.next(value);
    }

    constructor(
        private _treeControl: FlatTreeControl<T>,
        private _getChildren: (node: T) => Observable<T[]>
    ) { }

    connect(collectionViewer: CollectionViewer): Observable<T[]> {
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
    handleTreeControl(change: SelectionChange<T>) {
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
    toggleNode(node: T, expand: boolean) {
        node.isLoading = true;
        this._getChildren(node).subscribe(children => {
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

    /**
     * Checks if the given node has children.
     * Used by <mat-tree-node *matTreeNodeDef=... where clause.
     *
     * @param _ The index of the node.
     * @param _nodeData The data of the node.
     * @returns A boolean indicating whether the node has children.
     */
    hasChildren(_: number, _nodeData: T) {
        if (_nodeData.isLeaf !== undefined) {
            return !_nodeData.isLeaf;
        } else {
            return _nodeData.hasChildren;
        }
    }

}