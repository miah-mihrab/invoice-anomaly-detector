import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('products')
export class Product {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  sku: string;

  @Column()
  name: string;

  @Column()
  category: string;

  @Column({ name: 'base_cost', type: 'numeric' })
  baseCost: number;

  @Column()
  unit: string;
}