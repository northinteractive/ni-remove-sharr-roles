# ni-remove-sharr-roles
A script to remove remediation roles from AWS SHARR deployments from multiple accounts with a single assumed role. 

To use this script:

```pip install boto3```

Set up your credentials file for AWS so that boto3 can use your AWS IAM credentials.

Create a file for your account list (```aws-accounts.csv```)

...From the command line (with python3 installed)

```python remove-sharr-roles.py```
