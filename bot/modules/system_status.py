import psutil

CMD_NAME = "sys"
CMD_DESC = "Estado del sistema"


def report():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    return (
        f"CPU: {cpu}%\nRAM: {mem}%\nDisk: {disk.percent}%\n"
        f"Net: Sent {net.bytes_sent//1024}KB / Recv {net.bytes_recv//1024}KB"
    )


async def run(update, context):
    await update.message.reply_text(f"<pre>{report()}</pre>", parse_mode="HTML")

