import pylontech
import json
from io import BytesIO
from datetime import datetime
import os
import time

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
    

if __name__ == '__main__':

    try:
        p = pylontech.Pylontech(serial_port="COM30", baudrate=9600)
        print("Connection established with Energy storage device ")
        # print(p.get_protocol_version())
        # print(p.get_manufacturer_info())
        # print(p.get_system_parameters())
        #print(p.get_management_info(2))
        #print(p.get_module_serial_number())

    except Exception as e:
        print("Errror:  ", e)

    try:
            print("Saving data to files ")
            
            switch_saving = 1
            last_second = -1
            while True:
                    
                    now = datetime.now()
                    current_second = now.second
                    
                    if current_second%5==0:
                        start = time.time()
                        #File.save_container_as_json(p.get_management_info(2), "management_info")
                        #time.sleep(0.1)
                        #File.save_container_as_json(p.get_values_single(2), "values_single")
                        match switch_saving:
                            case 1:
                                File.save_container_as_json(p.get_management_info(2), "management_info")
                                switch_saving = 2
                            case 2:
                                File.save_container_as_json(p.get_values_single(2), "values_single")
                                switch_saving = 1
                            case _:
                                switch_saving = 1
                        last_second = current_second
                        print(f"Total time: {time.time() - start:.2f} seconds")
                    
    except Exception as e:
        print("error in getting data:", e)