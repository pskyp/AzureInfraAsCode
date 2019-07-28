import os.path
import json
from azure.mgmt.resource import ResourceManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from ast import literal_eval
from deployer import Deployer



# load in the deployment config file
template_path = os.path.join(os.path.dirname(
    __file__), 'templates', 'deployment.json')

with open(template_path, 'r') as template_file_fd:
    template = json.load(template_file_fd)
print(template["ResourceGroup"])

# setup environment variables
os.environ['AZURE_CLIENT_ID'] = 'f87d3ad4-c871-404e-9e06-df4541d49b55'
os.environ['AZURE_CLIENT_SECRET'] = '.c4HuV[gi-t/KXkNagXvH6dWqsGsdR66'
os.environ['AZURE_TENANT_ID'] = 'b6731642-66c3-4bf4-b365-ef82493bcdbf'


credentials = ServicePrincipalCredentials(
    client_id=os.environ['AZURE_CLIENT_ID'],
    secret=os.environ['AZURE_CLIENT_SECRET'],
    tenant=os.environ['AZURE_TENANT_ID']
)

my_subscription_id=template["AZURE_SUBSCRIPTION_ID"]

client = ResourceManagementClient(
    credentials, my_subscription_id)

my_pub_ssh_key_path = os.path.expanduser('~/.ssh/id_rsa.pub')


groupnames=[]
for item in client.resource_groups.list():
    groupnames.append(item.name)
print(groupnames)
x=template["Deployed_Region"]
for item in x:
    my_location = str(item)
    deployement_status = str(x[item])
    my_resource_group = template["ResourceGroup"]+"_"+my_location
    print(my_location + " : " + deployement_status)
    print(my_resource_group)
    deployer = Deployer(my_subscription_id, my_resource_group,
                    my_location, my_pub_ssh_key_path)
    
    if my_resource_group in groupnames:
        if deployement_status =="False":

            msg = "\nInitializing the Deployer class with subscription id: {}, resource group: {}" \
                "\nand public key located at: {}...\n\n"
            msg = msg.format(my_subscription_id, my_resource_group, my_pub_ssh_key_path)
            print(msg)
            deployer.destroy()
    if deployement_status =="True":
        msg = "\nInitializing the Deployer class with subscription id: {}, resource group: {}" \
                "\nand public key located at: {}...\n\n"
        msg = msg.format(my_subscription_id, my_resource_group, my_pub_ssh_key_path)
        print(msg)
        deployer.deploy()




#"{'properties': <azure.mgmt.resource.resources.models.resource_group_properties.ResourceGroupProperties object at 0x7c5802963c50>, 'name': 'AZ300', 'id': '/subscriptions/2a5752bf-ed9d-456e-830e-e398e97d9c7b/resourceGroups/AZ300', 'location': 'uksouth', 'tags': {'Owner': 'Piers', 'Environemnt': 'Test'}}"
