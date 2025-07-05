import psutil

def run():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters()
    return f"CPU: {cpu}%\nRAM: {mem}%\nDisk: {disk}%\nNet: Sent {net.bytes_sent//1024}KB / Recv {net.bytes_recv//1024}KB"
