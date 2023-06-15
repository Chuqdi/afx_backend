import { Injectable } from '@nestjs/common';
import { PrismaService } from 'nestjs-prisma';
import { errorResponse, successResponse } from 'src/common/helpers/http.helper';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import * as dayjs from 'dayjs';

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  async create(createUserDto: CreateUserDto) {
    try {
      const newUser = await this.prisma.user.create({
        data: {
          ...createUserDto,
          firstName: '',
          lastName: '',
          birthday: new Date(),
          pronoun: '',
          occupation: '',
          mentoringVoice: '',
          attractPeople: '',
          anxietries: [],
          interests: [],
        },
      });
      return successResponse(newUser);
    } catch (error) {
      return errorResponse(error);
    }
  }

  findAll() {
    return `This action returns all users`;
  }

  async findOneById(id: string) {
    try {
      const user = await this.prisma.user.findUniqueOrThrow({
        where: { id: id },
      });
      return successResponse(user);
    } catch (error) {
      return errorResponse(error);
    }
  }

  async findOneByCognitoId(cognitoId: string) {
    try {
      const user = await this.prisma.user.findUniqueOrThrow({
        where: { cognitoId: cognitoId },
        select: { id: true },
      });
      return successResponse(user);
    } catch (error) {
      return errorResponse(error);
    }
  }

  async update(id: string, updateUserDto: UpdateUserDto) {
    try {
      const updatedUser = await this.prisma.user.update({
        where: { id: id },
        data: {
          ...updateUserDto,
          birthday: dayjs(updateUserDto.birthday).toDate(),
        },
      });
      return successResponse(updatedUser);
    } catch (error) {
      return errorResponse(error);
    }
  }
}
