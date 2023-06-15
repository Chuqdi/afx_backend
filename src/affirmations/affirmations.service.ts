import { Injectable } from '@nestjs/common';
import { CreateAffirmationDto } from './dto/create-affirmation.dto';
import { UpdateAffirmationDto } from './dto/update-affirmation.dto';
import { errorResponse, successResponse } from '../common/helpers/http.helper';
import { PrismaService } from 'nestjs-prisma';

@Injectable()
export class AffirmationsService {
  constructor(private prisma: PrismaService) {}

  create(createAffirmationDto: CreateAffirmationDto) {
    return 'This action adds a new affirmation';
  }

  findAll() {
    return `This action returns all affirmations`;
  }

  async findByPackageId(packageId: string) {
    try {
      const affirmations = await this.prisma.affirmation.findMany({
        where: {
          packageId,
        },
      });
      return successResponse(affirmations);
    } catch (error) {
      console.log(error);
      return errorResponse(error);
    }
  }

  async findByUserId(userId: string) {
    try {
      const affirmations = await this.prisma.affirmation.findMany({
        where: {
          userId,
        },
      });
      return successResponse(affirmations);
    } catch (error) {
      console.log(error);
      return errorResponse(error);
    }
  }

  findOne(id: number) {
    return `This action returns a #${id} affirmation`;
  }

  update(id: number, updateAffirmationDto: UpdateAffirmationDto) {
    return `This action updates a #${id} affirmation`;
  }

  remove(id: number) {
    return `This action removes a #${id} affirmation`;
  }
}
