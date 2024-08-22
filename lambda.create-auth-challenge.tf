data "archive_file" "create_auth_challenge" {
  type        = "zip"
  source_file = "lambdas/create-auth-challenge.py"
  output_path = "create-auth-challenge.zip"
}

resource "aws_lambda_function" "create_auth_challenge" {
  filename      = "create-auth-challenge.zip"
  function_name = "create-auth-challenge"
  role             = aws_iam_role.this.arn
  handler          = "create-auth-challenge.handler"
  source_code_hash = data.archive_file.create_auth_challenge.output_base64sha256
  runtime          = "python3.8"	

  environment {
    variables = {
      DYNAMODB_COLLECTION_ID = aws_dynamodb_table.this.id
    }
  }
}
