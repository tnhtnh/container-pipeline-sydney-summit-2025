# aws-oidc-setup

This provides example CloudFormation on how to initially set up an OIDC trust between an AWS account and GitHub Actions for CI/CD. **This is an example setup for the repo `tnhtnh/container-pipeline-sydney-summit-2025`. You should customize it for your own environment and security requirements.**

## GitHub Actions and OIDC trust

The CloudFormation `oidc.yml` sets up an OIDC trust between AWS and GitHub Actions as per https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services

### How to use

1. Deploy the CloudFormation stack in your AWS account and region.
2. Provide the GitHub repo name and OIDC claims that you want to use.

#### Example

If you are generating an OIDC trust for the GitHub repo https://github.com/tnhtnh/container-pipeline-sydney-summit-2025, use `repo:tnhtnh/container-pipeline-sydney-summit-2025:*` as the subject claim.

### References

https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
https://github.com/aws-samples/aws-codedeploy-github-actions-deployment/tree/main/cloudformation
https://aws.amazon.com/blogs/devops/integrating-with-github-actions-ci-cd-pipeline-to-deploy-a-web-app-to-amazon-ec2/