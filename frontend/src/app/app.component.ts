import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ConfigService } from './config/config.service';
import { ChatComponent } from './chat/chat.component';
import { TerminalComponent } from './terminal/terminal.component';
import { FilesComponent } from './files/files.component';
import { DirTreeComponent } from './dir-tree/dir-tree.component';
import { WebsocketService } from './websocket.service';
import { AppStateService } from './app-state.service';
import { filter, of } from 'rxjs';

export interface Hello {
    Hello: string;
}
@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, RouterOutlet, ChatComponent, DirTreeComponent, FilesComponent, TerminalComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})

export class AppComponent {

    version = '';
    files = new Set<string>();
    file = "";

    constructor(private config: ConfigService, private wsService: WebsocketService, private appService: AppStateService) {
        this.config.getConfig().subscribe(c => {
            this.version = c.version;
        })
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
    
    openFile(file: string) {
        this.file = file;
        this.files = new Set(this.files.add(file));
    }
}
