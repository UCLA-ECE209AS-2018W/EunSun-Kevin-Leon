# Automatic Firewall
## Eun Sun Lee, Leon Kozinakov, Zhengxu Xia

## Background

**Introduction**

*The number of IoT devices is increasing rapidly in the average household. Devices can be full-fledged application computers, but also inexpensive devices with a prescribed task.We try to create a user friendly automated firewall to help manage a large number of these devices.*

**Background**

*We read some papers that attempted to characterize network traffic patterns (See References [1]) Patterns vary quite a lot from device to device, but there seems to be a category of home automation devices (smart bulb, smart lock, etc.) that follow a broad pattern.That is, the devices have a set of IP addresses they talk to in the initialization stage, and they don’t add very many new addresses afterwards. We assume that the device is not compromised in this grace period. (i.e. No zero-day vulnerability)*

## pfSense
**Possible Firewall Choices**

*IPFire: This is the first one we tried. Seemed to be well-maintained and allowed an ARM installation, so we hoped it would work on a Raspberry Pi 3. Problems with Installation, abandoned it*
*OpenWRT: The ARM port seemed like it was not maintained.*
*pfSense: By this point we aquired a NUC, so an x86 installation was viable. Our lab already uses it, so we had some familiarity.This was our final choice. Purpose-built hardware + software combo.*

**pfSense**
*Open source software distribution based on FreeBSD.
Combination of firewall, router, DHCP server, and etc.
Well designed web interface and easy to configure.
Easy deployment on physical device and virtual machine.
Limited command line options and features.*

**Device List**
*Intel NUC x1 (Pfsense Firewall)
Raspberry Pi x3 (IoT Device and 2 Servers)
Laptop x1 (Administrator)
Switch x 2
Ethernet Cables*

![networksetup](https://github.com/UCLA-ECE209AS-2018W/EunSun-Kevin-Leon/blob/master/media/Networksetup.png)

## Automatic Firewall
**Architecture**
*whitelist, blacklist, maillist*
![rulearchitecture](https://github.com/UCLA-ECE209AS-2018W/EunSun-Kevin-Leon/blob/master/media/rulesarchitecture.png)


**LAN Rules**
*Sample Rule List
Anti-lockout rule (Guaranteed admin access to web interface)
Add “Custom Rule 1” … “Custom Rule N”
Block all LAN to !LAN rule (Default)
Allow LAN to Any rule (Default)
Grace period timeout for each IoT
Block all new outgoing requests from local network*

**WAN Rules**
*Sample Rule List
Add “Custom Rule 1” … “Custom Rule N”
Block all incoming request from external network (Default)
Check whitelist and add Custom Rules
Sample Whitelist
{“192.168.1.30": [“2018-Jan-03:10:00:00”, “1.1.1.3", “192.168.10.2”], “192.168.1.10": [“2018-Jan-03:10:00:10”, “1.1.1.2"], “192.168.10.2”: [“2018-Jan-03:10:00:20", “192.168.1.30”]}*

**Email Notification**

*Administrator email address is configured in the web interface.
A notification is triggered when:
A LAN device is trying to communicate to a WAN IP after grace period.
A previously whitelisted LAN/WAN IP is blacklisted and any pass rule that includes blacklist IP is removed.*

**Blacklist**
*Update whitelist by checking blacklist periodically
No new rule added if the IP address is in the blacklist*

**Difficulties and Limitations**
*Current settings are in local network.
Lack access to public blacklist database.
Hardcoded grace period to trust newly deployed IoT devices.
Pfsense has very limited command line features.
LAN devices lose gateway record due to firewall cache removal.
Need to manually add gateway back at IoT side due to cache removal.*

**Future Work**
*Connect the network setup to internet.
Reply the email notification to add a rule.
Try different firewall distributions.
Reverse DNS lookup to detect the change of server IP address.
Access to public blacklist IP address database.
Test the firewall under real network traffic.
Use machine learning to detect anomalies in IoT traffic.*

**References**
*http://www2.ee.unsw.edu.au/~vijay/pubs/conf/17infocom.pdf
https://doc.pfsense.org/index.php/Main_Page*


* Possible
![pfSenseLogo](https://github.com/UCLA-ECE209AS-2018W/EunSun-Kevin-Leon/blob/master/media/pfSense-Logo.jpg)


  
