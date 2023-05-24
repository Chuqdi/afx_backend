import { ApiProperty } from '@nestjs/swagger';
import { IsString } from 'class-validator';

export class AuthForgotPasswordUserDto {
  @ApiProperty()
  @IsString()
  username: string;
}
