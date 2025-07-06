from subprocess import check_output

CMD_NAME = "fail2ban"
CMD_DESC = "Estado fail2ban"


def report():
    output = check_output("fail2ban-client status sshd", shell=True).decode()
    return output


async def run(update, context):
    await update.message.reply_text(f"<pre>{report()}</pre>", parse_mode="HTML")

