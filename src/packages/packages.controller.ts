import { Controller, Get, Param } from '@nestjs/common';
import { PackagesService } from './packages.service';
import { ApiTags } from '@nestjs/swagger';

@ApiTags('Packages')
@Controller('packages')
export class PackagesController {
  constructor(private readonly packagesService: PackagesService) {}

  @Get(':libraryId')
  findForLibraries(@Param('libraryId') libraryId: string) {
    return this.packagesService.findByLibrary(libraryId);
  }
}
