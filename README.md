SOS: Simple Objects Storage
===========================

> persistant dictionaries and lists for python

This is ideal for lists or dictionaries which either need persistence,
are too big to fit in memory or both.

There are existing alternatives like `shelve`, which are recommended for the default case.

There main difference with `sos` is that:
- the data is stored in a text format (*)
- it provides both persistent dicts *and* lists
- for dicts, only string keys are allowed
- objects must be json "dumpable" (no cyclic references, etc.)
- it's fast (whereas shelve is rather slow on windows)
- it's synchronous by design: when the function returns, you are sure it has been written on disk
- it's safe: even if the machine crashes in the middle of a big write, data will not be corrupted

(*) ...actually, it's *nearly* plain utf8 as it may contain some invalid utf8 characters in "garbage" bytes

Dictionaries
============

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



Lists
=====

What is it complicated anyway?
------------------------------
Imagine we would store it "in order" in a file:
````
A
B
C
...
```
This would be a disaster,since when we update B to B', we would have to either shift all following items, a no-go.
Or work with indexes:
````
1:A
#obsolete B
3:C
2:B'
...
```
That's already much better, and is the structure we use, thereby using a dictionary underneath.
With the only difference that the keys are ints.

The other difficulty are deletitions. If you remove B', you have to update all indexes following the item.
Going in the file and updating millions of indexes is a no-go too.


How does it work?
-----------------
Using a very simple but efficient trick!
First, new items will always use an autoincrement as key.
Then, a mapping will be used:
list index -> dict key -> value

The way to perform the mapping is utterly simple: it's the sorted keys of the dictionary!

Implementation notes
====================

Why not make it async writes?
-----------------------------
In the original version, there was a switch to choose between sync and async mode.
However, it turned out to have only a relatively small impact on overall performance.
Less than 25% on the hardware/OS/data I tested if I remember right.
Since the benefits seem rather low, I removed the flag and the associated code altogether, 
in order to ensure safety by default.
IMHO, it's preferable to loose a few microseconds rather than data upon a crash.

Why not use memory mapped files?
--------------------------------
I experimented with that too. In my experience, with the hardware/OS/data I tested,
it turned out to ...*suck*. Using memory mapped files lead to inconsistent and unpredictible performance,
often much slower than direct file access.

Why do you read values too when loading?
----------------------------------------
Of course, it could be done much faster if only keys would be read!
However, here as well, I opted for safety first.
The loading takes a couple of seconds more, but at least you know your data is ok,
instead of exploding in your face later at runtime.