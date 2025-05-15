#!/bin/bash

# Function to create or update a CloudFormation stack
deploy_stack() {
    local stack_name=$1
    local template_file=$2
    local operation=$3

    if [ "$operation" == "create" ]; then
        echo "Creating stack: $stack_name"
        aws cloudformation create-stack \
            --stack-name "$stack_name" \
            --template-body "file://$template_file" \
            --capabilities CAPABILITY_NAMED_IAM

        aws cloudformation wait stack-create-complete --stack-name "$stack_name"
    elif [ "$operation" == "update" ]; then
        echo "Updating stack: $stack_name"
        if aws cloudformation update-stack \
            --stack-name "$stack_name" \
            --template-body "file://$template_file" \
            --capabilities CAPABILITY_NAMED_IAM; then
            
            aws cloudformation wait stack-update-complete --stack-name "$stack_name"
        else
            echo "No updates are to be performed on $stack_name"
        fi
    else
        echo "Invalid operation: $operation"
        exit 1
    fi

    # shellcheck disable=SC2181
    if [ $? -eq 0 ]; then
        echo "$operation completed successfully for $stack_name"
    else
        echo "$operation failed for $stack_name"
        exit 1
    fi
}

# Main function to process the stacks
process_stacks() {
    local operation=$1
    shift
    local stacks=("$@")

    for stack in "${stacks[@]}"; do
        IFS=':' read -r -a stack_info <<< "$stack"
        stack_name="${stack_info[0]}"
        template_file="${stack_info[1]}"

        deploy_stack "$stack_name" "$template_file" "$operation"
    done
}

# Check if correct number of arguments is provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <create|update> <stack_name:template_file> [<stack2_name:template2_file> ...]"
    exit 1
fi

# Extract operation and shift arguments
operation=$1
shift

# Call the process_stacks function with the operation and the remaining arguments
process_stacks "$operation" "$@"