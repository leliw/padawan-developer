import { Injectable } from '@angular/core';
import { WebSocketSubject } from 'rxjs/webSocket';

export interface Message { 
    channel: string;
    text?: string;
    files?: string[];
}

@Injectable({
    providedIn: 'root',
})
export class WebsocketService {
    private socket$: WebSocketSubject<Message>;
    private endpoint = '/api/ws';

    constructor() {
        const url = new URL(window.origin);
        let host = url.host;
        let protocol = url.protocol === 'https:' ? 'wss' : 'ws';
        // Replace the port of the host if the app is running in development mode
        host = host.replace('localhost:4200', 'localhost:8000')
        const socketUrl = `${protocol}://${host}${this.endpoint}`;
        this.socket$ = new WebSocketSubject(socketUrl);
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
