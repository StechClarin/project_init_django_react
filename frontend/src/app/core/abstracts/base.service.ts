import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export abstract class BaseService {
    protected http = inject(HttpClient);

    // Endpoint spécifique à définir par l'enfant (ex: 'user', 'product')
    abstract endpoint: string;

    protected get apiUrl(): string {
        return `${environment.apiUrl || 'http://127.0.0.1:8000/api'}/${this.endpoint}`;
    }

    /**
     * Generic Upsert (Create or Update)
     * POST /api/{endpoint}/save/
     */
    save(data: any): Observable<any> {
        if (data.id) {
            return this.http.post(`${this.apiUrl}/save/${data.id}/`, data);
        }
        return this.http.post(`${this.apiUrl}/save/`, data);
    }

    /**
     * Generic Delete
     * DELETE /api/{endpoint}/delete/{id}/
     */
    delete(id: number | string): Observable<any> {
        return this.http.post(`${this.apiUrl}/delete/${id}/`, {});
    }

    /**
     * Generic Status Toggle
     * POST /api/{endpoint}/status/{id}/
     */
    status(id: number | string): Observable<any> {
        return this.http.post(`${this.apiUrl}/status/${id}/`, {});
    }
}
