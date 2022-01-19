import ipaddress
from ipaddress import AddressValueError, NetmaskValueError
from guietta import Gui, _, ___, III, R1, VSeparator

# This also works with ipadddress Network objects as well
def addressTypes(address):
	address_types = ""

	if address.is_multicast:
		address_types += "MULTICAST"
	if address.is_private:
		address_types += ", PRIVATE" if len(address_types) > 0 else "PRIVATE"
	if address.is_global:
		address_types += ", GLOBAL" if len(address_types) > 0 else "GLOBAL"
	if address.is_unspecified:
		address_types += ", UNSPECIFIED" if len(address_types) > 0 else "UNSPECIFIED"
	if address.is_reserved:
		address_types += ", RESERVED" if len(address_types) > 0 else "RESERVED"
	if address.is_loopback:
		address_types += ", LOOPBACK" if len(address_types) > 0 else "LOOPBACK"
	if address.is_link_local:
		address_types += ", LINK LOCAL" if len(address_types) > 0 else "LINK LOCAL"

	return address_types
	
def formatOutput(interface):
	address = interface.ip
	network = interface.network
	netmask = network.netmask
	prefixlen = network.prefixlen
	broadcast_address = network.broadcast_address
	network_address = network.network_address
	host_start = network_address + 1
	host_end = broadcast_address - 1
	hosts = network.num_addresses - 2

	address_types = addressTypes(address)

	output =  "IP Address:\t\t\t" + str(address) + "\n"
	output += "Network Address:\t\t" + network_address.compressed + "\n"
	output += "Broadcast Address:\t\t" + broadcast_address.compressed + "\n"
	output += "Prefix Length:\t\t\t" + str(prefixlen) + "\n"
	output += "Address Types:\t\t\t" + address_types + "\n"
	output += "Host Range:\t\t\t" + str(host_start) + " - " + str(host_end) + "\n"
	output += "Number of hosts:\t\t" + f'{hosts:,}'

	return output

def calculatev6(ip, netmask):
	address = ipaddress.IPv6Address(ip) # Used to check to make sure IP address is actually valid.
	interface = ipaddress.IPv6Interface(ip + "/" + netmask)

	network = interface.network

	output = formatOutput(interface)
	
	if network.prefixlen < 64:
		networks64 = 2 ** (64 - network.prefixlen)
		output += "\nNumber of /64 networks:\t\t" + f'{networks64:,}'
	
	if network.prefixlen < 56:
		networks56 = 2 ** (56 - network.prefixlen)
		output += "\nNumber of /56 networks:\t\t" + f'{networks56:,}'
	
	if network.prefixlen < 48:
		networks48 = 2 ** (48 - network.prefixlen)
		output += "\nNumber of /48 networks:\t\t" + f'{networks48:,}'

	return output

def calculatev4(ip, netmask):
	address = ipaddress.IPv4Address(ip) # Used to check to make sure IP address is actually valid.
	interface = ipaddress.IPv4Interface(ip + "/" + netmask)

	network = interface.network

	output = formatOutput(interface)

	if network.prefixlen < 24:
		networks24 = 2 ** (24 - network.prefixlen)
		output += "\nNumber of /24 networks:\t\t" + f'{networks24:,}'

	return output

def handler(gui, *args):
	address = gui.address
	netmask = gui.netmask
	
	v6checked = gui.IPv6.isChecked()
	v4checked = gui.IPv4.isChecked()
	
	if (gui.IPv6.isChecked()):
		try:
			output = calculatev6(address, netmask)
			gui.output = output
		except ValueError:
		        return
		except AddressValueError:
		        return
		except NetmaskValueError:
			return
	elif (gui.IPv4.isChecked()):
		try:
			output = calculatev4(address, netmask)
			gui.output = output
		except ValueError:
			return
		except AddressValueError:
			return
		except NetmaskValueError:
			return
	
	return


gui = Gui([R1('IPv4',1) , R1('IPv6')   , VSeparator,('','output') ,___],
          ['Address: '  , '__address__', III       ,III         ,III],
          ['Netmask: '  , '__netmask__', III       ,III         ,III],
          [_            , _            , III       ,III         ,III],
          [_            , _            , III       ,III         ,III])

gui.events([handler , handler                ,_,_,_],
           [_       , ('textEdited',handler) ,_,_,_],
           [_       , ('textEdited',handler) ,_,_,_],
           [_       , _                      ,_,_,_],
           [_       , _                      ,_,_,_])

gui.window().setGeometry( 100, 100, 700, 225 )
gui.column_stretch([2,3,1,2,2])
gui.title("PyIP Calculator")

gui.run()
