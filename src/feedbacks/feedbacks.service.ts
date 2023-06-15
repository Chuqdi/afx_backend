import { Injectable } from '@nestjs/common';
import { CreateFeedbackDto } from './dto/create-feedback.dto';
import { UpdateFeedbackDto } from './dto/update-feedback.dto';
import { PrismaService } from 'nestjs-prisma';
import { errorResponse, successResponse } from 'src/common/helpers/http.helper';

@Injectable()
export class FeedbacksService {
  constructor(private prisma: PrismaService) {}

  async create(cognitoId: string, createFeedbackDto: CreateFeedbackDto) {
    try {
      const newFeedback = await this.prisma.feedback.create({
        data: {
          ...createFeedbackDto,
          user: { connect: { cognitoId } },
        },
      });
      return successResponse(newFeedback);
    } catch (error) {
      console.log(error);
      return errorResponse(error);
    }
  }

  public async findAll(cognitoId: string, page: number, perPage: number) {
    try {
      const skip = +((page - 1) * perPage);
      const take = +perPage;
      const [items, total] = await Promise.all([
        this.prisma.feedback.findMany({
          where: { user: { cognitoId } },
          skip,
          take,
        }),
        this.prisma.feedback.count({
          where: { user: { cognitoId } },
        }),
      ]);
      const totalPages = Math.ceil(total / perPage);

      return successResponse({
        items,
        page,
        perPage,
        total,
        totalPages,
      });
    } catch (error) {
      return errorResponse(error);
    }
  }

  async findOne(id: string) {
    try {
      const feedback = await this.prisma.feedback.findUniqueOrThrow({
        where: { id },
      });
      return successResponse(feedback);
    } catch (error) {
      console.log(error);
      return errorResponse(error);
    }
  }
}
