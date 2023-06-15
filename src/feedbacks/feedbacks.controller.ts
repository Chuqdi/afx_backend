import {
  Body,
  Controller,
  Get,
  Param,
  Post,
  Query,
  Request,
  UseGuards,
} from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiBearerAuth, ApiQuery, ApiTags } from '@nestjs/swagger';
import { CreateFeedbackDto } from './dto/create-feedback.dto';
import { FeedbacksService } from './feedbacks.service';

@ApiTags('Feedbacks')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller('feedbacks')
export class FeedbacksController {
  constructor(private readonly feedbacksService: FeedbacksService) {}

  @Post()
  create(@Request() req, @Body() createFeedbackDto: CreateFeedbackDto) {
    return this.feedbacksService.create(req.user.username, createFeedbackDto);
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
    return this.feedbacksService.findAll(req.user.username, page, perPage);
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.feedbacksService.findOne(id);
  }
}
