from ConfigParser import ConfigParser
import os

from jira import JIRA

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILENAME = '.env'


def main(event, _):
    print 'recieved event "%s"' % event

    config_parser = ConfigParser()
    config_parser.read(os.path.join(ROOT_DIR, CREDENTIALS_FILENAME))

    jira_username = config_parser.get('jira', 'username')
    jira_password = config_parser.get('jira', 'password')
    jira_host = config_parser.get('jira', 'host')

    jira = JIRA(basic_auth=(jira_username, jira_password),
                server=jira_host)

    projects = jira.projects()
    print projects


if __name__ is '__main__':
    main({}, None)
