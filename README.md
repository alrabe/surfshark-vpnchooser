
# Choose VPN Server for Surfshark on Linux
You can use these scripts to establish an OpenVpn connection to any Surfsark VPN server. You will need the configurations for the servers and your login data file.

## Server Selection
The `vpnup.py` script lets you select a Surfshark VPN server from your VPN configuration files and starts the `startvpn` script.
  
  `$ vpnup.py`

## VPN Conection

The `startvpn` script will start the `openvpn` tool using the selected configuration. If `openvpn` ends (e.g. by pressing `Ctrl-C`) then the script will also shut down your network interface and ask you if you want to restart the network. For this to work you have to __provide the correct network interface__ in the `startvpn` file. In my case:

`INTERFACE="enp4s0"`

You can also run this script manually if you know the server configuration:

`$ startvpn nl-ams`

Both scripts must be executable (`chmod +x vpnup.py`) and should be located in the directory `./local/bin`.

## Configuration Files

The Surfshark configuration files must be located in the directory `./local/openvpn` and be named like this:
```
hk-hkg.prod.surfshark.com_udp.ovpn
hr-zag.prod.surfshark.com_tcp.ovpn
hr-zag.prod.surfshark.com_udp.ovpn
hu-bud.prod.surfshark.com_tcp.ovpn
hu-bud.prod.surfshark.com_udp.ovpn
```
_TODO: Provide a script that will modify original Surfshark scripts_

## Credential File

The Surkshark credentials are expected in the file `./local/openvpn/credentials/key`.

[You can find more details at Surfshark support](https://support.surfshark.com/hc/en-us/articles/360011051133-How-to-set-up-manual-OpenVPN-connection-using-Linux-Terminal#01H97YPS042298VER0KJBZXH79)
