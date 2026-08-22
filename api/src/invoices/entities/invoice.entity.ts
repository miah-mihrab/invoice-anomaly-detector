import { Entity, Column, PrimaryGeneratedColumn, OneToMany, ManyToOne, JoinColumn } from 'typeorm';
import { InvoiceItem } from './invoice-item.entity';
import { Supplier } from './supplier.entity';
import { Customer } from './customer.entity';

@Entity('invoices')
export class Invoice {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ name: 'invoice_number' })
  invoiceNumber: string;

  @Column({ name: 'supplier_id' })
  supplierId: string;

  @ManyToOne(() => Supplier)
  @JoinColumn({ name: 'supplier_id' })
  supplier: Supplier;

  @Column({ name: 'customer_id' })
  customerId: string;

  @ManyToOne(() => Customer)
  @JoinColumn({ name: 'customer_id' })
  customer: Customer;

  @Column({ name: 'invoice_date', type: 'timestamptz' })
  invoiceDate: Date;

  @Column()
  currency: string;

  @Column({ type: 'numeric' })
  subtotal: number;

  @Column({ type: 'numeric' })
  discount: number;

  @Column({ name: 'tax_rate', type: 'numeric' })
  taxRate: number;

  @Column({ name: 'tax_amount', type: 'numeric' })
  taxAmount: number;

  @Column({ type: 'numeric' })
  total: number;

  @OneToMany(() => InvoiceItem, (item) => item.invoice)
  items: InvoiceItem[];
}