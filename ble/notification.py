import time
import bluetooth
from aioble import core
import aioble
import asyncio
import gc
from constans import *
# Register GATT server.
#temp_service: aioble.Service
#_data_source: Characteristic
#noti_source: Characteristic
#control_source: Characteristic
from collections import deque

class NotificationService:
    def __init__(self, noti_flag):
        self.noti_flag = noti_flag
        core.register_irq_handler(self.client_irq_handler, None)
        self.notifications = []
        pass
        
    async def registerBLE(self):
        self.temp_service = aioble.Service(ENV_SENSE_UUID)
        self.temp_characteristic = aioble.Characteristic(self.temp_service, ENV_SENSE_TEMP_UUID, read=True, notify=True)
        aioble.register_services(self.temp_service)        
        t2 = asyncio.create_task(self.peripheral_task())
        await t2
        pass
    
    # Serially wait for connections. Don't advertise while a central is
    # connected.
    async def peripheral_task(self):
        while True:
            async with await aioble.advertise(
                ADV_INTERVAL_MS,
                name="mpy-temp",
                services=[ENV_SENSE_UUID],
                appearance=ADV_APPEARANCE_GENERIC_THERMOMETER,
            ) as connection:
                #global _data_source, control_source
                print("Connection from33", connection.device)
                print("Connection services", connection.services())
                #await connection.pair()
                service = await connection.service(ANCS_UUID_SERVICE)
                print("service: ", service)
                self.control_source = await service.characteristic(ANCS_UUID_CONTROL_SOURCE)
                self._data_source = await service.characteristic(ANCS_UUID_DATA_SOURCE)
                ret = await self._data_source.subscribe()
                
                print("data_source: ", ret)
                self.noti_source = await service.characteristic(ANCS_UUID_NOTI_SOURCE)
                ret = await self.noti_source.subscribe()
                
                print("noti_source: ", ret)
                await connection.disconnected(timeout_ms=None)



    def client_irq_handler(self, event, data):
        if event == IRQ_GATTC_SERVICE_RESULT:
            pass
        elif event == IRQ_GATTC_NOTIFY: #ESP_GATTC_NOTIFY_EVT
            conn_handle, value_handle, notify_data = data
            if (value_handle == 43): # data source notify
                bData = bytes(notify_data)
                result = self.receive_apple_data_source(bData)
                self.notifications.append(result)
                self.noti_flag.set()
                pass
            elif (value_handle == 40): # Noti source notify
                asyncio.run(self.handle_notify(notify_data))
                pass

            #gc.collect()
    
    async def handle_notify(self, data):
        bData = bytes(data)
        noti = Notification(bData)
        
        if (noti.eventID == EventIDNotificationAdded & noti.categoryID == CategoryIDIncomingCall):
            print("Incoming Call")
        elif (noti.eventID == EventIDNotificationAdded):
            asyncio.create_task(self.get_notification_attributes(self.control_source, noti.data))
            
    
    async def get_noti(self):
        print("Run heeeee33333")
        
    async def get_notification_attributes(self, control_point_char, data):
        print("Run hee22222eee", control_point_char)
        # Build the command packet
        cmd = bytearray()
        print("Write Command" , CommandIDGetNotificationAttributes)
        # Command ID (1 byte)
        cmd.append(CommandIDGetNotificationAttributes)
        
        # Notification UID (4 bytes)
        cmd.append(data[4])
        cmd.append(data[5])
        cmd.append(data[6])
        cmd.append(data[7])
        # Attribute IDs with optional max length
        cmd.append(NotificationAttributeIDAppIdentifier)
        cmd.append(NotificationAttributeIDTitle)
        cmd.append(0xff)
        cmd.append(0xff)
        cmd.append(NotificationAttributeIDMessage)
        cmd.append(0xff)
        cmd.append(0xff)
        # Write to control point with response
        print(f"Sent GetNotificationAttributes: {len(cmd)} bytes")
        try:
            await control_point_char.write(cmd, response=True)
            #asyncio.create_task(self.get_noti())
            print("Heooo")
        except Exception as e:
            print("Error ", e)
        gc.collect()

    def receive_apple_data_source(self, message):
        """
        Parse ANCS Data Source notification response.
        
        Args:
            message: bytes/bytearray received from ANCS Data Source characteristic
            
        Returns:
            dict with parsed notification data:
            {
                'command_id': int,
                'notification_uid': int,
                'attributes': {
                    attr_id: value (str or bytes)
                }
            }
        """
        if not message or len(message) == 0:
            return None
        
        # Extract command ID (first byte)
        command_id = message[0]
        
        result = {
            'command_id': command_id,
            'attributes': {}
        }
        
        if command_id == CommandIDGetNotificationAttributes:
            # Extract Notification UID (bytes 1-4, little-endian)
            notification_uid = (message[1] | 
                               (message[2] << 8) | 
                               (message[3] << 16) | 
                               (message[4] << 24))
            result['notification_uid'] = notification_uid
            
            print(f"Received Notification Attributes response, Command ID: {command_id}, UID: {notification_uid}")
            
            # Parse attributes (starting from byte 5)
            remain_attr_len = len(message) - 5
            offset = 5
            
            while remain_attr_len > 0:
                if offset >= len(message):
                    break
                    
                # Get Attribute ID (1 byte)
                attribute_id = message[offset]
                
                # Get length (2 bytes, little-endian)
                if offset + 2 >= len(message):
                    print("Data error: incomplete length field")
                    break
                attr_len = message[offset + 1] | (message[offset + 2] << 8)
                
                # Validate length
                if attr_len > (remain_attr_len - 3):
                    print("Data error: invalid attribute length")
                    break
                
                # Extract attribute value
                value_start = offset + 3
                value_end = value_start + attr_len
                
                if value_end > len(message):
                    print("Data error: attribute value extends beyond message")
                    break
                    
                attr_value = message[value_start:value_end]
                
                # Process based on attribute ID
                if attribute_id == NotificationAttributeIDAppIdentifier:
                    try:
                        decoded = attr_value.decode('utf-8')
                        print(f"App Identifier: {decoded}")
                        result['attributes'][attribute_id] = decoded
                    except:
                        print(f"App Identifier (raw): {attr_value}")
                        result['attributes'][attribute_id] = attr_value
                        
                elif attribute_id == NotificationAttributeIDTitle:
                    try:
                        decoded = attr_value.decode('utf-8')
                        print(f"Title: {decoded}")
                        result['attributes'][attribute_id] = decoded
                    except:
                        print(f"Title (raw): {attr_value}")
                        result['attributes'][attribute_id] = attr_value
                        
                elif attribute_id == NotificationAttributeIDSubtitle:
                    try:
                        decoded = attr_value.decode('utf-8')
                        print(f"Subtitle: {decoded}")
                        result['attributes'][attribute_id] = decoded
                    except:
                        print(f"Subtitle (raw): {attr_value}")
                        result['attributes'][attribute_id] = attr_value
                        
                elif attribute_id == NotificationAttributeIDMessage:
                    try:
                        decoded = attr_value.decode('utf-8')
                        print(f"Message: {decoded}")
                        result['attributes'][attribute_id] = decoded
                    except:
                        print(f"Message (raw): {attr_value}")
                        result['attributes'][attribute_id] = attr_value
                        
                elif attribute_id == NotificationAttributeIDMessageSize:
                    try:
                        decoded = attr_value.decode('utf-8')
                        print(f"Message Size: {decoded}")
                        result['attributes'][attribute_id] = decoded
                    except:
                        print(f"Message Size (raw): {attr_value}")
                        result['attributes'][attribute_id] = attr_value
                        
                elif attribute_id == NotificationAttributeIDDate:
                    # Format: yyyyMMdd'T'HHmmSS
                    try:
                        decoded = attr_value.decode('utf-8')
                        print(f"Date: {decoded}")
                        result['attributes'][attribute_id] = decoded
                    except:
                        print(f"Date (raw): {attr_value}")
                        result['attributes'][attribute_id] = attr_value
                        
                elif attribute_id == NotificationAttributeIDPositiveActionLabel:
                    print(f"Positive Action Label (hex): {attr_value.hex()}")
                    result['attributes'][attribute_id] = attr_value
                    
                elif attribute_id == NotificationAttributeIDNegativeActionLabel:
                    print(f"Negative Action Label (hex): {attr_value.hex()}")
                    result['attributes'][attribute_id] = attr_value
                    
                else:
                    print(f"Unknown Attribute ID {attribute_id} (hex): {attr_value.hex()}")
                    result['attributes'][attribute_id] = attr_value
                
                # Move to next attribute
                offset += (1 + 2 + attr_len)
                remain_attr_len -= (1 + 2 + attr_len)
            
        elif command_id == CommandIDGetAppAttributes:
            print("Received APP Attributes response")
            # Add parsing for app attributes if needed
            
        elif command_id == CommandIDPerformNotificationAction:
            print("Received Perform Notification Action response")
            
        else:
            print(f"Unknown Command ID: {command_id}")
        
        return result
    
class Notification:
    def __init__(self, data):
        self.data = data
        self.eventID = data[0]
        self.categoryID = data[2]
        #self.notiUID = (data[4]) | (data[5]<< 8) | (data[6]<< 16) | (data[7] << 24)