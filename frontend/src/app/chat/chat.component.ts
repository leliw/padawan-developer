import { AfterViewChecked, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Message, WebsocketService } from '../websocket.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { filter } from 'rxjs';
import { AppStateService } from '../app-state.service';

@Component({
    selector: 'app-chat',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './chat.component.html',
    styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, AfterViewChecked {

    @ViewChild('container') container!: ElementRef;
    messages: Message[] = [
        { channel: "padawan", text: "Hello! I'm your padawan Master.\nTry typing 'help' if you are not familiar wih my force." }
    ];
    newMessage = '';

    constructor(private wsService: WebsocketService, private appService: AppStateService) { }

    ngOnInit(): void {
        this.appService.get()
            .subscribe(state => this.messages = state.chat_history);
        this.wsService.connect()
            .pipe(filter(msg => msg.channel !== "files"))
            .subscribe(msg => this.messages.push(msg));
    }

    sendMessage(): void {
        this.messages.push({ channel: "master", "text": this.newMessage });
        if (this.newMessage.trim().length > 0) {
            this.wsService.send(this.newMessage);
            this.newMessage = '';
        }
    }

    ngAfterViewChecked(): void {
        this.scrollToBottom();
    }

    private scrollToBottom() {
        this.container.nativeElement.scrollTop = this.container.nativeElement.scrollHeight;
    }

}
