from tkinter import *
from tkinter import font
import os
import src.cayenneLPP as cayenneLPP
import src.postData as postData
import src.secrets as secrets


class MyApp:

    # A method to get and store the FPort value
    def getfPort(self):
        strfPort = self.ent1.get()

        if (strfPort != ""):                                     # If entry string is not empty 
            try:
                fPort = int(strfPort)                            # String to integer conversions

                if (1 <= fPort) and (fPort <= 223):              # Check if 1-223
                    self.fPort = fPort
                else:
                    self.textoutp.delete('1.0', END)
                    self.textoutp.insert("1.0", "Error - TTS settings - FPort out of 1 - 223 range!")
                    self.error = True
            except:
                self.textoutp.delete('1.0', END)
                self.textoutp.insert("1.0", "Error - TTS settings - FPort not a number!")
                self.error = True
        else:
            self.textoutp.delete('1.0', END)
            self.textoutp.insert("1.0", "Error - TTS settings - FPort empty entry!")
            self.error = True

    
    # This method is called by checking/unchecking the Confirmed downlink checkbox and updates this value
    def confirmedChange(self):
        if self.confirmedDownlinkVar.get():
            self.confirmedDownlink = True
        else:
            self.confirmedDownlink = False


    # Methods to store the new value selected in the OptionMenu elements
    def selectPriority(self, prior):
        self.priority = prior


    def selectInsertMode(self, mode):
        self.schedule = mode


    # Method for writing to the secrets.py file, where the API key, Application name and End device name are stored
    def saveEndSettings(self):
        newAPIkey = self.ent5.get()
        newAppName = self.ent6.get()
        newEndDeviceName = self.ent7.get()

        file_dir = os.path.dirname(os.path.realpath(__file__))
 
        f = open(file_dir+"/src/secrets.py", 'w')
        f.write("# TTS Information\n")
        f.write("APIKey = "+"\""+ newAPIkey +"\"\n")
        f.write("applicationName = "+"\""+ newAppName +"\"\n")
        f.write("endDeviceName = "+"\""+ newEndDeviceName +"\"\n")
        f.close()


    # A method in which a function is called that encodes the values in the lpp array into the Cayenne LPP format and sends this encoded payload 
    # with a POST request to the TTS network, which sends a downlink with the received payload to the specified end device.
    def encodeAndSendDownlink(self, lpp):
        
        strPassword = self.ent8.get()                                   # Password

        if strPassword != "":                                           # If entry string is not empty
            try:
                password = int(strPassword)                             # String to integer conversions

                if (0 <= password) and (password <= 9999):              # Check if 0 - 9999
                    lpp.append([100, "addPower", password])             # Adding data to the lpp array
                else:
                    self.textoutp.delete('1.0', END)
                    self.textoutp.insert("1.0", "Error - Downlinks password - Out of 0 - 9999 range!")
                    self.error = True
            except:
                self.textoutp.delete('1.0', END)
                self.textoutp.insert("1.0", "Error - Downlinks password - Not a number!")
                self.error = True
        else:
            self.textoutp.delete('1.0', END)
            self.textoutp.insert("1.0", "Error - Downlinks password - Empty entry!")
            self.error = True


        self.getfPort()                                                 # Calling the method to get the FPort number


        APIKey = self.ent5.get()
        applicationName = self.ent6.get()
        endDeviceName = self.ent7.get()

        if APIKey == "" or applicationName == "" or endDeviceName == "":    # If entry strings are not empty
            self.textoutp.delete('1.0', END)
            self.textoutp.insert("1.0", "Error - API key, Application name or End device name - Empty entry!")
            self.error = True


        if self.error != True:                                              # If the error is not True and the lpp array is not empty, then the data entered in the array are encoded
            if lpp != []:
                payload = cayenneLPP.encodeCayenneLPP(lpp)

                self.textoutp.delete('1.0', END)
                self.textoutp.insert("1.0", "Payload: ")
                self.textoutp.insert(END, payload)
                self.textoutp.insert(END, "\nSending payload!")

                statusCode = postData.sendData(payload, self.fPort, self.confirmedDownlink, self.priority, self.schedule.lower(), APIKey, applicationName, endDeviceName) # Method sends encoded payload using a POST request to the TTS network, which sends a downlink with the received payload to the specified end device.

                self.textoutp.insert(END, "\nStatus code: ")
                self.textoutp.insert(END, statusCode)
            else:
                self.textoutp.delete('1.0', END)
                self.textoutp.insert("1.0", "Nothing to send!")

        else:
            self.textoutp.insert(END, "\nNot sending!")
        self.error = False


    # Methods to store the new value selected in the OptionMenu elements
    def selectPowerGrid(self, pGrid):
        self.powerGrid = pGrid

    def selectWorkingMode(self, wMode):
        self.workingMode = wMode

    def selectTimezone(self, tZone):
        self.timezone = tZone

    def selectResetAndLoad(self, load):
        self.resetAndLoad = load


    # The following method is called by pressing the Send common settings button
    def downlinkCommon(self):
        lpp = []

        if ((self.chResetAndLoad == True) and (self.resetAndLoad == "Saved")) or (self.chResetAndLoad == False):            # If is Reset and load set to Defaul, there is no need to send any other settings


            if self.chSendDataEvery:                                            # Send data every 
                strSendDataEvery = self.ent10.get()

                if strSendDataEvery != "":                                      # If entry string is not empty 
                    try:
                        sendDataEvery = int(strSendDataEvery)                   # String to integer conversion

                        if (60 <= sendDataEvery) and (sendDataEvery <= 3600):   # Check if 60-3600
                            lpp.append([100, "addSmallTime", sendDataEvery])    # Adding data to the lpp array
                        else:
                            self.textoutp.delete('1.0', END)
                            self.textoutp.insert("1.0", "Error - Common settings - Send data every out of 60 - 3600 range!")
                            self.error = True
                    except:
                        self.textoutp.delete('1.0', END)
                        self.textoutp.insert("1.0", "Error - Common settings - Send data every is not a number!")
                        self.error = True
                else:
                    self.textoutp.delete('1.0', END)
                    self.textoutp.insert("1.0", "Error - Common settings - Send data every empty entry!")
                    self.error = True


            if self.chNumberOfSamples:                                          # Number of measured samples between send times
                strNumberOfSamples = self.ent12.get()

                if strNumberOfSamples != "":                                    # If entry string is not empty 
                    try:
                        numberOfSamples = int(strNumberOfSamples)               # String to integer conversions

                        if (1 <= numberOfSamples) and (numberOfSamples <= 10):  # Check if 1-10 samples
                            lpp.append([100, "addPresence", numberOfSamples])   # Adding data to the lpp array
                        else:
                            self.textoutp.delete('1.0', END)
                            self.textoutp.insert("1.0", "Error - Common settings - Number of samples out of 1 - 10 range!")
                            self.error = True
                    except:
                        self.textoutp.delete('1.0', END)
                        self.textoutp.insert("1.0", "Error - Common settings - Number of samples is not a number!")
                        self.error = True
                else:
                    self.textoutp.delete('1.0', END)
                    self.textoutp.insert("1.0", "Error - Common settings - Number of samples empty entry!")
                    self.error = True


            if self.chPowerGrid:                                                # Power Grid - if checkbox checked => Add Power grid
                if self.powerGrid == "230":
                    lpp.append([103, "addDigitalInput", 0])                     #  0 = 230 V
                else:
                    lpp.append([103, "addDigitalInput", 1])                     #  1 = 400 V


            if self.chWorkingMode:                                              # Working mode - if checkbox checked => Add Working mode
                if self.workingMode == "OFF":
                    lpp.append([101, "addDigitalInput", 0])                     #  0 = OFF
                elif self.workingMode == "ON":
                    lpp.append([101, "addDigitalInput", 1])                     #  1 = ON
                elif self.workingMode == "Ligh intensity":
                    lpp.append([101, "addDigitalInput", 2])                     #  2 = Ligh intensity
                elif self.workingMode == "Time":
                    lpp.append([101, "addDigitalInput", 3])                     #  3 = Time
                elif self.workingMode == "Ligh intensity in Time":
                    lpp.append([101, "addDigitalInput", 4])                     #  4 = Ligh intensity in Time
                elif self.workingMode == "Sunset / sunrise times":
                    lpp.append([101, "addDigitalInput", 5])                     #  5 = Sunset / sunrise times


            if self.chTimezone:                                                 # Timezone - if checkbox checked => Add Timezone
                if self.timezone == "Central European Time":                    
                    lpp.append([102, "addDigitalInput", 0])                     # 0 = Central European Time
                elif self.timezone == "United Kingdom":
                    lpp.append([102, "addDigitalInput", 1])                     # 1 = United Kingdom
                elif self.timezone == "UTC":
                    lpp.append([102, "addDigitalInput", 2])                     # 2 = UTC
                elif self.timezone == "US Eastern Time Zone":
                    lpp.append([102, "addDigitalInput", 3])                     # 3 = US Eastern Time Zone
                elif self.timezone == "US Central Time Zone":
                    lpp.append([102, "addDigitalInput", 4])                     # 4 = US Central Time Zone
                elif self.timezone == "US Mountain Time Zone":
                    lpp.append([102, "addDigitalInput", 5])                     # 5 = US Mountain Time Zone
                elif self.timezone == "US Arizona":
                    lpp.append([102, "addDigitalInput", 6])                     # 6 = US Arizona
                elif self.timezone == "US Pacific Time Zone":
                    lpp.append([102, "addDigitalInput", 7])                     # 7 = US Pacific Time Zone
                elif self.timezone == "Australia Eastern Time Zone":
                    lpp.append([102, "addDigitalInput", 8])                     # 8 = Australia Eastern Time Zone
 

            if self.chSendOnlySelected:                                         # Send only selected - if checkbox checked
                sendingData1 = [0,0,0,0,0,0,0,0]
                sendingData2 = [0,0,0,0,0,0,0,0]
                
                # Settings Data in sendingData1 - Send only selected 1/2:
                if self.chRelayState:                                           # Relay state info (opened/closed) - if checkbox checked
                    sendingData1[7] = 1

                if self.chNumberOfChanges:                                      # If relay was closed between sends - if checkbox checked
                    sendingData1[6] = 1                                         

                if self.chLightIntensity:                                       # BH1750 - Light intensity - if checkbox checked
                    sendingData1[5] = 1                                        

                if self.chBatteryVoltge:                                        # LC709203F - Battery voltage - if checkbox checked
                    sendingData1[4] = 1                                         

                if self.chBatteryPercentige:                                    # LC709203F - Battery percentage - if checkbox checked
                    sendingData1[3] = 1 

                if self.chBatteryTemperature:                                   # LC709203F - Battery temperature - if checkbox checked
                    sendingData1[2] = 1

                if self.chRTCTemperature:                                       # RTC - temperature - if checkbox checked
                    sendingData1[1] = 1

                if self.chPowerLineVoltage:                                     # PZEM - Power Line Voltage - if checkbox checked
                    sendingData1[0] = 1

                # Settings Data in sendingData2 - Send only selected 2/2:
                if self.chPowerLineFrequency:                                   # PZEM - Power Line Frequency - if checkbox checked
                    sendingData2[7] = 1                                         

                if self.chActiveEnergy:                                         # PZEM - Active Energy - if checkbox checked
                    sendingData2[6] = 1                                         

                if self.chCurrent:                                              # PZEM - Current - if checkbox checked
                    sendingData2[5] = 1                                         

                if self.chActivePower:                                          # PZEM - Active Power - if checkbox checked
                    sendingData2[4] = 1     
            
                if self.chPowerFactor:                                          # PZEM - Power factor - if checkbox checked
                    sendingData2[3] = 1

                if self.chSunrise:                                              # Sunrise - if checkbox checked
                    sendingData2[2] = 1

                if self.chSunset:                                               # Sunset - if checkbox checked
                    sendingData2[1] = 1
            

                resSendingData1 = int("".join(str(x) for x in sendingData1), 2)         # Converting binary list to integer value
                resSendingData2 = int("".join(str(x) for x in sendingData2), 2)         # Converting binary list to integer value

                lpp.append([1, "addDigitalOutput", resSendingData1])                    # Send only selected 1/2
                lpp.append([2, "addDigitalOutput", resSendingData2])                    # Send only selected 2/2


            if (self.chResetAndLoad == True) and (self.resetAndLoad == "Saved"):        # Reset Feather
                lpp.append([100, "addDigitalInput", 1])                                 # 1 - reset Feather and load saved config from EEPROM

        else:
            if (self.chResetAndLoad == True) and (self.resetAndLoad == "Default"):      # Reset Feather
                lpp.append([100, "addDigitalInput", 2])                                 # 2 - reset and load default config from Feather

            
        self.encodeAndSendDownlink(lpp)                                                 # Call method for encode lpp and send payload  



    # The following methods are called by changing the state of radio buttons in the Switching times block
    def rOnTime1NotChange(self):
        self.rSetOnTime1 = False
    def rOnTime1SetChange(self):
        self.rSetOnTime1 = True

    def rOnTime2NotChange(self):
        self.rSetOnTime2 = False
    def rOnTime2SetChange(self):
        self.rSetOnTime2 = True

    def rOnTime3NotChange(self):
        self.rSetOnTime3 = False
    def rOnTime3SetChange(self):
        self.rSetOnTime3 = True

    def rOffTime1NotChange(self):
        self.rSetOffTime1 = False
    def rOffTime1SetChange(self):
        self.rSetOffTime1 = True

    def rOffTime2NotChange(self):
        self.rSetOffTime2 = False
    def rOffTime2SetChange(self):
        self.rSetOffTime2 = True

    def rOffTime3NotChange(self):
        self.rSetOffTime3 = False
    def rOffTime3SetChange(self):
        self.rSetOffTime3 = True



    # Method that checks input values from Spinboxes with times and converts the times to seconds of the day. The method returns -1 on error
    def getTimeSecondsOfDay(self, timeName, strTimeHours, strTimeMinutes, strTimeSeconds):          # For all times same method

        if (strTimeHours != "") and (strTimeMinutes != "") and (strTimeSeconds != ""):              # If entry strings are not empty 
            try:
                timeHours = int(strTimeHours)                                                       # String to integer conversions
                timeMinutes = int(strTimeMinutes)
                timeSeconds = int(strTimeSeconds)

                if ((0 <= timeHours) and (timeHours <= 23)) and ((0 <= timeMinutes) and (timeMinutes <= 59)) and ((0 <= timeSeconds) and (timeSeconds <= 59)):          # Check if 0 <= hour <= 23  and  0 <= minute <= 59 and 0 <= second <= 59                    
                    secondsOfDay = (timeHours*3600)+(timeMinutes*60)+timeSeconds                                                                                        # Converts the times to seconds of the day
                else:
                    self.textoutp.delete('1.0', END)
                    self.textoutp.insert("1.0", "Error - Switching times - " + timeName + " - Out of 0 <= hour <= 23  and  0 <= minute <= 59 and 0 <= second <= 59 range!")
                    self.error = True
                    return -1
            except:
                self.textoutp.delete('1.0', END)
                self.textoutp.insert("1.0", "Error - Switching times - " + timeName + " - Not a Number!")
                self.error = True
                return -1
        else:
            self.textoutp.delete('1.0', END)
            self.textoutp.insert("1.0", "Error - Switching times - " + timeName + " - Empty entry!")
            self.error = True
            return -1

        return secondsOfDay



    # The following method is called by pressing the Send switching times settings
    def downlinkSwitchingTimes(self):
        lpp = []

        if self.chOnTime1:                                          # On time 1
            if self.rSetOnTime1:                                    # On time 1 - Set time
                strOnTime1Hours = self.ent40.get()
                strOnTime1Minutes = self.ent41.get()
                strOnTime1Seconds = self.ent42.get()

                setOnTime1 = self.getTimeSecondsOfDay("On time 1", strOnTime1Hours, strOnTime1Minutes, strOnTime1Seconds) # A call to the getTimeSecondsOfDay method that checks input values from Spinboxes with times and converts the times to seconds of the day. The method returns -1 on error

                if setOnTime1 != -1:
                    lpp.append([101, "addSmallTime", setOnTime1])   # Adding 0 - 86399 seconds of the day to the lpp array
            else:                                                   # On time 1 - Time not set
                lpp.append([101, "addSmallTime", 100000])           # 100000 = Not set


        if self.chOnTime2:                                          # On time 2
            if self.rSetOnTime2:                                    # On time 2 - Set time
                strOnTime2Hours = self.ent46.get()
                strOnTime2Minutes = self.ent47.get()
                strOnTime2Seconds = self.ent48.get()

                setOnTime2 = self.getTimeSecondsOfDay("On time 2", strOnTime2Hours, strOnTime2Minutes, strOnTime2Seconds) # A call to the getTimeSecondsOfDay method that checks input values from Spinboxes with times and converts the times to seconds of the day. The method returns -1 on error

                if setOnTime2 != -1:
                    lpp.append([103, "addSmallTime", setOnTime2])   # Adding 0 - 86399 seconds of the day to the lpp array
            else:                                                   # On time 2 - Time not set
                lpp.append([103, "addSmallTime", 100000])           # 100000 = Not set


        if self.chOnTime3:                                          # On time 3
            if self.rSetOnTime3:                                    # On time 3 - Set time
                strOnTime3Hours = self.ent52.get()
                strOnTime3Minutes = self.ent53.get()
                strOnTime3Seconds = self.ent54.get()

                setOnTime3 = self.getTimeSecondsOfDay("On time 3", strOnTime3Hours, strOnTime3Minutes, strOnTime3Seconds) # A call to the getTimeSecondsOfDay method that checks input values from Spinboxes with times and converts the times to seconds of the day. The method returns -1 on error

                if setOnTime3 != -1:
                    lpp.append([105, "addSmallTime", setOnTime3])   # Adding 0 - 86399 seconds of the day to the lpp array
            else:                                                   # On time 3 - Time not set
                lpp.append([105, "addSmallTime", 100000])           # 100000 = Not set


        if self.chOffTime1:                                         # Off time 1
            if self.rSetOffTime1:                                   # Off time 1 - Set time
                strOffTime1Hours = self.ent58.get()
                strOffTime1Minutes = self.ent59.get()
                strOffTime1Seconds = self.ent60.get()

                setOffTime1 = self.getTimeSecondsOfDay("Off time 1", strOffTime1Hours, strOffTime1Minutes, strOffTime1Seconds) # A call to the getTimeSecondsOfDay method that checks input values from Spinboxes with times and converts the times to seconds of the day. The method returns -1 on error

                if setOffTime1 != -1:
                    lpp.append([102, "addSmallTime", setOffTime1])  # Adding 0 - 86399 seconds of the day to the lpp array
            else:                                                   # Off time 1 - Time not set
                lpp.append([102, "addSmallTime", 100000])           # 100000 = Not set
        

        if self.chOffTime2:                                         # Off time 2
            if self.rSetOffTime2:                                   # Off time 2 - Set time
                strOffTime2Hours = self.ent64.get()
                strOffTime2Minutes = self.ent65.get()
                strOffTime2Seconds = self.ent66.get()

                setOffTime2 = self.getTimeSecondsOfDay("Off time 2", strOffTime2Hours, strOffTime2Minutes, strOffTime2Seconds) # A call to the getTimeSecondsOfDay method that checks input values from Spinboxes with times and converts the times to seconds of the day. The method returns -1 on error

                if setOffTime2 != -1:
                    lpp.append([104, "addSmallTime", setOffTime2])  # Adding 0 - 86399 seconds of the day to the lpp array
            else:                                                   # Off time 2 - Time not set
                lpp.append([104, "addSmallTime", 100000])           # 100000 = Not set


        if self.chOffTime3:                                         # Off time 3
            if self.rSetOffTime3:                                   # Off time 3 - Set time
                strOffTime3Hours = self.ent69.get()
                strOffTime3Minutes = self.ent70.get()
                strOffTime3Seconds = self.ent71.get()

                setOffTime3 = self.getTimeSecondsOfDay("Off time 3", strOffTime3Hours, strOffTime3Minutes, strOffTime3Seconds) # A call to the getTimeSecondsOfDay method that checks input values from Spinboxes with times and converts the times to seconds of the day. The method returns -1 on error.

                if setOffTime3 != -1:
                    lpp.append([106, "addSmallTime", setOffTime3])  # Adding 0 - 86399 seconds of the day to the lpp array
            else:                                                   # Off time 3 - Time not set
                lpp.append([106, "addSmallTime", 100000])           # 100000 = Not set

        self.encodeAndSendDownlink(lpp)                             # Call method for encode lpp and send payload    



    # The following method is called by pressing the Send light intensity settings button
    def downlinkLightIntensity(self):
        lpp = []

        if self.chThreshold:                                            # Light Intensity Threshold
            strthreshold = self.ent34.get()

            if strthreshold != "":                                      # If entry string is not empty  
                try:
                    threshold = int(strthreshold)                       # String to integer conversions

                    if (0 <= threshold) and (threshold <= 65535):       # 0-65535
                        lpp.append([101, "addLuminosity", threshold])   # Adding data to the lpp array
                    else:
                        self.textoutp.delete('1.0', END)
                        self.textoutp.insert("1.0", "Error - Light intensity settings - Threshold out of 0 - 65535 range!")
                        self.error = True
                except:
                    self.textoutp.delete('1.0', END)
                    self.textoutp.insert("1.0", "Error - Light intensity settings - Threshold is not a number!")
                    self.error = True
            else:
                self.textoutp.delete('1.0', END)
                self.textoutp.insert("1.0", "Error - Light intensity settings - Threshold empty entry!")
                self.error = True


        if self.chSafeZone:                                             # Light Intensity Threshold Safe Zone
            strSafeZone = self.ent36.get()

            if strSafeZone != "":                                       # If entry string is not empty  
                try:
                    safeZone = int(strSafeZone)                         # String to integer conversions

                    if (0 <= safeZone) and (safeZone <= 65535):         # 0-65535
                        lpp.append([102, "addLuminosity", safeZone])    # Adding data to the lpp array
                    else:
                        self.textoutp.delete('1.0', END)
                        self.textoutp.insert("1.0", "Error - Light intensity settings - Safe zone out of 0 - 65535 range!")
                        self.error = True
                except:
                    self.textoutp.delete('1.0', END)
                    self.textoutp.insert("1.0", "Error - Light intensity settings - Safe zone is not a number!")
                    self.error = True
            else:
                self.textoutp.delete('1.0', END)
                self.textoutp.insert("1.0", "Error - Light intensity settings - Safe zone empty entry!")
                self.error = True

        self.encodeAndSendDownlink(lpp)                                 # Call method for encode lpp and send payload           



    # The following method is called by pressing the Send sunset / sunrise settings button
    def downlinkSunsetSunrise(self):                            # Device location for sunset / sunrise times
        lpp = []

        strLatitude = self.ent72.get()
        strLongitude = self.ent73.get()

        if (strLatitude != "") and (strLongitude != ""):        # If entry string is not empty 
            try:
                latitude = float(strLatitude)                   # String to float conversions
                longitude = float(strLongitude)

                if ((-90 <= latitude) and (latitude <= 90)) and ((-180 <= longitude) and (longitude <= 180)):       # Check if -90 <= latitude <= 90  and  -180 <= longitude <= 180
                    lpp.append([101, "addGPS", latitude, longitude, 0.0])                                           # Adding data to the lpp array
                else:
                    self.textoutp.delete('1.0', END)
                    self.textoutp.insert("1.0", "Error - Sunset / sunrise settings - Out of -90 <= latitude <= 90  and  -180 <= longitude <= 180 range!")
                    self.error = True
            except:
                self.textoutp.delete('1.0', END)
                self.textoutp.insert("1.0", "Error - Sunset / sunrise settings - Not a Number!")
                self.error = True
        else:
            self.textoutp.delete('1.0', END)
            self.textoutp.insert("1.0", "Error - Sunset / sunrise settings - Empty entry!")
            self.error = True

        self.encodeAndSendDownlink(lpp)                         # Call method for encode lpp and send payload



    # Downlink chexkbox change state - this method is called by checking/unchecking any checkbox in the Downlinks block (except Send only selected) and updating the states of those checkboxes values
    def chDownlinksChange(self):

        if self.chSendDataEveryVar.get():
            self.chSendDataEvery = True
        else:
            self.chSendDataEvery = False

        if self.chNumberOfSamplesVar.get():
            self.chNumberOfSamples = True
        else:
            self.chNumberOfSamples = False

        if self.chPowerGridVar.get():
            self.chPowerGrid = True
        else:
            self.chPowerGrid = False

        if self.chWorkingModeVar.get():
            self.chWorkingMode = True
        else:
            self.chWorkingMode = False

        if self.chTimezoneVar.get():
            self.chTimezone = True
        else:
            self.chTimezone = False

        if self.chResetAndLoadVar.get():
            self.chResetAndLoad = True
        else:
            self.chResetAndLoad = False

        if self.chSendOnlySelectedVar.get():
            self.chSendOnlySelected = True
        else:
            self.chSendOnlySelected = False


        if self.chThresholdVar.get():
            self.chThreshold = True
        else:
            self.chThreshold = False

        if self.chSafeZoneVar.get():
            self.chSafeZone = True
        else:
            self.chSafeZone = False


        if self.chOnTime1Var.get():
            self.chOnTime1 = True
        else:
            self.chOnTime1 = False

        if self.chOnTime2Var.get():
            self.chOnTime2 = True
        else:
            self.chOnTime2 = False

        if self.chOnTime3Var.get():
            self.chOnTime3 = True
        else:
            self.chOnTime3 = False

        if self.chOffTime1Var.get():
            self.chOffTime1 = True
        else:
            self.chOffTime1 = False

        if self.chOffTime2Var.get():
            self.chOffTime2 = True
        else:
            self.chOffTime2 = False

        if self.chOffTime3Var.get():
            self.chOffTime3 = True
        else:
            self.chOffTime3 = False


    # Send only selected chexkbox change state - this method is called by checking/unchecking any checkbox in the Send only selected block and updating the states of all checkboxes values in the Send only selected block
    def chSendOnlySelectedChange(self):

        if self.chRelayStateVar.get():
            self.chRelayState = True
        else:
            self.chRelayState = False

        if self.chNumberOfChangesVar.get():
            self.chNumberOfChanges = True
        else:
            self.chNumberOfChanges = False

        if self.chLightIntensityVar.get():
            self.chLightIntensity = True
        else:
            self.chLightIntensity = False

        if self.chBatteryVoltgeVar.get():
            self.chBatteryVoltge = True
        else:
            self.chBatteryVoltge = False

        if self.chBatteryPercentigeVar.get():
            self.chBatteryPercentige = True
        else:
            self.chBatteryPercentige = False

        if self.chBatteryTemperatureVar.get():
            self.chBatteryTemperature = True
        else:
            self.chBatteryTemperature = False

        if self.chPowerLineVoltageVar.get():
            self.chPowerLineVoltage = True
        else:
            self.chPowerLineVoltage = False

        if self.chPowerLineFrequencyVar.get():
            self.chPowerLineFrequency = True
        else:
            self.chPowerLineFrequency = False

        if self.chActiveEnergyVar.get():
            self.chActiveEnergy = True
        else:
            self.chActiveEnergy = False

        if self.chCurrentVar.get():
            self.chCurrent = True
        else:
            self.chCurrent = False

        if self.chActivePowerVar.get():
            self.chActivePower = True
        else:
            self.chActivePower = False

        if self.chPowerFactorVar.get():
            self.chPowerFactor = True
        else:
            self.chPowerFactor = False

        if self.chRTCTemperatureVar.get():
            self.chRTCTemperature = True
        else:
            self.chRTCTemperature = False

        if self.chSunriseVar.get():
            self.chSunrise = True
        else:
            self.chSunrise = False

        if self.chSunsetVar.get():
            self.chSunset = True
        else:
            self.chSunset = False


    # In this method initialization of variable values to default values is done after the program is started.
    def setInitVars(self):
        #default global variables
        self.fPort = 1                          # FPort variable
        self.confirmedDownlinkVar = IntVar()    # Confirmed downlink variable
        self.confirmedDownlink = False          # True / False
        self.priority = "NORMAL"                # LOWEST / LOW / BELOW_NORMAL / NORMAL / ABOVE_NORMAL / HIGH / HIGHEST
        self.schedule = "REPLACE"               # PUSH / REPLACE

        self.powerGrid = "230"                  # 230 / 400
        self.workingMode = "OFF"                # OFF / ON / Ligh intensity / Time / Ligh intensity in Time /       Sunset / sunrise times
        self.timezone = "UTC"                   # Central European Time / United Kingdom / UTC / US Eastern Time Zone / US Central Time Zone / US Mountain Time Zone / US Arizona / US Pacific Time Zone / Australia Eastern Time Zone
        self.resetAndLoad = "Saved"             # Saved / Default
        
        # Common settings checkboxes values and variables
        self.chSendDataEveryVar = IntVar()
        self.chSendDataEvery = False
        self.chNumberOfSamplesVar = IntVar()
        self.chNumberOfSamples = False
        self.chPowerGridVar = IntVar()
        self.chPowerGrid = False
        self.chWorkingModeVar = IntVar()
        self.chWorkingMode = False
        self.chTimezoneVar = IntVar()
        self.chTimezone = False
        self.chResetAndLoadVar = IntVar()
        self.chResetAndLoad = False
        self.chSendOnlySelectedVar = IntVar()
        self.chSendOnlySelected = False
        
        # Light intensity checkboxes values and variables
        self.chThreshold = False
        self.chThresholdVar = IntVar()
        self.chSafeZone = False
        self.chSafeZoneVar = IntVar()

        # Switching times radio buttons Set/Not set variables
        self.rOnTime1 = StringVar()
        self.rOnTime1.set("notset1") 
        self.rOnTime2 = StringVar()
        self.rOnTime2.set("notset2")
        self.rOnTime3 = StringVar()
        self.rOnTime3.set("notset3")
        self.rOffTime1 = StringVar()
        self.rOffTime1.set("notset1")
        self.rOffTime2 = StringVar()
        self.rOffTime2.set("notset2")
        self.rOffTime3 = StringVar()
        self.rOffTime3.set("notset3")

        # Switching times radio buttons Set/Not set values
        self.rSetOnTime1 = False
        self.rSetOnTime2 = False
        self.rSetOnTime3 = False
        self.rSetOffTime1 = False
        self.rSetOffTime2 = False
        self.rSetOffTime3 = False

        # Switching times checkboxes values and variables
        self.chOnTime1 = False
        self.chOnTime1Var = IntVar()
        self.chOnTime2 = False
        self.chOnTime2Var = IntVar()
        self.chOnTime3 = False
        self.chOnTime3Var = IntVar()
        self.chOffTime1 = False
        self.chOffTime1Var = IntVar()
        self.chOffTime2 = False
        self.chOffTime2Var = IntVar()
        self.chOffTime3 = False
        self.chOffTime3Var = IntVar()


        # Send only selected checkboxes values and variables
        self.chRelayStateVar = IntVar()
        self.chRelayState = True
        self.chNumberOfChangesVar = IntVar()
        self.chNumberOfChanges = True
        self.chLightIntensityVar = IntVar()
        self.chLightIntensity = True

        self.chBatteryVoltgeVar = IntVar()
        self.chBatteryVoltge = True
        self.chBatteryPercentigeVar = IntVar()
        self.chBatteryPercentige = True
        self.chBatteryTemperatureVar = IntVar()
        self.chBatteryTemperature = True

        self.chPowerLineVoltageVar = IntVar()
        self.chPowerLineVoltage = True
        self.chPowerLineFrequencyVar = IntVar()
        self.chPowerLineFrequency = True
        self.chActiveEnergyVar = IntVar()
        self.chActiveEnergy = True

        self.chCurrentVar = IntVar()
        self.chCurrent = True
        self.chActivePowerVar = IntVar()
        self.chActivePower = True
        self.chPowerFactorVar = IntVar()
        self.chPowerFactor = True

        self.chRTCTemperatureVar = IntVar()
        self.chRTCTemperature = True

        self.chSunriseVar = IntVar()
        self.chSunrise = True
        self.chSunsetVar = IntVar()
        self.chSunset = True

        self.error = False



    def __init__(self, root):

        self.setInitVars()                                                      # In this method initialization of variable values to default values is done after the program is started.

        root.title("TTS Multiswitch")                                           # The name of the program window
        root.configure(bg="#64b6f5")                                            # Setting the background color and choosing the font
        self.font = font.Font(size=10, weight="bold")
        self.font2 = font.Font(size=10, weight="normal")
        
        # Below, in the rest of this method, the graphic layout of individual program elements is defined using grids and frames. 
        # It is also defined here which methods will be called when the state of the elements changes or, for example, buttons are pressed.

        self.allOpts = Frame(root, relief=GROOVE, bg="#64b6f5")
        self.allOpts.pack( pady= 10)

        self.opts = LabelFrame(self.allOpts, text="TTS settings", bg="#64b6f5", bd=2, relief=SOLID , font=font.Font(size=11, weight="bold"),  padx=5, pady=5)
        self.opts.grid(row=0, column=0, padx= 10, sticky=W+N+S+E)

        self.lbl1 = Label(self.opts, text="FPort:", bg="#64b6f5", font=self.font)
        self.ent1 = Spinbox(self.opts, from_=1, to=223, width = 10)
        self.lbl1.grid(row=0, column=0, padx=2, pady=2, sticky=W+N+S)
        self.ent1.grid(row=0, column=1, padx=6, pady=2, sticky=W+N+S)

        self.lbl2 = Label(self.opts, text="Confirmed downlink:", bg="#64b6f5", font=self.font)
        self.ent2 = Checkbutton(self.opts, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.confirmedDownlinkVar, command=self.confirmedChange)
        self.lbl2.grid(row=1, column=0, padx=2, pady=2, ipady=10, sticky=W+N+S)
        self.ent2.grid(row=1, column=1, pady=2, sticky=W+N+S)
        
        self.choosePriority = StringVar(self.opts)
        self.choosePriority.set("NORMAL")
        self.lbl3 = Label(self.opts, text="Priority:", bg="#64b6f5", font=self.font)
        self.ent3 = OptionMenu(self.opts, self.choosePriority, "NORMAL", "LOWEST", "LOW", "BELOW_NORMAL", "ABOVE_NORMAL", "HIGH", "HIGHEST", command=self.selectPriority)
        self.lbl3.grid(row=2, column=0, padx=2, pady=2, sticky=W+N+S)
        self.ent3.grid(row=2, column=1, padx=6, pady=2, sticky=W+N+S)

        self.chooseSchedule = StringVar(self.opts)
        self.chooseSchedule.set("REPLACE")
        self.lbl4 = Label(self.opts, text="Insert mode:", bg="#64b6f5", font=self.font)
        self.ent4 = OptionMenu(self.opts, self.chooseSchedule, "REPLACE", "PUSH", command=self.selectInsertMode)
        self.lbl4.grid(row=3, column=0, padx=2, pady=2, sticky=W+N+S)
        self.ent4.grid(row=3, column=1, padx=6, pady=2, sticky=W+N+S)



        self.opts2 = LabelFrame(self.allOpts, text="End device", bg="#64b6f5", bd=2, relief=SOLID , font=font.Font(size=11, weight="bold"),  padx=5, pady=5)
        self.opts2.grid(row=0, column=1, padx= 10, sticky=W+N+S+E)

        self.lbl5 = Label(self.opts2, text="API key:", bg="#64b6f5", font=self.font)
        self.ent5 = Entry(self.opts2, width=15, font=self.font2, show="*")
        self.ent5.delete(0, END)
        try:
            self.ent5.insert(0,str(secrets.APIKey))
        except:
            print("Exception - No API Key in secrets")
        self.lbl5.grid(row=0, column=0, padx=2, pady=5, sticky=W+N+S)
        self.ent5.grid(row=0, column=1, padx=6, pady=5, sticky=W+N+S)

        self.lbl6 = Label(self.opts2, text="Application name:", bg="#64b6f5", font=self.font)
        self.ent6 = Entry(self.opts2, width=15, font=self.font2)
        self.ent6.delete(0, END)
        try:
            self.ent6.insert(0,str(secrets.applicationName))
        except:
            print("Exception - No Applicatin name in secrets")
        self.lbl6.grid(row=1, column=0, padx=2, pady=5, sticky=W+N+S)
        self.ent6.grid(row=1, column=1, padx=6, pady=5, sticky=W+N+S)

        self.lbl7 = Label(self.opts2, text="End device name:", bg="#64b6f5", font=self.font)
        self.ent7 = Entry(self.opts2, width=15, font=self.font2)
        self.ent7.delete(0, END)
        try:
            self.ent7.insert(0,str(secrets.endDeviceName))
        except:
            print("Exception - No End device name in secrets")
        self.lbl7.grid(row=2, column=0, padx=2, pady=5, sticky=W+N+S)
        self.ent7.grid(row=2, column=1, padx=6, pady=5, sticky=W+N+S)

        self.btn1 = Button(self.opts2, text="Save", bg="#fcaa2d", width=10, height=1, font=self.font, command=self.saveEndSettings)
        self.btn1.grid(row=3, column=0, columnspan=2, padx=5, pady=9, sticky=W+N+S+E)



        self.opts4 = LabelFrame(self.allOpts, text="Operational information", bg="#64b6f5", bd=2, relief=SOLID , font=font.Font(size=11, weight="bold"),  padx=5, pady=5)
        self.opts4.grid(row=0, column=2, padx= 10, sticky=W+N+S+E)

        self.textoutp = Text(self.opts4, height = 9, width = 82, font=self.font2)
        self.textoutp.pack()



        self.allOpts2 = Frame(root, relief=GROOVE, bg="#64b6f5")
        self.allOpts2.pack()

        self.opts3 = LabelFrame(self.allOpts2, text="Downlinks", bg="#64b6f5", bd=2, relief=SOLID , font=font.Font(size=11, weight="bold"),  padx=5, pady=5)
        self.opts3.pack(side=BOTTOM, padx=5, pady=5)

        self.lbl8 = Label(self.opts3, text="Settings password:", bg="#64b6f5", font=self.font)
        self.ent8 = Entry(self.opts3, width=8, font=self.font2, show="*")
        self.ent8.delete(0, END)
        self.lbl8.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky=N+S+E)
        self.ent8.grid(row=0, column=3, columnspan=2, padx=0, pady=40, sticky=W+N+S)


        self.opts31 = LabelFrame(self.opts3, text="Common settings", bg="#64b6f5", bd=1, relief=SOLID , font=font.Font(size=10, weight="bold"),  padx=5, pady=5)
        self.opts31.grid(row=1, column=1, columnspan=4, rowspan=8,  padx=5, pady=5, sticky=N+S+E+W)
        
        self.ent9 = Checkbutton(self.opts31, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chSendDataEveryVar, command=self.chDownlinksChange)
        self.lbl9 = Label(self.opts31, text="Send data every [s]:", bg="#64b6f5", font=self.font)
        self.ent10 = Spinbox(self.opts31, from_=60, to=3600, width = 8)
        self.ent9.grid(row=0, column=0, pady=2, sticky=E+N+S)
        self.lbl9.grid(row=0, column=1, padx=0, pady=5, sticky=W+N+S)
        self.ent10.grid(row=0, column=2, padx=15, pady=6, sticky=W+N+S)


        self.ent11 = Checkbutton(self.opts31, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chNumberOfSamplesVar, command=self.chDownlinksChange)
        self.lbl10 = Label(self.opts31, text="Number of samples:", bg="#64b6f5", font=self.font)
        self.ent12 = Spinbox(self.opts31, from_=1, to=10, width = 8)
        self.ent11.grid(row=1, column=0, pady=2, sticky=W+N+S)
        self.lbl10.grid(row=1, column=1, padx=0, pady=5, sticky=W+N+S)
        self.ent12.grid(row=1, column=2, padx=15, pady=6, sticky=W+N+S)


        self.ent17 = Checkbutton(self.opts31, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chPowerGridVar, command=self.chDownlinksChange)
        self.choosePowerGrid= StringVar(self.opts)
        self.choosePowerGrid.set("230")                  # standard value
        self.lbl13 = Label(self.opts31, text="Power grid [V]:", bg="#64b6f5", font=self.font)
        self.ent18 = OptionMenu(self.opts31, self.choosePowerGrid, "230", "400", command=self.selectPowerGrid)
        self.ent17.grid(row=2, column=0, pady=2, sticky=W+N+S)
        self.lbl13.grid(row=2, column=1, padx=0, pady=5, sticky=W+N+S)
        self.ent18.grid(row=2, column=2, padx=15, pady=6, sticky=W+N+S)


        self.ent13 = Checkbutton(self.opts31, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chWorkingModeVar, command=self.chDownlinksChange)
        self.chooseWorkingMode = StringVar(self.opts)
        self.chooseWorkingMode.set("OFF")
        self.lbl11 = Label(self.opts31, text="Working mode:", bg="#64b6f5", font=self.font)
        self.ent14 = OptionMenu(self.opts31, self.chooseWorkingMode, "OFF", "ON", "Ligh intensity", "Time", "Ligh intensity in Time", "Sunset / sunrise times", command=self.selectWorkingMode)
        self.ent13.grid(row=0, column=3, pady=2, sticky=W+N+S)
        self.lbl11.grid(row=0, column=4, padx=0, pady=5, sticky=W+N+S)
        self.ent14.grid(row=0, column=5, padx=6, pady=4, sticky=W+N+S)


        self.ent15 = Checkbutton(self.opts31, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chTimezoneVar, command=self.chDownlinksChange)
        self.chooseTimezone = StringVar(self.opts)
        self.chooseTimezone.set("UTC")
        self.lbl12 = Label(self.opts31, text="Timezone:", bg="#64b6f5", font=self.font)
        self.ent16 = OptionMenu(self.opts31, self.chooseTimezone, "Central European Time", "United Kingdom", "UTC", "US Eastern Time Zone", "US Central Time Zone", "US Mountain Time Zone", "US Arizona", "US Pacific Time Zone", "Australia Eastern Time Zone", command=self.selectTimezone)
        self.ent15.grid(row=1, column=3, pady=2, sticky=W+N+S)
        self.lbl12.grid(row=1, column=4, padx=0, pady=5, sticky=W+N+S)
        self.ent16.grid(row=1, column=5, padx=6, pady=4, sticky=W+N+S)


        self.ent19 = Checkbutton(self.opts31, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chResetAndLoadVar, command=self.chDownlinksChange)
        self.chooseReset = StringVar(self.opts)
        self.chooseReset.set("Saved")
        self.lbl14 = Label(self.opts31, text="Reset and load:", bg="#64b6f5", font=self.font)
        self.ent20 = OptionMenu(self.opts31, self.chooseReset, "Saved", "Default", command=self.selectResetAndLoad)
        self.ent19.grid(row=2, column=3, pady=2, sticky=W+N+S)
        self.lbl14.grid(row=2, column=4, padx=2, pady=5, sticky=W+N+S)
        self.ent20.grid(row=2, column=5, padx=6, pady=6, sticky=W+N+S)


        self.ent21 = Checkbutton(self.opts31, bg="#64b6f5", variable=self.chSendOnlySelectedVar, command=self.chDownlinksChange)
        self.opts311 = LabelFrame(self.opts31, text="Send only selected", bg="#64b6f5", bd=1, relief=SOLID , font=font.Font(size=10, weight="bold"),  padx=5, pady=5)
        self.ent21.grid(row=3, column=0, pady=2, sticky=W+N+S)
        self.opts311.grid(row=3, column=1, columnspan=5, padx=5, pady=5, sticky=N+S+E)

        self.ent22 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chRelayStateVar, command=self.chSendOnlySelectedChange)
        self.ent22.select()                                                                # check the checkbox  
        self.lbl15 = Label(self.opts311, text="Relay state", bg="#64b6f5", font=self.font)
        self.ent22.grid(row=0, column=0, pady=2, sticky=E+N+S)
        self.lbl15.grid(row=0, column=1, padx=0, pady=5, sticky=W+N+S)
        
        self.ent23 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chNumberOfChangesVar, command=self.chSendOnlySelectedChange)
        self.ent23.select() 
        self.lbl16 = Label(self.opts311, text="Number of changes", bg="#64b6f5", font=self.font)
        self.ent23.grid(row=0, column=2, pady=2, sticky=E+N+S)
        self.lbl16.grid(row=0, column=3, padx=0, pady=5, sticky=W+N+S)

        self.ent24 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chLightIntensityVar, command=self.chSendOnlySelectedChange)
        self.ent24.select() 
        self.lbl17 = Label(self.opts311, text="Light intensity", bg="#64b6f5", font=self.font)
        self.ent24.grid(row=0, column=4, padx=0, pady=2, sticky=E+N+S)
        self.lbl17.grid(row=0, column=5, padx=0, pady=5, sticky=W+N+S)


        self.ent25 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chBatteryVoltgeVar, command=self.chSendOnlySelectedChange)
        self.ent25.select()
        self.lbl18 = Label(self.opts311, text="Battery voltage", bg="#64b6f5", font=self.font)
        self.ent25.grid(row=1, column=0, pady=2, sticky=E+N+S)
        self.lbl18.grid(row=1, column=1, padx=0, pady=5, sticky=W+N+S)
        
        self.ent26 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chBatteryPercentigeVar, command=self.chSendOnlySelectedChange)
        self.ent26.select()
        self.lbl19 = Label(self.opts311, text="Battery percentage", bg="#64b6f5", font=self.font)
        self.ent26.grid(row=1, column=2, pady=2, sticky=E+N+S)
        self.lbl19.grid(row=1, column=3, padx=0, pady=5, sticky=W+N+S)

        self.ent26 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chBatteryTemperatureVar, command=self.chSendOnlySelectedChange)
        self.ent26.select()
        self.lbl20 = Label(self.opts311, text="Battery temperature", bg="#64b6f5", font=self.font)
        self.ent26.grid(row=1, column=4, padx=0, pady=2, sticky=E+N+S)
        self.lbl20.grid(row=1, column=5, padx=0, pady=5, sticky=W+N+S)


        self.ent74 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chRTCTemperatureVar, command=self.chSendOnlySelectedChange)
        self.ent74.select()
        self.lbl60 = Label(self.opts311, text="RTC temperature", bg="#64b6f5", font=self.font)
        self.ent74.grid(row=2, column=0, pady=2, sticky=E+N+S)
        self.lbl60.grid(row=2, column=1, padx=0, pady=5, sticky=W+N+S)

        self.ent27 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chPowerLineVoltageVar, command=self.chSendOnlySelectedChange)
        self.ent27.select()
        self.lbl21 = Label(self.opts311, text="Power line voltage", bg="#64b6f5", font=self.font)
        self.ent27.grid(row=2, column=2, pady=2, sticky=E+N+S)
        self.lbl21.grid(row=2, column=3, padx=0, pady=5, sticky=W+N+S)
        
        self.ent28 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chPowerLineFrequencyVar, command=self.chSendOnlySelectedChange)
        self.ent28.select()
        self.lbl22 = Label(self.opts311, text="Power line frequency", bg="#64b6f5", font=self.font)
        self.ent28.grid(row=2, column=4, pady=0, sticky=E+N+S)
        self.lbl22.grid(row=2, column=5, padx=0, pady=5, sticky=W+N+S)


        self.ent29 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chActiveEnergyVar, command=self.chSendOnlySelectedChange)
        self.ent29.select()
        self.lbl23 = Label(self.opts311, text="Active energy", bg="#64b6f5", font=self.font)
        self.ent29.grid(row=3, column=0, pady=2, sticky=E+N+S)
        self.lbl23.grid(row=3, column=1, padx=0, pady=5, sticky=W+N+S)

        self.ent30 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chCurrentVar, command=self.chSendOnlySelectedChange)
        self.ent30.select()
        self.lbl24 = Label(self.opts311, text="Current", bg="#64b6f5", font=self.font)
        self.ent30.grid(row=3, column=2, pady=2, sticky=E+N+S)
        self.lbl24.grid(row=3, column=3, padx=0, pady=5, sticky=W+N+S)
        
        self.ent31 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chActivePowerVar, command=self.chSendOnlySelectedChange)
        self.ent31.select()
        self.lbl25 = Label(self.opts311, text="Active power", bg="#64b6f5", font=self.font)
        self.ent31.grid(row=3, column=4, pady=2, sticky=E+N+S)
        self.lbl25.grid(row=3, column=5, padx=0, pady=5, sticky=W+N+S)


        self.ent32 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chPowerFactorVar, command=self.chSendOnlySelectedChange)
        self.ent32.select()
        self.lbl26 = Label(self.opts311, text="Power factor", bg="#64b6f5", font=self.font)
        self.ent32.grid(row=4, column=0, padx=0, pady=2, sticky=E+N+S)
        self.lbl26.grid(row=4, column=1, padx=0, pady=5, sticky=W+N+S)

        self.ent100 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chSunriseVar, command=self.chSendOnlySelectedChange)
        self.ent100.select()
        self.lbl100 = Label(self.opts311, text="Sunrise", bg="#64b6f5", font=self.font)
        self.ent100.grid(row=4, column=2, pady=2, sticky=E+N+S)
        self.lbl100.grid(row=4, column=3, padx=0, pady=5, sticky=W+N+S)
        
        self.ent101 = Checkbutton(self.opts311, bg="#64b6f5", variable=self.chSunsetVar, command=self.chSendOnlySelectedChange)
        self.ent101.select()
        self.lbl101 = Label(self.opts311, text="Sunset", bg="#64b6f5", font=self.font)
        self.ent101.grid(row=4, column=4, pady=2, sticky=E+N+S)
        self.lbl101.grid(row=4, column=5, padx=0, pady=5, sticky=W+N+S)


        self.btn2 = Button(self.opts31, text="Send common settings", bg="#fcaa2d", height=1, font=self.font, command=self.downlinkCommon)
        self.btn2.grid(row=5, column=0, columnspan=6, padx=5, pady=5, sticky=W+N+S+E)




        self.opts32 = LabelFrame(self.opts3, text="Light intensity settings", bg="#64b6f5", bd=1, relief=SOLID , font=font.Font(size=10, weight="bold"),  padx=5, pady=5)
        self.opts32.grid(row=0, column=5, columnspan=4, padx=20, pady=7, sticky=N+S+E+W)
        
        self.ent33 = Checkbutton(self.opts32, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chThresholdVar, command=self.chDownlinksChange)
        self.lbl27 = Label(self.opts32, text="Threshold [lux]:", bg="#64b6f5", font=self.font)
        self.ent34 = Spinbox(self.opts32, from_=0, to=65535, width = 8)
        self.ent33.grid(row=0, column=0, pady=2, sticky=E+N+S)
        self.lbl27.grid(row=0, column=1, padx=0, pady=5, sticky=W+N+S)
        self.ent34.grid(row=0, column=2, padx=15, pady=6, sticky=W+N+S)

        self.ent35 = Checkbutton(self.opts32, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chSafeZoneVar, command=self.chDownlinksChange)
        self.lbl28 = Label(self.opts32, text="Safe zone [lux]:", bg="#64b6f5", font=self.font)
        self.ent36 = Spinbox(self.opts32, from_=0, to=65535, width = 8)
        self.ent35.grid(row=0, column=4, pady=2, sticky=E+N+S)
        self.lbl28.grid(row=0, column=5, padx=0, pady=5, sticky=E+N+S)
        self.ent36.grid(row=0, column=6, padx=15, pady=6, sticky=E+N+S)

        self.lbl29 = Label(self.opts32, text="                     ", bg="#64b6f5", font=self.font)
        self.lbl29.grid(row=0, column=3, padx=0, pady=5, sticky=E+N+S)

        self.btn3 = Button(self.opts32, text="Send light intensity settings", bg="#fcaa2d", height=1, font=self.font, command=self.downlinkLightIntensity)
        self.btn3.grid(row=4, column=0, columnspan=7, padx=5, pady=1, sticky=W+N+S+E)



        self.opts33 = LabelFrame(self.opts3, text="Switching times settings", bg="#64b6f5", bd=1, relief=SOLID , font=font.Font(size=10, weight="bold"),  padx=5, pady=5)
        self.opts33.grid(row=2, column=5, columnspan=4, padx=20, pady=5, sticky=N+S+E+W)
        

        self.ent37 = Checkbutton(self.opts33, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chOnTime1Var, command=self.chDownlinksChange)
        self.lbl30 = Label(self.opts33, text="On time 1:", bg="#64b6f5", font=self.font)
        self.ent37.grid(row=0, column=0, pady=2, sticky=E+N+S)
        self.lbl30.grid(row=0, column=1, padx=0, pady=5, sticky=W+N+S)

        self.ent38 = Radiobutton(self.opts33, text="Time not set", bg="#64b6f5", font=self.font2, value="notset1", variable=self.rOnTime1, command=self.rOnTime1NotChange)
        self.ent38.grid(row=0, column=2, padx=25, pady=2, sticky=W+N+S)

        self.lbl31 = Label(self.opts33, text="          ", bg="#64b6f5", font=self.font)
        self.lbl31.grid(row=0, column=3, padx=0, pady=5, sticky=W+N+S)

        self.ent39 = Radiobutton(self.opts33, text="Set time", bg="#64b6f5", font=self.font2, value="set1", variable=self.rOnTime1, command=self.rOnTime1SetChange)
        self.ent39.grid(row=0, column=4, padx=2, pady=2, sticky=W+N+S)

        self.ent40 = Spinbox(self.opts33, from_=0, to=23, width = 3)
        self.lbl32 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent41 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        self.lbl33 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent42 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        
        self.ent40.grid(row=0, column=5, padx=5, pady=6, sticky=W+N+S)
        self.lbl32.grid(row=0, column=6, padx=0, pady=5, sticky=W+N+S)
        self.ent41.grid(row=0, column=7, padx=5, pady=6, sticky=W+N+S)
        self.lbl33.grid(row=0, column=8, padx=0, pady=5, sticky=W+N+S)
        self.ent42.grid(row=0, column=9, padx=5, pady=6, sticky=W+N+S)


        self.ent43 = Checkbutton(self.opts33, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chOnTime2Var, command=self.chDownlinksChange)
        self.lbl34 = Label(self.opts33, text="On time 2:", bg="#64b6f5", font=self.font)
        self.ent43.grid(row=1, column=0, pady=2, sticky=E+N+S)
        self.lbl34.grid(row=1, column=1, padx=0, pady=5, sticky=W+N+S)

        self.ent44 = Radiobutton(self.opts33, text="Time not set", bg="#64b6f5", font=self.font2, value="notset2", variable=self.rOnTime2, command=self.rOnTime2NotChange)
        self.ent44.grid(row=1, column=2, padx=25, pady=2, sticky=W+N+S)

        self.lbl35 = Label(self.opts33, text="          ", bg="#64b6f5", font=self.font)
        self.lbl35.grid(row=1, column=3, padx=0, pady=5, sticky=W+N+S)

        self.ent45 = Radiobutton(self.opts33, text="Set time", bg="#64b6f5", font=self.font2, value="set2", variable=self.rOnTime2, command=self.rOnTime2SetChange)
        self.ent45.grid(row=1, column=4, padx=2, pady=2, sticky=W+N+S)

        self.ent46 = Spinbox(self.opts33, from_=0, to=23, width = 3)
        self.lbl36 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent47 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        self.lbl37 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent48 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        
        self.ent46.grid(row=1, column=5, padx=5, pady=6, sticky=W+N+S)
        self.lbl36.grid(row=1, column=6, padx=0, pady=5, sticky=W+N+S)
        self.ent47.grid(row=1, column=7, padx=5, pady=6, sticky=W+N+S)
        self.lbl37.grid(row=1, column=8, padx=0, pady=5, sticky=W+N+S)
        self.ent48.grid(row=1, column=9, padx=5, pady=6, sticky=W+N+S)


        self.ent49 = Checkbutton(self.opts33, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chOnTime3Var, command=self.chDownlinksChange)
        self.lbl38 = Label(self.opts33, text="On time 3:", bg="#64b6f5", font=self.font)
        self.ent49.grid(row=3, column=0, pady=2, sticky=E+N+S)
        self.lbl38.grid(row=3, column=1, padx=0, pady=5, sticky=W+N+S)

        self.ent50 = Radiobutton(self.opts33, text="Time not set", bg="#64b6f5", font=self.font2, value="notset3", variable=self.rOnTime3, command=self.rOnTime3NotChange)
        self.ent50.grid(row=3, column=2, padx=25, pady=2, sticky=W+N+S)

        self.lbl39 = Label(self.opts33, text="          ", bg="#64b6f5", font=self.font)
        self.lbl39.grid(row=3, column=3, padx=0, pady=5, sticky=W+N+S)

        self.ent51 = Radiobutton(self.opts33, text="Set time", bg="#64b6f5", font=self.font2, value="set3", variable=self.rOnTime3, command=self.rOnTime3SetChange)
        self.ent51.grid(row=3, column=4, padx=2, pady=2, sticky=W+N+S)

        self.ent52 = Spinbox(self.opts33, from_=0, to=23, width = 3)
        self.lbl40 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent53 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        self.lbl41 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent54 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        
        self.ent52.grid(row=3, column=5, padx=5, pady=6, sticky=W+N+S)
        self.lbl40.grid(row=3, column=6, padx=0, pady=5, sticky=W+N+S)
        self.ent53.grid(row=3, column=7, padx=5, pady=6, sticky=W+N+S)
        self.lbl41.grid(row=3, column=8, padx=0, pady=5, sticky=W+N+S)
        self.ent54.grid(row=3, column=9, padx=5, pady=6, sticky=W+N+S)


        self.lbl42 = Label(self.opts33, text="", bg="#64b6f5", font=self.font)
        self.lbl42.grid(row=4, column=0, padx=0, pady=0, sticky=W+N+S)



        self.ent55 = Checkbutton(self.opts33, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chOffTime1Var, command=self.chDownlinksChange)
        self.lbl43 = Label(self.opts33, text="Off time 1:", bg="#64b6f5", font=self.font)
        self.ent55.grid(row=5, column=0, pady=2, sticky=E+N+S)
        self.lbl43.grid(row=5, column=1, padx=0, pady=5, sticky=W+N+S)

        self.ent56 = Radiobutton(self.opts33, text="Time not set", bg="#64b6f5", font=self.font2, value="notset1", variable=self.rOffTime1, command=self.rOffTime1NotChange)
        self.ent56.grid(row=5, column=2, padx=25, pady=2, sticky=W+N+S)

        self.lbl44 = Label(self.opts33, text="          ", bg="#64b6f5", font=self.font)
        self.lbl44.grid(row=5, column=3, padx=0, pady=5, sticky=W+N+S)

        self.ent57 = Radiobutton(self.opts33, text="Set time", bg="#64b6f5", font=self.font2, value="set1", variable=self.rOffTime1, command=self.rOffTime1SetChange)
        self.ent57.grid(row=5, column=4, padx=2, pady=2, sticky=W+N+S)

        self.ent58 = Spinbox(self.opts33, from_=0, to=23, width = 3)
        self.lbl45 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent59 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        self.lbl46 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent60 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        
        self.ent58.grid(row=5, column=5, padx=5, pady=6, sticky=W+N+S)
        self.lbl45.grid(row=5, column=6, padx=0, pady=5, sticky=W+N+S)
        self.ent59.grid(row=5, column=7, padx=5, pady=6, sticky=W+N+S)
        self.lbl46.grid(row=5, column=8, padx=0, pady=5, sticky=W+N+S)
        self.ent60.grid(row=5, column=9, padx=5, pady=6, sticky=W+N+S)


        self.ent61 = Checkbutton(self.opts33, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chOffTime2Var, command=self.chDownlinksChange)
        self.lbl47 = Label(self.opts33, text="Off time 2:", bg="#64b6f5", font=self.font)
        self.ent61.grid(row=6, column=0, pady=2, sticky=E+N+S)
        self.lbl47.grid(row=6, column=1, padx=0, pady=5, sticky=W+N+S)

        self.ent62 = Radiobutton(self.opts33, text="Time not set", bg="#64b6f5", font=self.font2, value="notset2", variable=self.rOffTime2, command=self.rOffTime2NotChange)
        self.ent62.grid(row=6, column=2, padx=25, pady=2, sticky=W+N+S)

        self.lbl48 = Label(self.opts33, text="          ", bg="#64b6f5", font=self.font)
        self.lbl48.grid(row=6, column=3, padx=0, pady=5, sticky=W+N+S)

        self.ent63 = Radiobutton(self.opts33, text="Set time", bg="#64b6f5", font=self.font2, value="set2", variable=self.rOffTime2, command=self.rOffTime2SetChange)
        self.ent63.grid(row=6, column=4, padx=2, pady=2, sticky=W+N+S)

        self.ent64 = Spinbox(self.opts33, from_=0, to=23, width = 3)
        self.lbl49 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent65 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        self.lbl50 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent66 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        
        self.ent64.grid(row=6, column=5, padx=5, pady=6, sticky=W+N+S)
        self.lbl49.grid(row=6, column=6, padx=0, pady=5, sticky=W+N+S)
        self.ent65.grid(row=6, column=7, padx=5, pady=6, sticky=W+N+S)
        self.lbl50.grid(row=6, column=8, padx=0, pady=5, sticky=W+N+S)
        self.ent66.grid(row=6, column=9, padx=5, pady=6, sticky=W+N+S)


        self.ent67 = Checkbutton(self.opts33, bg="#64b6f5", highlightcolor="#64b6f5", variable=self.chOffTime3Var, command=self.chDownlinksChange)
        self.lbl51 = Label(self.opts33, text="Off time 3:", bg="#64b6f5", font=self.font)
        self.ent67.grid(row=7, column=0, pady=2, sticky=E+N+S)
        self.lbl51.grid(row=7, column=1, padx=0, pady=5, sticky=W+N+S)

        self.ent68 = Radiobutton(self.opts33, text="Time not set", bg="#64b6f5", font=self.font2, value="notset3", variable=self.rOffTime3, command=self.rOffTime3NotChange)
        self.ent68.grid(row=7, column=2, padx=25, pady=2, sticky=W+N+S)

        self.lbl52 = Label(self.opts33, text="          ", bg="#64b6f5", font=self.font)
        self.lbl52.grid(row=7, column=3, padx=0, pady=5, sticky=W+N+S)

        self.ent68 = Radiobutton(self.opts33, text="Set time", bg="#64b6f5", font=self.font2, value="set3", variable=self.rOffTime3, command=self.rOffTime3SetChange)
        self.ent68.grid(row=7, column=4, padx=2, pady=2, sticky=W+N+S)

        self.ent69 = Spinbox(self.opts33, from_=0, to=23, width = 3)
        self.lbl53 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent70 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        self.lbl54 = Label(self.opts33, text=":", bg="#64b6f5", font=self.font)
        self.ent71 = Spinbox(self.opts33, from_=0, to=59, width = 3)
        
        self.ent69.grid(row=7, column=5, padx=5, pady=6, sticky=W+N+S)
        self.lbl53.grid(row=7, column=6, padx=0, pady=5, sticky=W+N+S)
        self.ent70.grid(row=7, column=7, padx=5, pady=6, sticky=W+N+S)
        self.lbl54.grid(row=7, column=8, padx=0, pady=5, sticky=W+N+S)
        self.ent71.grid(row=7, column=9, padx=5, pady=6, sticky=W+N+S)


        self.btn4 = Button(self.opts33, text="Send switching times settings", bg="#fcaa2d", height=1, font=self.font, command=self.downlinkSwitchingTimes)
        self.btn4.grid(row=8, column=0, columnspan=15, padx=5, pady=5, sticky=W+N+S+E)



        self.opts34 = LabelFrame(self.opts3, text="Sunset / sunrise settings", bg="#64b6f5", bd=1, relief=SOLID , font=font.Font(size=10, weight="bold"),  padx=5, pady=5)
        self.opts34.grid(row=3, column=5, columnspan=4, padx=20, pady=5, ipady=2, sticky=N+S+E+W)

        self.lbl55 = Label(self.opts34, text="        ", bg="#64b6f5", font=self.font)
        self.lbl55.grid(row=0, column=0, padx=0, pady=5, sticky=W+N+S)
        
        self.lbl56 = Label(self.opts34, text="Latitude:", bg="#64b6f5", font=self.font)
        self.ent72 = Entry(self.opts34, width=10, font=self.font2)
        self.ent72.delete(0, END)
        self.ent72.insert(0,str(49.8305572))        
        self.lbl56.grid(row=0, column=1, padx=0, pady=5, sticky=W+N+S)
        self.ent72.grid(row=0, column=2, padx=15, pady=6, sticky=W+N+S)


        self.lbl57 = Label(self.opts34, text="                           ", bg="#64b6f5", font=self.font)
        self.lbl57.grid(row=0, column=3, padx=0, pady=5, sticky=E+N+S)


        self.lbl58 = Label(self.opts34, text="Longitude:", bg="#64b6f5", font=self.font)
        self.ent73 = Entry(self.opts34, width=10, font=self.font2)
        self.ent73.delete(0, END)
        self.ent73.insert(0,str(18.1605611))        
        self.lbl58.grid(row=0, column=4, padx=0, pady=5, sticky=W+N+S)
        self.ent73.grid(row=0, column=5, padx=15, pady=6, sticky=W+N+S)

        self.lbl59 = Label(self.opts34, text="        ", bg="#64b6f5", font=self.font)
        self.lbl59.grid(row=0, column=6, padx=0, pady=5, sticky=W+N+S)

        self.btn5 = Button(self.opts34, text="Send sunset / sunrise settings", bg="#fcaa2d", height=1, font=self.font, command=self.downlinkSunsetSunrise)
        self.btn5.grid(row=1, column=0, columnspan=7, padx=5, pady=1, sticky=W+N+S+E)


root = Tk()                             # Creating the main program window
app = MyApp(root)                       # Defining the program, the root window passed to the class as a parameter
root.mainloop()                         # The main event-handling and GUI-updating loop that runs until the user exits the program