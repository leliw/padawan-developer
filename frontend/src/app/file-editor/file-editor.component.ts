import { HttpClient } from '@angular/common/http';
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CodemirrorModule } from '@ctrl/ngx-codemirror';
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
    
    content = "";

    constructor(private http: HttpClient) { }

    ngOnChanges(changes: SimpleChanges): void {
        if (changes['file'])
            this.http.get("/api/files/" + changes['file'].currentValue, { responseType: 'text' })
                .subscribe(content => this.content = content);
    }

}
