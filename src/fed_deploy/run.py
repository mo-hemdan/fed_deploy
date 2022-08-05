from ansible import context
from ansible.cli import CLI
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
import yaml
import shutil
import os

FED_DIRPATH = os.path.dirname(__file__)
os.environ["FED_DIRPATH"] = FED_DIRPATH
INVENTORY_FILENAME = os.path.join(FED_DIRPATH, 'inventory.yaml')

class ContainerRunner(object):
    def __init__(self):
        self.loader = DataLoader()
        self.nclients = 0
        self.inventory_path = INVENTORY_FILENAME
        self.inventory_yaml = {
            "clients": {
                "hosts": {}
            },
            "server": {
                "hosts": {
                    "fs": {}
                },
            },
            "monitor": { 
                "hosts": {
                    "fm": {}
                },
            },
        }
        context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                            module_path=None, forks=100, remote_user='root', private_key_file=None,
                            ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                            become_method='sudo', become_user='root', verbosity=True, check=False, start_at_task=None)
    def install_req(self):
        install_req_path = os.path.join(FED_DIRPATH, 'install_req.yaml')
        pbex = PlaybookExecutor(playbooks=[install_req_path], inventory=self.inventory, variable_manager=self.variable_manager, loader=self.loader, passwords={})
        results = pbex.run()
        return results
    
    def create_yaml(self, filename=INVENTORY_FILENAME):
        self.inventory_path = filename
        with open(filename, 'w') as f:
            data = yaml.dump(self.inventory_yaml, f)

    def add_client(self, ansible_host, partition=None, data_dir=None, filename=None):
        data =  {"ansible_host": ansible_host,
                "partition": partition,
                "data_dir": data_dir,
                "filename": filename}
        self.nclients+=1
        client_name = "fc" + str(self.nclients)
        self.inventory_yaml["clients"]["hosts"][client_name] = data
        self.create_yaml()

    def server_config(self, ansible_host, partition=None, data_dir=None, filename=None):
        data =  {"ansible_host": ansible_host,
                "partition": partition,
                "data_dir": data_dir,
                "filename": filename}
        self.inventory_yaml["server"]["hosts"]["fs"] = data
        self.create_yaml()
    
    def monitor_config(self, ansible_host, partition=None, data_dir=None, filename=None):
        data =  {"ansible_host": ansible_host,
                "partition": partition,
                "data_dir": data_dir,
                "filename": filename}
        self.inventory_yaml["monitor"]["hosts"]["fm"] = data
        self.create_yaml()
    
    def run_playbook(self, playbook_filename):
        self.inventory = InventoryManager(loader=self.loader, sources=(self.inventory_path,))
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory, version_info=CLI.version_info(gitinfo=False))
        pbex = PlaybookExecutor(playbooks=[playbook_filename], inventory=self.inventory, variable_manager=self.variable_manager, loader=self.loader, passwords={})
        results = pbex.run()
        return results

    def run_client(self, programpath):
        self.copy(programpath, 'client')
        client_run_path = os.path.join(FED_DIRPATH, 'client_run.yaml')
        return self.run_playbook(client_run_path)
    
    def run_server(self, programpath):
        self.copy(programpath, 'server')
        server_run_path = os.path.join(FED_DIRPATH, 'server_run.yaml')
        return self.run_playbook(server_run_path)

    def run_monitor(self, programpath):
        self.copy(programpath, 'monitor')
        monitor_run_path = os.path.join(FED_DIRPATH, 'monitor_run.yaml')
        return self.run_playbook(monitor_run_path)
    
    def copy(self, src_path, device_type):
        if device_type == 'monitor':
            dst_filename = 'fed/monitor/monitor.py'
            dst = os.path.join(FED_DIRPATH, dst_filename)
        elif device_type == 'server':
            dst_filename = 'fed/server/server.py'
            dst = os.path.join(FED_DIRPATH, dst_filename)
        elif device_type == 'client':
            dst_filename = 'fed/client/client.py'
            dst = os.path.join(FED_DIRPATH, dst_filename)
        else:
            raise Exception("Copying to this device not supported")
        shutil.copy(src_path, dst)