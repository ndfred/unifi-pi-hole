#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
import re

# See appendToListsFile in https://github.com/pi-hole/pi-hole/blob/master/automated%20install/basic-install.sh
AD_LISTS = [
    ('StevenBlack\'s Unified Hosts List', 'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'),
    ('MalwareDomains', 'https://mirror1.malwaredomains.com/files/justdomains'),
    ('Cameleon', 'http://sysctl.org/cameleon/hosts'),
    ('ZeusTracker', 'https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist'),
    ('Disconnect.me Tracking', 'https://s3.amazonaws.com/lists.disconnect.me/simple_tracking.txt'),
    ('Disconnect.me Ads', 'https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt'),
    ('Hosts-file.net Ads', 'https://hosts-file.net/ad_servers.txt'),
]
# See https://v.firebog.net/hosts/lists.php
FIREBOG_CONSERVATIVE_URLS_LIST = 'https://v.firebog.net/hosts/lists.php?type=tick'
DOMAIN_EXPR = re.compile(r'^[a-zA-Z0-9\.\-_]+$')
ZERO_IP_PREFIXES = ('0.0.0.0 ', '127.0.0.1 ', '0 ', ':: ')
INVALID_DOMAINS = frozenset(('localhost', '0.0.0.0'))
OUTPUT_BLACKLIST_PATH = 'blacklist.conf'
DOMAIN_EXTENSIONS_URL = 'https://publicsuffix.org/list/public_suffix_list.dat'
DOMAIN_EXTENSIONS = None

def get_domain_extensions():
    global DOMAIN_EXTENSIONS

    if DOMAIN_EXTENSIONS == None:
        DOMAIN_EXTENSIONS = frozenset(parse_host_file(DOMAIN_EXTENSIONS_URL))

    return DOMAIN_EXTENSIONS

def download_file(url):
    request = urllib2.Request(url)
    # Needed to bypass Cloudflare's bot detection
    request.add_header('User-Agent', 'curl/7.54.0')

    return urllib2.urlopen(request).read()

def download_ads_list_urls(url):
    return [(list_url, list_url) for list_url in download_file(url).split('\n') if list_url]

def cleanup_domain_line(line):
    if '#' in line:
        line = line[:line.index('#')]

    line = line.strip().replace('\t ', ' ').replace('\t', ' ')

    return line

def is_domain(domain):
    if not '.' in domain:
        return True

    extension = domain[domain.index('.') + 1:]

    if extension in get_domain_extensions():
        return True

    return False

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

    # Uncomment to visually debug unmatched lines and make sure we parse all hosts
    # if original_line and domain is None and not original_line.startswith('#'):
    #     print original_line.decode('utf8')

    return domain

def parse_host_file(url):
    found_domains = False

    for line in download_file(url).split('\n'):
        domain = parse_domain_line(line)

        if domain:
            found_domains = True
            yield domain

    if not found_domains:
        raise Exception('Couldn\'t find any domains in URL %s' % url)

def remove_duplicate_domains(domains):
    top_level_domains = set()
    top_level_domains_suffixes = set()
    hosts = set()
    filtered_hosts = set()

    for domain in domains:
        if is_domain(domain):
            top_level_domains.add(domain)
            top_level_domains_suffixes.add('.%s' % domain)
        else:
            hosts.add(domain)

    top_level_domains_suffixes = tuple(top_level_domains_suffixes)

    for host in hosts:
        if not host.endswith(top_level_domains_suffixes):
            filtered_hosts.add(host)

    return sorted(list(top_level_domains.union(filtered_hosts)))

def output_hosts(ads_lists_ulrs=FIREBOG_CONSERVATIVE_URLS_LIST, output_blacklist_path=OUTPUT_BLACKLIST_PATH):
    # ads_lists = download_ads_list_urls(ads_lists_ulrs)
    ads_lists = AD_LISTS
    domains = []

    for name, url in ads_lists:
        print 'Parsing %s' % name
        domains += parse_host_file(url)

    domains = remove_duplicate_domains(domains)

    with open(output_blacklist_path, 'w') as blacklist_file:
        for domain in domains:
            blacklist_file.write('server=/%s/\n' % domain)

    print 'Wrote %d host names in %s' % (len(domains), output_blacklist_path)

    return 0

def main():
    output_hosts()

    return 0

if __name__ == '__main__':
    sys.exit(main())
