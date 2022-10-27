import paramiko

import sys
sys.path.append("../..") 
import auto_scaler.config as config

def run_cache(ip_addr):
    pkey = paramiko.RSAKey.from_private_key_file(config.config_info['ssh']['private_key_file'])

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip_addr,
          port=22,
          username='ubuntu',
          pkey=pkey)
    git_clone_command = "git clone git@ECE1779-Group15:Halyul/ECE1779-Group15.git"
    exec_command = "cd ECE1779-Group15/A2; source start_cache.sh"
    stdin, stdout, stderr = ssh.exec_command("{}; {}".format(git_clone_command, exec_command))
    return
