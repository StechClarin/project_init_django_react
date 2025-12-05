import { Injectable } from '@angular/core';
import { BaseService } from '@core/abstracts/base.service';

@Injectable({
    providedIn: 'root'
})
export class UserService extends BaseService {
    endpoint = 'user';
}
