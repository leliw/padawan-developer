import { Component } from '@angular/core';
import { MatTabsModule } from '@angular/material/tabs';
import { WebsocketService } from '../websocket.service';
import { filter } from 'rxjs';


@Component({
    selector: 'app-files',
    standalone: true,
    imports: [MatTabsModule],
    templateUrl: './files.component.html',
    styleUrl: './files.component.css'
})
export class FilesComponent {

    files = new Set<string>();

    constructor(private wsService: WebsocketService) {
        this.wsService.connect()
            .pipe(filter(msg => (msg.channel == "files" && msg.files !== undefined)))
            .subscribe(msg => this.files = new Set([...this.files, ...(msg.files ?? [])]));
    }

}