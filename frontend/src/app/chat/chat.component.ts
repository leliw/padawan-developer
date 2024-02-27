import { Component, OnInit } from '@angular/core';
import { WebsocketService } from '../websocket.service'; // Załóżmy, że ten serwis już istnieje
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

    messages: any[] = [];
    newMessage = '';

    constructor(private wsService: WebsocketService) { }

    ngOnInit(): void {
        this.wsService.connect().subscribe(
            msg => {
                this.messages.push(msg);
            }
        );
    }

    sendMessage(): void {
        this.messages.push(this.newMessage);
        console.log(this.newMessage)
        console.log(this.messages)
        if (this.newMessage.trim().length > 0) {
            this.wsService.send({ text: this.newMessage });
            this.newMessage = '';
        }
    }

}
