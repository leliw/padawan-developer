import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';


export class DirTreeItem {
    constructor(
        public item: string,
        public path: string,
        public is_dir: boolean,
        public has_items: boolean,
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
        return this.getChildren("/");
    }

    getChildren(path: string, level = 0): Observable<DirTreeItem[]> {
        return this.get(path).pipe(map(data => { data.forEach(d => d.level = level); return data; }));
    }

}
