from ConfigParser import ConfigParser
import datetime
import os

from jira import JIRA
import boto3

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILENAME = '.env'
DYNAMO_DB_TABLENAME = 'assertion-error-counts'
EPOCH = datetime.datetime.utcfromtimestamp(0)


print 'Loading function'


def main(event, _):
    print 'recieved event "%s"' % event

    # get creds
    config_parser = ConfigParser()
    config_parser.read(os.path.join(ROOT_DIR, CREDENTIALS_FILENAME))
    jira_username = config_parser.get('jira', 'username')
    jira_password = config_parser.get('jira', 'password')
    jira_host = config_parser.get('jira', 'host')

    # set up query
    search_query = ' AND '.join((
        'project=WordStream',
        'status in (Open, "In Progress", "Dev Complete")',
        'text ~ "assertionerror OR keyerror OR valueerror OR notimplementederror"'
    ))
    print 'performing jira search with %s' % search_query

    # perform search; count number of matching issues
    jira = JIRA(basic_auth=(jira_username, jira_password), server=jira_host)
    num_issues = 0
    for _ in jira.search_issues(search_query, maxResults=False):
        num_issues += 1
    print 'found %s issues' % num_issues

    # determine timestamp for record
    timestamp = datetime.datetime.utcnow()
    seconds_since_epoch = int((timestamp - EPOCH).total_seconds())
    human_readable_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    # save number of issues to dynamodb
    dynamo = boto3.resource('dynamodb').Table(DYNAMO_DB_TABLENAME)
    return dynamo.update_item(
        Key={
            'source': 'jira',
            'timestamp': seconds_since_epoch,
        },
        UpdateExpression=("add jira_issues :count "
                          "set timestamp_hr_utc = :timestamp_hr_utc "
                          ),
        ExpressionAttributeValues={
            ':count': num_issues,
            ':timestamp_hr_utc': human_readable_timestamp,
        },
    )


if __name__ == '__main__':
    main({}, None)
