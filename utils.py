import subprocess

def get_cpu_temp():
    try:
        return str(subprocess.check_output('cat /sys/class/thermal/thermal_zone*/temp'.split()))
    except: return '2.000.000 °С'

def get_uptime():
    try:
        return str(subprocess.check_output('uptime -p'.split()))
    except: return '1 секунда'