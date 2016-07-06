import pysos

pysos.csv2sos('../data/omdb.txt', encoding='Windows-1252')
exit()
#data = open('../data/omdb.txt', 'rb').read(10*1024*1024)
#data = open('temp.sos_dict', 'rb').read(1024*1024)

#import chardet
#print(chardet.detect(data))

#print(data[669-500:669+20])
#print(data[179988919-500:179988919+20])

#exit()

encs = [
'UTF-8',
'UTF-16LE',
'UTF-16BE',
'ISO-8859-1',
'Windows-1251',
'Shift JIS',
'Windows-1252',
'GB2312',
'EUC-KR',
'EUC-JP',
'GBK',
'ISO-8859-2',
'ISO-8859-15',
'Windows-1250',
'Windows-1256',
'ISO-8859-9',
'Big5',
'Windows-1254'
]

encs = [
'Windows-1252',
'UTF-8',
'ISO-8859-1'
]

#n = data.count(b'\ufffd')

#data2 = rrr(data)
#diff = len(data) - len(data2)
#perc = 100 * diff / len(data)
#print('> %d = %.3f%%' % (diff, perc))



for e in encs:
    try:
        #dec = data.decode(e)
        #print('Decoding success: ' + e)
        dec = data.decode(e, 'replace')
        enc = dec.encode('utf-8')
        #print('Decoding success: %s \t %d ?' % (e, dec.count('\ufffd')) )
        print('%16s \t %8d E \t %8d L' % (e, dec.count('\ufffd'), len(enc) - len(data) ) )
    except UnicodeDecodeError as ex:
        print('Decoding failure: ' + str(ex))