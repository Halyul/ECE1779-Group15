import time

import paramiko
import logging

import sys
sys.path.append("../..") 
import auto_scaler.config as config

def run_cache(ip_addr):
    pkey = paramiko.RSAKey.from_private_key_file(config.private_key_file)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip_addr,
          port=22,
          username='ubuntu',
          pkey=pkey)
    
    sftp = ssh.open_sftp()
    sftp.put(config.credential_file, '.aws/credentials')
    sftp.close()
    
    git_clone_command = "git clone https://username:" + config.github_access_token + "@github.com/Halyul/ECE1779-Group15.git"
    logging.info("Cloning repository")

    error_count = 0
    while True:
        try:
            time.sleep(10)
            exec_command = "cd /home/ubuntu/ECE1779-Group15/A2; source start_cache.sh"
            stdin, stdout, stderr = ssh.exec_command("{}; {};".format(git_clone_command, exec_command))
            logging.info("Git clone done, Starting instance 2")
            break
        except Exception as error:
            error_count += 1
            if error_count > 5:
                logging.error("Starting instance 2 failed due to {}".format(error))
                return
            continue
    return
