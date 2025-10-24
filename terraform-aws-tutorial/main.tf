# 1. Tells Terraform you want to use the AWS provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # Use any recent version
    }
  }
}

# 2. Configures the AWS provider (e.g., which region)
# It will automatically use the credentials you set with 'aws configure'
provider "aws" {
  region = "us-east-1"
}

# 3. This is your resource
# It defines an S3 bucket
resource "aws_s3_bucket" "my_first_tf_bucket" {
  
  # IMPORTANT: CHANGE THIS NAME to something unique
  # Bucket names must be globally unique, like a domain name
  bucket = "dataengineering-terraform-s3-bucket-73564"
  
  tags = {
    Name        = "My first TF S3 bucket"
    Environment = "Dev"
  }
}