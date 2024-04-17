#!/usr/bin/env python

from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from time import sleep
import post

'''
Pn532_i2c() -> def __init__(self, address=PN532_I2C_SLAVE_ADDRESS, i2c_channel=RPI_DEFAULT_I2C_NEW):
PN532_I2C_SLAVE_ADDRESS = 0x24
RPI_DEFAULT_I2C_NEW = 0x01

pn532.SAMconfigure() -> def SAMconfigure(self, frame=None): 如果沒有frame參數便會自行產生

'''

'''
read_mifare send_command_check_ack then return read_response()
read_response() will return frame

# Type of frame.
PN532_FRAME_TYPE_DATA = 0
PN532_FRAME_TYPE_ACK = 1
PN532_FRAME_TYPE_NACK = 2
PN532_FRAME_TYPE_ERROR = 3

# methods:
@func get_length(self):               Gets the frame's data length.
@func get_length_checksum(self):      Gets the checksum of get_length().
@func get_data(self):                 Gets the frame's data.
@func get_data_checksum(self):        Gets a checksum for the frame's data.
@func get_frame_type(self):           Gets the frame's type.
@func to_tuple(self):                 return (byte_array)

@staticmethod
@func from_response(response):        Fractory that generates a Pn532Frame from a response from the PN532.
@func is_valid_response(response):    Checks if a response from the PN532 is valid. 
@func is_ack(response):               Checks if the response is an ACK frame.
@func is_error(response):             Checks if the response is an error frame.

Manufacturer data : 
        ['4B', '01', '01', '00', '04', '08', '04']

UID :   ['63', '05', 'E6', '02']
        ['11', '39', 'EF', '4C']
        ['65', '11', '71', '2A']
        ['2C', '0B', '6A', '22']
'''
pn532=Pn532_i2c()
pn532.SAMconfigure()

card_list = ["6305E602",
             "1139EF4C",
             "6511712A",
             "2C0B6A22"]

while True:
        print()
        print("###########################################################")
        print("###########################################################")
        print("#---------> Please hold your tag near the reader！<-------#")
        print("###########################################################")
        print("###########################################################")
        print("#---------> You can type Ctrl+C to STOP anytime <---------#")
        print("###########################################################")
        data = pn532.read_mifare().get_data()  # get_data is a method inside frame 
        print("Reading......")
        #print(data)
        c_state = False
        if  len(data) == 11:
                print("Card detected,You can move your card now......")
                uid = str("%02X%02X%02X%02X" % (data[7],data[8],data[9],data[10]))
                msg = f"The UID is : {uid}"
                print(msg)
                res = post.checkin(uid,"1") # post(uid, room_nmuber)                       
                print(res)
                if 'Checking successfully' in res:
                        print('簽到成功')
                else:
                        print('簽到失敗')            
                sleep(1)
        else:
                print("驗證失敗，非正式發行的卡片。")
                sleep(1)


