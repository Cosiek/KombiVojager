#!/usr/bin/env python
# encoding: utf-8

import sqlite3


# make a connection
connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()

# chceck if db file has tables already (it cn be a fresh new file)
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='solver_runs'")
if not cursor.fetchone():
    # this seems to be a fresh file - need to create missing tables
    sql = ('CREATE  TABLE "main"."solver_runs" '
            '("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
            '"solver" TEXT, '
            '"task" TEXT, '
            '"time" TEXT, '
            '"cycles" INTEGER, '
            '"solution" TEXT, '
            '"distance" FLOAT, '
            '"timedout" BOOL NOT NULL DEFAULT 0'
           ')'
    )

    cursor.execute(sql)
