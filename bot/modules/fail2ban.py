def run():
    from subprocess import check_output
    output = check_output("fail2ban-client status sshd", shell=True).decode()
    return output
