import { Component, OnInit } from '@angular/core';
import { Message, WebsocketService } from '../websocket.service'; // Załóżmy, że ten serwis już istnieje
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-chat',
    standalone: true,
    imports: [ CommonModule, FormsModule ],
    templateUrl: './chat.component.html',
    styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {

    messages: Message[] = [];
    newMessage = '';

    constructor(private wsService: WebsocketService) { }

    ngOnInit(): void {
        this.wsService.connect().subscribe(
            msg => {
                msg.dir = "received";
                this.messages.push(msg);
            }
        );
    }

    sendMessage(): void {
        this.messages.push({ dir:"sent", "text": this.newMessage});
        if (this.newMessage.trim().length > 0) {
            this.wsService.send({ text: this.newMessage });
            this.newMessage = '';
        }
    }

}
