import logging.handlers
import argparse
import boto3
import re


def delete_cloudformation_stack(cloud_session, contain_string, stack_status=["ROLLBACK_COMPLETE"], dryrun=False):
    """
    Delete stack based on contain_strings and stack_status
    :param cloud_session: the session to amazon cloud formation
    :param contain_string: the string that match the stack to be deleted
    :param stack_status: the status of the stack to be deleted
    """

    stack_list = []
    if not contain_string:
        contain_string = '.*'

    logging.info("Attempting to delete stacks contain str '{0}' with status: {1}".format(contain_string,stack_status))
    response = cloud_session.list_stacks(StackStatusFilter=stack_status)
    for i in response['StackSummaries']:

        if 'DeletionTime' in i:
            stack_list.append(i['StackName'])

    # match regular expressions from contain_string
    del_list = _filter_list(stack_list, contain_string)

    if len(del_list) == 0:
        logging.info("No stack with name matching: '{0}'".format(contain_string))
    else:
        logging.info("Stacks to be deleted:")
        for s_name in del_list:
            logging.info("\t{0}".format(s_name))

    if not dryrun:
        logging.info("Dry Run not selected - delete matching stacks from cloudformation")
        _delete_stacks(cloud_session, del_list)
    else:
        logging.info("Dry Run selected - will NOT delete any stacks from cloudformation")


def _filter_list(a_list, regex_str):
    """
    filter a list of string by regex
    :param a_list:
    :param regex_str:
    :return: the filtered list
    """
    regex = re.compile(regex_str)
    selected_list = filter(regex.search, a_list)
    return list(selected_list)


def _delete_stacks(cloud_session, stack_list):
    """
    delete stacks from a list of stacks
    :param cloud_session: the session
    :param stack_list: the list to be deleted
    :return:
    """
    # delete stacks from the list
    result = ""
    logging.info("In Delete stacks function ")
    for stack_name in stack_list:
        logging.info("Delete stack with name: {0}".format(stack_name))
        response = cloud_session.delete_stack(
            StackName=stack_name
        )
        logging.debug("Delete Response: {0}".format(response))


if __name__ == "__main__":

    LOG_FILENAME = 'cloudformation_stack_delete.log'

    parser = argparse.ArgumentParser(description='cloudformation_stack_delete')

    # parser.add_argument("--aws-access-key-id", help="AWS Access Key ID", dest='aws_access_key', required=False)
    # parser.add_argument("--aws-secret-access-key", help="AWS Secret Access Key", dest='aws_secret_key',
    #                      required=False)
    parser.add_argument("--stack-status", help="Stack status match to be deleted StackName. "
                                               "Example: ROLLBACK_COMPLETE", nargs='+', dest='stack_status',
                        required=True)
    parser.add_argument("--contain-string", help="Regex String that match to be deleted StackName. Example: A.* ",
                        dest='contain_string',
                        required=False)
    parser.add_argument("--region", help="The AWS region the stack is in", dest='region', required=True)
    parser.add_argument("--profile", help="The name of an aws cli profile to use.", dest='profile', default=None,
                        required=False)
    parser.add_argument("--verbose", help="Turn on DEBUG logging", action='store_true', required=False)
    parser.add_argument("--dryrun", help="Do a dryrun - no changes will be performed", dest='dryrun',
                        action='store_true', default=False, required=False)
    args = parser.parse_args()
    log_level = logging.INFO

    if args.verbose:
        print("Verbose logging selected")
        log_level = logging.DEBUG

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=5242880, backupCount=5)
    fh.setLevel(logging.DEBUG)
    # create console handler using level set in log_level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    console_formatter = logging.Formatter('%(levelname)8s: %(message)s')
    ch.setFormatter(console_formatter)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)8s: %(message)s')
    fh.setFormatter(file_formatter)
    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    # create the session for the boto3 with profile and region from user parameters
    SESSION = boto3.session.Session(profile_name=args.profile, region_name=args.region)
    cf = SESSION.client('cloudformation')

    logging.info("AWS Region: {0}".format(args.region))
    
    delete_cloudformation_stack(cf, contain_string=args.contain_string, stack_status=args.stack_status,
                                dryrun=args.dryrun)





