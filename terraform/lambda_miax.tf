resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "lamda_policy" {
  name = "policy-lambds"
  description = "S3 Textract and Dynamo"
  policy =jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
          "Effect": "Allow",
          "Action": [
              "s3:*",
              "s3-object-lambda:*"
          ],
          "Resource": "*"
        },
        # {
        #   "Effect": "Allow",
        #   "Action": [
        #       "textract:*"
        #   ],
        #   "Resource": "*"
        # },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "test-attach" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lamda_policy.arn
}

resource "aws_lambda_function" "executable" {
  function_name = "test_terraform"
  image_uri     = "076977333390.dkr.ecr.eu-west-1.amazonaws.com/miax11minicloudprojectlambda:a856a9c6400e65c1a8d8f41b448200e9c9dcc77b"
  package_type  = "Image"
  role          = aws_iam_role.lambda_execution_role.arn
  memory_size = 1024
  timeout = 300
  environment {
    variables = {
      MIAX_API_KEY = "AIzaSyDHAEqnHMPZ5UTM_JSnEY0u65HFHiH6XaY"
    }
  }
}


resource "aws_cloudwatch_event_rule" "schedule" {
    name = "triger_each_day"
    description = "Schedule for Textract each five minutes"
    schedule_expression = "rate(1 minute)"
}

resource "aws_cloudwatch_event_target" "schedule_lambda" {
    rule = aws_cloudwatch_event_rule.schedule.name
    arn = aws_lambda_function.executable.arn
}

resource "aws_lambda_permission" "allow_events_bridge_to_run_lambda" {
    function_name = aws_lambda_function.executable.function_name
    
    statement_id = "CloudWatchInvoke"
    action = "lambda:InvokeFunction"

    source_arn = aws_cloudwatch_event_rule.schedule.arn

    principal = "events.amazonaws.com"
}

