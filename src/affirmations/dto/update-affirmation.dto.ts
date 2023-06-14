import { PartialType } from '@nestjs/swagger';
import { CreateAffirmationDto } from './create-affirmation.dto';

export class UpdateAffirmationDto extends PartialType(CreateAffirmationDto) {}
