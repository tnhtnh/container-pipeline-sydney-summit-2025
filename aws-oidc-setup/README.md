# aws-oidc-setup

This provides example CloudFormation on how to initially set up an OIDC trust between the account and GitHub

## GitHub Actions and OIDC trust

The CloudFormation `oidc.yml` sets up an OIDC trust between AWS and GitHub Actions as per https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services

### How to use

1. Deploy the CloudFormation stack in the region in your account
2. Provide the GitHub repo name and OIDC claims that you want to use

#### Example

If you are wanting to generate an OIDC trust for GitHub repo https://github.com/bjss/example-aws-sam-app, use "repo:bjss/example-aws-sam-app:*" as the subject claim.


### References

https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
https://github.com/aws-samples/aws-codedeploy-github-actions-deployment/tree/main/cloudformation
https://aws.amazon.com/blogs/devops/integrating-with-github-actions-ci-cd-pipeline-to-deploy-a-web-app-to-amazon-ec2/