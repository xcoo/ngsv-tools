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
import gzip

from ngsvtools.cache import Cache
from ngsvtools.sam.data.chromosome import Chromosome
from ngsvtools.sam.data.cytoband import CytoBand
from ngsvtools.exception import AlreadyLoadedError


def _update_database(fp, cytoband_data, chromosome_data):

    count = 0

    # load cytoband data
    for line in fp:
        cyto_chr, cyto_start, cyto_end, cyto_name, cyto_gie = line[:-1].split('\t')

        c_name = cyto_chr
        c_name = c_name.replace('Chr', '')
        c_name = c_name.replace('chr', '')
        c_name = c_name.replace('.', '')

        c = chromosome_data.get_by_name(c_name)

        if c is None:
            chromosome_data.append(c_name)
            c = chromosome_data.get_by_name(c_name)

        cytoband_data.append(c['id'],
                             long(cyto_start),
                             long(cyto_end),
                             cyto_name,
                             cyto_gie)

        count += 1

        logging.debug("Loaded %d bands\r" % count)

    logging.debug("Loaded %d bands" % count)


def load(db):
    cytoband_data = CytoBand(db)
    chromosome_data = Chromosome(db)

    if cytoband_data.count() > 0:
        raise AlreadyLoadedError('CytoBand is already loaded')

    url = "http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/cytoBand.txt.gz"

    logging.info("Begin to download from %s" % url)

    c = Cache(url)
    c.load()

    logging.info("updating database")

    f = gzip.open(c.name)

    _update_database(f, cytoband_data, chromosome_data)

    f.close()
