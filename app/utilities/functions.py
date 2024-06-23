# Função para verificar se um processo está rodando
import subprocess
import cv2

script_path = "app/scripts/recon.py"

def is_process_running(camera, show=None):
    if show is None:
        process_name = f"python {script_path} {camera}"
    else:
        process_name = f"python {script_path} {camera} {show}"
    command = ["pgrep", "-f", process_name]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    return result.returncode == 0

# Função para parar um processo (adaptar conforme necessário)
def stop_process(camera, show=None):
    if show is None:
        process_name = f"python {script_path} {camera}"
    else:
        process_name = f"python {script_path} {camera} {show}"
    command = ["pkill", "-f", process_name]
    subprocess.run(command)

# Função para iniciar um script Python como processo separado
def start_script(camera, show=None):
    if show is None:
      command = ["python", script_path, camera]
    else:
      command = ["python", script_path, camera, show]
    subprocess.Popen(command)

def list_v4l2_devices():
    devices = []
    try:
        result = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True)
        output = result.stdout.split('\n')
        for i, line in enumerate(output):
            if '/dev/video' in line:
                device = line.strip().split(':')[0]
                devices.append(device)
    except Exception as e:
        print(f"Error listing v4l2 devices: {e}")
    return devices

def list_available_cameras():
    devices = list_v4l2_devices()
    available_cameras = []
    for device in devices:
        cap = cv2.VideoCapture(device, cv2.CAP_V4L2)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                available_cameras.append(device)
                print(f"Camera {device} is available and working.")
            else:
                print(f"Camera {device} could not capture a frame.")
            cap.release()
        else:
            print(f"Camera {device} could not be opened.")
    return available_cameras