#!/usr/bin/env python

import datetime

class USTime(datetime.tzinfo):
    def __init__(self, dude, letter):
        self.dude = dude
        self.letter = letter

    def utcoffset(self, dt):
        return datetime.timedelta(hours=-self.dude) + self.dst(dt)

    def dst(self, dt):
        dst_start = datetime.datetime(2008, 11, 2)
        dst_end = datetime.datetime(2009, 3, 8)

        if dst_start <= dt.replace(tzinfo=None) < dst_end:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(hours=0)

    def tzname(self, dt):
        if self.dst(dt) == datetime.timedelta(hours=0):
            return self.letter + "ST"
        else:
            return self.letter + "DT"

eastern_time = USTime(4, 'E')
pacific_time = USTime(7, 'P')
