import pandas as pd
import pickle
import os
from tqdm import tqdm
import math

dpath = 'data'

def load_test(fname, output):
    df = pd.read_csv(os.path.join(dpath, fname), sep=' ', header=None, names=['uid', 'mid', 'rating'])

    test = {}
    for uid, mid, rating in df.values:
        if uid not in test:
            test[uid] = {
                'rated': {},
                'to_predict': []
            }
        if rating != 0:
            test[uid]['rated'][mid] = rating
        else:
            test[uid]['to_predict'].append(mid)
    
    for uid, uinfo in test.items():
        uinfo['avg'] = sum(uinfo['rated'].values()) / len(uinfo['rated'])
    
    pickle.dump(test, open(os.path.join(dpath, output), 'wb'))
    return test

train = pd.read_csv(os.path.join(dpath, 'train.txt'), sep=' ', header=None, names=['uid', 'mid', 'rating'])
udict = {}
mdict = {}
for uid, mid, rating in train.values:
    if uid not in udict:
        udict[uid] = {
            'rated': {}
        }
    udict[uid]['rated'][mid] = rating

    if mid not in mdict:
        mdict[mid] = {
            'rated': {},
            'dev': {'like': {}, 'dislike': {}},
            'dev_len': {'like': {}, 'dislike': {}}
        }
    mdict[mid]['rated'][uid] = rating
    assert(rating >= 1 and rating <= 5)

for uid, uinfo in udict.items():
    uinfo['avg'] = sum(uinfo['rated'].values()) / len(uinfo['rated'])

for mid, minfo in mdict.items():
    minfo['avg'] = sum(minfo['rated'].values()) / len(minfo['rated'])
    minfo['IUF'] = math.log2(len(udict) / len(minfo['rated']))


all_mid = list(mdict.keys())
mid_len = len(all_mid)
for i in tqdm(range(mid_len - 1)):
    for j in range(i + 1, mid_len):
        m1_id = all_mid[i]
        m1_info = mdict[m1_id]
        m2_id = all_mid[j]
        m2_info = mdict[m2_id]

        dev_12_like = []
        dev_12_dislike = []
        for uid, m1_rate in m1_info['rated'].items():
            m1_like = m1_info['rated'][uid] >= udict[uid]['avg']
            if uid in m2_info['rated']:
                m2_like = m2_info['rated'][uid] >= udict[uid]['avg']
                if m1_like and m2_like:
                    dev_12_like.append(m1_rate - m2_info['rated'][uid])
                elif not m1_like and not m2_like:
                    dev_12_dislike.append(m1_rate - m2_info['rated'][uid])
        
        interlen_like = len(dev_12_like)
        if interlen_like > 0:
            dev_12_like = sum(dev_12_like) / interlen_like
            mdict[m1_id]['dev']['like'][m2_id] = dev_12_like
            mdict[m1_id]['dev_len']['like'][m2_id] = interlen_like
            mdict[m2_id]['dev']['like'][m1_id] = -dev_12_like
            mdict[m2_id]['dev_len']['like'][m1_id] = interlen_like

        interlen_dislike = len(dev_12_dislike)
        if interlen_dislike > 0:
            dev_12_dislike = sum(dev_12_dislike) / interlen_dislike
            mdict[m1_id]['dev']['dislike'][m2_id] = dev_12_dislike
            mdict[m1_id]['dev_len']['dislike'][m2_id] = interlen_dislike
            mdict[m2_id]['dev']['dislike'][m1_id] = -dev_12_dislike
            mdict[m2_id]['dev_len']['dislike'][m1_id] = interlen_dislike


test5 = load_test('test5.txt', 'test5.pkl')
test10 = load_test('test10.txt', 'test10.pkl')
test20 = load_test('test20.txt', 'test20.pkl')

pickle.dump(udict, open(os.path.join(dpath, 'udict.pkl'), 'wb'))
pickle.dump(mdict, open(os.path.join(dpath, 'mdict.pkl'), 'wb'))

print(
    'udict_len =', len(udict), 
    'mdict_len =', len(mdict), 
    'test5_len =', len(test5), 
    'test10_len =', len(test10), 
    'test20_len =', len(test20)
)