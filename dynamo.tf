resource "aws_dynamodb_table" "this" {
  name           = "face-authentication-table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "UserId"

  attribute {
    name = "UserId"
    type = "S"
  }

  global_secondary_index {
    name            = "UserId-index"
    hash_key        = "UserId"
    write_capacity  = 1
    read_capacity   = 1
    projection_type = "ALL"
  }
}
