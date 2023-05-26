import { ApiProperty } from '@nestjs/swagger';
import {
  ArrayMinSize,
  IsArray,
  IsBoolean,
  IsString,
  MinLength,
} from 'class-validator';

export class UpdateUserDto {
  @ApiProperty()
  @IsBoolean()
  readonly onboarded: boolean;

  @ApiProperty()
  @IsString()
  @MinLength(2, { message: 'First name is too short' })
  readonly firstName: string;

  @ApiProperty()
  @IsString()
  @MinLength(2, { message: 'Last name is too short' })
  readonly lastName: string;

  @ApiProperty()
  @IsString()
  readonly birthday: string;

  @ApiProperty()
  @IsString()
  readonly pronoun: string;

  @ApiProperty()
  @IsString()
  readonly occupation: string;

  @ApiProperty()
  @IsString()
  readonly mentoringVoice: string;

  @ApiProperty()
  @IsString()
  readonly attractPeople: string;

  @ApiProperty()
  @IsArray()
  @IsString({ each: true })
  @ArrayMinSize(1)
  readonly anxietries: string[];

  @ApiProperty()
  @IsArray()
  @IsString({ each: true })
  @ArrayMinSize(1)
  readonly interests: string[];
}
