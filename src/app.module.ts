import { Module, Logger } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AuthModule } from './auth/auth.module';
import { UsersModule } from './users/users.module';
import { GoalsModule } from './goals/goals.module';
import { LibrariesModule } from './libraries/libraries.module';
import { PackagesModule } from './packages/packages.module';
import { PrismaModule, loggingMiddleware } from 'nestjs-prisma';
import { AffirmationsModule } from './affirmations/affirmations.module';
import { FeedbacksModule } from './feedbacks/feedbacks.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    PrismaModule.forRoot({
      isGlobal: true,
      prismaServiceOptions: {
        middlewares: [
          loggingMiddleware({
            logger: new Logger('PrismaMiddleware'),
            logLevel: 'log',
          }),
        ],
      },
    }),
    AuthModule,
    UsersModule,
    GoalsModule,
    AffirmationsModule,
    FeedbacksModule,
    LibrariesModule,
    PackagesModule,
  ],
})
export class AppModule {}
