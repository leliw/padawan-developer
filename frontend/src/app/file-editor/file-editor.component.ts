import { HttpClient } from '@angular/common/http';
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CodemirrorModule } from '@ctrl/ngx-codemirror';

import 'codemirror/mode/css/css';
import 'codemirror/mode/javascript/javascript';
import 'codemirror/mode/markdown/markdown';

@Component({
    selector: 'app-file-editor',
    standalone: true,
    imports: [FormsModule, CodemirrorModule],
    templateUrl: './file-editor.component.html',
    styleUrl: './file-editor.component.css'
})
export class FileEditorComponent implements OnChanges {
    @Input() file: string = '';
    
    fileName: string = "";
    name: string = "";
    content = "";
    options = { 
        lineNumbers: true, 
        theme: 'material', 
        mode: 'markdown'
    };

    constructor(private http: HttpClient) { }

    ngOnChanges(changes: SimpleChanges): void {
        if (changes['file']) {
            this.fileName =  changes['file'].currentValue;
            this.name = this.fileName.split('/').pop() ?? '';
            this.http.get("/api/files/" + changes['file'].currentValue, { responseType: 'text' })
                .subscribe(content => {
                    if (this.file.endsWith(".ts"))
                        this.options.mode = 'javascript';
                    this.content = content
                });
            }
    }

}
