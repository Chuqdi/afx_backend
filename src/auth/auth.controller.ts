import {
  Body,
  Controller,
  Post,
  UsePipes,
  ValidationPipe,
} from '@nestjs/common';
import { ApiTags } from '@nestjs/swagger';
import { AwsCognitoService } from './aws-cognito.service';
import { AuthChangePasswordUserDto } from './dtos/auth-change-password-user.dto';
import { AuthConfirmPasswordUserDto } from './dtos/auth-confirm-password-user.dto';
import { AuthConfirmRegistrationUserDto } from './dtos/auth-confirm-registration-user.dto';
import { AuthForgotPasswordUserDto } from './dtos/auth-forgot-password-user.dto';
import { AuthLoginUserDto } from './dtos/auth-login-user.dto';
import { AuthRegisterUserDto } from './dtos/auth-register-user.dto';
import { AuthRefreshSessionUserDto } from './dtos/auth-refresh-session-user.dto';

@ApiTags('Auth')
@Controller('auth')
export class AuthController {
  constructor(private awsCognitoService: AwsCognitoService) {}

  @Post('/register')
  async register(@Body() authRegisterUserDto: AuthRegisterUserDto) {
    return await this.awsCognitoService.registerUser(authRegisterUserDto);
  }

  @Post('/confirm-registration')
  async confirmRegistration(
    @Body() authConfirmRegistrationUserDto: AuthConfirmRegistrationUserDto,
  ) {
    return await this.awsCognitoService.conformUserRegistration(
      authConfirmRegistrationUserDto,
    );
  }

  @Post('/login')
  @UsePipes(ValidationPipe)
  async login(@Body() authLoginUserDto: AuthLoginUserDto) {
    return await this.awsCognitoService.authenticateUser(authLoginUserDto);
  }

  @Post('/refresh-session')
  @UsePipes(ValidationPipe)
  async refreshSession(
    @Body() authRefreshSessionUserDto: AuthRefreshSessionUserDto,
  ) {
    return await this.awsCognitoService.refreshUserSession(
      authRefreshSessionUserDto,
    );
  }

  @Post('/change-password')
  @UsePipes(ValidationPipe)
  async changePassword(
    @Body() authChangePasswordUserDto: AuthChangePasswordUserDto,
  ) {
    const result = await this.awsCognitoService.changeUserPassword(
      authChangePasswordUserDto,
    );

    if (result == 'SUCCESS') {
      return { status: 'success' };
    }
  }

  @Post('/forgot-password')
  @UsePipes(ValidationPipe)
  async forgotPassword(
    @Body() authForgotPasswordUserDto: AuthForgotPasswordUserDto,
  ) {
    return await this.awsCognitoService.forgotUserPassword(
      authForgotPasswordUserDto,
    );
  }

  @Post('/confirm-password')
  @UsePipes(ValidationPipe)
  async confirmPassword(
    @Body() authConfirmPasswordUserDto: AuthConfirmPasswordUserDto,
  ) {
    return await this.awsCognitoService.confirmUserPassword(
      authConfirmPasswordUserDto,
    );
  }
}
