"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.InvoicesService = void 0;
const common_1 = require("@nestjs/common");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const invoice_entity_1 = require("./entities/invoice.entity");
const ml_client_service_1 = require("../ml-client/ml-client.service");
let InvoicesService = class InvoicesService {
    invoiceRepository;
    mlClientService;
    constructor(invoiceRepository, mlClientService) {
        this.invoiceRepository = invoiceRepository;
        this.mlClientService = mlClientService;
    }
    async findAll(page, limit) {
        const [invoices, total] = await this.invoiceRepository.findAndCount({
            relations: {
                supplier: true,
                customer: true,
                items: {
                    product: true,
                },
            },
            order: { invoiceDate: 'DESC' },
            skip: (page - 1) * limit,
            take: limit,
        });
        return {
            data: invoices,
            meta: { total, page, limit, totalPages: Math.ceil(total / limit) },
        };
    }
    async findOne(id) {
        const invoice = await this.invoiceRepository.findOne({
            where: { id },
            relations: {
                supplier: true,
                customer: true,
                items: { product: true },
            },
        });
        if (!invoice) {
            throw new common_1.NotFoundException(`Invoice ${id} not found`);
        }
        const prediction = await this.mlClientService.predict(invoice);
        const itemsWithHistory = await Promise.all(invoice.items.map(async (item) => ({
            ...item,
            productHistory: await this.getProductHistory(item.productId, invoice.id),
        })));
        console.log(itemsWithHistory);
        return { ...invoice, items: itemsWithHistory, prediction };
    }
    async getProductHistory(productId, excludeInvoiceId) {
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
};
exports.InvoicesService = InvoicesService;
exports.InvoicesService = InvoicesService = __decorate([
    (0, common_1.Injectable)(),
    __param(0, (0, typeorm_1.InjectRepository)(invoice_entity_1.Invoice)),
    __metadata("design:paramtypes", [typeorm_2.Repository,
        ml_client_service_1.MlClientService])
], InvoicesService);
//# sourceMappingURL=invoices.service.js.map