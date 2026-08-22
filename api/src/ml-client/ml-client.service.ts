import { Injectable, Logger } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

import { Invoice } from '../invoices/entities/invoice.entity';

export interface PredictResponse {
  invoice_id: string;
  is_anomaly_unsupervised: boolean;
  is_anomaly_supervised: boolean;
  anomaly_score: number;
  reasons: string[];
}

@Injectable()
export class MlClientService {
  private readonly logger = new Logger(MlClientService.name);

  constructor(private readonly httpService: HttpService) {}

  async predict(invoice: Invoice): Promise<PredictResponse | null> {
    const payload = {
      invoice_id: invoice.id,
      items: invoice.items.map((item) => ({
        quantity: Number(item.quantity),
        unit_price: Number(item.unitPrice),
        tax_rate: Number(item.taxRate),
      })),
    };

    try {
      const response = await firstValueFrom(
        this.httpService.post<PredictResponse>('/predict', payload),
      );
      return response.data;
    } catch (error) {
      this.logger.error(`Prediction failed for invoice ${invoice.id}`, error);
      return null;
    }
  }
}