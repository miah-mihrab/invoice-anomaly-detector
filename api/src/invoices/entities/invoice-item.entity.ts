import { Entity, Column, PrimaryGeneratedColumn, ManyToOne, JoinColumn } from 'typeorm';
import { Invoice } from './invoice.entity';
import { Product } from './product.entity';

@Entity('invoice_items')
export class InvoiceItem {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ name: 'invoice_id' })
  invoiceId: string;

  @ManyToOne(() => Invoice, (invoice) => invoice.items)
  @JoinColumn({ name: 'invoice_id' })
  invoice: Invoice;

  @Column({ name: 'product_id' })
  productId: string;

  @ManyToOne(() => Product)
  @JoinColumn({ name: 'product_id' })
  product: Product;

  @Column({ type: 'numeric' })
  quantity: number;

  @Column({ name: 'unit_price', type: 'numeric' })
  unitPrice: number;

  @Column({ type: 'numeric' })
  discount: number;

  @Column({ name: 'tax_rate', type: 'numeric' })
  taxRate: number;

  @Column({ name: 'tax_amount', type: 'numeric' })
  taxAmount: number;

  @Column({ type: 'numeric' })
  subtotal: number;

  @Column({ type: 'numeric' })
  total: number;
}