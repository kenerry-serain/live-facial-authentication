data "archive_file" "s3_rekognition_index" {
  type        = "zip"
  source_file = "lambdas/s3-rekognition-index.py"
  output_path = "s3-rekognition-index.zip"
}

resource "aws_lambda_function" "s3_rekognition_index" {
  filename      = "s3-rekognition-index.zip"
  function_name = "s3-rekognition-index"
  role             = aws_iam_role.this.arn
  handler          = "s3-rekognition-index.handler"
  source_code_hash = data.archive_file.s3_rekognition_index.output_base64sha256
  runtime          = "python3.8"

  environment {
    variables = {
      DYNAMODB_COLLECTION_ID = aws_dynamodb_table.this.id
      REKOGNITION_COLLECTION_ID = aws_rekognition_collection.this.collection_id
    }
  }
}
