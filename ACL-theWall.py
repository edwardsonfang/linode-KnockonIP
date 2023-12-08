import requests
import time
import os
import paramiko
from ping3 import ping

# Set your Linode API access token
ACCESS_TOKEN = "{Your Token}"

# Set deployment parameters
region = "jp-osa"  # Replace with your desired region
image = "linode/ubuntu22.04"  # Replace with your desired Ubuntu image
label = "TestCodeInstance"  # Replace with your desired label
root_pass = "{Your Root Password}"  # Replace with your desired root password
type = "g6-nanode-1"  # Replace with your desired instance type

# Provision 2 instances with desired CPU model
counter = 1 #initial counter
while counter <= 2: #condition for 50 instances to be provisioned
    print(f"Provisioning instance {counter}...")

    # Create the Linode instance
    create_instance_payload = {
        "label": f"{label}{counter}",
        "image": image,
        "type": type,
        "region": region,
        "root_pass": root_pass,
        "booted": True
    }

    create_instance_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    create_instance_response = requests.post(
        "https://api.linode.com/v4/linode/instances",
        json=create_instance_payload,
        headers=create_instance_headers
    )

    # Extract the Linode instance ID from the response
    instance_id = create_instance_response.json().get("id")

    # Wait for the Linode instance to be running
    while True:
        instance_status_response = requests.get(
            f"https://api.linode.com/v4/linode/instances/{instance_id}",
            headers=create_instance_headers
        )

        instance_status = instance_status_response.json().get("status")

        if instance_status == "running":
            break
        #let the linode instance done all the initial setup
        time.sleep(150)

    # Get the Linode instance IP address
    instance_ip = instance_status_response.json().get("ipv4")[0]

    # Ping instance IP to check if its accessable
    success = 0
    fail = 0
    for count in range(0,5):
        second = ping(instance_ip, unit='ms')
        if second == None:
            fail += 1
            print('This is a None')
        elif second == False:
            fail += 1
            print('This is a False')
        else:
            success += 1
            print('it took {} miliseconds'.format(second))
    if fail == 5:
        print('Success =  {}'.format(success))
        print('Fail =  {}'.format(fail))
        print(f"Linode:{instance_id} is totally unaccessable! IP:{instance_ip}. Deleting!")
        delete_instance_response = requests.delete(
            f"https://api.linode.com/v4/linode/instances/{instance_id}",
            headers=create_instance_headers
            )
    elif fail > success:
        print('Success =  {}'.format(success))
        print('Fail =  {}'.format(fail))
        print(f"Linode:{instance_id} is nearly unaccessable! IP:{instance_ip}")
        delete_instance_response = requests.delete(
            f"https://api.linode.com/v4/linode/instances/{instance_id}",
            headers=create_instance_headers
    elif fail == 0 and success == 5:
        print('Fail =  {}'.format(fail))
        print('Success =  {}'.format(success))
        print(f"Linode:{instance_id} is totally accessable! IP:{instance_ip}")
    else:
        print('Success =  {}'.format(success))
        print('Fail =  {}'.format(fail))
        print(f"Linode:{instance_id} is nearly accessable! IP:{instance_ip}")
    counter += 1 #initial counter
