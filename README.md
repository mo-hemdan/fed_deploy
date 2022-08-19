# Fed_Deploy Package

This package enables you to deploy federated learning models on remote machines. It is made to ease up the deployment in a way that the user doesn't have to deal with the remote machines or deal with the dependancies there. 

<h1> Installation </h1>
Since the package is still in the testing phase, no production version has been published. You can install it using test-pypi by running the following command.

```sh
$ python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps fed_deploy
```

If it doesn't work, you can clone the repo and install it. You can use the following commands:
```sh
$ git clone https://github.com/mashrafhemdan1/fed_deploy.git
$ cd fed_deploy
$ pip install .
```
This way, you installed the package. The package requires ansible which should be installed automatically in your device. 

<h1> Requirements </h1>
There are several things you need to make sure of

1. Your clients and server are running CentOS. Support for other operating systems has not been added yet. If support is added for new OSs, it will be probably Linux based systems since ansible requires clients to have linux. It 

2. ansible command should be working fine. Just run this command: It should give you the ansible version. If it says ansible is not installed. Then, the package probably might find an error installing it. If that is the case, you should install it yourself.
```sh
$ ansible --version
```

3. You have access to your remote machines using passwordless ssh. Make sure you can ssh into your machines without needing to enter the password. 

If you don't have ssh on your remote machines, here are the steps (for CentOs only):
```sh
$ sudo yum install openssh-server
$ sudo systemctl enable ssh
$ sudo systemctl start ssh
```
You can check if ssh is running using the following command
```sh
$ sudo systemctl status ssh
```
That has to be done on each machine. Some machines has ssh enabled by default. Just make sure it's working.

Then, you need to enable passwordless ssh from your machine to the remote machines. The following commands shows how to enable so but from an ubuntu machine.
```sh
$ ssh-keygen -t rsa
$ ssh-copy-id [remote_username]@[server_ip_address]
```
Next time you ssh, it should work. Make sure you can do so for all the remote machines you have.

<h1> Usage </h1>
Once your setup is completed, you can now use the package. There is an example for how to use the package in the example directory. 