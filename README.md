## greengrass-v2-secrets-manager-python

This code sample demonstrates how to integrate Secrets Manager with Greengrass v2 via components. At the end of the sample, you will have a Python-based component that can use secret values stored on the cloud and synced to the edge. 

### AWS CLI setup

Ensure you have AWS CLI installed, a IAM user with an access key, and a named profile configured:

* [Installing, updating, and uninstalling the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
* [Configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
* [Named profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)

### Define key variables

```console
export AWS_PROFILE=<PROFILE-NAME>
export AWS_REGION=<REGION>
export BUCKET_NAME=<YOUR_BUCKET_NAME> 
```

### Optional: create AWS S3 bucket for GGv2 component
```console
aws s3 mb s3://$BUCKET_NAME --profile $AWS_PROFILE --region $AWS_REGION
```

### Define your secret value
> NOTE: This will be stored in AWS Secrets Manager, do not hard-code these variables in your application!
```console
echo -n Enter secret value: && read -s SECRET_VALUE
```

### Create secret in AWS Secrets Manager

```console
aws secretsmanager create-secret --name greengrass_v2_secret --profile $AWS_PROFILE --region $AWS_REGION
export SECRET_ARN=$(aws secretsmanager describe-secret --secret-id greengrass_v2_secret --profile $AWS_PROFILE)
aws secretsmanager put-secret-value --profile $AWS_PROFILE --secret-id greengrass_v2_secret --secret-string "{\"SECRET_VALUE\":\"$SECRET_VALUE\"}" --region $AWS_REGION
```

### Update Token Exchange Service (TES) role for Greengrass v2

> NOTE: the following assumes your Greengrass v2 TES role name is the default value, **MyGreengrassV2TokenExchangeRole**. If you have a custom role name for TES, please update accordingly.

Add permissions for Secrets Manager
```console
export SECRET_POLICY_DOC="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Action\":\"secretsmanager:GetSecretValue\",\"Resource\":\"$SECRET_ARN\"}]}"
export SECRET_POLICY_ARN=$(aws iam create-policy --policy-name secret_ggv2_policy --policy-document $SECRET_POLICY_DOC --profile $AWS_PROFILE | jq -r .Policy.Arn)
aws iam attach-role-policy --profile $AWS_PROFILE --role-name MyGreengrassV2TokenExchangeRole --policy-arn $SECRET_POLICY_ARN
```

Add permissions for S3
```console
export S3_POLICY_DOC="{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Allow\",\"Action\":[\"s3:GetObject\"],\"Resource\":\"arn:aws:s3:::$BUCKET_NAME/*\"}]}"
export S3_POLICY_ARN=$(aws iam create-policy --policy-name s3_ggv2_policy --policy-document $S3_POLICY_DOC --profile $AWS_PROFILE | jq -r .Policy.Arn)
aws iam attach-role-policy --profile $AWS_PROFILE --role-name MyGreengrassV2TokenExchangeRole --policy-arn $S3_POLICY_ARN
```


### Update recipes
* In components/recipe/aws.sagemaker.edgeManager-0.1.0.yaml, update the URI with by replacing <YOUR_BUCKET_NAME> with your S3 bucket for Greengrass v2 components:
```yaml
- URI: s3://YOUR_BUCKET_NAME/artifacts/com.aws.secretsManagerPythonExample/0.1.0/secrets_manager_demo.py
```

### Upload your custom components to S3 bucket
```console
./scripts/upload_component_version.sh $AWS_PROFILE com.aws.secretsManagerPythonExample 0.1.0 $BUCKET_NAME $AWS_REGION
```

> NOTE: you cannot overwrite an existing component version. To upload a new version, you will need to update the version number in the artifact directory, the recipe file name, and the version numbers in the recipe file.
> As an alternative, you can also delete a specific component version. For this, use the following command:
```console
./delete_component.sh $AWS_PROFILE <COMPONENT-NAME> <COMPONENT-VERSION> $AWS_REGION
```

### Update your Greengrass v2 deployment

Create a new Greengrass v2 deployment, including the following components:
* com.aws.secretsManagerPythonExample v0.1.0

When [configuring your component](https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html), make sure you copy/the following JSON snippet into **Configuration to merge** (with your secret ARN created previously). Then click **Confirm**.

```json
{
  "cloudSecrets": [
    {
      "arn": "YOUR_SECRET_ARN"
    } 
  ]
}
```

### Test and validate

In the AWS Management Console, go to **AWS IoT Core** >> **Test** >> **MQTT test client**.

In *Subscription Topic*, enter **ggv2/secrets/demo**, and click **Subscribe to topic**. You should now see your secret being published to AWS IoT Core. 

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.





