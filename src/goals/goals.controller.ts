import {
  Body,
  Controller,
  Get,
  Post,
  Query,
  Request,
  UseGuards,
  Param,
} from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiBearerAuth, ApiQuery, ApiTags } from '@nestjs/swagger';
import { CreateGoalDto } from './dto/create-goal.dto';
import { GoalsService } from './goals.service';

@ApiTags('Goals')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller('goals')
export class GoalsController {
  constructor(private readonly goalsService: GoalsService) {}

  @Post()
  create(@Request() req, @Body() createGoalDto: CreateGoalDto) {
    return this.goalsService.create(req.user.username, createGoalDto);
  }

  @Get()
  @ApiQuery({
    name: 'page',
    description: 'Page number',
    example: 1,
    required: true,
  })
  @ApiQuery({
    name: 'perPage',
    description: 'Prize per page',
    example: 10,
    required: true,
  })
  findAll(
    @Request() req,
    @Query('page') page: number,
    @Query('perPage') perPage: number,
  ) {
    return this.goalsService.findAll(req.user.username, page, perPage);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.goalsService.findOne(id);
  }
}
