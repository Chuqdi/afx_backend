import { Injectable } from '@nestjs/common';
import { errorResponse, successResponse } from '../common/helpers/http.helper';
import { PrismaService } from 'nestjs-prisma';

@Injectable()
export class LibrariesService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    try {
      const libraries = await this.prisma.library.findMany({});

      return successResponse(libraries);
    } catch (error) {
      console.log(error);
      return errorResponse(error);
    }
  }
}
