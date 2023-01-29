import subprocess
import os

def get_cpu_temp():
    tempfile = open('/sys/class/thermal/thermal_zone0/temp')
    cpu_temp = tempfile.read()
    tempfile.close()
    return float(cpu_temp) / 1000

def get_uptime():
    try:
        return str(subprocess.check_output('uptime -p'.split()))
    except: return '1 секунда'
