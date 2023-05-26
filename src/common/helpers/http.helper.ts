const successResponse = <T>(
  data: T,
): {
  success: true;
  data: T;
} => {
  return {
    success: true,
    data,
  };
};

const errorResponse = (
  errorMsg: string | null = null,
): {
  success: false;
  data: null;
  message: string | null;
} => {
  return {
    success: false,
    data: null,
    message: errorMsg,
  };
};

export { successResponse, errorResponse };
