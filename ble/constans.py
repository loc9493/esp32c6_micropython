import bluetooth
#IRQ Client EventID
IRQ_GATTC_SERVICE_RESULT = const(9)
IRQ_GATTC_SERVICE_DONE = const(10)
IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
IRQ_GATTC_DESCRIPTOR_DONE = const(14)
IRQ_GATTC_READ_RESULT = const(15)
IRQ_GATTC_READ_DONE = const(16)
IRQ_GATTC_WRITE_DONE = const(17)
IRQ_GATTC_NOTIFY = const(18)
IRQ_GATTC_INDICATE = const(19)

#EventID
EventIDNotificationAdded     = 0
EventIDNotificationModified  = 1
EventIDNotificationRemoved   = 2

#CategoryID
CategoryIDOther              = 0
CategoryIDIncomingCall       = 1
CategoryIDMissedCall         = 2
CategoryIDVoicemail          = 3
CategoryIDSocial             = 4
CategoryIDSchedule           = 5
CategoryIDEmail              = 6
CategoryIDNews               = 7
CategoryIDHealthAndFitness   = 8
CategoryIDBusinessAndFinance = 9
CategoryIDLocation           = 10
CategoryIDEntertainment      = 11

#NotifcationAttributeID
NotificationAttributeIDAppIdentifier       = 0
NotificationAttributeIDTitle               = 1 #//(Needs to be followed by a 2-bytes max length parameter)
NotificationAttributeIDSubtitle            = 2 #//(Needs to be followed by a 2-bytes max length parameter)
NotificationAttributeIDMessage             = 3 #//(Needs to be followed by a 2-bytes max length parameter)
NotificationAttributeIDMessageSize         = 4
NotificationAttributeIDDate                = 5
NotificationAttributeIDPositiveActionLabel = 6
NotificationAttributeIDNegativeActionLabel = 7

#CommandID
CommandIDGetNotificationAttributes = 0
CommandIDGetAppAttributes          = 1
CommandIDPerformNotificationAction = 2

# org.bluetooth.service.environmental_sensing
ENV_SENSE_UUID = bluetooth.UUID(0x181A)
ANCS_UUID_SERVICE = bluetooth.UUID('7905f431-b5ce-4e99-a40f-4b1e122d00d0')
ANCS_UUID_NOTI_SOURCE = bluetooth.UUID('9fbf120d-6301-42d9-8c58-25e699a21dbd')
ANCS_UUID_DATA_SOURCE = bluetooth.UUID('22eac6e9-24d6-4bb5-be44-b36ace7c7bfb')
ANCS_UUID_CONTROL_SOURCE = bluetooth.UUID('69d1d8f3-45e1-49a8-9821-9bbdfdaad9d9')
# org.bluetooth.characteristic.temperature
ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
# org.bluetooth.characteristic.gap.appearance.xml
ADV_APPEARANCE_GENERIC_THERMOMETER = const(960)

# How frequently to send advertising beacons.
ADV_INTERVAL_MS = 250_000

