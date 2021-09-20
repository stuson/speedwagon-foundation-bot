from urllib import request
import psutil
from elevate import elevate
from time import sleep

JAR_DIRECTORY = "C:\\Users\\Sam\\AppData\\Roaming\\Forge\\"
JAR_NAME = "forge-1.16.5-36.1.0.jar"


class ServerStatus:
    def __init__(self, ip=None, running=False):
        self.ip = ip
        self.running = running

    def message(self):
        line_starter = "+" if self.running else "-"

        return (
            "```diff\n"
            f"{line_starter} Server: {'RUNNING' if self.running else 'DOWN'}\n"
            f"{line_starter} IP: {self.ip}\n"
            "```"
        )


def get_status():
    ip = get_ip()
    running = get_running()

    return ServerStatus(ip=ip, running=running)


def get_ip():
    return request.urlopen("http://api.ipify.org").read().decode("utf-8")


def get_process():
    java_processes = list(
        p for p in psutil.process_iter() if p.name().startswith("java")
    )

    for java_process in java_processes:
        if "forge" in java_process.cmdline()[2]:
            return java_process

    return None


def get_running():
    try:
        return get_process().is_running()
    except AttributeError:
        return False


def run_server():
    psutil.Popen(["java", "-jar", JAR_DIRECTORY + JAR_NAME], cwd=JAR_DIRECTORY)
    max_retries = 10
    retries = 0
    running = False

    while not running and retries < max_retries:
        running = get_running()
        retries += 1
        sleep(1)

    sleep(10)
    return running


def stop_server():
    process = get_process()
    process.terminate()
