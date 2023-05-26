import { Injectable, Logger } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { PrismaService } from 'src/common/db/prisma.service';
import { errorResponse, successResponse } from 'src/common/helpers/http.helper';

@Injectable()
export class UsersService {
  private logger = new Logger(UsersService.name);
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
      this.logger.error(error);
      return errorResponse();
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
      this.logger.error(error);
      return errorResponse('No user found with that id');
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
      this.logger.error(error);
      return errorResponse('No user found with that cognitoId');
    }
  }

  async update(id: string, updateUserDto: UpdateUserDto) {
    try {
      const updatedUser = await this.prisma.user.update({
        where: { id: id },
        data: {
          ...updateUserDto,
          birthday: new Date(updateUserDto.birthday),
        },
      });
      return successResponse(updatedUser);
    } catch (error) {
      this.logger.error(error);
      return errorResponse();
    }
  }
}
