import multiprocessing
import time
import datetime
import uuid

# Assume that we have a raspberry pi device tagged to fridge
# This script is simulating parallel execution of 3 activities
# Each activity (method) contains endless while loop to monitor environment changes
# Method 1: upload_sensor_data
# Method 2: monitor_door
# Method 3: monitor_camera

def upload_sensor_data(process):
    """ Reads and uploads sensor data every second """
    while True:
        print(datetime.datetime.now(), f'Process {process}:', 'upload sensor data')
        time.sleep(1)

def monitor_door(process):
    """ Monitor status of door """
    door_triggers = [1, 3, 5, 7] #Seconds that event happens (open/close door)
    door_time = time.time()
    door_status = False

    while True:
        if door_triggers and (time.time() - door_time) > door_triggers[0]:
            door_status = not door_status
            door_triggers.pop(0)
            print(datetime.datetime.now(), f'Process {process}:', 'open door' if door_status else 'close door')

def monitor_camera(process):
    """ Monitor camera, capture image that contains qr code """
    camera_triggers = [5, 9] #Seconds that event happens (open/close door)
    camera_time = time.time()
    camera_status = False

    # Initialize camera
    print(datetime.datetime.now(), f'Process {process}:','turn on camera')

    while True:
        if camera_triggers and (time.time() - camera_time) > camera_triggers[0]:
            camera_status = not camera_status
            camera_triggers.pop(0)
            # Assume that qr code has GUID format
            print(datetime.datetime.now(), f'Process {process}:', f'Added item {uuid.uuid4()}' if camera_status else f'Removed item {uuid.uuid4()}')

if __name__ == '__main__':
    tasks = [upload_sensor_data, monitor_door, monitor_camera]

    # Parallel tasks running concurrently at the background
    for index, task in enumerate(tasks, 1):
        p = multiprocessing.Process(target=task, args=(index,))
        p.start()