import { CommonModule } from '@angular/common';
import { Component, AfterViewInit, ElementRef, ViewChild, ViewEncapsulation } from '@angular/core';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { WebsocketService } from '../websocket.service';
import { filter } from 'rxjs';


@Component({
    selector: 'app-terminal',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './terminal.component.html',
    styleUrl: './terminal.component.css',
    encapsulation: ViewEncapsulation.None
})
export class TerminalComponent implements AfterViewInit {
    @ViewChild('terminal', { static: true }) terminalDiv!: ElementRef;
    terminal!: Terminal;

    constructor(private wsService: WebsocketService) { }


    ngAfterViewInit() {
        this.terminal = new Terminal({ cursorBlink: true, convertEol: true });
        const fitAddon = new FitAddon();
        this.terminal.loadAddon(fitAddon);
        this.terminal.open(this.terminalDiv.nativeElement);
        fitAddon.fit();
        this.wsService.connect()
            .pipe(filter(msg => msg.channel?.startsWith("bash")))
            .subscribe(msg => this.terminal.write(msg.text));
    }
}
