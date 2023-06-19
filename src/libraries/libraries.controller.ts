import { Controller, Get } from '@nestjs/common';
import { LibrariesService } from './libraries.service';
import { ApiTags } from '@nestjs/swagger';

@ApiTags('Libraries')
@Controller('libraries')
export class LibrariesController {
  constructor(private readonly librariesService: LibrariesService) {}

  @Get()
  findAll() {
    return this.librariesService.findAll();
  }
}
