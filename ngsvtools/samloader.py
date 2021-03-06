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
import re

import pysam

from ngsvtools.sam.data.sam import Sam
from ngsvtools.sam.data.chromosome import Chromosome
from ngsvtools.sam.util import trim_chromosome_name
from ngsvtools.exception import AlreadyLoadedError, UnsupportedFileError


def load(filepath, db):
    filename = os.path.basename(filepath)
    base, ext = os.path.splitext(filepath)
    if not re.match('^\.(sam|bam)', ext):
        raise UnsupportedFileError('ERROR: Not supported file format')

    sam_data = Sam(db)
    chr_data = Chromosome(db)

    if sam_data.get_by_filename(filename) is not None:
        raise AlreadyLoadedError('WARNING: Already loaded "%s"' % filename)

    logging.info("Begin to load '%s'" % filename)

    # Convert sam to bam
    if ext == '.sam':
        insam = pysam.Samfile(filepath, 'r')
        filepath = base + '.bam'
        outbam = pysam.Samfile(filepath, 'wb', template=insam)
        for s in insam:
            outbam.write(s)

    # Create index if not exist
    bai = filepath + '.bai'
    if not os.path.isfile(bai):
        logging.info("Create index '%s'" % os.path.basename(bai))
        pysam.index(filepath)

    # load sam
    samfile = pysam.Samfile(filepath)
    sam_data.append(filename,
                    samfile.header, samfile.lengths,
                    samfile.mapped,
                    samfile.nreferences, samfile.references)

    # load chromosome
    for ref in samfile.references:
        chr_data.append(trim_chromosome_name(ref))
