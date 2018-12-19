# cf-stack-remover
delete specified stacks from cloudformation

# Purpose


# Prerequisites


# Usage
cf  

The easiest way to run the tool is from docker (because docker rocks).
You will need to pass in variables specific to the ECS task you want to affect

```bash
usage: cf_delete_stacks.py [-h] --stack-status STACK_STATUS [STACK_STATUS ...]
                           [--contain-string CONTAIN_STRING] --region REGION
                           [--profile PROFILE] [--verbose] [--dryrun]

cloudformation_stack_delete

optional arguments:
  -h, --help            show this help message and exit
  --stack-status STACK_STATUS [STACK_STATUS ...]
                        Stack status match to be deleted StackName
  --contain-string CONTAIN_STRING
                        Regex String that match to be deleted StackName
  --region REGION       The AWS region the stack is in
  --profile PROFILE     The name of an aws cli profile to use.
  --verbose             Turn on DEBUG logging
  --dryrun              Do a dryrun - no changes will be performed
