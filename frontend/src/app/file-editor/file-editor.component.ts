import { HttpClient } from '@angular/common/http';
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-file-editor',
  standalone: true,
  imports: [],
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
