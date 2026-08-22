import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

import { Invoice } from './entities/invoice.entity';
import { InvoiceItem } from './entities/invoice-item.entity';
import { Supplier } from './entities/supplier.entity';
import { Customer } from './entities/customer.entity';
import { Product } from './entities/product.entity';

import { InvoicesController } from './invoices.controller';
import { InvoicesService } from './invoices.service';
import { MlClientModule } from '../ml-client/ml-client.module';

@Module({
  imports: [
    TypeOrmModule.forFeature([Invoice, InvoiceItem, Supplier, Customer, Product]),
    MlClientModule,
  ],
  controllers: [InvoicesController],
  providers: [InvoicesService],
  exports: [InvoicesService],
})
export class InvoicesModule {}