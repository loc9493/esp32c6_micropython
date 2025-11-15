import sys

# ruff: noqa: E402
sys.path.append("")

from micropython import const

import asyncio
import aioble
import bluetooth
from aioble import core
import random
import struct
import time
from notification import *

# Helper to encode the temperature characteristic encoding (sint16, hundredths of a degree).
def _encode_temperature(temp_deg_c):
    return struct.pack("<h", int(temp_deg_c * 100))


# This would be periodically polling a hardware sensor.
async def sensor_task():
    t = 24.5
    while True:
        temp_characteristic.write(_encode_temperature(t), send_update=True)
        t += random.uniform(-0.5, 0.5)
        await asyncio.sleep_ms(1000)


# Run both tasks.
async def main():
    core.register_irq_handler(client_irq_handler, None)
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)


asyncio.run(main())


# 
# if (param->notify.handle == gl_profile_tab[PROFILE_A_APP_ID].notification_source_handle) {
#             esp_receive_apple_notification_source(param->notify.value, param->notify.value_len);
#             uint8_t *notificationUID = &param->notify.value[4];
#             if (param->notify.value[0] == EventIDNotificationAdded && param->notify.value[2] == CategoryIDIncomingCall) {
#                  ESP_LOGI(BLE_ANCS_TAG, "IncomingCall, reject");
#                  //Call reject
#                  esp_perform_notification_action(notificationUID, ActionIDNegative);
#              } else if (param->notify.value[0] == EventIDNotificationAdded) {
#                 //get more information
#                 ESP_LOGI(BLE_ANCS_TAG, "Get detailed information");
#                 esp_get_notification_attributes(notificationUID, sizeof(p_attr)/sizeof(esp_noti_attr_list_t), p_attr);
#              }
#         } else if (param->notify.handle == gl_profile_tab[PROFILE_A_APP_ID].data_source_handle) {
#             memcpy(&data_buffer.buffer[data_buffer.len], param->notify.value, param->notify.value_len);
#             data_buffer.len += param->notify.value_len;
#             if (param->notify.value_len == (gl_profile_tab[PROFILE_A_APP_ID].MTU_size - 3)) {
#                 // copy and wait next packet, start timer 500ms
#                 esp_timer_start_periodic(periodic_timer, 500000);
#             } else {
#                 esp_timer_stop(periodic_timer);
#                 esp_receive_apple_data_source(data_buffer.buffer, data_buffer.len);
#                 memset(data_buffer.buffer, 0, data_buffer.len);
#                 data_buffer.len = 0;
#             }
#         } else {
#             ESP_LOGI(BLE_ANCS_TAG, "unknown handle, receive notify value:");
#         }
#         break;