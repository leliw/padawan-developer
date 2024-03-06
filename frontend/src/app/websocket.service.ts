import { Injectable } from '@angular/core';
import { WebSocketSubject } from 'rxjs/webSocket';

export interface Message { 
    channel: string;
    text: string;
    files?: string[];
}

@Injectable({
    providedIn: 'root',
})
export class WebsocketService {
    private socket$: WebSocketSubject<Message>;
    private socketUrl = 'ws://localhost:8000/api/ws'; // URL do Twojego WebSocket endpoint

    constructor() {
        this.socket$ = new WebSocketSubject(this.socketUrl);
    }

    public connect(): WebSocketSubject<Message> {
        return this.socket$;
    }

    public send(message: any): void {
        this.socket$.next(message);
    }

    public close(): void {
        this.socket$.complete();
    }
}
