from modules.comb_modules import CombModules
import pickle
import os

dpath = 'data'
udict = pickle.load(open(os.path.join(dpath, 'udict.pkl'), 'rb'))
mdict = pickle.load(open(os.path.join(dpath, 'mdict.pkl'), 'rb'))
test5 = pickle.load(open(os.path.join(dpath, 'test5.pkl'), 'rb'))
test10 = pickle.load(open(os.path.join(dpath, 'test10.pkl'), 'rb'))
test20 = pickle.load(open(os.path.join(dpath, 'test20.pkl'), 'rb'))

cm = CombModules(udict, mdict)

rpath = 'data/results'
res5 = cm.cf(test5)
res5.to_csv(os.path.join(rpath, 'result5_comb_modules.txt'), index=None, header=None, sep=' ')
res10 = cm.cf(test10)
res10.to_csv(os.path.join(rpath, 'result10_comb_modules.txt'), index=None, header=None, sep=' ')
res20 = cm.cf(test20)
res20.to_csv(os.path.join(rpath, 'result20_comb_modules.txt'), index=None, header=None, sep=' ')