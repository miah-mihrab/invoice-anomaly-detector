import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { Invoice } from './entities/invoice.entity';
import { MlClientService } from '../ml-client/ml-client.service';

@Injectable()
export class InvoicesService {
    constructor(
        @InjectRepository(Invoice)
        private readonly invoiceRepository: Repository<Invoice>,
        private readonly mlClientService: MlClientService,
    ) { }

    async findAll(page: number, limit: number) {
        // TypeORM's findAndCount does the SELECT and the COUNT(*) in one call —
        // convenient for building pagination metadata (total pages, etc.)
        const [invoices, total] = await this.invoiceRepository.findAndCount({
            relations: {
                supplier: true,
                customer: true,
                items: {
                    product: true,
                },
            }, // joins these in, not just IDs
            order: { invoiceDate: 'DESC' },
            skip: (page - 1) * limit,
            take: limit,
        });

        return {
            data: invoices,
            meta: { total, page, limit, totalPages: Math.ceil(total / limit) },
        };
    }


    async findOne(id: string) {
        const invoice = await this.invoiceRepository.findOne({
            where: { id },
            relations: {
                supplier: true,
                customer: true,
                items: { product: true },
            },
        });

        if (!invoice) {
            throw new NotFoundException(`Invoice ${id} not found`);
        }

        const prediction = await this.mlClientService.predict(invoice);


        const itemsWithHistory = await Promise.all(
            invoice.items.map(async (item) => ({
                ...item,
                productHistory: await this.getProductHistory(item.productId, invoice.id),
            })),
        );

        return { ...invoice, items: itemsWithHistory, prediction };
    }


    async getProductHistory(productId: string, excludeInvoiceId: string) {
        // Raw query, since this is an aggregation (avg/min/max/count), not a
        // simple entity fetch — TypeORM's query builder handles this cleanly.
        const stats = await this.invoiceRepository.manager
            .createQueryBuilder()
            .select('item.product_id', 'productId')
            .addSelect('COUNT(*)', 'sampleSize')
            .addSelect('AVG(item.quantity)', 'avgQuantity')
            .addSelect('MIN(item.quantity)', 'minQuantity')
            .addSelect('MAX(item.quantity)', 'maxQuantity')
            .addSelect('AVG(item.unit_price)', 'avgUnitPrice')
            .addSelect('MIN(item.unit_price)', 'minUnitPrice')
            .addSelect('MAX(item.unit_price)', 'maxUnitPrice')
            .from('invoice_items', 'item')
            .where('item.product_id = :productId', { productId })
            .andWhere('item.invoice_id != :excludeInvoiceId', { excludeInvoiceId })
            .groupBy('item.product_id')
            .getRawOne();

        if (!stats) {
            return { hasHistory: false };
        }

        return {
            hasHistory: true,
            sampleSize: Number(stats.sampleSize),
            quantity: {
                avg: Number(stats.avgQuantity),
                min: Number(stats.minQuantity),
                max: Number(stats.maxQuantity),
            },
            unitPrice: {
                avg: Number(stats.avgUnitPrice),
                min: Number(stats.minUnitPrice),
                max: Number(stats.maxUnitPrice),
            },
        };
    }
}