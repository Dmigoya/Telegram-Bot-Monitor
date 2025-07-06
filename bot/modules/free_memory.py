from subprocess import check_output


def run():
    output = check_output("free -h", shell=True).decode()
    return output.strip()
