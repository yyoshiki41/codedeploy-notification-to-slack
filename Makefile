.PHONY: clean package deploy

clean:
	rm -f packaged.yaml

package:
	sam package --template-file template.yaml \
		--output-template-file packaged.yaml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix codedeploy-notification-to-slack

deploy: package
	sam deploy --template-file packaged.yaml \
		--stack-name sam-app-codedeploy-notification-to-slack \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides \
		SNSTopicArn=$(SNS_TOPIC_ARN) \
		KeyIdParameter=$(KEY_ID) \
		slackChannelParameter=$(SLACK_CHANNEL) \
		kmsEncryptedHookUrlParameter=$(KMS_ENCRYPTED_HOOK_URL)
