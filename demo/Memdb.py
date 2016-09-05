#!/usr/bin/python
#-*- coding: UTF-8 -*-
#
# memdb.py
#   python memory db
#
# 2015-12
########################################################################
# The MIT License (MIT)
#    http://opensource.org/licenses/MIT
#
#  Copyright (c) 2015 copyright cheungmine
#
# Permission is hereby granted, free of charge, to any person obtaining
#  a copy of this software and associated documentation files (the
#  "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject
#  to the following conditions:
#
# The above copyright notice and this permission notice shall be
#  included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
########################################################################
 
from multiprocessing import RLock
 
# sync for threading
class ObjectSync:
    def __init__(self, name):
        self.refcount = 0
        self.synclock = RLock()
        self.keyname = name
 
 
    def Lock(self):
        self.synclock.acquire()
        self.refcount = self.refcount + 1
 
 
    def Unlock(self):
        self.refcount = self.refcount - 1
        self.synclock.release()
 
 
class ObjectSyncFactory:
    def __init__(self):
        self.globalLock = ObjectSync("")
        self.rowlocks = {}
 
 
    def __RemoveLock(self, sem, keyname):
        self.globalLock.Lock()
        self.rowlocks[keyname] = None
        self.globalLock.Unlock()
 
 
    def GetLock(self, tablename, key):
        keyname = tablename + "," + str(key)
        self.globalLock.Lock()
 
        l = None
        try:
            l = self.rowlocks[keyname]
            if l == None:
                self.rowlocks[keyname] = ObjectSync(keyname)
                l = self.rowlocks[keyname]
        except:
            self.rowlocks[keyname] = ObjectSync(keyname)
            l = self.rowlocks[keyname]
 
        self.globalLock.Unlock()
 
        return l
 
 
class PairGuard:
    def __init__(self, factory, sem):
        self.syncfactory = factory
        self.host = sem
        self.host.Lock()
 
 
    def __del__(self):
        self.host.Unlock()
        if self.host.refcount == 0 :
            self.syncfactory._ObjectSyncFactory__RemoveLock(self.host, self.host.keyname)
 
 
########################################
# Database table
class MemTable:
    def __init__(self):
        self.rows = {}
        self.tableLock = ObjectSync("")
 
 
    def GetRowCount(self):
        return len(self.rows)
 
 
    def DeleteAll(self):
        self.tableLock.Lock()
        self.rows = {}
        self.tableLock.Unlock()
 
 
    def __DeleteAll(self):
        self.rows = {}
 
 
    def GetAllValue(self):
        return self.rows
 
 
    # throw KeyError if key not found.
    def GetValue(self, key):
        if(self.rows.get(key) != None):
            return self.rows[key]
        else:
            return None
 
 
    # not exist: Add
    # exist: Update
    def AddValue(self, key, value):
        self.tableLock.Lock()
        self.rows[key] = value
        self.tableLock.Unlock()
 
 
    def __AddValue(self, key, value):
        self.rows[key] = value
 
 
    def DelValue(self, key):
        self.AddValue(key,None)
 
 
    def __DelValue(self, key):
        self._MemTable__AddValue(key, None)

    def AppendValue(self, key, value):
        self.tableLock.Lock()
        if(self.GetValue(key) == None):
            self.rows[key] = []
        self.rows[key].append(value)
        self.tableLock.Unlock()
 
 
    def __AppendValue(self, key, value):
        self.rows[key] = value
 
 
########################################
# MemDB
class MemDB:
    def __init__(self):
        self.tables = {}
        self.syncFactory = ObjectSyncFactory()
 
 
    # is not thread safed
    def CreateTable(self, tablename):
        self.tables[tablename] = MemTable()
 
 
    # is not thread safed
    def DropTable(self, tablename):
        self.tables[tablename] = None
 
 
    def GetValue(self, tablename, key):
        mt = self.tables[tablename]
        PairGuard(self.syncFactory, self.syncFactory.GetLock(tablename, key))
        return mt.GetValue(key)
 
 
    def AddValue(self, tablename, key, value):
        mt = self.tables[tablename]
        PairGuard(self.syncFactory, self.syncFactory.GetLock(tablename, key))
        mt.AddValue(key, value)
 
 
    def DelValue(self, tablename, key):
        mt = self.tables[tablename]
        PairGuard(self.syncFactory, self.syncFactory.GetLock(tablename, key))
        mt.DelValue(key)

    def AppendValue(self,tablename,key,value):
        mt = self.tables[tablename]
        PairGuard(self.syncFactory, self.syncFactory.GetLock(tablename, key))
        mt.AppendValue(key, value)
 
 
    def __GetValue(self, tablename, key):
        mt = self.tables[tablename]
        return mt.GetValue(key)
 
 
    def __AddValue(self, tablename, key, value):
        mt = self.tables[tablename]
        mt._MemTable__AddValue(key, value)
 
 
    def __DelValue(self, tablename, key):
        mt = self.tables[tablename]
        mt._MemTable__DelValue(key)
 
 
class Transaction:
    def __init__(self, conn):
        self.dbconn = conn
        self.logs = []
 
 
    def Commit(self):
        syncs = []
        tables = {}
 
        for p in self.logs:
            tables[p[0]] = True
 
        for name in tables:
            syncTable = self.dbconn.memdb.syncFactory.GetLock(name, 'table')
            syncs.append((syncTable.keyname, syncTable))
 
        syncs.sort()
 
        #lock
        guards = []
        for sync in syncs:
            guards.append(PairGuard(self.dbconn.memdb.syncFactory, sync[1]))
 
        #commit
        self.logs.reverse()
        while True:
            if len(self.logs) == 0:
                break
            p = self.logs.pop()
            self.dbconn.memdb._MemDB__AddValue(p[0], p[1], p[2])
 
        #unlock
        guards.reverse()
        while True:
            if len(guards) == 0:
                break
            guards.pop()
 
        self.dbconn._MemDBConnect__EndTransaction()
 
 
    def Rollback(self):
        self.dbconn._MemDBConnect__EndTransaction()
 
 
    def LogPoint(self, tablename, key, value):
        self.logs.append((tablename, key, value))
 
 
class MemDBConnect:
    def __init__(self, db):
        self.memdb = db
        self.bTransaction = False
        self.trans = None
 
 
    def BeginTransaction(self):
        self.bTransaction = True
        self.trans = Transaction(self)
        return self.trans
 
 
    def __EndTransaction(self):
        self.bTransaction = False
        self.trans = None
 
 
    def CommitTransaction(self):
        if self.bTransaction:
            self.bTransaction = False
            ts = self.trans
            self.trans = None
            if ts:
                ts.Commit()
 
 
    def RollbackTransaction(self):
        if self.bTransaction:
            self.bTransaction = False
            ts = self.trans
            self.trans = None
            if ts:
                ts.Rollback()
 
 
    # not thread safe
    def CreateTable(self, tablename):
        self.memdb.CreateTable(tablename)
 
    # not thread safe
    def DropTable(self, tablename):
        self.memdb.DropTable(tablename)
 
 
    # not thread safe
    def HasTable(self, tablename):
        if self.memdb.tables.get(tablename):
            return True
        else:
            return False
 
 
    def GetValue(self, tablename, key):
        if self.bTransaction:
            return self.memdb._MemDB__GetValue(tablename, key)
        else:
            return self.memdb.GetValue(tablename, key)
 
 
    def AddValue(self, tablename, key, value):
        if self.bTransaction:
            self.trans.LogPoint(tablename, key, value)
        else:
            self.memdb.AddValue(tablename, key, value)
 
 
    def DelValue(self, tablename, key):
        if self.bTransaction:
            self.trans.LogPoint(tablename, key, None)
        else:
            self.memdb.DelValue(tablename, key)
 
 
    def QueryTablesNothrow(self):
        tables = []
        try:
            self.BeginTransaction()
 
            for tablename,_ in self.memdb.tables.items():
                tables.append(tablename)
 
            self.CommitTransaction()
        except:
            tables = []
            self.RollbackTransaction()
        finally:
            return tables
 
 
    def QueryTableKeysNothrow(self, tablename):
        keys = []
        try:
            self.BeginTransaction()
 
            if self.HasTable(tablename):
                rows_dict = self.memdb.tables[tablename].rows
                for key, _ in rows_dict.items():
                    keys.append(key)
 
            self.CommitTransaction()
        except:
            keys = []
            self.RollbackTransaction()
        finally:
            return keys
 
 
    def CreateTableNothrow(self, tablename):
        try:
            self.BeginTransaction()
 
            if not self.HasTable(tablename):
                self.memdb.CreateTable(tablename)
                self.CommitTransaction()
        except:
            self.RollbackTransaction()
        finally:
            pass
 
 
    def DropTableNothrow(self, tablename):
        try:
            self.BeginTransaction()
 
            if self.HasTable(tablename):
                self.memdb.DropTable(tablename)
                self.CommitTransaction()
        except:
            self.RollbackTransaction()
        finally:
            pass
 
 
    def GetValueNothrow(self, tablename, key, defaultvalue):
        result = defaultvalue
        try:
            self.BeginTransaction()
 
            result = self.GetValue(tablename, key)
 
            self.CommitTransaction()
        except:
            self.RollbackTransaction()
        finally:
            return result
 
 
    def AddValueNothrow(self, tablename, key, value):
        result = False
        try:
            self.BeginTransaction()
 
            self.AddValue(tablename, key, value)
 
            self.CommitTransaction()
 
            result = True
        except:
            self.RollbackTransaction()
        finally:
            return result
 
 
    def DelValueNothrow(self, tablename, key):
        result = False
        try:
            self.BeginTransaction()
 
            self.DelValue(tablename, key)
 
            self.CommitTransaction()
 
            result = True
        except:
            self.RollbackTransaction()
        finally:
            return result
 
 
    def AppendValueListNothrow(self, tablename, key, value, non_repeated_value):
        try:
            self.BeginTransaction()
 
            if self.HasTable(tablename):
                try:
                    values = self.GetValue(tablename, key)
 
                    if non_repeated_value:
                        if value not in values:
                            values.append(value)
                            self.AddValue(tablename, key, values)
                    else:
                        values.append(value)
                        self.AddValue(tablename, key, values)
                except KeyError:
                    self.AddValue(tablename, key, [value])
                finally:
                    self.CommitTransaction()
        except:
            self.RollbackTransaction()
        finally:
            pass
 
 
    def AppendValueListMultiNothrow(self, tablenames, keys, values, non_repeated_values):
        try:
            self.BeginTransaction()
 
            for i in range(0, len(tablenames)):
                t, k, v, nrv = tablenames[i], keys[i], values[i], non_repeated_values[i]
 
                if self.HasTable(t):
                    try:
                        vals = self.GetValue(t, k)
 
                        if nrv:
                            if v not in vals:
                                vals.append(v)
                                self.AddValue(t, k, vals)
                        else:
                            vals.append(v)
                            self.AddValue(t, k, vals)
                    except KeyError:
                        self.AddValue(t, k, [v])
 
            self.CommitTransaction()
        except:
            self.RollbackTransaction()
        finally:
            pass

def test():
    db = MemDB()
    tname = "table1"
    db.CreateTable(tname)
    #print(db.GetValue(tname, 1))
    #for i in range(100000):
    #    db.AddValue(tname,i,"sdfsd")
    db.AppendValue(tname, 1,{1:1,2:2,3:3})
    db.AppendValue(tname, 1,{1:1,2:2,3:3})
    db.AppendValue(tname, 1,{1:1,2:2,3:3})
    print(db.GetValue(tname, 1))
    #db.GetValue(tname, 1).append({1:1,2:2,3:3})
    #db.GetValue(tname, 1).append({1:1,2:2,3:3})
    #print(db.GetValue(tname, 1))
 
    db.AddValue(tname,11,"dddddd")
    print(db.GetValue(tname,11))
 
    db.AddValue(tname,12,"dsfdsfd")
    print(db.GetValue(tname,12))
 
    conn = MemDBConnect(db)
    t = conn.BeginTransaction()
    for i in range(100000):
        conn.AddValue(tname,i,"sdfsd")
    conn.AddValue(tname,12,"sfdas")
    conn.AddValue(tname,12,"ddddd")
    t.Commit()
    print(db.GetValue(tname,12))

test()