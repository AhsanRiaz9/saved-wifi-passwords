import os
import pandas as pd
import json

outputs = ['.csv', '.json']

def save_json(saved_wifi_list):
    print("Saving wifi data in json ...")
    save_file = open("saved_wifi_paswords.json", "w")  
    json.dump(saved_wifi_list, save_file, indent = 3)  
    save_file.close()  
    
def save_csv(saved_wifi_list):
    print("Saving wifi data in csv ...")
    df = pd.DataFrame(saved_wifi_list)
    df.to_csv('saved_wifi_passwords.csv', index=False)

if __name__ == '__main__':
    network_path = '/etc/NetworkManager/system-connections/'
    wifi_list = [wifi for wifi in os.listdir(network_path) if '.nmconnection' in wifi]
    saved_wifi_list = []
    for wifi_name in wifi_list:
        wifi_detail = os.popen(f'sudo cat {network_path}/\'{wifi_name}\'').read()
        if 'psk=' in wifi_detail:
            ssid = wifi_detail.split('id=')[1].split('\n')[0]
            password = wifi_detail.split('psk=')[1].split('\n')[0]
            saved_wifi_list.append({'ssid': ssid, 'password': password})
    if saved_wifi_list:    
        # saving output
        for output in outputs:
            if output == '.csv':
                save_csv(saved_wifi_list)
            elif output == '.json':
                save_json(saved_wifi_list)
            else:
                print(f'Output format {output} is not supported.')
    else:
        print('No saved wifi passwords found.')
