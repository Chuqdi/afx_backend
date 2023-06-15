import { Injectable } from '@nestjs/common';
import { PrismaService } from 'nestjs-prisma';
import { errorResponse, successResponse } from 'src/common/helpers/http.helper';
import { CreateGoalDto } from './dto/create-goal.dto';
import * as dayjs from 'dayjs';

@Injectable()
export class GoalsService {
  constructor(private prisma: PrismaService) {}

  async create(cognitoId: string, createGoalDto: CreateGoalDto) {
    try {
      const newGoal = await this.prisma.goal.create({
        data: {
          ...createGoalDto,
          startAt: dayjs(createGoalDto.startAt).toDate(),
          endAt: dayjs(createGoalDto.endAt).toDate(),
          user: { connect: { cognitoId } },
        },
      });
      return successResponse(newGoal);
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
        this.prisma.goal.findMany({
          where: { user: { cognitoId } },
          skip,
          take,
        }),
        this.prisma.goal.count({
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
      const goal = await this.prisma.goal.findUniqueOrThrow({
        where: { id },
      });
      return successResponse(goal);
    } catch (error) {
      console.log(error);
      return errorResponse(error);
    }
  }
}
