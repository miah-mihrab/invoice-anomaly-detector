import { HttpService } from '@nestjs/axios';
import { Invoice } from '../invoices/entities/invoice.entity';
export interface PredictResponse {
    invoice_id: string;
    is_anomaly_unsupervised: boolean;
    is_anomaly_supervised: boolean;
    anomaly_score: number;
    reasons: string[];
}
export declare class MlClientService {
    private readonly httpService;
    private readonly logger;
    constructor(httpService: HttpService);
    predict(invoice: Invoice): Promise<PredictResponse | null>;
}
