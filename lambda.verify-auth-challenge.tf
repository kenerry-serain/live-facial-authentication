data "archive_file" "verify_auth_challenge" {
  type        = "zip"
  source_file = "lambdas/verify-auth-challenge.py"
  output_path = "verify-auth-challenge.zip"
}

resource "aws_lambda_function" "verify_auth_challenge" {
  filename         = "verify-auth-challenge.zip"
  function_name    = "verify-auth-challenge"
  role             = aws_iam_role.this.arn
  handler          = "verify-auth-challenge.handler"
  source_code_hash = data.archive_file.verify_auth_challenge.output_base64sha256
  runtime          = "python3.8"

  environment {
    variables = {
      USER_FACES_BUCKET         = aws_s3_bucket.this.bucket
      REKOGNITION_COLLECTION_ID = aws_rekognition_collection.this.collection_id
    }
  }
}
