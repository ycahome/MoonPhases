"""
MoonPhases Plugin

Author: Ycahome, 2017 CREDITS TO jackslayter

Version:    1.0.0: Initial Release
Version:    1.0.1: Southern hemisphere moon images
Version:    1.0.4: Changed icon/zip names to avoid underscores - something fishy in domoticz images or the python api

"""

"""
<plugin key="MoonPhases" name="Moon Phases" author="ycahome ft. jackslayter"
  version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/"
  externallink="http://www.domoticz.com/forum/viewtopic.php?f=65&t=21993">
     <description>
        <h3>----------------------------------------------------------------------</h3>
        <h2>Moon Phases v.1.0.5</h2><br/>
        <h3>----------------------------------------------------------------------</h3>
     </description>
     <params>
        <param field="Mode1" label="WU Key" width="200px" required="true" default="your_Wunderground_key"/>
        <param field="Mode2" label="CountryCode" width="100px" required="true" default="au"/>
        <param field="Mode3" label="City" width="300px" required="true" default="sydney"/>
        <param field="Mode4" label="Polling interval (minutes)" width="40px" required="true" default="60"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="True" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import urllib.request
import json
from datetime import datetime
from datetime import timedelta


icons = {"MoonPhases1NM": "MoonPhases1NM.zip",
         "MoonPhases2WC": "MoonPhases2WC.zip",
         "MoonPhases3FQ": "MoonPhases3FQ.zip",
         "MoonPhases4WG": "MoonPhases4WG.zip",
         "MoonPhases5FM": "MoonPhases5FM.zip",
         "MoonPhases6WG": "MoonPhases6WG.zip",
         "MoonPhases7LQ": "MoonPhases7LQ.zip",
         "MoonPhases8WC": "MoonPhases8WC.zip",
         "MoonPhases1NMSH": "MoonPhases1NMSH.zip",
         "MoonPhases2WCSH": "MoonPhases2WCSH.zip",
         "MoonPhases3FQSH": "MoonPhases3FQSH.zip",
         "MoonPhases4WGSH": "MoonPhases4WGSH.zip",
         "MoonPhases5FMSH": "MoonPhases5FMSH.zip",
         "MoonPhases6WGSH": "MoonPhases6WGSH.zip",
         "MoonPhases7LQSH": "MoonPhases7LQSH.zip",
         "MoonPhases8WCSH": "MoonPhases8WCSH.zip"}


class BasePlugin:

    def __init__(self):
        self.debug = False
        self.nextupdate = datetime.now()
        self.pollinterval = 60  # default polling interval in minutes
        self.error = False
        self.southern_hemi = False
        self.suffix= 'SH'
        self.reload = True
        return

    def onStart(self):
        Domoticz.Debug("onStart called")
        global icons
        if Parameters["Mode6"] == 'Debug':
            self.debug = True
            Domoticz.Debugging(1)
            DumpConfigToLog()
        else:
            Domoticz.Debugging(0)

        # load custom MoonPhase images
        for key, value in icons.items():
            if key not in Images:
                Domoticz.Image(value).Create()
                Domoticz.Debug("Added icon: " + key + " from file " + value)
        Domoticz.Debug("Number of icons loaded = " + str(len(Images)))
        for image in Images:
            Domoticz.Debug("Icon " + str(Images[image].ID) + " " + Images[image].Name)
        # create the mandatory child device if it does not yet exist
        if 1 not in Devices:
            Domoticz.Device(Name="Status", Unit=1, TypeName="Custom",Options={"Custom": "1;Days"},Used=1).Create()
        # check polling interval parameter
        try:
            temp = int(Parameters["Mode4"])
        except:
            Domoticz.Error("Invalid polling interval parameter")
        else:
            if temp < 60:
                temp = 60  # minimum polling interval
                Domoticz.Error("Specified polling interval too short: changed to 60 minutes")
            elif temp > 1440:
                temp = 1440  # maximum polling interval is 1 day
                Domoticz.Error("Specified polling interval too long: changed to 1440 minutes (24 hours)")
            self.pollinterval = temp
        Domoticz.Log("Using polling interval of {} minutes".format(str(self.pollinterval)))

    def onStop(self):
        Domoticz.Debug("onStop called")
        Domoticz.Debugging(0)

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        now = datetime.now()
        if now >= self.nextupdate:
            self.nextupdate = now + timedelta(minutes=self.pollinterval)
            u =  "http://api.wunderground.com/api/%s/astronomy/q/%s/%s.json"  % (Parameters["Mode1"],Parameters["Mode2"],Parameters["Mode3"])
            Domoticz.Debug('Moon URL:%s' % u)
            data = json.loads(urllib.request.urlopen(u).read().decode('ascii'))
            lune = data['moon_phase']['phaseofMoon'].rstrip()
            luneage = data['moon_phase']['ageOfMoon'].strip()
            self.southern_hemi = (data['moon_phase']['hemisphere'].rstrip() == "South")
            Domoticz.Log("Moon Phase:"+str(lune))
            Domoticz.Log("Moon Age:"+str(luneage))
            self.UpdateDevice(lune,luneage)



    def UpdateDevice(self, lune, luneage):
        Domoticz.Debug("UpdateDevice called")
        # Make sure that the Domoticz device still exists (they can be deleted) before updating it
        datafr = ""
        if 1 in Devices:
            if lune == "New Moon":
                datafr = "MoonPhases1NM"
                phase = 1
            elif lune == "Waxing Crescent":
                datafr = "MoonPhases2WC"
                phase = 2
            elif lune == "First Quarter":
                datafr = "MoonPhases3FQ"
                phase = 3
            elif lune == "Waxing Gibbous":
                datafr = "MoonPhases4WG"
                phase = 4
            elif lune == "Full":
                datafr = "MoonPhases5FM"
                phase = 5
            elif lune == "Waning Gibbous":
                datafr = "MoonPhases6WG"
                phase = 6
            elif lune == "Last Quarter":
                datafr = "MoonPhases7LQ"
                phase = 7
            elif lune == "Waning Crescent":
                datafr = "MoonPhases8WC"
                phase = 8

            if self.southern_hemi:
                datafr = '%s%s' % (datafr,self.suffix)
            titl = "1;Days, %s" % lune
            Domoticz.Debug("Setting Custom to" + titl +  ", Icon to " + str(datafr))
            try:
               Devices[1].Update(nValue=0,  sValue=str(luneage), Image=Images[datafr].ID, Options={"Custom": titl})
            except:
               Domoticz.Error("Failed to update device unit 1 with values %s:%s:" % (lune,luneage))

        return



global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
    return
