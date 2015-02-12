"""         @author:            Guang Yang
            @mktime:            2/3/2015
            @description:       support functions for front-end API
"""
import time
import random


def random_hex_color():
    """ Generates a random hex color to be used in HTML """
    return "#" + "".join([random.choice('0123456789ABCDEF') for x in range(6)])


def mktime_to_ms(mktime):
    """ Converts a time.mktime() into miliseconds (from 1970/1/1) so
    it can be used in highchart
    """

    epoch_sec = time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))
    # converting second (from mktime) to milisecond
    time_in_ms = 1000*int(mktime - epoch_sec)
    return time_in_ms
