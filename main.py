import pylontech
import json
from io import BytesIO
from datetime import datetime
import os
import asyncio

class File: 
    @staticmethod
    def path_of_daily_file(filename):
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        date_str = now.strftime("%Y-%m-%d")

        folder_path = os.path.join("data", year, month)
        os.makedirs(folder_path, exist_ok=True)
        os.path.join(folder_path, f"{filename}_{date_str}.jsonl")
        return os.path.join(folder_path, f"{filename}_{date_str}.jsonl")

    @staticmethod
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

        with open(File.path_of_daily_file(filename), "a", encoding="utf-8") as f:
            f.write(json.dumps(wrapped) + "\n")


async def main_loop():
    switch_saving = 1
    last_second = -1
    while True:
                    now = datetime.now()
                    current_second = now.second
                    
                    if current_second!=last_second:
                        match switch_saving:
                            case 1:
                                await File.save_container_as_json(p.get_management_info(2), "management_info")
                                switch_saving = 2
                            case 2:
                                await File.save_container_as_json(p.get_values_single(2), "values_single")
                                switch_saving = 1
                            case _:
                                switch_saving = 1
                        last_second = current_second

if __name__ == '__main__':
    with pylontech.Pylontech(serial_port="COM7", baudrate=9600) as p:
        print("Connection established with Energy storage device ")
        # print(p.get_protocol_version())
        # print(p.get_manufacturer_info())
        # print(p.get_system_parameters())
        #print(p.get_management_info(2))
        #print(p.get_module_serial_number())

        try:
            print("Saving data to files ")
            
            asyncio.run(main_loop())

        except Exception as e:
            print("Errror:  ", e)
