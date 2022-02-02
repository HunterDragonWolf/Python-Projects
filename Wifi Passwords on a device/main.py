
#   Import subprocess so we can use system commands.
import subprocess

#   Import the re module so we can make use of regular expressions.
import re


#   Python allows us to run system commands using the function
#   provided by the subprocess module.

commandOutput = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()



#   We imported the re module to make use of regular expressions.
profileNames = (re.findall("All User Profile     : (.*)\r", commandOutput))


#   We create an empty list outside of the loop where dictionaries
#   containing all the wifi usernames and passwords will be saved.

wifiList = []

#   So we run this part to check the
#   details of the wifi and see whether we can get their passwords.
if len(profileNames) != 0:
    for name in profileNames:



        #   Every wifi connection will need its own dictionary which
        #   will be appended to the variable wifi_list.
        wifiProfile = {}

        #   We can now run a more specific command to see the information
        #   about the wifi connection.
        profileInfo = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()


        #   We use the regular expression to only look for the absent cases so we can ignore them.

        if re.search("Security key           : Absent", profileInfo):
            continue
        else:



            #   Assign the ssid of the wifi profile to the dictionary
            wifiProfile['ssid'] = name

            #   These cases aren't absent and we should run the
            #   "key=clear" command part to get the password.
            profileInfoPass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()

            #   Again run the regular expression to capture the
            #   group after the : (which is the password).
            password = re.search("Key Content            : (.*)\r", profileInfoPass)

            #   Check if we found a password using the regular expression.
            if password == None:
                wifiProfile["Password"] = None

            else:


                #   We assign the grouping that we are interested in
                #   to the password key in the dictionary.
                wifiProfile["Password"] = password[1]

            #   We append the wifi information to the variable wifi_list.
            wifiList.append(wifiProfile)

for s in range(len(wifiList)):
    print(wifiList[s])