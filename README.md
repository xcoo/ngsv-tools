# NGSV Tools

Python modules and command line tools for accessing database of NGSV.

# Requirements

* Python (v2.7)
    * pysam (>= v0.7)
    * MySQL-python
    * Cython
* MySQL

# Usage

## Create database

ngsv uses MySQL database.
First, create database.

```
$ cd db
$ mysql -u root -p < ngsv.sql
```

## Install ngsv-tools

```
$ python setup.py install
```

# License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
