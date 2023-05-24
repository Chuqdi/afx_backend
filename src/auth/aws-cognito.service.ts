import { Injectable, Logger } from '@nestjs/common';
import {
  AuthenticationDetails,
  CognitoRefreshToken,
  CognitoUser,
  CognitoUserAttribute,
  CognitoUserPool,
} from 'amazon-cognito-identity-js';
import { AuthChangePasswordUserDto } from './dtos/auth-change-password-user.dto';
import { AuthConfirmRegistrationUserDto } from './dtos/auth-confirm-registration-user.dto';
import { AuthLoginUserDto } from './dtos/auth-login-user.dto';

import { AuthConfirmPasswordUserDto } from './dtos/auth-confirm-password-user.dto';
import { AuthForgotPasswordUserDto } from './dtos/auth-forgot-password-user.dto';
import { AuthRegisterUserDto } from './dtos/auth-register-user.dto';
import { AuthRefreshSessionUserDto } from './dtos/auth-refresh-session-user.dto';

@Injectable()
export class AwsCognitoService {
  private userPool: CognitoUserPool;
  logger = new Logger(AwsCognitoService.name);

  constructor() {
    this.userPool = new CognitoUserPool({
      UserPoolId: process.env.AWS_COGNITO_USER_POOL_ID,
      ClientId: process.env.AWS_COGNITO_CLIENT_ID,
    });
  }

  async registerUser(authRegisterUserDto: AuthRegisterUserDto) {
    const { username, name, email, password } = authRegisterUserDto;

    return new Promise((resolve, reject) => {
      this.userPool.signUp(
        username,
        password,
        [
          new CognitoUserAttribute({
            Name: 'name',
            Value: name,
          }),
          new CognitoUserAttribute({
            Name: 'email',
            Value: email,
          }),
        ],
        [
          new CognitoUserAttribute({
            Name: 'email',
            Value: email,
          }),
        ],
        (err, result) => {
          if (!result) {
            reject(err);
          } else {
            resolve(result.user);
          }
        },
      );
    });
  }

  async conformUserRegistration(
    authConfirmRegistrationUserDto: AuthConfirmRegistrationUserDto,
  ) {
    const { username, confirmationCode } = authConfirmRegistrationUserDto;

    const userData = {
      Username: username,
      Pool: this.userPool,
    };

    const userCognito = new CognitoUser(userData);

    return new Promise((resolve, reject) => {
      userCognito.confirmRegistration(
        confirmationCode,
        false,
        (err, result) => {
          if (!result) {
            reject(err);
          } else {
            resolve(result.user);
          }
        },
      );
    });
  }

  async getUserInformation(authLoginUserDto: AuthLoginUserDto) {
    const { username, password } = authLoginUserDto;

    const userData = {
      Username: username,
      Pool: this.userPool,
    };

    const userCognito = new CognitoUser(userData);

    const authenticationDetails = new AuthenticationDetails({
      Username: username,
      Password: password,
    });

    return new Promise((resolve, reject) => {
      userCognito.authenticateUser(authenticationDetails, {
        onSuccess: () => {
          userCognito.getUserAttributes((err, result) => {
            if (err) {
              reject(err);
              return;
            }
            resolve(result);
          });
        },
        onFailure: (err) => {
          reject(err);
        },
      });
    });
  }

  async authenticateUser(authLoginUserDto: AuthLoginUserDto) {
    const { username, password } = authLoginUserDto;
    const userData = {
      Username: username,
      Pool: this.userPool,
    };

    const authenticationDetails = new AuthenticationDetails({
      Username: username,
      Password: password,
    });

    const userCognito = new CognitoUser(userData);

    return new Promise((resolve, reject) => {
      userCognito.authenticateUser(authenticationDetails, {
        onSuccess: (session) => {
          userCognito.getUserAttributes((err, userAttributes) => {
            if (err) {
              reject(err);
              return;
            }
            resolve({
              accessToken: session.getAccessToken().getJwtToken(),
              refreshToken: session.getRefreshToken().getToken(),
              information: userAttributes.reduce((user, currentAttr) => {
                user[currentAttr.Name] = currentAttr.Value;
                return user;
              }, {}),
            });
          });
        },
        onFailure: (err) => {
          reject(err);
        },
      });
    });
  }

  async refreshUserSession(
    authRefreshSessionUserDto: AuthRefreshSessionUserDto,
  ) {
    const { username, refreshToken } = authRefreshSessionUserDto;

    const cognitoRefreshToken = new CognitoRefreshToken({
      RefreshToken: refreshToken,
    });

    const userData = {
      Username: username,
      Pool: this.userPool,
    };

    const userCognito = new CognitoUser(userData);

    return new Promise((resolve, reject) => {
      userCognito.refreshSession(cognitoRefreshToken, (err, result) => {
        if (!result) {
          reject(err);
        } else {
          resolve({
            accessToken: result.getAccessToken().getJwtToken(),
            refreshToken: result.getRefreshToken().getToken(),
          });
        }
      });
    });
  }

  async changeUserPassword(
    authChangePasswordUserDto: AuthChangePasswordUserDto,
  ) {
    const { username, currentPassword, newPassword } =
      authChangePasswordUserDto;

    const userData = {
      Username: username,
      Pool: this.userPool,
    };

    const authenticationDetails = new AuthenticationDetails({
      Username: username,
      Password: currentPassword,
    });

    const userCognito = new CognitoUser(userData);

    return new Promise((resolve, reject) => {
      userCognito.authenticateUser(authenticationDetails, {
        onSuccess: () => {
          userCognito.changePassword(
            currentPassword,
            newPassword,
            (err, result) => {
              if (err) {
                reject(err);
                return;
              }
              resolve(result);
            },
          );
        },
        onFailure: (err) => {
          reject(err);
        },
      });
    });
  }

  async forgotUserPassword(
    authForgotPasswordUserDto: AuthForgotPasswordUserDto,
  ) {
    const { username } = authForgotPasswordUserDto;

    const userData = {
      Username: username,
      Pool: this.userPool,
    };

    const userCognito = new CognitoUser(userData);

    return new Promise((resolve, reject) => {
      userCognito.forgotPassword({
        onSuccess: (result) => {
          resolve(result);
        },
        onFailure: (err) => {
          reject(err);
        },
      });
    });
  }

  async confirmUserPassword(
    authConfirmPasswordUserDto: AuthConfirmPasswordUserDto,
  ) {
    const { username, confirmationCode, newPassword } =
      authConfirmPasswordUserDto;

    const userData = {
      Username: username,
      Pool: this.userPool,
    };

    const userCognito = new CognitoUser(userData);

    return new Promise((resolve, reject) => {
      userCognito.confirmPassword(confirmationCode, newPassword, {
        onSuccess: () => {
          resolve({ status: 'success' });
        },
        onFailure: (err) => {
          reject(err);
        },
      });
    });
  }
}
