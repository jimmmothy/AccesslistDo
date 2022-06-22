## AccesslistDo
Check geographic location of bot SSH/Telnet attempts 

I was curious to see where these bot login attempts were coming from after using this basic access list. Obviously doesn't account for firewall in use, but fun anyway.

```
access-list 100 deny   tcp any any eq 22 log
access-list 100 deny   tcp any any eq telnet log
access-list 100 deny   ip 10.0.0.0 0.255.255.255 any log
access-list 100 deny   ip 172.16.0.0 0.15.255.255 any log
access-list 100 deny   ip 192.168.0.0 0.0.255.255 any log
access-list 100 deny   ip 127.0.0.0 0.255.255.255 any log
access-list 100 permit ip any any
```

### Usage
Use any kind of access list live above, and have syslog turned on directed to the PC/Server running rsyslog/syslog-ng
```
logging host 192.168.40.40
```

Basic syslog-ng config that works for this
```
#
# listens on UDP 514 from cisco router
# basic blocking of all external SSH/telnet
# + 10.0.0.0/8 172.168.0.0/12 192.168.0.0/16
/etc/syslog-ng/syslog-ng.conf
@version: 3.30
@include "scl.conf"

options {
  stats_freq (0);
  flush_lines (0);
  time_reopen (10);
  log_fifo_size (10000);
  chain_hostnames (off);
  dns_cache (no);
  use_dns (no);
  use_fqdn (no);
  create_dirs (no);
  keep_hostname (yes);
  perm(0640);
  group("log");
};

source s_net { udp(); };

filter f_host { host( "192.168.40.40" ); };

destination d_ciscol { file("/var/log/cisco.log"); };

log { source(s_net); filter(f_host); destination(d_ciscol); };
```
