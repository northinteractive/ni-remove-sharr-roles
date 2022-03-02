import boto3
import csv
import time

sts_client = boto3.client('sts')
accountlist = 'aws-accounts.csv'
rolelist = 'sharr-roles.csv'
role_exists = False

with open(accountlist, 'r') as accounts:
    datareader = csv.reader(accounts)
    for account in datareader:
        print("===============================================")
        print("Removing roles from account ["+str(account[0])+"]")
        print("===============================================")

        ## assume execution role for each account
        try:
            adminrole = "arn:aws:iam::"+str(account[0])+":role/AWSCloudFormationStackSetExecutionRole"

            assumed_role_object=sts_client.assume_role(
                RoleArn=adminrole,
                RoleSessionName="AssumeRoleSession1"
            )
            credentials=assumed_role_object['Credentials']

            iam_resource=boto3.resource(
                'iam',
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
            )

        except:
            print("Unable to assume role for account"+str(account[0]))

        with open(rolelist, 'r') as roles:
            datareader = csv.reader(roles)
            for rolename in datareader:
                
                role = iam_resource.Role(rolename[0])
                try:
                    role.load()
                    role_exists = True
                except:
                    role_exists = False
                    # Skipping Role
                    print("Missing: Role ["+role.name+"] does not exist in account["+str(account[0])+"].")

                if role_exists:
                    print("Role ["+role.name+"] exists for account "+str(account[0])+" - attempting to delete policies")

                    try:
                        #policies = role.attached_policies.all()
                        policies = role.policies.all()
                        for policy in policies:
                            #print(policy.name)

                            role_policy = iam_resource.RolePolicy(role.name,policy.name)
                            print("Deleting policy "+role_policy.name+" From role "+role.name)
                            role_policy.delete()
                            
                        #for policy in policies:
                        #    response = role.detach_policy(PolicyArn=policy.arn)
                    except:
                        print("No policies for role "+role.name)

                    try:
                        print("Removing role ["+role.arn+"] from account ["+str(account[0])+"]")
                        role.delete()
                    except:
                        print("Unable to remove role ["+str(role.name)+"] From account "+str(account[0]))
                
                ## Break role loop (for testing)
                #break
            ## Break account loop (for testing)
            #break
                

                
                
        
        


