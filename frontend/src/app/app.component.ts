import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ConfigService } from './config/config.service';
import { ChatComponent } from './chat/chat.component';
import { TerminalComponent } from './terminal/terminal.component';
import { FilesComponent } from './files/files.component';
import { DirTreeComponent } from './dir-tree/dir-tree.component';

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

    constructor(private config: ConfigService) {
        this.config.getConfig().subscribe(c => {
            this.version = c.version;
        })
    }

}
