import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { MatTabsModule } from '@angular/material/tabs';
import { WebsocketService } from '../websocket.service';
import { filter, of } from 'rxjs';
import { FileEditorComponent } from '../file-editor/file-editor.component';
import { AppStateService } from '../app-state.service';
import { MatIconModule } from '@angular/material/icon';


@Component({
    selector: 'app-files',
    standalone: true,
    imports: [MatTabsModule, FileEditorComponent, MatIconModule],
    templateUrl: './files.component.html',
    styleUrl: './files.component.css'
})
export class FilesComponent implements OnChanges {
    
    @Input() openFile = '';

    files = new Set<string>();
    selected = 0;

    constructor(private wsService: WebsocketService, private appService: AppStateService) {
        this.appService.get()
            .subscribe(state => {
                of(...state.chat_history)
                    .pipe(filter(msg => (msg.channel == "files" && msg.files !== undefined)))
                    .subscribe(msg => this.files = new Set([...this.files, ...(msg.files ?? [])]));
            })
        this.wsService.connect()
            .pipe(filter(msg => (msg.channel == "files" && msg.files !== undefined)))
            .subscribe(msg => this.files = new Set([...this.files, ...(msg.files ?? [])]));
    }
    
    ngOnChanges(changes: SimpleChanges): void {
        if (changes['openFile']?.currentValue) {
            this.files.add(changes['openFile'].currentValue);
            const arrayFromSet = Array.from(this.files);
            this.selected = arrayFromSet.indexOf(this.openFile);
        }
    }

    removeTab(index: number) {
        this.files.delete([...this.files][index]);
    }
}

