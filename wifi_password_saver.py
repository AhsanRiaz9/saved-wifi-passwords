import subprocess
import pandas as pd
import json
import os
import platform

class WifiService:
    def __init__(self):
        self.current_os = platform.system()
        self.outputs = ['.csv', '.json']
        self.network_path = '/etc/NetworkManager/system-connections/'

    def __fetch_profile_for_windows(self):
        result = subprocess.run(
            ["netsh", "wlan", "show", "profile"],
            capture_output=True,
            text=True
        )
        user_profiles = result.stdout.split("User profiles")[1].strip().split("All User Profile")
        result = [profile.strip()[2:] for profile in user_profiles if ' : ' in profile] 
        return result
    
    def __for_profiles_for_linux(self):
        result = [wifi for wifi in os.listdir(self.network_path) if '.nmconnection' in wifi]    
        return result
     
    def fetch_profiles(self):
        result = []
        if self.current_os == 'Windows':
            result = self.__fetch_profile_for_windows() 
        else:
            result = self.__for_profiles_for_linux()
        return result
    
    def __fetch_profile_password_for_windows(self, profile_name):
        result = subprocess.run(
            ["netsh", "wlan", "show", "profile", profile_name, "key=clear"],
            capture_output=True,
            text=True
        )
        password = result.stdout.split("Key Content")[1].strip().split("Cost settings")[0][2:].strip()
        return password   
    
    def __fetch_profile_password_for_linux(self, profile_name):
        wifi_detail = os.popen(f'sudo cat {self.network_path}/\'{profile_name}\'').read()
        if 'psk=' in wifi_detail:
            ssid = wifi_detail.split('id=')[1].split('\n')[0]
            password = wifi_detail.split('psk=')[1].split('\n')[0]
        return password
    
    def fetch_profile_password(self, profile_name):
        password = ''
        if self.current_os == 'Windows':
            password = self.__fetch_profile_password_for_windows(profile_name) 
        else:
            password = self.__fetch_profile_password_for_linux(profile_name)
        return password
    
    def __save_json(self, saved_wifi_list):
        print("Saving wifi data in json ...")
        save_file = open("saved_wifi_paswords.json", "w")  
        json.dump(saved_wifi_list, save_file, indent = 3)  
        save_file.close()  
    
    def __save_csv(self, saved_wifi_list):
        print("Saving wifi data in csv ...")
        df = pd.DataFrame(saved_wifi_list)
        df.to_csv('saved_wifi_passwords.csv', index=False)

    def save_output(self, saved_wifi_list):
        for output in self.outputs:
            if output == '.csv':
                self.__save_csv(saved_wifi_list)
            elif output == '.json':
                self.__save_json(saved_wifi_list)
            else:
                print(f'Output format {output} is not supported.')
    
if __name__ == '__main__':
    saved_wifi_list = []
    wifi_service = WifiService()
    profile_names = wifi_service.fetch_profiles()
    for profile_name in profile_names:
        password = wifi_service.fetch_profile_password(profile_name)
        profile = {'ssid': profile_name, 'password': password}
        saved_wifi_list.append(profile)
    if saved_wifi_list:    
        wifi_service.save_output(saved_wifi_list)
    else:
        print('No saved wifi passwords found.')
