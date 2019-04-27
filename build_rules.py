#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
import re

# See https://v.firebog.net/hosts/lists.php
FIREBOG_CONSERVATIVE_URLS_LIST = 'https://v.firebog.net/hosts/lists.php?type=tick'
DOMAIN_EXPR = re.compile(r'^[a-zA-Z0-9\.\-_]+$')
ZERO_IP_PREFIXES = ('0.0.0.0 ', '127.0.0.1 ', '0 ', ':: ')
INVALID_DOMAINS = frozenset(('localhost', '0.0.0.0'))
OUTPUT_HOSTS_PATH = 'hosts.txt'
OUTPUT_DOMAINS_PATH = 'domains.txt'
BLACKHOLE_IP = '0.0.0.0'

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
    # Take .co.uk into account?
    if domain.count('.') > 1:
        return False
    else:
        return True

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
        raise Exception('Couldn\'t find any domains in that URL')

def output_hosts(ads_lists_ulrs=FIREBOG_CONSERVATIVE_URLS_LIST, output_hosts_path=OUTPUT_HOSTS_PATH, output_domains_path=OUTPUT_DOMAINS_PATH, blackhole_ip=BLACKHOLE_IP):
    ads_lists = download_ads_list_urls(ads_lists_ulrs)
    domains = []

    for name, url in ads_lists:
        print 'Parsing %s' % name
        domains += parse_host_file(url)

    domains = sorted(set(domains))

    with open(output_hosts_path, 'w') as hosts_file:
        with open(output_domains_path, 'w') as domains_file:
            for domain in domains:
                if is_domain(domain):
                    hosts_file.write('%s %s\n' % (blackhole_ip, domain))
                else:
                    domains_file.write('%s %s\n' % (blackhole_ip, domain))

    print 'Wrote %d host names in %s and %s' % (len(domains), output_hosts_path, output_domains_path)

    return 0

def main():
    output_hosts()

    return 0

if __name__ == '__main__':
    sys.exit(main())
