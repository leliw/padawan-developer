import { Component, ViewChild } from '@angular/core';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTreeModule } from '@angular/material/tree';
import { DirectoryItem, KnowledgeBaseService } from '../knowledge-base.service';
import { FlatTreeControl } from '@angular/cdk/tree';
import { DynamicDataSource } from '../../utils/DynamicTree';
import { CommonModule } from '@angular/common';
import { CodemirrorComponent, CodemirrorModule } from '@ctrl/ngx-codemirror';
import { FormsModule } from '@angular/forms';
import { MatTooltipModule } from '@angular/material/tooltip';

import 'codemirror/mode/css/css';
import 'codemirror/mode/javascript/javascript';
import 'codemirror/mode/markdown/markdown';
import { RouterModule } from '@angular/router';

@Component({
    selector: 'app-konwledge-base-page',
    standalone: true,
    imports: [MatTreeModule, MatButtonModule, MatIconModule, MatTooltipModule,  MatProgressBarModule, CommonModule, FormsModule, CodemirrorModule, RouterModule],
    templateUrl: './konwledge-base-page.component.html',
    styleUrl: './konwledge-base-page.component.css'
})
export class KonwledgeBasePageComponent {

    @ViewChild('myEditor') myEditorComponent!: CodemirrorComponent;
    
    treeControl: FlatTreeControl<DirectoryItem>;
    dataSource: DynamicDataSource<DirectoryItem>;
    
    selectedNode!: DirectoryItem;
    content: string = "";
    code: string = "";
    org_code: string = "";
    editMode = false;

    options = { 
        lineNumbers: true, 
        theme: 'material', 
        mode: 'javascript'
    };

    constructor(private service: KnowledgeBaseService) {
        this.treeControl = new FlatTreeControl<DirectoryItem>(
            node => node.level,
            node => !node.isLeaf
        );
        this.dataSource = new DynamicDataSource(this.treeControl, service.getChildren.bind(service));
        service.getChildren().subscribe(data => this.dataSource.data = data);
    }

    open(node: DirectoryItem) {
        this.service.getContent(node.path)
            .subscribe(data => {
                this.content = data;
                if (node.path.endsWith(".json")) {
                    this.options.mode = 'javascript';
                    this.code = JSON.stringify(data, null, 2);
                } else if (node.path.endsWith(".md")) { 
                    this.options.mode = 'markdown';
                    this.code = data;
                } else {
                    this.options.mode = 'text';
                    this.code = data;
                }
                this.selectedNode = node;
                this.org_code = this.code
                this.myEditorComponent?.codeMirror?.refresh();
            });
    }

    onCodeChange(event: any) {
        this.editMode = true;
    }

    save() {
        this.service.putContent(this.selectedNode.path, this.code).subscribe(data => {
            this.editMode = false;
        });
    }

    cancel() {
        this.code = this.org_code;
        this.myEditorComponent?.codeMirror?.refresh();
        this.editMode = false;
    }

    rename() {
        const name = prompt("Enter new name", this.selectedNode.name);
        if (name) {
            this.service.rename(this.selectedNode.path, name).subscribe(data => {
                this.selectedNode.path = this.selectedNode.path.replace(this.selectedNode.name, name);
                this.selectedNode.name = name;
            });
        }
    }
}
