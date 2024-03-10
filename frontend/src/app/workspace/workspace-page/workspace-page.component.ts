import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChatComponent } from '../../chat/chat.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { DirTreeComponent } from '../../dir-tree/dir-tree.component';
import { FilesComponent } from '../../files/files.component';
import { TerminalComponent } from '../../terminal/terminal.component';
import { WebsocketService } from '../../websocket.service';
import { AppStateService } from '../../app-state.service';
import { filter, of } from 'rxjs';

@Component({
    selector: 'app-workspace-page',
    standalone: true,
    imports: [CommonModule, RouterOutlet, ChatComponent, DirTreeComponent, FilesComponent, TerminalComponent, MatToolbarModule, MatTooltipModule, MatIconModule, MatButtonModule],
    templateUrl: './workspace-page.component.html',
    styleUrl: './workspace-page.component.css'
})
export class WorkspacePageComponent {
    
    files = new Set<string>();
    file = "";

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

    openFile(file: string) {
        this.file = file;
        this.files = new Set(this.files.add(file));
        // If user opens a file, close tab and try open again
        setTimeout(() => this.file = "", 1000);
    }
    
}
