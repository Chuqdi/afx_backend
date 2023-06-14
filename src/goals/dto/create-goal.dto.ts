import { ApiProperty } from '@nestjs/swagger';
import { IsDateString, IsString } from 'class-validator';

export class CreateGoalDto {
  @ApiProperty()
  @IsString()
  readonly content: string;

  @ApiProperty()
  @IsDateString()
  readonly startAt: Date;

  @ApiProperty()
  @IsDateString()
  readonly endAt: Date;
}
