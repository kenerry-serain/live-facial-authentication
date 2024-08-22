data "archive_file" "define_auth_challenge" {
  type        = "zip"
  source_file = "lambdas/define-auth-challenge.py"
  output_path = "define-auth-challenge.zip"
}

resource "aws_lambda_function" "define_auth_challenge" {
  filename      = "define-auth-challenge.zip"
  function_name = "define-auth-challenge"
  role             = aws_iam_role.this.arn
  handler          = "define-auth-challenge.handler"
  source_code_hash = data.archive_file.define_auth_challenge.output_base64sha256
  runtime          = "python3.8"

  environment {
    variables = {
      DYNAMODB_COLLECTION_ID = aws_dynamodb_table.this.id
    }
  }
}
