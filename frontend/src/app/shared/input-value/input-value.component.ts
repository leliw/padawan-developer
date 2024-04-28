import { Component, Inject } from '@angular/core';
import {
    MAT_DIALOG_DATA,
    MatDialogRef,
    MatDialogTitle,
    MatDialogContent,
    MatDialogActions,
    MatDialogClose,
} from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';


export interface InputValueData {
    title: string;
    prompt: string;
    label: string;
    value: any;
}
@Component({
    selector: 'input-value',
    templateUrl: './input-value.component.html',
    styleUrl: './input-value.component.css',
    standalone: true,
    imports: [
        MatFormFieldModule,
        MatInputModule,
        FormsModule,
        MatButtonModule,
        MatDialogTitle,
        MatDialogContent,
        MatDialogActions,
        MatDialogClose,
    ],
})
export class InputValueComponent {
    constructor(
        public dialogRef: MatDialogRef<InputValueComponent>,
        @Inject(MAT_DIALOG_DATA) public data: InputValueData,
    ) { }

    cancel(): void {
        this.dialogRef.close();
    }
}