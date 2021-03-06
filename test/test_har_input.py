# -*- coding: utf-8; -*-

import os

from httpolice.inputs.har import har_input
from httpolice.known import m
from httpolice.structure import Unavailable, http11, http2


def load_from_file(name):
    path = os.path.join(os.path.dirname(__file__), 'har_data', name)
    return list(har_input([path]))


def test_http2bin_chrome():
    exchanges = load_from_file('http2bin_chrome.har')

    assert exchanges[0].request.version is None
    assert exchanges[0].responses[0].version is None
    assert exchanges[0].responses[0].body is Unavailable

    assert exchanges[1].request.target == u'https://http2bin.org/encoding/utf8'
    assert not exchanges[1].responses[0].reason

    assert exchanges[4].responses[0].body == b''

    assert exchanges[10].request.body is Unavailable
    assert exchanges[10].request.decoded_body is Unavailable
    assert exchanges[10].request.unicode_body == (u'custname=qwedqwed&'
                                                  u'custtel=dqwedwe&'
                                                  u'custemail=&'
                                                  u'size=medium&'
                                                  u'delivery=&'
                                                  u'comments=')


def test_http2bin_firefox():
    exchanges = load_from_file('http2bin_firefox.har')

    assert exchanges[0].request.version == http2
    assert exchanges[0].responses[0].body is Unavailable
    assert exchanges[0].responses[0].decoded_body is Unavailable
    assert exchanges[0].responses[0].unicode_body[:5] == u'{\n  "'
    assert exchanges[0].responses[0].json_data['url'] == \
        u'https://http2bin.org/get'

    assert exchanges[5].responses[0].body == b''
    assert exchanges[5].responses[0].decoded_body == b''
    assert exchanges[5].responses[0].unicode_body == u''

    assert exchanges[7].responses[0].body is Unavailable
    assert len(exchanges[7].responses[0].decoded_body) == 1024

    assert exchanges[10].request.body is Unavailable
    assert exchanges[10].request.decoded_body is Unavailable
    assert exchanges[10].request.unicode_body == (u'custname=ferferf&'
                                                  u'custtel=rfwrefwerf&'
                                                  u'custemail=&'
                                                  u'size=medium&'
                                                  u'delivery=&'
                                                  u'comments=')


def test_spdy_chrome():
    exchanges = load_from_file('spdy_chrome.har')
    assert exchanges[0].request.version is None
    assert exchanges[0].responses[0].version is None
    assert exchanges[1].request.version is None
    assert exchanges[1].responses[0].version is None


def test_spdy_firefox():
    exchanges = load_from_file('spdy_firefox.har')
    assert exchanges[0].responses[0].version is None
    assert exchanges[1].responses[0].version is None


def test_xhr_chrome():
    exchanges = load_from_file('xhr_chrome.har')
    assert exchanges[0].request.target == u'/put'
    assert exchanges[0].request.version == http11
    assert exchanges[0].responses[0].version == http11
    assert exchanges[0].request.body is Unavailable
    assert exchanges[0].request.decoded_body is Unavailable
    assert exchanges[0].request.unicode_body == u'wrfqerfqerferg45rfrqerf'
    assert exchanges[0].responses[0].body is Unavailable
    assert exchanges[0].responses[0].decoded_body is Unavailable
    assert exchanges[0].responses[0].unicode_body[:5] == u'{\n  "'
    assert exchanges[0].responses[0].json_data['data'] == \
        u'wrfqerfqerferg45rfrqerf'


def test_xhr_firefox():
    exchanges = load_from_file('xhr_chrome.har')
    assert exchanges[0].request.target == u'/put'
    assert exchanges[0].request.version == http11
    assert exchanges[0].responses[0].version == http11


def test_httpbin_edge():
    exchanges = load_from_file('httpbin_edge.har')

    assert exchanges[0].request.target == u'/get'
    assert exchanges[0].request.version is None
    assert exchanges[0].responses[0].version is None
    assert exchanges[0].responses[0].body is Unavailable
    assert exchanges[0].responses[0].json_data['url'] == \
        u'http://httpbin.org/get'

    assert u'Unicode Demo' in exchanges[1].responses[0].unicode_body

    assert exchanges[4].responses[0].body == b''
    assert exchanges[5].responses[0].body == b''


def test_xhr_edge():
    exchanges = load_from_file('xhr_edge.har')
    assert exchanges[1].request.method == m.DELETE
    assert exchanges[1].request.body == b''
    assert exchanges[2].request.method == u'FOO-BAR'
