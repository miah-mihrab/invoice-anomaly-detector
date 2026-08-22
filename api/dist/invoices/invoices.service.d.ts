import { Repository } from 'typeorm';
import { Invoice } from './entities/invoice.entity';
import { MlClientService } from '../ml-client/ml-client.service';
export declare class InvoicesService {
    private readonly invoiceRepository;
    private readonly mlClientService;
    constructor(invoiceRepository: Repository<Invoice>, mlClientService: MlClientService);
    findAll(page: number, limit: number): Promise<{
        data: Invoice[];
        meta: {
            total: number;
            page: number;
            limit: number;
            totalPages: number;
        };
    }>;
    findOne(id: string): Promise<{
        items: {
            productHistory: {
                hasHistory: boolean;
                sampleSize?: undefined;
                quantity?: undefined;
                unitPrice?: undefined;
            } | {
                hasHistory: boolean;
                sampleSize: number;
                quantity: {
                    avg: number;
                    min: number;
                    max: number;
                };
                unitPrice: {
                    avg: number;
                    min: number;
                    max: number;
                };
            };
            id: string;
            invoiceId: string;
            invoice: Invoice;
            productId: string;
            product: import("./entities/product.entity").Product;
            quantity: number;
            unitPrice: number;
            discount: number;
            taxRate: number;
            taxAmount: number;
            subtotal: number;
            total: number;
        }[];
        prediction: import("../ml-client/ml-client.service").PredictResponse | null;
        id: string;
        invoiceNumber: string;
        supplierId: string;
        supplier: import("./entities/supplier.entity").Supplier;
        customerId: string;
        customer: import("./entities/customer.entity").Customer;
        invoiceDate: Date;
        currency: string;
        subtotal: number;
        discount: number;
        taxRate: number;
        taxAmount: number;
        total: number;
    }>;
    getProductHistory(productId: string, excludeInvoiceId: string): Promise<{
        hasHistory: boolean;
        sampleSize?: undefined;
        quantity?: undefined;
        unitPrice?: undefined;
    } | {
        hasHistory: boolean;
        sampleSize: number;
        quantity: {
            avg: number;
            min: number;
            max: number;
        };
        unitPrice: {
            avg: number;
            min: number;
            max: number;
        };
    }>;
}
