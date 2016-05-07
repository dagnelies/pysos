"""SOS: Simple Objects Storage / persistant dictionary.

This is ideal for dictionaries which either need persistence,
are too big to fit in memory or both. It's high performance and supports
both synchronous and asynchronous modes.

The keys have a max size of 2^16 bytes (~65kb) and the values are limited to 2^32 bytes (~4Gb).


How is the file structured?
---------------------------

Like json, but with commented lines:
```
# comment line
"key":"value"
"content":["arbitrary JSON",123,true,null,["sub-list"],{"key":"value"}]
"encoding":"UTF-8"
# commenting lines is useful to mark deleted items
# instead of rewriting a huge file
"foo":123
# empty lines are not allowed
```

How does it work?
-----------------

Two structures are kept in memory:
- a dictionary "key -> file offset"
- a list of free buckets (size, file offset), sorted by size

When an item is added, the best fitting bucket is looked up.
Or, if there is none, it's put at the end.

When an item is removed, simply set it's key size to 0 to mark it as deleted and add the bucket's (size,offset) to the "free list".

When an item is updated, we *NEVER* update the value in place.
Why not? Because if process is killed in the middle of the write, you'll have inconsistent data.
It'll contain a portion of the new value, and the remainder of the old value.
Therefore, we'll play it safe: write the new item, and when it's done, remove the old one.

In order to ensure proper consistency, it is therefore important to write the key size (marking it valid) at the very last.


What happens in case of a crash?
--------------------------------

By simply reading the file, we can build both the (key -> offset) index and the free buckets list on the fly.
And since we always add/update values safely by marking it valid at the end, we can ensure their consistency.

...as a last comment: when a bucket is filled with a smaller content, the remaining space becomes a new bucket.
...except if it's too small to be worthwhile (< 20 bytes). Here also, first write the new bucket, then resize the old one!


How does caching work?
----------------------

The cache is divided into two parts:
- new generation
- old generation

When a lookup occurs, the new generation is looked up.
- if exists: return it
- if not: the old one is looked up.
    - if exists: get it from old and put it in new
    - if not: fetch it from disk and put it in new
    - if new generation cache reaches size limit:
        - old generation = new generation 
        - new generation = {}

When the old cache is discarded, it therefore contain entries other than the last N fetched ones.

The alternative would be to use timestamps/counters and sweep through the cache.
However, this may be slow for large caches.
"""

import io
import os.path
import bisect
try:
    import ujson as json
except:
    import json
# import mmap

def _parseLine(line):
    #print(line)
    dic = json.loads( '{' + line.decode('UTF-8') + '}' )
    return dic.popitem()

    
class FileDict:
    START_FLAG = b'# FILE-DICT v1\n'
    def __init__(self, path, async=False):
        self.path = path
        self.async = async
        if os.path.exists(path):
            file = io.open(path, 'r+b')
        else:
            file = io.open(path, 'w+b')
            file.write( self.START_FLAG )
            file.flush()
        
        # mmaps appear to have inconsistent performance, often slower
        # file = mmap.mmap(file.fileno(),0)
        
        self._file = file
        self._offsets = {}
        # the (size, offset) of the lines, where size is in bytes, including the trailing \n
        self._free_lines = []
        
        offset = 0
        while True:
            line = file.readline()
            if line == b'': # end of file
                break
            
            # ignore empty lines
            if line == b'\n':
                offset += len(line) 
                continue
            
            if line[0] == 35: # 35 is the '#' character
                if len(line) > 5:
                #if self._isWorthIt( len(line) ):
                    self._free_lines.append( (len(line), offset) )
            else:
                # let's parse the value as well to be sure the data is ok
                (key,value) = _parseLine(line)
                self._offsets[key] = offset
            
            offset += len(line) 
            
        self._free_lines.sort()
        print("free lines: " + str(len(self._free_lines)))
        
    def _freeLine(self, offset):
        self._file.seek(offset)
        self._file.write(b'#')
        size = 1
        # let's be clean and avoid cutting unicode chars in the middle
        while self._file.peek(1)[0] & 0x80 == 0x80: # it's a continuation byte
            self._file.write(b'.')
            size += 1
        if not self.async:
            self._file.flush()
        line = self._file.readline()
        size += len(line)
        if size > 5:
        #if self._isWorthIt(size):
            bisect.insort(self._free_lines, (len(line)+1, offset) )
        
    def _findLine(self, size):
        index = bisect.bisect( self._free_lines, (size,0) )
        if index >= len( self._free_lines ):
            return None
        else:
            return self._free_lines.pop(index)
        
    def _isWorthIt(self, size):
        # determines if it's worth to add the free line to the list
        # we don't want to clutter this list with a large amount of tiny gaps
        return (size > 5 + len(self._free_lines))
        
    def __getitem__(self, key):
        offset = self._offsets[key]
        self._file.seek(offset)
        line = self._file.readline()
        item = _parseLine(line)
        return item[1]
        
    def __setitem__(self, key, value):
        if key in self._offsets:
            # to be removed once the new value has been written
            old_offset = self._offsets[key]
        else:
            old_offset = None
        
        line = json.dumps(key,ensure_ascii=False) + ':' + json.dumps(value,ensure_ascii=False) + '\n'
        line = line.encode('UTF-8')
        size = len(line)
        
        found = self._findLine(size)

        if found:
            # great, we can recycle a commented line
            (place, offset) = found
            self._file.seek(offset)
            diff = place - size
            # if diff is 0, we'll override the line perfectly:        XXXX\n -> YYYY\n
            # if diff is 1, we'll leave an empty line after:          XXXX\n -> YYY\n\n
            # if diff is > 1, we'll need to comment out the rest:     XXXX\n -> Y\n#X\n (diff == 3)
            if diff > 1:
                line += b'#'
                if diff > 5:
                #if self._isWorthIt( diff ):
                    # it's worth to reuse that space
                    bisect.insort(self._free_lines, (diff, offset + size) )
                
        else:
            # go to end of file
            self._file.seek(0, os.SEEK_END)
            offset = self._file.tell()
            #   > for mmap
            # self._file.resize(offset + size)
            #   > or add a bigger chunk at once
            # line += b'#'
            # chunk = 1024 * 1024
            # self._file.resize(offset + size + chunk)
            # bisect.insort(self._free_lines, (chunk, offset + size) )
        
        
        if self.async:
            self._file.write(line)
        else:
            # if it's a really big line, it won't be written at once on the disk
            # so until it's done, let's consider it a comment
            self._file.write(b'#' + line[1:])
            if line[-1] == 35:
                # let's be clean and avoid cutting unicode chars in the middle
                while self._file.peek(1)[0] & 0x80 == 0x80: # it's a continuation byte
                    self._file.write(b'.')
            self._file.flush()
            # now that everything has been written...
            self._file.seek(offset)
            self._file.write(b'"')
            self._file.flush()
        
        # and now remove the previous entry
        if old_offset:
            self._freeLine(old_offset)
        
        self._offsets[key] = offset
            
        
    def __delitem__(self, key):
        offset = self._offsets[key]
        self._freeLine(offset)
        del self._offsets[key]
        
        
    def __contains__(self, key):
        return (key in self._offsets)
    
    def keys(self):
        return self._offsets.keys()
    
    def __iter__(self):
        offset = 0
        while True:
            # if somethig was read/written while iterating, the stream might be positioned elsewhere
            if self._file.tell() != offset:
                self._file.seek(offset) #put it back on track
            
            line = self._file.readline()
            if line == b'': # end of file
                break
            
            offset += len(line)
            # ignore empty and commented lines
            if line == b'\n' or line[0] == 35:
                continue
            yield _parseLine(line)
            
    def __len__(self):
        return len(self._offsets)
        

    
    def size(self):
        self._file.size()
        
    def flush(self):
        self._file.flush()
        
    def close(self):
        self._file.close()
        print("free lines: " + str(len(self._free_lines)))

