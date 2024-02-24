import logging

from bash_executer import BashExecuter

create_angular_service = [
    {
        "bash": [
            { "cwd": "{project_name}/frontend", "command": "ng generate service proxy/proxy"}
        ]
    },
    {
        "TypeScript": [
            { "add": "import { HttpClient } from '@angular/common/http';" },
            { "add":
"""export interface Status {
    status: string;
    port: number;
    target_url: string
}"""},
            { "class": "ProxyService", "add_property": "private apiUrl = \"/api/proxy\""},
            { "class": "ProxyService", "method": "constructor", "add_parameter": "private http: HttpClient"},
            { "class": "ProxyService", "add_method":
"""getStatus(): Observable<Status> {
        return this.http.get<Status>(this.apiUrl + '/status');
}"""},
        ]
    }
]
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    p = {
            "project_name": "my_project",
            "service_file": "src/app/proxy/proxy.service.ts"
        }
    for exec_seq in create_angular_service:
        executer  = list(exec_seq.keys())[0]
        if executer == "bash":
            bash = BashExecuter("/home/mleliwa/src/", p)
            bash.execute_seq(exec_seq.get(executer))
        elif executer == "TypeScript":
            print(exec_seq.get(executer))