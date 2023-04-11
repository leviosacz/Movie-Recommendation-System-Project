from modules.cf_item import CFItem
import pickle
import os

dpath = 'data'
udict = pickle.load(open(os.path.join(dpath, 'udict.pkl'), 'rb'))
mdict = pickle.load(open(os.path.join(dpath, 'mdict.pkl'), 'rb'))
test5 = pickle.load(open(os.path.join(dpath, 'test5.pkl'), 'rb'))
test10 = pickle.load(open(os.path.join(dpath, 'test10.pkl'), 'rb'))
test20 = pickle.load(open(os.path.join(dpath, 'test20.pkl'), 'rb'))

cfi = CFItem(udict, mdict)

rpath = 'data/results'
res5 = cfi.cf(test5, k=5)
res5.to_csv(os.path.join(rpath, 'result5_cf_item.txt'), index=None, header=None, sep=' ')
res10 = cfi.cf(test10, k=10)
res10.to_csv(os.path.join(rpath, 'result10_cf_item.txt'), index=None, header=None, sep=' ')
res20 = cfi.cf(test20, k=20)
res20.to_csv(os.path.join(rpath, 'result20_cf_item.txt'), index=None, header=None, sep=' ')