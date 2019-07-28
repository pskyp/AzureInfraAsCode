import os.path
import json
from deployer import Deployer
from azure.mgmt.resource import ResourceManagementClient
from azure.common.credentials import ServicePrincipalCredentials


# This script expects that the following environment vars are set:
#
# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret

my_subscription_id = os.environ.get(
    'AZURE_SUBSCRIPTION_ID', '2a5752bf-ed9d-456e-830e-e398e97d9c7b')   # your Azure Subscription Id

# load in the deployment config file
template_path = os.path.join(os.path.dirname(
    __file__), 'templates', 'deployment.json')

with open(template_path, 'r') as template_file_fd:
    template = json.load(template_file_fd)


# the resource group for deployment
my_resource_group = template["ResourceGroup"]


# logic to either delete, create or update resource groups in regions

# TODO:get list currently lits of deployed regions for that resource group

# set up service coonection
os.environ['AZURE_CLIENT_ID'] = 'f87d3ad4-c871-404e-9e06-df4541d49b55'
os.environ['AZURE_CLIENT_SECRET'] = '.c4HuV[gi-t/KXkNagXvH6dWqsGsdR66'
os.environ['AZURE_TENANT_ID'] = 'b6731642-66c3-4bf4-b365-ef82493bcdbf'


credentials = ServicePrincipalCredentials(
    client_id=os.environ['AZURE_CLIENT_ID'],
    secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant=os.environ['AZURE_TENANT_ID']
    
# get list of deployed resource groups


# TODO: compare the wished for deployment with the current deployment
# TODO: delete ones not in desired state
# TODO: Update ones that are in current list
# TODO: create new ones if they don't exist


my_location = 'uksouth'
# the path to your rsa public key file
my_pub_ssh_key_path = os.path.expanduser('~/.ssh/id_rsa.pub')

msg = "\nInitializing the Deployer class with subscription id: {}, resource group: {}" \
    "\nand public key located at: {}...\n\n"
msg = msg.format(my_subscription_id, my_resource_group, my_pub_ssh_key_path)
print(msg)


# Initialize the deployer class
deployer = Deployer(my_subscription_id, my_resource_group,
                    my_location, my_pub_ssh_key_path)

print("Beginning the deployment... \n\n")
# Deploy the template
# deployer.deploy()

print("Done deploying!!\n\nYou can connect via: `ssh azureSample@{}.westus.cloudapp.azure.com`".format(
    deployer.dns_label_prefix))

# Destroy the resource group which contains the deployment
deployer.destroy()
()
