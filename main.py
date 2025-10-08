import pylontech
import json
from io import BytesIO
from datetime import datetime
import os


def make_daily_jsonl_file(filename):
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    date_str = now.strftime("%Y-%m-%d")

    folder_path = os.path.join("data", year, month)
    os.makedirs(folder_path, exist_ok=True)
    LOG_FILE = os.path.join(folder_path, f"{filename}_{date_str}.jsonl")
  
    return LOG_FILE

def save_container_as_json(container, filename):
    def convert(obj):
        if isinstance(obj, BytesIO):
            return None  # lub obj.getvalue().hex()
        elif hasattr(obj, "items"):  # Container lub dict
            return {k: convert(v) for k, v in dict(obj).items() if k != "_io"}
        else:
            return obj

    structured = convert(container)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
    wrapped = {timestamp: structured}

    with open(make_daily_jsonl_file(filename), "a", encoding="utf-8") as f:
        f.write(json.dumps(wrapped) + "\n")


if __name__ == '__main__':
    p = pylontech.Pylontech(serial_port="COM7", baudrate=9600)
    # print(p.get_protocol_version())
    # print(p.get_manufacturer_info())
    # print(p.get_system_parameters())
    # print(p.get_management_info())
    # print(p.get_module_serial_number())
    data = p.get_values_single(2)
    print(data)
    save_container_as_json(data, "values_single")