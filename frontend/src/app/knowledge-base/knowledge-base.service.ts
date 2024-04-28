import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { TreeItem } from '../utils/DynamicTree';


export class DirectoryItem implements TreeItem {
    constructor(
        public name: string,
        public path: string,
        public isDir: boolean,
        public isLeaf: boolean,
        public level = 1,
        public isLoading = false,
    ) { }
}

@Injectable({
    providedIn: 'root'
})
export class KnowledgeBaseService {

    endpoint = "/api/kb";

    constructor(private httpClient: HttpClient) { }

    getItems(path: string): Observable<DirectoryItem[]> {
        let params = new HttpParams().append('path', path);
        return this.httpClient.get<DirectoryItem[]>(this.endpoint, { params: params });
    }

    getChildren(node?: any): Observable<DirectoryItem[]> {
        const path = node?.path ?? "/"
        const level = (node?.level ?? -1) + 1;
        return this.getItems(path).pipe(
            map(data => { data.forEach(d => d.level = level); return data; })
            );
    }

    getContent(path: string): Observable<any> {
        let params = new HttpParams().append('path', path);
        return this.httpClient.get<any>(`${this.endpoint}/content`, { params: params });
    }

    putContent(path: string, content: string): Observable<any> {
        let params = new HttpParams().append('path', path);
        return this.httpClient.put<any>(`${this.endpoint}/content`, content, { params: params });
    }

    rename(path: string, new_path: string): Observable<any> {
        let params = new HttpParams().append('path', path);
        return this.httpClient.patch<any>(`/api/knowledge-base/articles`, new_path, { params: params });
    }
}
