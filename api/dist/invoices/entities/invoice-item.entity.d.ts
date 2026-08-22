import { Invoice } from './invoice.entity';
import { Product } from './product.entity';
export declare class InvoiceItem {
    id: string;
    invoiceId: string;
    invoice: Invoice;
    productId: string;
    product: Product;
    quantity: number;
    unitPrice: number;
    discount: number;
    taxRate: number;
    taxAmount: number;
    subtotal: number;
    total: number;
}
