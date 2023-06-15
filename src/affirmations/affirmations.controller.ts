import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  UseGuards,
} from '@nestjs/common';
import { AffirmationsService } from './affirmations.service';
import { CreateAffirmationDto } from './dto/create-affirmation.dto';
import { UpdateAffirmationDto } from './dto/update-affirmation.dto';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { AuthGuard } from '@nestjs/passport';

@ApiTags('Affirmations')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
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
