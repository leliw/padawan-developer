import { AfterViewChecked, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Message, WebsocketService } from '../websocket.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-chat',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './chat.component.html',
    styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, AfterViewChecked {

    @ViewChild('container') container!: ElementRef;
    messages: Message[] = [{ dir: "received", text: "Hello!" }];
    newMessage = '';

    constructor(private wsService: WebsocketService) { }

    ngOnInit(): void {
        this.wsService.connect().subscribe(
            msg => this.messages.push(msg)
        );
    }

    sendMessage(): void {
        this.messages.push({ dir: "sent", "text": this.newMessage });
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
