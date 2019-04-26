# Unifi Pi-hole

Get the [Pi-hole](https://github.com/pi-hole/pi-hole) project working on my [Unifi Security Gateway](https://www.ui.com/unifi-routing/usg/). Inspired by the [blacklist project](https://github.com/britannic/blacklist).

## Running

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

## Testing

Just run the test script:

	$ python build_rules_tests.py 
	........
	----------------------------------------------------------------------
	Ran 8 tests in 0.001s

	OK
