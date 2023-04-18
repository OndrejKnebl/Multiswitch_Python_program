import ctypes

# The individual types of data that the encoder can encode are defined here, it is stated here what type of data it is, what the resulting size is
# of encoded data in bytes (without type and channel), by what value should the input value inserted in the lpp field be multiplied, if the input value can
# take negative values and what are its maximum and minimum values, finally what is the expected number of values in the field for the given data type
# where for example with 'arrLen':3 the field is expected to contain the channel number, data type and value to be encoded.
sensor_types = {
    'addDigitalInput' : {'type':"00", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':3},
    'addDigitalOutput' : {'type':"01", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':3},
    'addAnalogInput' : {'type':"02", 'size':2, 'multipl':100, 'signed':True, 'min':-327.67, 'max':327.67, 'arrLen':3},
    'addAnalogOutput' : {'type':"03", 'size':2, 'multipl':100, 'signed':True, 'min':-327.67, 'max':327.67, 'arrLen':3},
    'addGenericSensor' : {'type':"64", 'size':4, 'multipl':1, 'signed':False, 'min':0, 'max':4294967295, 'arrLen':3},
    'addLuminosity' : {'type':"65", 'size':2, 'multipl':1, 'signed':False, 'min':0, 'max':65535, 'arrLen':3},
    'addPresence' : {'type':"66", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':3},    
    'addTemperature' : {'type':"67", 'size':2, 'multipl':10, 'signed':True, 'min':-3276.7, 'max':3276.7, 'arrLen':3},
    'addRelativeHumidity' : {'type':"68", 'size':1, 'multipl':2, 'signed':False, 'min':0, 'max':100, 'arrLen':3}, #'max':127.5
    'addAccelerometer' : {'type':"71", 'size':6, 'multipl':1000, 'signed':True, 'min':-32.767, 'max':32.767, 'arrLen':5},
    'addBarometricPressure' : {'type':"73", 'size':2, 'multipl':10, 'signed':False, 'min':0, 'max':6553.5, 'arrLen':3},
    'addVoltage' : {'type':"74", 'size':2, 'multipl':100, 'signed':False, 'min':0, 'max':655.34, 'arrLen':3},
    'addCurrent' : {'type':"75", 'size':2, 'multipl':1000, 'signed':False, 'min':0, 'max':65.535, 'arrLen':3},
    'addFrequency' : {'type':"76", 'size':4, 'multipl':1, 'signed':False, 'min':0, 'max':4294967295, 'arrLen':3},
    'addPercentage' : {'type':"78", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':3},
    'addAltitude' : {'type':"79", 'size':2, 'multipl':1, 'signed':True, 'min':-32767, 'max':32767, 'arrLen':3},
    'addConcentration' : {'type':"7D", 'size':2, 'multipl':1, 'signed':False, 'min':0, 'max':65535, 'arrLen':3},
    'addPower' : {'type':"80", 'size':2, 'multipl':1, 'signed':False, 'min':0, 'max':65535, 'arrLen':3},
    'addDistance' : {'type':"82", 'size':4, 'multipl':1000, 'signed':False, 'min':0, 'max':4294967.295, 'arrLen':3},
    'addEnergy' : {'type': "83", 'size':4, 'multipl':1000, 'signed':False, 'min':0, 'max':4294967.295, 'arrLen':3},
    'addDirection' : {'type':"84", 'size':2, 'multipl':1, 'signed':False, 'min':0, 'max':65535, 'arrLen':3},
    'addUnixTime' : {'type':"85", 'size':4, 'multipl':1, 'signed':False, 'min':0, 'max':4294967295, 'arrLen':3},
    'addGyrometer' : {'type':"86", 'size':6, 'multipl':100, 'signed':True, 'min':-327.67, 'max':327.67, 'arrLen':5},
    'addColour' : {'type':"87", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':5}, # size changed
    'addGPS' : {'type':"88", 'size':9, 'multipl_l_l' : 10000, 'multipl_alt' : 100, 'signed': True, 'min_l_l':-838.8607, 'max_l_l':838.8607, 'min_alt':-83886.07, 'max_alt':83886.07, 'arrLen':5},
    'addSwitch' : {'type':"8E", 'size':1, 'multipl':1, 'signed':False, 'min':0, 'max':255, 'arrLen':3},

    # myTypes
    'addSmallTime':{'type':"C0", 'size':3, 'multipl':1, 'signed':False, 'min':0, 'max':16777215, 'arrLen':3}
}


# A function in which the entered data in the array is encoded into the Cayenne LPP format, where the output is a string with the encoded data
def encodeCayenneLPP(lpp):

    payload = ""                                                                                                            # The resulting encoded data will be gradually added to this variable
    onePayload = ""                                                                                                         # Data of the currently encoded type will be added to this variable each cycle


    for i in range(0,len(lpp)):                                                                                     
            
        sensorInfo = sensor_types.get(lpp[i][1])                                                                            # Determining what type of data to encode

        if sensorInfo == None:                                                                                              # Unknown data type
            print("Unknown type " + str(lpp[i][1]) + " in channel " + str(lpp[i][0]) + ".")
            continue

        if len(lpp[i]) != sensorInfo.get("arrLen"):                                                                         # There are more or fewer elements in the data field to be encoded than expected for this detected type
            print("Too few/many values in channel " + str(lpp[i][0]) + " of the type " + str(lpp[i][1]))

        else:                                                                                                               # Here begins the creation of the payload of a specific item in the lpp field

            try:
                onePayload += str(f'{lpp[i][0]:02x}')                                                                       # Adding a channel
            except:
                print("The channel number is in the wrong format!")
                continue
                                                                            

            onePayload += sensorInfo.get("type")                                                                            # Here we add the data type in Cayenne LPP to the payload


            for j in range(2,len(lpp[i])):                                                                                  # Cycle for encoding the specified values to be encoded (for example, encoding a temperature value of 27.5)

                error = False                                                                                               # Variable to check if an error occurred during encoding
                value = lpp[i][j]                                               


                if type(value) != int and type(value) != float:                                                             # Check if a numeric data value has been entered
                    print("The value in channel " + str(lpp[i][0]) + " of the type " + lpp[i][1] + " is not a number.")
                    error = True
                    break


                # Range and *
                if lpp[i][1] == "addGPS":                                                                                   # GPS is coded differently because it contains multiple multipliers and different max, min values for coordinates and for altitude
                    if j < 4:
                        if not (value >= sensorInfo.get("min_l_l") and value <= sensorInfo.get("max_l_l")):
                            print("Value " + str(value) + " in channel " + str(lpp[i][0]) + " of the type " + lpp[i][1] + " is outside the " + str(sensorInfo.get("min_l_l")) + " - " + str(sensorInfo.get("max_l_l")) + " range!")
                            error = True
                            break
                        valueConversion = int(value * sensorInfo.get("multipl_l_l"))                                        # When the longitude/latitude value is in the range, we multiply it by a multiplier and turn the resulting value into an integer

                    else:
                        if not (value >= sensorInfo.get("min_alt") and value <= sensorInfo.get("max_alt")):
                            print("Value " + str(value) + " in channel " + str(lpp[i][0]) + " of the type " + lpp[i][1] + " is outside the " + str(sensorInfo.get("min_alt")) + " - " + str(sensorInfo.get("max_alt")) + " range!")
                            error = True
                            break
                        valueConversion = int(value * sensorInfo.get("multipl_alt"))                                        # When the altitude value is in the range, we multiply it by a multiplier and turn the resulting value into an integer
                        
                else:                                                                                                       # Encoding other data types
                    if not (value >= sensorInfo.get("min") and value <= sensorInfo.get("max")):
                        print("Value " + str(value) + " in channel " + str(lpp[i][0]) + " of the type " + lpp[i][1] + " is outside the " + str(sensorInfo.get("min")) + " - " + str(sensorInfo.get("max")) + " range!")
                        error = True
                        break
                    valueConversion = int(value * sensorInfo.get("multipl"))                                                # When the data value is in the range, we multiply it by a multiplier and turn the resulting value into an integer


                # Signed conversion
                sign = False
            
                if value < 0:                                                                                               # Check if the value is negative
                    sign = True

                if sensorInfo.get("signed") & sign:                                                                         # When the value is negative and the data type can be negative
                    if lpp[i][1] == "addGPS":
                        valueConversion = ctypes.c_uint32(valueConversion).value                                            # Convert negative GPS values to positive using a 32-bit non-negative integer
                    else:
                        valueConversion = ctypes.c_uint16(valueConversion).value                                            # Convert negative values to positive using a 16-bit non-negative integer


                # Here the encoded number is converted to a hexadecimal string with the corresponding number of digits
                # Subsequently, this string is added to the channel and type in the onePayload variable
                if sensorInfo.get("size") == 1:
                    onePayload += str(f'{valueConversion:02x}')[-2:]
                elif sensorInfo.get("size") == 2:
                    onePayload += str(f'{valueConversion:04x}')[-4:]
                elif sensorInfo.get("size") == 3:
                    onePayload += str(f'{valueConversion:06x}')[-6:]
                elif sensorInfo.get("size") == 4:
                    onePayload += str(f'{valueConversion:08x}')[-8:]
                elif sensorInfo.get("size") == 6:
                    onePayload += str(f'{valueConversion:04x}')[-4:]
                elif sensorInfo.get("size") == 9:
                    onePayload += str(f'{valueConversion:06x}')[-6:]
            
            if error == False:
                
                payload += onePayload                                                                                       # If there was no error while encoding one type of data, then we add the encoded data of one type to the total payload string
                onePayload = ""                                                                                             # Clearing the onePayload variable for the next round of the cycle
            else:
                onePayload = ""

    return payload                                                                                                          # Returning the resulting payload string with encoded data in Cayenne LPP format
