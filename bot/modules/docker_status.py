from subprocess import check_output

CMD_NAME = "docker"
CMD_DESC = "Contenedores Docker"


def report():
    output = check_output("docker ps --format '{{.Names}}: {{.Status}}'", shell=True).decode()
    return output.strip()


async def run(update, context):
    await update.message.reply_text(report())

