import json
import time

devices_db = "devices.json"


def read_devices(fp: str) -> list:
    # we check if the 'db' exists already, otherwise we return empty list
    try:
        with open(fp, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_devices(fp: str, devices: list) -> None:
    # for writing the devices to the 'db'
    with open(fp, "w") as f:
        json.dump(devices, f, indent=4)


def parse_devices_input(input_str: str) -> list:
    # we remove the "devices = " part (case-insensitive)
    prefix = "devices = "
    if input_str.lower().startswith(prefix):
        input_str = input_str[len(prefix):].strip()

    # and we split the string by commas and clean up each device name from the quotes
    devices = [device.strip().strip('"').strip("“").strip("”") for device in input_str.split(",")]
    return devices


def main():
    added_devices = []
    # get the current inventory of devices
    inventory = read_devices(devices_db)
    # get the input from the user
    user_input = input("Enter devices:\n")
    # call the helper function to parse the input
    new_devices = parse_devices_input(user_input)


    # start timer for the check
    check_start = time.time()

    # we check every device from the input to see if it's already in the 'db'
    # we'll return an output if the device exists to the user, if not we'll append it to a list, so we can
    # return the added devices afterwards
    for device in new_devices:
        if device in inventory:
            print(f"Device: {device} already exists.")
        else:
            inventory.append(device)
            added_devices.append(device)

    # end the timer for the check
    check_end = time.time()
    check_time = check_end - check_start

    # save the new devices to the 'db'
    write_devices(devices_db, inventory)

    # we return to the user the devices that were added succesfully or if nothing was added we return according output
    if added_devices:
        print("Devices added:")
        for device in added_devices:
            print(f"• {device}")
    else:
        print("No new devices were added.")

    # at the end we return the timer for the check
    print(f"Time for performing the check: {check_time:.4f} seconds")


if __name__ == "__main__":
    main()
