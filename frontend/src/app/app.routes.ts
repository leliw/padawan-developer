import { Routes } from '@angular/router';
import { WorkspacePageComponent } from './workspace/workspace-page/workspace-page.component';

export const routes: Routes = [
    { path: '', redirectTo: 'workspace', pathMatch: 'full' },
    { path: 'workspace', component: WorkspacePageComponent }
];
