resource "aws_s3_bucket" "this" {
  bucket = "face-authentication-bucket-01"
}

resource "aws_s3_bucket_notification" "this" {
  bucket = aws_s3_bucket.this.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_rekognition_index.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "rekognition-sign-up"
  }

  depends_on = [aws_lambda_permission.s3_rekognition_index]
}
