#!/usr/bin/env python
# -*- coding: utf-8 -*-

from build_rules import *
import unittest

class TestDomainParsing(unittest.TestCase):
    def test_domain_expr(self):
        self.assertFalse(DOMAIN_EXPR.match('Hello world'))
        self.assertFalse(DOMAIN_EXPR.match('https://www.google.com'))
        self.assertTrue(DOMAIN_EXPR.match('google.com'))
        self.assertTrue(DOMAIN_EXPR.match('my-google.com'))
        self.assertTrue(DOMAIN_EXPR.match('sub.my-google.com'))
        self.assertTrue(DOMAIN_EXPR.match('sub.google.com'))
        self.assertTrue(DOMAIN_EXPR.match('927697--storno-sicher-konto_identity.sicherheitsvorbeugung-schutz.cf'))

    def test_cleanup_domain_line(self):
        self.assertEqual(cleanup_domain_line(' '), '')
        self.assertEqual(cleanup_domain_line('# Comment'), '')
        self.assertEqual(cleanup_domain_line('domain.com # Comment'), 'domain.com')
        self.assertEqual(cleanup_domain_line(' domain.com # Comment'), 'domain.com')
        self.assertEqual(cleanup_domain_line('0.0.0.0 domain.com # Comment'), '0.0.0.0 domain.com')
        self.assertEqual(cleanup_domain_line('0.0.0.0\t domain.com # Comment'), '0.0.0.0 domain.com')

    def test_StevenBlack(self):
        self.assertIsNone(parse_domain_line('# This hosts file is a merged collection of hosts from reputable sources,'))
        self.assertIsNone(parse_domain_line('# ==============================================================='))
        self.assertIsNone(parse_domain_line('127.0.0.1 localhost'))
        self.assertIsNone(parse_domain_line('::1 localhost'))
        self.assertIsNone(parse_domain_line('0.0.0.0 0.0.0.0'))
        self.assertEqual(parse_domain_line('0.0.0.0 1493361689.rsc.cdn77.org'), '1493361689.rsc.cdn77.org')
        self.assertEqual(parse_domain_line('0.0.0.0 123greetings.com  # contains one link to distributor of adware or spyware'), '123greetings.com')

    def test_MalwareDomains(self):
        self.assertIsNone(parse_domain_line(''))
        self.assertEqual(parse_domain_line('amazon.co.uk.security-check.ga'), 'amazon.co.uk.security-check.ga')

    def test_Cameleon(self):
        self.assertIsNone(parse_domain_line('# Last updated : 2018-03-17'))
        self.assertIsNone(parse_domain_line('127.0.0.1        localhost'))
        self.assertEqual(parse_domain_line('127.0.0.1	 0.r.msn.com'), '0.r.msn.com')
        self.assertEqual(parse_domain_line('127.0.0.1        0.r.msn.com'), '0.r.msn.com')

    def test_ZeusTracker(self):
        self.assertIsNone(parse_domain_line('##############################################################################'))
        self.assertEqual(parse_domain_line('039b1ee.netsolhost.com'), '039b1ee.netsolhost.com')

    def test_Disconnect(self):
        self.assertIsNone(parse_domain_line('# Basic tracking list by Disconnect'))
        self.assertEqual(parse_domain_line('bango.combango.org'), 'bango.combango.org')

    def test_Hostsfile(self):
        self.assertIsNone(parse_domain_line('# hpHosts - Ad and Tracking servers only'))
        self.assertIsNone(parse_domain_line('# Hosts: 45737'))
        self.assertEqual(parse_domain_line('127.0.0.1	005.free-counter.co.uk'), '005.free-counter.co.uk')
        self.assertEqual(parse_domain_line('127.0.0.1	118d654612df63bc8395-aecfeaabe29a34ea9a877711ec6d8aed.r37.cf2.rackcdn.com'), '118d654612df63bc8395-aecfeaabe29a34ea9a877711ec6d8aed.r37.cf2.rackcdn.com')

    def test_get_domain_extensions(self):
        domain_extensions = get_domain_extensions()
        self.assertTrue('com' in domain_extensions)
        self.assertTrue('co.uk' in domain_extensions)

    def test_is_domain(self):
        self.assertTrue(is_domain('google.com'))
        self.assertFalse(is_domain('www.google.com'))
        self.assertTrue(is_domain('bbc.co.uk'))

    def test_remove_duplicate_domains(self):
        self.assertEqual(remove_duplicate_domains(['domain.com', 'sub.domain.com']), ['domain.com'])
        self.assertEqual(remove_duplicate_domains(['domain.com', 'otherdomain.com']), ['domain.com', 'otherdomain.com'])

if __name__ == '__main__':
    sys.exit(unittest.main())
