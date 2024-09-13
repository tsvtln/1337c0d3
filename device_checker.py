import json
import time

devices_db = 'devices.json'


def read_devices(fp):
    try:
        with open(fp, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_devices(fp, devices):
    with open(fp, 'w') as file: json.dump(devices, file, indent=4)


def main():
    start_time = time.time()
    devices = read_devices(devices_db)
    new_device = input("Enter the device name: ").strip()
    if new_device in [' ', '']:
        print('Empty input. Please enter valid device name!')
        exit()
    if new_device not in devices:
        devices.append(new_device)
        write_devices(devices_db, devices)
        print(f"Device '{new_device}' added.")
    else:
        print(f"Device '{new_device}' is already in the list.")

    print("Current list of devices:")
    print("\n".join(f"• {device}" for device in devices))


    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
