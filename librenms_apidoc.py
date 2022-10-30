#!/usr/bin/env python3
import logging
import os
import re
import urllib3
import pandas as pd
from tabulate import tabulate
import librenms_apidoc_settings
from librenms_handler.devices import Devices
from librenms_handler.device_groups import DeviceGroups

#disable wanrings - if using self signed cert
urllib3.disable_warnings()
logging.getLogger("urllib3").setLevel(logging.WARNING)

#---Global VARs---
#IMPORTED FROM librenms_apidoc_settings

#Request Devices
devices = Devices(
    librenms_apidoc_settings.MON_HOST,
    librenms_apidoc_settings.TOKEN,
    verify = False
)
#Request DeviceGroups
devicesG = DeviceGroups(
    librenms_apidoc_settings.MON_HOST,
    librenms_apidoc_settings.TOKEN,
    verify = False
)

#Dict for Devices
responseDevices=devices.list_devices()
dict_responseDevices=responseDevices.json()
#Dict for DeviceGroups
responseGroups=devicesG.get_devicegroups()
dict_responseGroups=responseGroups.json()

#Results dataframe
df = pd.DataFrame()

#Build the list of groups...
ITERATOR1=0
grouplist=[]
error_grouplist=[]
while ITERATOR1 < int(dict_responseGroups['count']):
    GROUP_NAME=(dict_responseGroups['groups'][ITERATOR1]['name'])
    if GROUP_NAME in librenms_apidoc_settings.EXCLUDE_GROUPS:
        pass
    else:
        grouplist.append(GROUP_NAME)
    ITERATOR1 += 1

#Work through list of groups and their devices but if an error group don't
for group in grouplist:
    deviceByGroup=devicesG.get_devices_by_group(group)
    deviceByGroup_dict=deviceByGroup.json()
    #print(deviceByGroup_dict)
    GROUPSTATUS=str(deviceByGroup_dict['status'])
    #DEBUG ONLY
    #print("WORKING THROUGH THIS GROUP....."+group)
    if GROUPSTATUS == "ok":
        #use device count within group to determine iteration
        count_now=int(deviceByGroup_dict['count'])
        #initialise
        ITERATOR2=0
        while ITERATOR2 < count_now:
            #create local var for group and deviceID
            this_deviceID=(deviceByGroup_dict['devices'][ITERATOR2]['device_id'])
            this_group=group
            #DEBUG
            #print(this_group)
            #sort out response, make dict
            response_this_device=devices.get_device(this_deviceID)
            response_this_device_dict=response_this_device.json()
            #single device, index 0, create local vars for fields, host and location first
            this_hostname=response_this_device_dict['devices'][0]['hostname']
            this_location=response_this_device_dict['devices'][0]['location']
            #Get the serial
            this_serial=response_this_device_dict['devices'][0]['serial']
            #remove VMWare serials
            if librenms_apidoc_settings.VMWARE_SERIAL_REPLACE == 'TRUE':
                this_serial=re.sub('(V|v)(M|m)(W|w)(A|a)(R|r)(E|e).*', 'VMWare', str(this_serial))
            #OS
            this_features=response_this_device_dict['devices'][0]['features']
            #Notes
            this_notes=response_this_device_dict['devices'][0]['notes']
            #create list of desired fields
            this_list=[this_group, this_hostname, this_serial, this_location, this_features, this_notes]
            #append all necessary fields
            df = df.append(pd.DataFrame([this_list], columns=["Group","Hostname","Serial","Location","OS","Notes"]), ignore_index=True)
            #increment for loop
            ITERATOR2 += 1
    #group has any error e.g. empty
    else:
        #DEBUG ONLY
        #print("ERROR FOR GROUP  "+group+" "+GROUPSTATUS)
        #remove error groups from grouplist
        grouplist.remove(group)
        error_grouplist.append(group)

#DBUG, print df as string
#print(df.to_string())

#find cwd
WORKDIR=os.getcwd()


#Write output
table_var0=tabulate(df, headers='keys', tablefmt=librenms_apidoc_settings.TABLE_FORMAT)

with open(WORKDIR+"/"+librenms_apidoc_settings.OUTPUT_FILE_NAME, "w", encoding="utf-8") as file1:
    file1.write(table_var0)
