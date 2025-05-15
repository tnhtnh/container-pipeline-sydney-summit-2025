# AWS ECS Deployment Demo

## Overview
This repository contains an example project for Trent Hornibrook's talk at AWS Sydney Summit 2025. It demonstrates modern deployment patterns for containerized applications on AWS using ECS Fargate, GitHub Actions, and infrastructure as code with CloudFormation.

## Architecture

This project showcases a complete CI/CD pipeline for deploying containerized applications to AWS with the following components:

- **ECS Fargate** for running containerized applications without managing servers
- **GitHub Actions** with AWS OIDC integration for secure deployments
- **CloudFormation** templates for infrastructure as code
- **Auto-scaling** based on CPU and memory metrics
- **Load balancing** with Application Load Balancer
- **Health monitoring** with CloudWatch alarms and Route53 health checks

## Repository Structure

- `/aws-oidc-setup/`: Scripts and templates for setting up OIDC trust between GitHub and AWS
- `/cloudformation/`: CloudFormation templates for infrastructure deployment:
  - `ecs.yml`: ECS cluster, service, and task definition
  - `ecr.yml`: Elastic Container Registry setup
  - `vpc.yml`: Virtual Private Cloud configuration
  - `dns.yml`: Route53 DNS configuration
  - `fis.yml`: Fault Injection Simulator configuration
  - `ecs-fargate-logs.yml`: Log configuration for Fargate tasks
  - `codeguru-bucket.yml`: S3 bucket setup for AWS CodeGuru

## Getting Started

### Prerequisites
- AWS CLI configured with appropriate permissions
- GitHub account with repository secrets configured
- Docker installed locally for container testing

### Setting up OIDC Trust

The repository includes an automated setup for GitHub Actions OIDC trust with AWS:

1. Navigate to the `aws-oidc-setup` directory
2. Run `./setup.sh create` to create the necessary OIDC provider and IAM roles
3. Configure your GitHub repository secrets using the output values

### Deploying Infrastructure

1. Review and customize the CloudFormation templates in the `/cloudformation/` directory
2. Deploy the infrastructure stack:
   ```
   aws cloudformation deploy --stack-name <stack-name> --template-file cloudformation/ecs.yml --capabilities CAPABILITY_IAM
   ```

### CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

1. Code changes pushed to main branch trigger the pipeline
2. Container images are built and pushed to ECR
3. ECS services are updated with the new container image
4. Health checks verify successful deployment

## Monitoring and Logging

The deployment includes several CloudWatch alarms for monitoring:
- CPU utilization
- Memory utilization
- HTTP 5xx error rates
- Response time metrics

## Security Features

- IAM roles with least privilege
- Security groups for network isolation
- OIDC trust for secure GitHub to AWS authentication
- No long-lived AWS credentials in CI/CD pipeline

## Contributing

This is an example project for demonstration purposes. Feel free to fork and modify according to your requirements.

## License

See the LICENSE file for details.

## Acknowledgments

- Trent Hornibrook for creating this example for AWS Sydney Summit 2025
- AWS for providing the services and documentation