# Automatic Firewall
## Eun Sun Lee, Leon Kozinakov, Zhengxu Xia

## Background

**Introduction**

*The number of IoT devices is increasing rapidly in the average household. Devices can be full-fledged application computers, but also inexpensive devices with a prescribed task.We try to create a user friendly automated firewall to help manage a large number of these devices.*

**Background**

*We read some papers that attempted to characterize network traffic patterns (See References [1]) Patterns vary quite a lot from device to device, but there seems to be a category of home automation devices (smart bulb, smart lock, etc.) that follow a broad pattern.That is, the devices have a set of IP addresses they talk to in the initialization stage, and they don’t add very many new addresses afterwards. We assume that the device is not compromised in this grace period. (i.e. No zero-day vulnerability)*

## pfSense
**Possible Firewall Choices**

*IPFire: This is the first one we tried. Seemed to be well-maintained and allowed an ARM installation, so we hoped it would work on a Raspberry Pi 3. However we faced problems with the installation, so we abandoned it*
*OpenWRT: The ARM port seemed like it was not maintained.*
*pfSense: By this point we aquired an x86 platform, so the pfSense installation image was viable. Our lab already uses it, so we had some familiarity.This was our final choice.*

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
*The architecture of automatic firewall is described in the image below. The firewall rules are divided into WAN rules and LAN rules. Both rules then have default rules and custom rules, which are added by the automatic firewall we designed. Separate from the rules, we keep a whitelist, blacklist, and a maillist. The whitelist is updated along with the WAN and LAN rules. We added a blacklist file which contains a list of IP addresses. There are websites which list the blacklisted IP addresses. However, our firewall setup operates within local network so the file is added to simulate the checking of blacklised IP address from such websites. Lastly, we keep a maillist file so that we do not pour large amount of emails to the administrator. This prevents the multiple emails with the same notification.*

![rulearchitecture](https://github.com/UCLA-ECE209AS-2018W/EunSun-Kevin-Leon/blob/master/media/rulesarchitecture.png)


**LAN Rules**
*To guarantee administrator's access to pfSense web interface, the is unmodifiable and highest-prioritized anti-lockout rule in LAN rules. Then the rules start with two default rules. First default rule blocks all communication from LAN to non-LAN. Then, the second default rule allows LAN to any. This has less priority than the first defult rule. Then, the custom rules added by automatic firewall have higher priority than the two default rules. Once the automatic firewall begins, all the communication going from LAN to non-LAN are added into the rules list and whitelist. However, whitelist keeps the timestamp when each sourceip address is first added so no more new rules with the source ip can be added after the grace period. Once the grace period of the source ip has passed, any new outgoing request is blocked. The list below shows the priority of all LAN rules in order.*

*List of LAN rules in their priority order:*
* Anti-lockout rule (Guaranteed admin access to web interface)
* Bullet list item 2
* Anti-lockout rule (Guaranteed admin access to web interface)
* “Custom Rule 1” … “Custom Rule N”
* Block all LAN to !LAN rule (Default)
* Allow LAN to Any rule (Default)


**WAN Rules**
*WAN rules begin by blocking all as default. This is a very restricted setting which blocks any WAN rule from the beggining. New WAN rules are added only if a LAN has talked to the specific WAN address. We achieve this by allowing WAN rules only if the opposite communication already existing in the witelist. Unlike LAN rules, we do not check grace period timeout because it is already strictly checked by whitelist. Below list shows the WAN rules in their priority order. From the sample whitelist, for example, the last rule from the WAN IP address, 192.168.10.,2 to the LAN IP address, 192.168.1.30, can be added only after the first rule from 192.168.1.30 to 192.1668.10.2 has been added.*

*List of WAN rules in their priority order:*
* “Custom Rule 1” … “Custom Rule N”
* Block all incoming request from external network (Default)

*Sample Whitelist :*
*{“192.168.1.30": [“2018-Jan-03:10:00:00”, “1.1.1.3", “192.168.10.2”], “192.168.1.10": [“2018-Jan-03:10:00:10”, “1.1.1.2"], “192.168.10.2”: [“2018-Jan-03:10:00:20", “192.168.1.30”]}*

**Email Notification**
*One feature we included for the administrator's convenience is email notification. First the administrator's email address and IP address is configured in the web interface. A notification is triggered in two cases. First, a email is sent when a LAN device is tryng to communicate to a WAN IP after the grace period. The second case is when a previously whitelisted LAN/WAN device is blacklisted and any pass rule that includes blacklist IP is removed.*

**Blacklist**
*As mentioned above, the blacklist is generated manually to simulate online websitat that keep blacklist IP address. While the automatic firewall is running, we manually add blacklist and check if the rules with blacklisted IP are removed from pfSense web interface. First, we periodically update whitelist and rule by chekcing blacklist file. We also block any rule to be added if the IP address is in the blacklist.*

## Difficulties and Limitations
*Current settings are in local network.
Lack access to public blacklist database.
Hardcoded grace period to trust newly deployed IoT devices.
Pfsense has very limited command line features.
LAN devices lose gateway record due to firewall cache removal.
Need to manually add gateway back at IoT side due to cache removal.*

## Future Work
*Connect the network setup to internet.
*Reply the email notification to add a rule.
*Try different firewall distributions.
*Reverse DNS lookup to detect the change of server IP address.
*Access to public blacklist IP address database.
*Test the firewall under real network traffic.
*Use machine learning to detect anomalies in IoT traffic.*

## References
*http://www2.ee.unsw.edu.au/~vijay/pubs/conf/17infocom.pdf
https://doc.pfsense.org/index.php/Main_Page*


* Possible
![pfSenseLogo](https://github.com/UCLA-ECE209AS-2018W/EunSun-Kevin-Leon/blob/master/media/pfSense-Logo.jpg)


  
