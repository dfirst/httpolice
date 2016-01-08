# -*- coding: utf-8; -*-

from httpolice import common


class HeaderEntry(common.ReportNode):

    self_name = 'header'

    def __init__(self, name, value):
        super(HeaderEntry, self).__init__()
        self.name = name
        self.value = value

    def __repr__(self):
        return '<HeaderEntry %s>' % self.name


class FieldName(common.CaseInsensitive):

    __slots__ = ()


def is_bad_for_trailer(name):
    return known_headers.get_info(name).get('bad_for_trailer')


known_headers = common.Known([
    {
        'name': FieldName('Content-Length'),
        'bad_for_trailer': True,
    },
    {
        'name': FieldName('Transfer-Encoding'),
        'bad_for_trailer': True,
    },
])
