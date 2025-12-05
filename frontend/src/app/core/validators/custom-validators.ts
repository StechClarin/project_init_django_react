import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export class CustomValidators {
    /**
     * Valide que deux champs ont la même valeur.
     * @param controlName Nom du premier champ (ex: 'password')
     * @param matchingControlName Nom du champ de confirmation (ex: 'password2')
     */
    static match(controlName: string, matchingControlName: string): ValidatorFn {
        return (group: AbstractControl): ValidationErrors | null => {
            const control = group.get(controlName);
            const matchingControl = group.get(matchingControlName);

            if (!control || !matchingControl) {
                return null;
            }

            // Si le champ de confirmation a déjà une autre erreur, on ne fait rien
            if (matchingControl.errors && !matchingControl.errors['match']) {
                return null;
            }

            if (control.value !== matchingControl.value) {
                matchingControl.setErrors({ match: true });
                return { match: true };
            } else {
                matchingControl.setErrors(null);
                return null;
            }
        };
    }
}
