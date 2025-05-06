# aws-oicd-setup

This provides example cloudformaiton on how to initally set up an OICD trust between the account and GitHub

## GitHub Actions and OICD trust

The cloudformation `oicd.yml` sets up an OICD trust between AWS and GitHub Actions as per https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services

### How to use

1. Deploy the cloudformaiton stack in the region in your account
2. Provide the GitHub repo name and OICD claims that you want to use

#### Example

If you are wanting to generate a OICD trust for GitHub repo https://github.com/bjss/example-aws-sam-python-devsecops-pipeline including all branches and all environments, set the `GitHubOIDCSubject` Cloudformation paramter as `repo:bjss/example-aws-sam-python-devsecops-pipeline:*`


### References

https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
https://github.com/aws-samples/aws-codedeploy-github-actions-deployment/tree/main/cloudformation
https://aws.amazon.com/blogs/devops/integrating-with-github-actions-ci-cd-pipeline-to-deploy-a-web-app-to-amazon-ec2/