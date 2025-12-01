import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-product-list',
    standalone: true,
    imports: [CommonModule],
    template: `<p>Product List Works!</p>`,
})
export class ProductListComponent { }
