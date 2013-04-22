# NGSV Tools

Python modules and command line tools for accessing database of NGSV.

# Requirements

* Python (v2.7)
    * pysam (>= v0.7)
    * MySQL-python
    * Cython
* MySQL

# Usage

## 1. Install ngsv-tools

```
$ python setup.py install
```

## 2. Create database

ngsv uses MySQL database.
First, create database.

```
$ ngsv initdb [--dbuser DBUSER] [--dbpassword DBPASSWORD]
```

## 3. Load genome data into the database

### Load sam/bam files

```
$ ngsv loadsam [--dbuser DBUSER] [--dbpassword DBPASSWORD] samfile1 samfile2 ...
```

### Load bed files

```
$ ngsv loadbed [--dbuser DBUSER] [--dbpassword DBPASSWORD] bedfile1 bedfile2 ...
```

### Load cytoband data

```
$ ngsv loadcytoband [--dbuser DBUSER] [--dbpassword DBPASSWORD]
```

### Load refgenes data

```
$ ngsv loadrefgene [--dbuser DBUSER] [--dbpassword DBPASSWORD]
```

## Help

You can see more detail usage by `-h` option.

# License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
