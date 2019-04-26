#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
import re

# See appendToListsFile in https://github.com/pi-hole/pi-hole/blob/master/automated%20install/basic-install.sh
# Other sources at https://firebog.net
AD_LISTS = [
    ('StevenBlack\'s Unified Hosts List', 'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'),
    ('MalwareDomains', 'https://mirror1.malwaredomains.com/files/justdomains'),
    ('Cameleon', 'http://sysctl.org/cameleon/hosts'),
    ('ZeusTracker', 'https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist'),
    ('Disconnect.me Tracking', 'https://s3.amazonaws.com/lists.disconnect.me/simple_tracking.txt'),
    ('Disconnect.me Ads', 'https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt'),
    ('Hosts-file.net Ads', 'https://hosts-file.net/ad_servers.txt'),
]

DOMAIN_EXPR = re.compile(r'^[a-zA-Z0-9\.\-_]+$')
ZERO_IP_PREFIXES = ('0.0.0.0 ', '127.0.0.1 ')
INVALID_DOMAINS = frozenset(('localhost', '0.0.0.0'))

def cleanup_domain_line(line):
    if '#' in line:
        line = line[:line.index('#')]

    line = line.strip().replace('\t ', ' ').replace('\t', ' ')

    return line

def parse_domain_line(line):
    original_line = line
    line = cleanup_domain_line(line)
    domain = None

    if DOMAIN_EXPR.match(line):
        domain = line
    else:
        for prefix in ZERO_IP_PREFIXES:
            if line.startswith(prefix):
                domain = line[len(prefix):].strip()

                if domain in INVALID_DOMAINS:
                    domain = None

    # if original_line and domain is None and not original_line.startswith('#'):
    #     print original_line.decode('utf8')

    return domain

def download_file(url):
    return urllib2.urlopen(url).read()

def parse_host_file(url):
    for line in download_file(url).split('\n'):
        domain = parse_domain_line(line)

        if domain:
            yield domain

def output_rules(configuration_script_path):
    prefix = 'service dns forwarding blacklist'
    domains_buffer = []

    for name, url in AD_LISTS:
        print 'Parsing %s' % name

        for domain in parse_host_file(url):
            if domain.count('.') > 1:
                domains_buffer.append('set %s hosts exclude %s' % (prefix, domain))
            else:
                domains_buffer.append('set %s exclude %s' % (prefix, domain))

    domains_buffer = sorted(set(domains_buffer))

    with open(configuration_script_path, 'w') as config_script:
        config_script.write('configure\n')
        config_script.write('delete %s\n' % prefix)
        config_script.write('set %s dns-redirect-ip 0.0.0.0\n' % prefix)
        config_script.write('\n'.join(domains_buffer))
        config_script.write('\ncommit; save; exit\n')

    print 'Wrote %d host names in %s' % (len(domains_buffer), configuration_script_path)

    return 0

def main():
    output_rules('configure.sh')

    return 0

if __name__ == '__main__':
    sys.exit(main())