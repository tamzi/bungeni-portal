# ------------------------------------------------------------------------------
import os, os.path, sys, traceback

# ------------------------------------------------------------------------------
class FolderDeleter:
    def delete(dirName):
        '''Recursively deletes p_dirName.'''
        dirName = os.path.abspath(dirName)
        for root, dirs, files in os.walk(dirName, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(dirName)
    delete = staticmethod(delete)

# ------------------------------------------------------------------------------
class Traceback:
    '''Dumps the last traceback into a string.'''
    def get():
        res = ''
        excType, excValue, tb = sys.exc_info()
        tbLines = traceback.format_tb(tb)
        for tbLine in tbLines:
            res += ' %s' % tbLine
        res += ' %s: %s' % (str(excType), str(excValue))
        return res
    get = staticmethod(get)

# ------------------------------------------------------------------------------
