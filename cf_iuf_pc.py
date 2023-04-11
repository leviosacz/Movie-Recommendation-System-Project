from modules.cf_iuf_pc import CFIufPC
import pickle
import os

dpath = 'data'
udict = pickle.load(open(os.path.join(dpath, 'udict.pkl'), 'rb'))
mdict = pickle.load(open(os.path.join(dpath, 'mdict.pkl'), 'rb'))
test5 = pickle.load(open(os.path.join(dpath, 'test5.pkl'), 'rb'))
test10 = pickle.load(open(os.path.join(dpath, 'test10.pkl'), 'rb'))
test20 = pickle.load(open(os.path.join(dpath, 'test20.pkl'), 'rb'))

cfip = CFIufPC(udict, mdict)

rpath = 'data/results'
res5 = cfip.cf(test5)
res5.to_csv(os.path.join(rpath, 'result5_cf_iuf_pc.txt'), index=None, header=None, sep=' ')
res10 = cfip.cf(test10)
res10.to_csv(os.path.join(rpath, 'result10_cf_iuf_pc.txt'), index=None, header=None, sep=' ')
res20 = cfip.cf(test20)
res20.to_csv(os.path.join(rpath, 'result20_cf_iuf_pc.txt'), index=None, header=None, sep=' ')