import { Component } from '@angular/core';
import { MatTabsModule } from '@angular/material/tabs';
import { WebsocketService } from '../websocket.service';
import { filter, of } from 'rxjs';
import { FileEditorComponent } from '../file-editor/file-editor.component';
import { AppStateService } from '../app-state.service';


@Component({
    selector: 'app-files',
    standalone: true,
    imports: [MatTabsModule, FileEditorComponent],
    templateUrl: './files.component.html',
    styleUrl: './files.component.css'
})
export class FilesComponent {

    files = new Set<string>();

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

}
