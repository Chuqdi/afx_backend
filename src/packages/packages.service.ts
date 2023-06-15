import { Injectable } from '@nestjs/common';
import { errorResponse, successResponse } from '../common/helpers/http.helper';
import { PrismaService } from 'nestjs-prisma';

@Injectable()
export class PackagesService {
  constructor(private prisma: PrismaService) {}

  async findByLibrary(libraryId: string) {
    try {
      const packages = await this.prisma.package.findMany({
        where: {
          libraries: {
            some: {
              id: libraryId,
            },
          },
        },
      });

      return successResponse(packages);
    } catch (error) {
      console.log(error);
      return errorResponse(error);
    }
  }
}
