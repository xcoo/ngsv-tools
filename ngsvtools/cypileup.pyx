# -*- coding: utf-8 -*-

#
#   ngsv-tools
#   http://github.com/xcoo/ngsv-tools
#   Copyright (C) 2012-2013, Xcoo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import absolute_import

import logging

from ngsvtools.sam.data.samhistogram import SamHistogram
from ngsvtools.sam.data.histogrambin import HistogramBin
from ngsvtools.action import HistogramLoaderAction


cdef class Bin:

    cdef int size
    cdef int sum
    cdef int hist_id
    cdef int pos

    def __init__(self, size):
        self.size = size
        self.sum = 0
        self.hist_id = 0
        self.pos = 0


def pileup(samfile, chromosomes, samId, db, action=None):
    cdef tuple bins
    cdef int bufsize
    cdef Bin b

    sam_hist = SamHistogram(db)
    hist_bin = HistogramBin(db)

    bins = (Bin(100), Bin(10000), Bin(1000000))

    bufsize = 10000

    for b in bins:
        sam_hist.append(samId, b.size)
        b.hist_id = sam_hist.get_by_samid_binSize(samId, b.size)['hist_id']

    for i, c in enumerate(chromosomes):

        logging.debug('Load HistogramBin: ChrID %2d, ChrName %s' % (c['id'],
                                                                    c['name']))

        for p in samfile.pileup(str(c['ref'])):

            for b in bins:
                if b.size == 1:
                    hist_bin.appendbuf(b.hist_id, p.n, p.pos, c['id'])
                    if hist_bin.lenbuf() >= bufsize:
                        hist_bin.flush()
                else:
                    if p.pos >= b.pos + b.size:
                        hist_bin.appendbuf(b.hist_id, b.sum, b.pos, c['id'])

                        if hist_bin.lenbuf() >= bufsize:
                            hist_bin.flush()

                        b.sum = 0
                        b.pos = p.pos / b.size * b.size

                    b.sum += p.n

        for b in bins:
            if b.sum != 0:
                hist_bin.appendbuf(b.hist_id, b.sum, b.pos, c['id'])

        hist_bin.flush()

        for b in bins:
            b.sum = 0
            b.pos = 0

        if action is not None:
            act = action()
            if isinstance(act, HistogramLoaderAction):
                progress = (i + 1) * 100 / len(chromosomes)
                act(progress)
