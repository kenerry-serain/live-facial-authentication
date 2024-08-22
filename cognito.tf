resource "aws_cognito_user_pool" "this" {
  name = "face-authentication-user-pool"

  lambda_config {
    create_auth_challenge          = aws_lambda_function.create_auth_challenge.arn
    define_auth_challenge          = aws_lambda_function.define_auth_challenge.arn
    verify_auth_challenge_response = aws_lambda_function.verify_auth_challenge.arn
  }
}

resource "aws_cognito_user_pool_client" "this" {
  name                = "client"
  user_pool_id        = aws_cognito_user_pool.this.id
  explicit_auth_flows = ["ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"]
}
