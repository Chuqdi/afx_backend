import { ApiProperty } from '@nestjs/swagger';
import { IsString } from 'class-validator';

export class AuthRefreshSessionUserDto {
  @ApiProperty()
  @IsString()
  username: string;

  @ApiProperty()
  @IsString()
  refreshToken: string;
}
