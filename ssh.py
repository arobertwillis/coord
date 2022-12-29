import argparse
import logging
import os
import sys
import paramiko

from contextlib import closing


logger = logging.getLogger(__name__)

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def ssh(host: str, user: str, cmd: str):
    password = os.getenv("SSH_PASSWORD")

    with closing(paramiko.SSHClient()) as ssh:

        ssh.load_system_host_keys()

        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())

        if password is None:

            key_filename = f'/home/{user}/.ssh/id_rsa'
            if os.path.exists(key_filename):
                logger.info(f"No password so using key_filename {key_filename}")
                ssh.connect(host, username=user, key_filename=key_filename, look_for_keys=True)
            else:
                ssh.connect(host, username=user)
        else:

            logger.info(f"Using password from environment variable SSH_PASSWORD")

            ssh.connect(host, username=user, password=password)

        logger.info(f"Running on host [{host}] cmd [{cmd}]")

        stdin, stdout, stderr = ssh.exec_command(cmd)

        for line in iter(stdout.readline, ""):
            print(line, end="")

        print(f'STDERR: {stderr.read().decode("utf8")}')

        return stdout.channel.recv_exit_status()


if __name__ == "__main__":
    ssh('desktop-tthtjf3','andrewwi','docker images ')