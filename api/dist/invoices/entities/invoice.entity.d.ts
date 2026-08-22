import { InvoiceItem } from './invoice-item.entity';
import { Supplier } from './supplier.entity';
import { Customer } from './customer.entity';
export declare class Invoice {
    id: string;
    invoiceNumber: string;
    supplierId: string;
    supplier: Supplier;
    customerId: string;
    customer: Customer;
    invoiceDate: Date;
    currency: string;
    subtotal: number;
    discount: number;
    taxRate: number;
    taxAmount: number;
    total: number;
    items: InvoiceItem[];
}
