# -*- coding: utf-8 -*-

#
#   ngsv-console
#   http://github.com/xcoo/ngsv-console
#   Copyright (C) 2012, Xcoo, Inc.
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
import os.path

import ngsvtools.pybed as pybed
from ngsvtools.sam.data.chromosome import Chromosome
from ngsvtools.sam.data.bed import Bed
from ngsvtools.sam.data.bedfragment import BedFragment
from ngsvtools.exception import AlreadyLoadedError, UnsupportedFileError
from ngsvtools.action import BedLoaderAction


def load(filepath, db, action=None):

    filename = os.path.basename(filepath)

    file_ext = filename.split('.')[-1]
    if file_ext != 'bed':
        raise UnsupportedFileError('ERROR: Not supported file format')

    bed_data = Bed(db)
    chr_data = Chromosome(db)
    bed_fragment_data = BedFragment(db)

    if bed_data.get_by_filename(filename) is not None:
        raise AlreadyLoadedError('WARNING: Already loaded "%s"' % filename)

    logging.info("Begin to load '%s'" % filename)

    # load bed
    bedfile = pybed.BedReader(open(filepath, 'r'))

    bed_data.append(filename, "", "", 0, 0)

    bed = bed_data.get_by_filename(filename)

    # load bed fragments
    count = 0

    for line in bedfile.yield_lines():
        b = bedfile.get_line(line)

        c_name = b['chrom']
        c_name = c_name.replace('Chr', '')
        c_name = c_name.replace('chr', '')
        c_name = c_name.replace('.', '')

        c = chr_data.get_by_name(c_name)

        if c is None:
            chr_data.append(c_name)
            c = chr_data.get_by_name(c_name)

        if bed['rgb'] == 0:
            rgb = b['itemRgb'].split(',')
            if len(rgb) == 3:
                [ir, ig, ib] = map(long, b['itemRgb'].split(','))
            else:
                [ir, ig, ib] = [0, 0, 0]
        else:
            [ir, ig, ib] = [0, 0, 0]

        if b['strand'] == '+':
            strand = 0
        elif b['strand'] == '-':
            strand = 1
        else:
            strand = -1

        bed_fragment_data.append(bed['id'], c['id'],
                                 long(b['chromStart']),
                                 long(b['chromEnd']),
                                 b['name'],
                                 long(b['score']),
                                 strand,
                                 long(b['thickStart']),
                                 long(b['thickEnd']),
                                 ir, ig, ib,
                                 long(b['blockCount']),
                                 b['blockSizes'],
                                 b['blockStarts'])

        count += 1

        if bedfile.length >= 100 and count % (bedfile.length / 100) == 0:
            if action is not None:
                act = action()
                if isinstance(act, BedLoaderAction):
                    progress = (count + 1) * 100 / bedfile.length
                    act(progress)

    logging.debug('Loaded %d fragments' % count)
