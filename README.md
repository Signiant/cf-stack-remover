# cf-stack-remover
delete specified stacks from cloudformation

# Purpose
Remove CloudFormation stacks from Amazon services. At time when manually deleting the stacks is possiblem it's certainly a pain. Obviously the solution is to automate the process. This solution will perform the following ways to delete the stacks within CloudFormation:
* Group delete stacks based on the StackStatus of the stacks
* Group delete Stacks based on the regex string which match a set of stacks
* Group delete 

# Prerequisites
* Python installed
* boto3 module instsalled
* Either an AWS role (if running on EC2) or an access key/secret key

# AWS Lambda/Cloudformation deployment

Manually creation of the template.yaml file

```
aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket dev2-useast1-lambda-deploy \
    --s3-prefix lambda-stack-remover \
    --output-template-file packaged-template.yaml \
    --profile dev2
```
Above command put template in bucket and stored at dev2-uswest2-lambda-deploy at lambda-stack-remover folder at dev2 user

```
aws cloudformation deploy  \
  --capabilities CAPABILITY_IAM \
  --template-file ./packaged-template.yaml  \
  --stack-name cloudformation-stack-remover  \
  --parameter-overrides StackStatus=ROLLBACK_COMPLETE ContainString=.* Dryrun=False Region=us-east-1 ExpireDays=30  \
  --profile dev2  \
  --region us-east-1
```

# Usage

The easiest way to run the tool is from docker (because docker rocks) or from any python environment.
You will need to pass in variables specific to the ECS task you want to affect

```
usage: lambda_cf_delete_stacks.py [-h] --stack-status STACK_STATUS
                                  [STACK_STATUS ...]
                                  [--contain-string CONTAIN_STRING]
                                  [--expire-days EXPIRE_DAYS] --region REGION
                                  [--profile PROFILE] [--verbose] [--dryrun]

Perform deletion on AWS cloudformation stacks based on criterias listed

optional arguments:
  -h, --help            show this help message and exit
  --stack-status STACK_STATUS [STACK_STATUS ...]
                        Stack status match to be deleted StackName. Example:
                        ROLLBACK_COMPLETE
  --contain-string CONTAIN_STRING
                        Regex String that match to be deleted StackName.
                        Example: 'A.*'
  --expire-days EXPIRE_DAYS
                        days since creation of the stack to be deleted.
                        Example: 30 will delete all stacks that are older than
                        30 days
  --region REGION       The AWS region the stack is in
  --profile PROFILE     The name of an aws cli profile to use.
  --verbose             Turn on DEBUG logging
  --dryrun              Do a dryrun - no changes will be performed
```

