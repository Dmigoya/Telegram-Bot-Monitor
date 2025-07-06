from subprocess import check_output

CMD_NAME = "mem"
CMD_DESC = "Uso de RAM"


def report():
    output = check_output("free -h", shell=True).decode()
    return output.strip()


async def run(update, context):
    await update.message.reply_text(f"<pre>{report()}</pre>", parse_mode="HTML")

