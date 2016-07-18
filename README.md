# JIRA Issue count -> DynamoDB
Reads the current JIRA Issue count (matching a search string) and saves count to DynamoDB

# What it does
1. Query JIRA for any open issues that match our assertion error naming (AssertionError, KeyError)
2. Counts them
3. Saves the count to DynamoDB, keyed by current timestamp. Example output:

  | source | timestamp | jira_issues | timestamp_hr_utc |
  | --- | --- | --- | --- |
  | jira | 1468806803 | 170 | 2016-07-18 01:53:23 |
  | jira | 1468809579 | 170 | 2016-07-18 02:39:39 |

# Steps to use
1. Create a credentials file. Expected to be in this directory as '.env'. Must
have these fields:

  ```
  [jira]
  username = <insert username. example: jsmith>
  password = <insert password>
  host = <insert jira server hostname. example: https://mycompany.atlassian.net>
  ```

2. Set your `DYNAMO_DB_TABLENAME` in run.py
3. Create a virtualenv. Mine is named `asserts`
4. In your virtualenv, run `pip install -r requirements.txt`
5. Confirm that the VIRTUALENV_DIR path in build.sh matches your virtualenv's
   packages path
6. Run `./build.sh`
7. Build step leaves a `package.zip`. Upload file to AWS Lambda.
8. Run your script! I set up a Cloudwatch cron job to run regularly.

# Notes
- Not expected to run locally - DynamoDB credentials are not set and we don't
  install `boto3`. Runs on Lambda.

# License
Released with the MIT license, Copyright 2016 topher200@gmail.com
