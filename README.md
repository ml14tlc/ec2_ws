# Metronom Demo

The playbook carries out the following operations:

* it configures a VPC deploying a subnet, a gateway (adding the default route for the subnet) and setting up a security group to provide free access on ports 22 and 80
* it lauches an instance, associating a floating IP, configuring Apache to run a CGI script handling a form

## Prerequsites
The following Python packages should be installed on the Ansible host, i.e., the maschine used to run the playbook:

* *boto*
* *boto3*
* *botocore*

Please install them via _pip_ or your package manager.

**Important note**: the playbook is configured to **automatically add the host key** to the list of known hosts, in order to not require any human intervention.

## Parameters
The needed variables are contained in *group\_vars/all*. Each of them is commented, just refer to the file. What needs to be customised is:

* **aws\_access\_key**: please use Amazon's IAM to create your access key;
* **aws\_sec\_key**: please use Amazon's IAM to create your private key. It's good practice to encrypt it. To do so, please type *
ansible-vault encrypt\_string --ask-vault-pass --stdin-name 'aws_sec_key'*, then enter the security key from the IAM page and hit _Ctrl d_. Copy the output into the file;
* **instance\_keypair**: the public SSH key that will be copied into the Image. It is possible to create a pair from the EC2 dashboard

## Additional Files
The following files are needed and should be placed in the same folder of the playbook, _ec2_ws.yaml_:

* *index,jinja2*: it's the template of the main page, _index.html_. It'll be customised with the FQDN of the instance;
* *pwdfomr.py*: the Python script to handle the html form contained in the main page. It'll be copied to the dafault CGI folder;
* *password.py*: the Python Flask application providing the REST API to generate the password;
* *password.wsgi*: the configuratin file for the Apache WSGI module, in order to run the application inside Apache;
* *vhost-rest.conf*: the Apache default virtual host configuration, it will replace */etc/apache2/sites-enabled/000-defafult.conf* in order to provide the REST interface.

## Run the playbook
Pleas type

	ansible-playbook --ask-vault-pass -i localhost, ec2_ws.yaml

and type the password it has been used to encrypt the AWS security key.

The playbook will configure (and create, if necessary) the VPC and a Ubuntu instance. If the instance has already been created and it only has to be configured, then call the playbook with the tag _instance_, providing the public IP and the instance ID, i.e.:

	ansible-playbook --ask-vault-pass -i localhost, -t instance -e '{"ec2_instance_ip": "1.2.3.4", "ec2_instance_id": "i-04c053d0e2c1d8cce"}' ec2_ws.yaml
	
where *ec2\_instance\_ip* is the public IP and *ec2\_instance\_id* is the EC2 identifier.

When the playbook runs till the end without errors, point the browser to the instance's public IP and fill the form, clicking on the _Submit_ button.

## Connecting to the instance

In order to gain shell access, please type the following on a Linux terminal:

	ssh -i <path to the AWS key pair> ubuntu@<Elastic IP>
	
The AWS key pair is made up of a private key and a public certificate. The private key is shown only during the key pair creation. If you didn't save it, please create a new key pair, save all the info, terminate the instance (removing the Elastic IP manually, see later on) and re-run the playbook from the beginning. Please note that the file permission of the keypair should be *0600*.

## REST API call
Please use the address *&lt;Instance public IP&gt;/rest/password/&lt;password length&gt;*. The password length should be an integer between _5_ and _20_.

## Terminate the instance
The playbook _stop.yaml_ will terminate the instance. Once again, the public IP and the ID are needed:

ansible-playbook --ask-vault-pass -i localhost, -e '{"ec2_instance_ip": "1.2.3.4", "ec2_instance_id": "i-04c053d0e2c1d8cce"}' stop.yaml
	
where *ec2\_instance\_ip* is the public IP and *ec2\_instance\_id* is the EC2 identifier.

**Important**: the playbook **will not release the Elastic IP**, hence you'll incur into charging if your Elastic IP isn't associated to a running instance. **Please release the Elastic IP manually**, from the EC2 Dashboard.