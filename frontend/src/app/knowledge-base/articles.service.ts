import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Article {
    articleId: string;
    title: string;
    content: string;
}

@Injectable({
    providedIn: 'root'
})
export class ArticlesService {

    private endpoint = '/api/knowledge-base/articles';

    constructor(private http: HttpClient) { }

    getAll(): Observable<Article[]> {
        return this.http.get<Article[]>(this.endpoint);
    }

    post(Article: Article): Observable<void> {
        return this.http.post<void>(this.endpoint, Article);
    }

    get(key: string): Observable<Article> {
        const eKey = encodeURIComponent(key);
        return this.http.get<Article>(`${this.endpoint}/${eKey}`);
    }

    put(key: string, Article: Article): Observable<void> {
        const eKey = encodeURIComponent(key);
        return this.http.put<void>(`${this.endpoint}/${eKey}`, Article);
    }

    delete(key: string): Observable<void> {
        const eKey = encodeURIComponent(key);
        return this.http.delete<void>(`${this.endpoint}/${eKey}`);
    }
}
