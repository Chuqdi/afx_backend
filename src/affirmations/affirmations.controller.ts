import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { AffirmationsService } from './affirmations.service';
import { CreateAffirmationDto } from './dto/create-affirmation.dto';
import { UpdateAffirmationDto } from './dto/update-affirmation.dto';
import { ApiTags } from '@nestjs/swagger';

@ApiTags('Affirmations')
@Controller('affirmations')
export class AffirmationsController {
  constructor(private readonly affirmationsService: AffirmationsService) {}

  @Post()
  create(@Body() createAffirmationDto: CreateAffirmationDto) {
    return this.affirmationsService.create(createAffirmationDto);
  }

  @Get()
  findAll() {
    return this.affirmationsService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.affirmationsService.findOne(+id);
  }

  @Get('package/:packageId')
  findForPackage(@Param('packageId') packageId: string) {
    return this.affirmationsService.findByPackageId(packageId);
  }

  @Get('user/:userId')
  findForUser(@Param('userId') userId: string) {
    return this.affirmationsService.findByUserId(userId);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateAffirmationDto: UpdateAffirmationDto,
  ) {
    return this.affirmationsService.update(+id, updateAffirmationDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.affirmationsService.remove(+id);
  }
}
