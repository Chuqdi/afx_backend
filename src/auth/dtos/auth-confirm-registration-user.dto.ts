import { ApiProperty } from '@nestjs/swagger';
import { IsString } from 'class-validator';

export class AuthConfirmRegistrationUserDto {
  @ApiProperty()
  @IsString()
  username: string;

  @ApiProperty()
  @IsString()
  confirmationCode: string;
}
