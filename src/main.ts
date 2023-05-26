import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { AllExceptionsFilter } from './common/filters/http-exception.filter';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { PrismaService } from './common/db/prisma.service';
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Validation
  app.useGlobalPipes(new ValidationPipe());

  // enable shutdown hook
  const prismaService: PrismaService = app.get(PrismaService);
  await prismaService.enableShutdownHooks(app);

  // Filter
  app.useGlobalFilters(new AllExceptionsFilter());

  // Swagger Api
  const config = new DocumentBuilder()
    .setTitle('Affirmatrix API')
    .setDescription('The Affirmatrix API description')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, document);

  // Cors
  app.enableCors({
    origin: '*',
  });

  await app.listen(3000);
}
bootstrap();
