import { Component } from '@angular/core';
import { Validators, FormBuilder, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { Article, ArticlesService } from '../articles.service';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
    selector: 'app-article-form',
    standalone: true,
    imports: [CommonModule, MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule, ReactiveFormsModule, FormsModule],
    templateUrl: './article-form.component.html',
    styleUrl: './article-form.component.css'
})
export class ArticleFormComponent {

    form = this.fb.group({
        title: ['', [Validators.required, Validators.minLength(5)]],
        content: ['', [Validators.required, Validators.minLength(5)]]
    });

    articleId = this.activatedRoute.snapshot.params["articleId"];
    article!: Article;

    constructor(private fb: FormBuilder, private activatedRoute: ActivatedRoute, private articlesService: ArticlesService) {
        if (this.articleId === '__NEW__') return;
        this.articlesService.get(this.articleId).subscribe(article => {
            this.article = article;
            this.form.patchValue(article);
        });
    }

    onSubmit() {
        if (this.form.invalid) return;
        const article = this.form.getRawValue() as Article;
        if (this.articleId === '__NEW__') {
            this.articlesService.post(article).subscribe(() => {
                this.form.reset();
            });
        } else {
            this.articlesService.put(this.articleId, article).subscribe(() => {
                this.form.reset();
            });
        }
    }

    goBack() {
        console.log("back")
        window.history.back();
    }

}
