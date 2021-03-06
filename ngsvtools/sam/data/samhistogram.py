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

from sql import *


class SamHistogram:

    def __init__(self, db):

        self.db = db

    def get_by_samid(self, samId):

        sql = u"SELECT sam_id, binsize, sam_histogram_id FROM sam_histogram WHERE sam_id = '%d' ORDER BY created_date DESC LIMIT 1" % samId

        result = self.db.execute(sql)

        if len(result) > 0:
            return {'id': result[0][0],
                    'size': result[0][1],
                    'hist_id': result[0][2]}
        else:
            return None

    def get_by_samid_binSize(self, samId, binSize):

        sql = u"SELECT sam_id, binsize, sam_histogram_id FROM sam_histogram WHERE sam_id = '%d' AND binsize = '%d' ORDER BY created_date DESC LIMIT 1" % (samId, binSize)

        result = self.db.execute(sql)

        if len(result) > 0:
            return {'id': result[0][0],
                    'size': result[0][1],
                    'hist_id': result[0][2]}
        else:
            return None

    def append(self, samId, binSize):

        sql = u"INSERT INTO sam_histogram (sam_id, binsize, created_date) VALUES (%d, %d, %d)" % (samId, binSize, get_time())

        self.db.execute(sql)
