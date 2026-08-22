"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AppModule = void 0;
const common_1 = require("@nestjs/common");
const config_1 = require("@nestjs/config");
const typeorm_1 = require("@nestjs/typeorm");
const invoice_entity_1 = require("./invoices/entities/invoice.entity");
const invoice_item_entity_1 = require("./invoices/entities/invoice-item.entity");
const supplier_entity_1 = require("./invoices/entities/supplier.entity");
const customer_entity_1 = require("./invoices/entities/customer.entity");
const product_entity_1 = require("./invoices/entities/product.entity");
const invoices_module_1 = require("./invoices/invoices.module");
let AppModule = class AppModule {
};
exports.AppModule = AppModule;
exports.AppModule = AppModule = __decorate([
    (0, common_1.Module)({
        imports: [
            config_1.ConfigModule.forRoot({ isGlobal: true }),
            typeorm_1.TypeOrmModule.forRootAsync({
                inject: [config_1.ConfigService],
                useFactory: (config) => ({
                    type: 'postgres',
                    host: config.get('PG_HOST'),
                    port: config.get('PG_PORT'),
                    database: config.get('PG_DB'),
                    username: config.get('PG_USER'),
                    password: config.get('PG_PASS'),
                    entities: [invoice_entity_1.Invoice, invoice_item_entity_1.InvoiceItem, supplier_entity_1.Supplier, customer_entity_1.Customer, product_entity_1.Product],
                    synchronize: false,
                }),
            }),
            invoices_module_1.InvoicesModule,
        ],
    })
], AppModule);
//# sourceMappingURL=app.module.js.map