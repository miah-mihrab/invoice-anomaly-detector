import { Module } from '@nestjs/common';
import { HttpModule } from '@nestjs/axios';
import { ConfigModule, ConfigService } from '@nestjs/config';

import { MlClientService } from './ml-client.service';

@Module({
  imports: [
    HttpModule.registerAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        baseURL: config.get('ML_SERVICE_URL'), // http://ml:8000, from .env
        timeout: 5000, // fail fast rather than hang if the ML service is down
      }),
    }),
  ],
  providers: [MlClientService],
  exports: [MlClientService],
})
export class MlClientModule {}