import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';

import { Invoice } from './invoices/entities/invoice.entity';
import { InvoiceItem } from './invoices/entities/invoice-item.entity';
import { Supplier } from './invoices/entities/supplier.entity';
import { Customer } from './invoices/entities/customer.entity';
import { Product } from './invoices/entities/product.entity';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    TypeOrmModule.forRootAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        type: 'postgres',
        host: config.get('PG_HOST'),
        port: config.get<number>('PG_PORT'),
        database: config.get('PG_DB'),
        username: config.get('PG_USER'),
        password: config.get('PG_PASS'),
        entities: [Invoice, InvoiceItem, Supplier, Customer, Product],
        synchronize: false,
      }),
    }),
  ],
})
export class AppModule {}