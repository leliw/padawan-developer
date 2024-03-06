import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Message } from './websocket.service';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ChatHistoryService {

    endpoint = "/api/history";

    constructor(private httpClient: HttpClient) { }

    get(): Observable<Message[]> {
        return this.httpClient.get<Message[]>(this.endpoint);
    }
    
}
