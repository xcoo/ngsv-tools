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
import os.path
import re

import pysam

import ngsvtools.cypileup as cypileup
from ngsvtools.sam.data.sam import Sam
from ngsvtools.sam.data.chromosome import Chromosome
from ngsvtools.sam.util import trim_chromosome_name
from ngsvtools.exception import UnsupportedFileError


def _load_sam(filepath, db):
    filename = os.path.basename(filepath)
    base, ext = os.path.splitext(filepath)

    if not re.match('^\.(sam|bam)', ext):
        raise UnsupportedFileError('ERROR: Not supported file format')

    logging.info("Begin to load '%s'" % filename)

    if ext == '.sam':
        if os.path.isfile(base + '.bam'):
            filepath = base + '.bam'
        else:
            insam = pysam.Samfile(filepath, 'r')
            filepath = base + '.bam'
            outbam = pysam.Samfile(filepath, 'wb', template=insam)
            for s in insam:
                outbam.write(s)

    samfile = pysam.Samfile(filepath)

    return samfile


def load(filepath, db, action=None):
    samfile = _load_sam(filepath, db)

    sam_data = Sam(db)
    chromosome_data = Chromosome(db)

    chromosomes = []
    for ref in samfile.references:
        name = trim_chromosome_name(ref)

        c = chromosome_data.get_by_name(name)
        c['ref'] = ref

        chromosomes.append(c)

    filename = os.path.basename(filepath)
    sam = sam_data.get_by_filename(filename)

    if sam is None:
        logging.error('Error : please load "%s" first' % filename)

    samId = sam['id']

    # cypileup
    cypileup.pileup(samfile, chromosomes, samId, db, action)

    samfile.close()
