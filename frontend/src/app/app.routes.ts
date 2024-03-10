import { Routes } from '@angular/router';
import { WorkspacePageComponent } from './workspace/workspace-page/workspace-page.component';
import { KonwledgeBasePageComponent } from './knowledge-base/konwledge-base-page/konwledge-base-page.component';

export const routes: Routes = [
    { path: '', redirectTo: 'workspace', pathMatch: 'full' },
    { path: 'workspace', component: WorkspacePageComponent },
    { path: 'knowledge-base', component: KonwledgeBasePageComponent }
];
