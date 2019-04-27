# Unifi Pi-hole

Get the [Pi-hole](https://github.com/pi-hole/pi-hole) project working on my [Unifi Security Gateway](https://www.ui.com/unifi-routing/usg/). Inspired by the [blacklist project](https://github.com/britannic/blacklist).

## Installing

⚠️ This is a work in progress, don't follow these instructions yet!

SSH into your USG and run these commands:

	configure
	delete service dns forwarding blacklist
	set service dns forwarding blacklist dns-redirect-ip 0.0.0.0

	edit service dns forwarding blacklist domains source unifi-pi-hole
	set url [needs a URL here]
	set description "See https://github.com/ndfred/unifi-pi-hole"
	set prefix 0.0.0.0
	top

	edit service dns forwarding blacklist hosts source unifi-pi-hole
	set url [needs a URL here]
	set description "See https://github.com/ndfred/unifi-pi-hole"
	set prefix 0.0.0.0
	top

	set service dns forwarding blacklist hosts exclude [needs a whitelisted host here]
	set service dns forwarding blacklist domains exclude [needs a whitelisted domain here]
	commit; save; exit

## Building the hosts list

Clone the repo and run the `build_rules.py` script to download and parse the rules files, and generate the `configure.sh` script:

    $ python build_rules.py
    Parsing StevenBlack's Unified Hosts List
    Parsing MalwareDomains
    Parsing Cameleon
    Parsing ZeusTracker
    Parsing Disconnect.me Tracking
    Parsing Disconnect.me Ads
    Parsing Hosts-file.net Ads
    Wrote 111813 host names in configure.sh

You can then copy the `configure.sh` script to your [Unifi Security Gateway](https://www.ui.com/unifi-routing/usg/) and run it there to filter these domains like a [Pi-hole](https://github.com/pi-hole/pi-hole) would.

The lists come from the [Pi-hole installation script](https://github.com/pi-hole/pi-hole/blob/master/automated%20install/basic-install.sh), I may tweak it from [other sources](https://firebog.net) in the future.

## Testing [![Build Status](https://travis-ci.com/ndfred/unifi-pi-hole.svg?branch=master)](https://travis-ci.com/ndfred/unifi-pi-hole/)

Just run the test script:

	$ python build_rules_tests.py 
	........
	----------------------------------------------------------------------
	Ran 8 tests in 0.001s

	OK

# Configuration reference

I SSH-ed into my USG, put myself in configuration mode, and queried completion suggestions to get to the documentation:

	# set service dns forwarding blacklist
	Possible completions:
	  disabled	Option to disable blacklisting
	  dns-redirect-ip
	  		Global redirect IP address for hosts and domains (zones)
	  domains	Configure DNS forwarding blacklist DOMAINS
	  exclude	domains to GLOBALLY EXCLUDE from DNS forwarding domains and hosts blacklist
	  hosts		Configure DNS forwarding blacklist hosts (must be fully qualified domain names)

	# set service dns forwarding blacklist domains 
	Possible completions:
	  dns-redirect-ip
	  		Blackhole IP address for domains
	  exclude	Domains to EXCLUDE from DNS forwarding blacklist
	  include	Domains to INCLUDE in the DNS forwarding blacklist
	  source	Blacklisted domains source name

	# set service dns forwarding blacklist hosts
	Possible completions:
	  dns-redirect-ip
	  		Blackhole IP address for hosts - overrides global blackhole IP
	  exclude	Hosts to EXCLUDE from DNS forwarding blacklist
	  include	Hosts to INCLUDE in the DNS forwarding blacklist
	  source	Blacklisted hosts source name

	# set service dns forwarding blacklist domains source unifi-pi-hole
	Possible completions:
	  description	Blacklist domain source description
	  dns-redirect-ip
	  		Blackhole IP address for a domain source - overrides global blackhole IP
	  file		A path and filename that provides a list of domains to blacklist, e.g. /config/user-data/hacked_domains.txt
	  prefix	Prefix string must include all text before the domain name
	  url		A blacklist source url that provides a list of domain names to block

	# set service dns forwarding blacklist exclude
	Possible completions:
	  <text>	domains to GLOBALLY EXCLUDE from DNS forwarding domains and hosts blacklist
