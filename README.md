# smrt

A utility to configure your TP-Link Easy Smart Switch
on Linux or Mac OS X. This tool is written in Python.

Supposedly supported switches:

* TL-SG105E (tested)
* TL-SG108E (tested)
* TL-SG108PE
* TL-SG1016DE (tested)
* TL-SG1024DE

## Discover switches

### Simple discovery

```
$ ./discovery.py
```

### Multiple interfaces

If more than one interface, error message gives the list:

```
Error: more than 1 interface. Use -i or --interface to specify the name
Interfaces:
    'enp3s0'
    'virbr0'
    'virbr0-nic'
```

### Default output

Give the right interface:
```
$ ./discovery.py -i enp3s0
```

Output (found 2 switches):
```
192.168.9.36
ba.ff.ee.ff.ac.ee
(1, 'type', 'TL-SG108E')
(2, 'hostname', 'sg108ev4')
(3, 'mac', '01:01:01:01:01:01')
(7, 'firmware', '1.0.0 Build 20181120 Rel.40749')
(8, 'hardware', 'TL-SG108E 4.0')
(9, 'dhcp', False)
(4, 'ip_addr', IPv4Address('192.168.9.202'))
(5, 'ip_mask', IPv4Address('255.255.255.0'))
(6, 'gateway', IPv4Address('192.168.9.1'))
(13, 'auto_save', True)
----------------
(1, 'type', 'TL-SG108E')
(2, 'hostname', 'sg108ev1')
(3, 'mac', '02:02:02:02:02:02')
(7, 'firmware', '1.1.2 Build 20141017 Rel.50749')
(8, 'hardware', 'TL-SG108E 1.0')
(9, 'dhcp', False)
(4, 'ip_addr', IPv4Address('192.168.9.203'))
(5, 'ip_mask', IPv4Address('255.255.255.0'))
(6, 'gateway', IPv4Address('192.168.9.1'))
```

### Command output with -c

With switch `-c` or `--command`, output gives the syntax for using smrt with right arguments

```
$ ./discovery.py -i enp3s0 -c
./smrt.py --username admin --password admin -i enp3s0 --switch-mac 01:01:01:01:01:01
./smrt.py --username admin --password admin -i enp3s0 --switch-mac 02:02:02:02:02:02
```

### Alias

After discovery, setting an shell alias reduces command size

```
$ alias smrt='python ~/smrt/smrt.py --switch-mac 60:E3:27:83:25:3F  -i eth0 --username admin --password admin'
```

## smrt.py

### without command gives list of command

```
$ ./smrt.py --username admin --password admin --interface==eth0 --switch-mac 01:01:01:01:01:01
Actions: type hostname mac ip_addr ip_mask gateway firmware hardware dhcp num_ports v4 username password save get_token_id igmp_snooping ports trunk mtu_vlan vlan_enabled vlan pvid vlan_filler qos1 qos2 mirror stats loop_prev
```

### vlan

```
$ smrt vlan # use alias

(8704, 'vlan_enabled', '01')
(8705, 'vlan', [1, '1,2,3,4,5,6,7,8', '', 'Default_VLAN'])
(8705, 'vlan', [90, '1,2,3,4,5,6,7,8', '', 'LAN'])
(8705, 'vlan', [100, '1,2,3', '1', 'vlan_test_1'])
(8707, 'vlan_filler', ' ')
```

### pvid

```
$ smrt pvid
(8706, 'pvid', (1, 90))
(8706, 'pvid', (2, 90))
(8706, 'pvid', (3, 90))
(8706, 'pvid', (4, 90))
(8706, 'pvid', (5, 90))
(8706, 'pvid', (6, 90))
(8706, 'pvid', (7, 90))
(8706, 'pvid', (8, 90))
(8707, 'vlan_filler', ' ')
```

### stats

```
$ smrt stats
(16384, 'stats', (1, 1, 6, 48, 0, 6356, 14))
(16384, 'stats', (2, 1, 0, 0, 0, 0, 0))
(16384, 'stats', (3, 1, 0, 0, 0, 0, 0))
(16384, 'stats', (4, 1, 5, 6404, 0, 0, 14))
(16384, 'stats', (5, 1, 0, 0, 0, 0, 0))
(16384, 'stats', (6, 1, 0, 0, 0, 0, 0))
(16384, 'stats', (7, 1, 0, 0, 0, 0, 0))
(16384, 'stats', (8, 1, 0, 0, 0, 0, 0))
```

### smrt ports

```
$ smrt ports
(4096, 'ports', '01:01:00:01:06:00:00')
(4096, 'ports', '02:01:00:01:00:00:00')
(4096, 'ports', '03:01:00:01:00:00:00')
(4096, 'ports', '04:01:00:01:05:00:00')
(4096, 'ports', '05:01:00:01:00:00:00')
(4096, 'ports', '06:01:00:01:00:00:00')
(4096, 'ports', '07:01:00:01:00:00:00')
(4096, 'ports', '08:01:00:01:00:00:00')
```
## Set VLAN settings

### Syntax

`smrt.py` shows parameters and can change them for VLANs if `--vlan` is present

Specific VLAN parameters:

* `--vlan`: vlan number (1-4093)
* `--vlan_name`: acceptable vlan name for TP-Link switch 
* `--vlan_member`: comma separated list without space of member ports. Ex: 1,2,4
* `--vlan_tagged`: comma separated list without space of tagged ports. Ex: 1,2
* `--vlan_pvid`: set pvid to `--vlan` for given ports

### Example 1 : add new vlan 120

```
$ smrt vlan
(8704, 'vlan_enabled', '01')
(8705, 'vlan', [1, '1,2,3,4,5,6,7,8', '', 'Default_VLAN'])
(8705, 'vlan', [90, '1,2,3,4,5,6,7,8', '', 'LAN'])
(8705, 'vlan', [100, '1,2,3', '1', 'vlan_test_1'])
(8707, 'vlan_filler', ' ')
$ smrt vlan --vlan 120 --vlan_name "vlan_test_2" --vlan_member 1,4,5,6 --vlan_tagged 1
(8704, 'vlan_enabled', '01')
(8705, 'vlan', [1, '1,2,3,4,5,6,7,8', '', 'Default_VLAN'])
(8705, 'vlan', [90, '1,2,3,4,5,6,7,8', '', 'LAN'])
(8705, 'vlan', [100, '1,2,3', '1', 'vlan_test_1'])
(8705, 'vlan', [120, '1,4,5,6', '1', 'vlan_test_2'])
(8707, 'vlan_filler', ' ')
```

### Example 2 : change to pvid 120 for ports 5 and 6

Note : vlan must exist (see example 1) before this command.

```
$ smrt pvid
(8706, 'pvid', (1, 90))
(8706, 'pvid', (2, 90))
(8706, 'pvid', (3, 90))
(8706, 'pvid', (4, 90))
(8706, 'pvid', (5, 90))
(8706, 'pvid', (6, 90))
(8706, 'pvid', (7, 90))
(8706, 'pvid', (8, 90))
(8707, 'vlan_filler', ' ')
$ smrt vlan --vlan 120 --vlan_pvid 5,6
(8706, 'pvid', (1, 90))
(8706, 'pvid', (2, 90))
(8706, 'pvid', (3, 90))
(8706, 'pvid', (4, 90))
(8706, 'pvid', (5, 120))
(8706, 'pvid', (6, 120))
(8706, 'pvid', (7, 90))
(8706, 'pvid', (8, 90))
(8707, 'vlan_filler', ' ')
```

### Exemple 3 : remove vlan 120

```
$ smrt vlan --vlan 120 --delete
(8704, 'vlan_enabled', '01')
(8705, 'vlan', [1, '1,2,3,4,5,6,7,8', '', 'Default_VLAN'])
(8705, 'vlan', [90, '1,2,3,4,5,6,7,8', '', 'LAN'])
(8705, 'vlan', [100, '1,2,3', '1', 'vlan_test_1'])
(8707, 'vlan_filler', ' ')
```

Note that, for PVID, corresponding ports are reinitialized to vlan 1:
```
$ smrt pvid
(8706, 'pvid', (1, 90))
(8706, 'pvid', (2, 90))
(8706, 'pvid', (3, 90))
(8706, 'pvid', (4, 90))
(8706, 'pvid', (5, 1))
(8706, 'pvid', (6, 1))
(8706, 'pvid', (7, 90))
(8706, 'pvid', (8, 90))
(8707, 'vlan_filler', ' ')
```

### Exemple 4 : add new vlan and pvid

```
$ smrt vlan --vlan 130 --vlan_name "vlan_test_3" --vlan_member 1,4,5,6 --vlan_tagged 1 --vlan_pvid 4,5,6
(8704, 'vlan_enabled', '01')
(8705, 'vlan', [1, '1,2,3,4,5,6,7,8', '', 'Default_VLAN'])
(8705, 'vlan', [90, '1,2,3,4,5,6,7,8', '', 'LAN'])
(8705, 'vlan', [100, '1,2,3', '1', 'vlan_test_1'])
(8705, 'vlan', [130, '1,4,5,6', '1', 'vlan_test_3'])
(8707, 'vlan_filler', ' ')
(8706, 'pvid', (1, 90))
(8706, 'pvid', (2, 90))
(8706, 'pvid', (3, 90))
(8706, 'pvid', (4, 130))
(8706, 'pvid', (5, 130))
(8706, 'pvid', (6, 130))
(8706, 'pvid', (7, 90))
(8706, 'pvid', (8, 90))
(8707, 'vlan_filler', ' ')
```
