import { Component, EventEmitter, Output } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Observable } from 'rxjs';
import { FormUtils } from '../utils/form.utils';
import { inject } from '@angular/core';
import { ToastService } from '@core/services/toast.service';

@Component({ template: '' })
export abstract class BaseFormComponent {
    @Output() cancel = new EventEmitter<void>();
    @Output() success = new EventEmitter<void>();

    abstract form: FormGroup;
    isSubmitting = false;
    errorMessage: string | null = null;

    protected toastService = inject(ToastService);

    abstract save(): Observable<any>;

    submit() {
        if (this.form.valid) {
            this.isSubmitting = true;
            this.errorMessage = null;

            this.save().subscribe({
                next: () => {
                    this.isSubmitting = false;
                    this.success.emit();
                },
                error: (err) => {
                    console.error('Erreur soumission formulaire:', err);
                    this.isSubmitting = false;
                    // Injection automatique des erreurs dans les champs
                    this.errorMessage = FormUtils.setErrors(this.form, err);
                    if (this.errorMessage) {
                        this.toastService.error(this.errorMessage);
                    } else {
                        this.toastService.error('Une erreur est survenue lors de l\'enregistrement.');
                    }
                }
            });
        } else {
            this.form.markAllAsTouched();
        }
    }

    onCancel() {
        this.cancel.emit();
    }
}
