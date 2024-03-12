import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { TreeItem } from './utils/DynamicTree';


export class DirTreeItem implements TreeItem {
    constructor(
        public name: string,
        public path: string,
        public isDir: boolean,
        public hasChildren: boolean,
        public level = 1,
        public isLoading = false,
    ) { }

}

@Injectable({
    providedIn: 'root'
})
export class DirTreeService {

    endpoint = "/api/dir-tree";

    constructor(private httpClient: HttpClient) { }

    get(path: string): Observable<DirTreeItem[]> {
        let params = new HttpParams().append('path', path);
        return this.httpClient.get<DirTreeItem[]>(this.endpoint, { params: params });
    }

    initialData(): Observable<DirTreeItem[]> {
        return this.getChildren();
    }

    getChildren(node?: any): Observable<DirTreeItem[]> {
        const path = node?.path ?? "/"
        const level = (node?.level ?? -1) + 1;
        return this.get(path).pipe(map(data => { data.forEach(d => d.level = level); return data; }));
    }

}
