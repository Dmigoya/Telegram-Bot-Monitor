def run():
    from subprocess import check_output
    output = check_output("docker ps --format '{{.Names}}: {{.Status}}'", shell=True).decode()
    return output.strip()
