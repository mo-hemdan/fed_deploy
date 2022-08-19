from fed_deploy.run import ContainerRunner
# import fed_deploy

runner = ContainerRunner()
runner.add_client(
    ansible_host= "188.185.101.118",
    partition= "1",
    data_dir= "/root/data_cifar",
    filename= "data_batch_1",
)
runner.add_client(
    ansible_host= "188.185.87.9",
    partition= "2",
    data_dir= "/root/data_cifar",
    filename= "data_batch_2",
)
runner.add_client(
    ansible_host= "188.185.120.31",
    partition= "3",
    data_dir= "/root/data_cifar",
    filename= "data_batch_3",
)
runner.server_config(
    ansible_host= "188.185.11.183",
    partition= "3",
    data_dir= "/root/data_cifar",
    filename= "data_batch_3",
)
runner.monitor_config(
    ansible_host= "188.185.11.183",
)

runner.run_monitor('./monitor.py')
runner.run_server('./server.py')
runner.run_client('./client.py')

