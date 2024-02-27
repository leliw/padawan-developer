import { Injectable } from '@angular/core';
import { WebSocketSubject } from 'rxjs/webSocket';

@Injectable({
    providedIn: 'root',
})
export class WebsocketService {
    private socket$: WebSocketSubject<any>;
    private socketUrl = 'ws://localhost:8000/ws'; // URL do Twojego WebSocket endpoint

    constructor() {
        this.socket$ = new WebSocketSubject(this.socketUrl);
    }

    public connect(): WebSocketSubject<any> {
        return this.socket$;
    }

    public send(message: any): void {
        this.socket$.next(message);
    }

    public close(): void {
        this.socket$.complete();
    }
}
