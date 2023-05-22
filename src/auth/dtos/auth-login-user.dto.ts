import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, Matches } from 'class-validator';

export class AuthLoginUserDto {
  @ApiProperty()
  @IsEmail()
  email: string;

  @ApiProperty({
    description:
      'Minimum eight characters, at least one uppercase letter, one lowercase letter, one number, and one special character',
  })
  @Matches(
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$&+,:;=?@#|'<>.^*()%!-])[A-Za-z\d@$&+,:;=?@#|'<>.^*()%!-]{8,}$/,
    { message: 'invalid password' },
  )
  password: string;
}
