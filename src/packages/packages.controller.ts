import { Controller, Get, Param, UseGuards } from '@nestjs/common';
import { PackagesService } from './packages.service';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { AuthGuard } from '@nestjs/passport';

@ApiTags('Packages')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller('packages')
export class PackagesController {
  constructor(private readonly packagesService: PackagesService) {}

  @Get(':libraryId')
  findForLibraries(@Param('libraryId') libraryId: string) {
    return this.packagesService.findByLibrary(libraryId);
  }
}
