import {
  Controller,
  Get,
  UseGuards,
} from '@nestjs/common';
import { LibrariesService } from './libraries.service';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { AuthGuard } from '@nestjs/passport';

@ApiTags('Libraries')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller('libraries')
export class LibrariesController {
  constructor(private readonly librariesService: LibrariesService) {}

  @Get()
  findAll() {
    return this.librariesService.findAll();
  }
}
