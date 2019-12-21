# AWS Lambda function to notify codedeploy events to slack

AWS Serverless Application: CodeDeploy notification to slack

## Design

1. CodeDeploy send event notification to Amazon SNS
2. Invoking AWS Lambda functions via Amazon SNS
3. Post to slack

## Resources

- CodeDeploy
- SNS Topic
- KMS
- lambda (python3.7)

## Preparation

### 1. Create a SNS Topic

```bash
$ aws sns create-topic --name codedeploy
```

### 2. Create notification rule in CodeDeploy application.

Select events that trigger notifications, and then choose above SNS Topic as targets.

### 3. Create a customer managed CMK.

https://docs.aws.amazon.com/en_us/kms/latest/developerguide/concepts.html#customer-cmk

### 4. Prepare parameters

Encrypt slack webhook url using above CMK.

```bash
$ aws kms encrypt --key-id alias/xxx --plaintext "hooks.slack.com/services/xxx"
{
    "CiphertextBlob": "xxx",
    "KeyId": "arn:aws:kms:ap-northeast-1:abc:key/xxx"
}
```

- `KMS_ENCRYPTED_HOOK_URL`
  "CiphertextBlob"
- `KEY_ID`
  "KeyId"

### 5. Deploy lambda function

```bash
$ S3_BUCKET=sam-artifacts \
SNS_TOPIC_ARN=arn:aws:sns:ap-northeast-1:abc:xxx \
KEY_ID=xxx \
SLACK_CHANNEL=#channel \
KMS_ENCRYPTED_HOOK_URL=xxx \
make deploy
```

### Environment variables

- `S3_BUCKET`
  s3 bucket for lambda source code
- `SNS_TOPIC_ARN`
  created sns topic
- `KEY_ID`
  created a customer managed CMK key id
- `SLACK_CHANNEL`
  slack channel
- `KMS_ENCRYPTED_HOOK_URL`
  encrypted slack webhook url using CMK

## Related Projects

- [CodePipeline notification to slack](https://github.com/yyoshiki41/codepipeline-notification-to-slack)
