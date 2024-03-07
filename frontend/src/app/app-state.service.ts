import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Message } from './websocket.service';
import { Observable } from 'rxjs';


export interface AppState { 
    chat_history: Message[];
    parameters: any;
    open_files: string[];
}

@Injectable({
    providedIn: 'root'
})
export class AppStateService {

    endpoint = "/api/app-state";

    constructor(private httpClient: HttpClient) { }

    get(): Observable<AppState> {
        return this.httpClient.get<AppState>(this.endpoint);
    }
    
}
