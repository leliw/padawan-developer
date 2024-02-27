import { Injectable } from '@angular/core';
import { WebSocketSubject } from 'rxjs/webSocket';

@Injectable({
    providedIn: 'root'
})
export class WebsocketService {

    private socket!: WebSocketSubject<any>;

    public connect(url: string): WebSocketSubject<any> {
        if (!this.socket || this.socket.closed) {
            this.socket = new WebSocketSubject(url);
        }
        return this.socket;
    }
}
