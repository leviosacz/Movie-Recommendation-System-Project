from tqdm import tqdm
import math
import pandas as pd

class CFItem:

    def __init__(self, udict: dict, mdict: dict):
        self.udict = udict
        self.mdict = mdict
        self.smooth_para = 3
    
    def cf(self, testdata: dict, round_=True, k=20, sim=0.2):
        res = []

        for uid, uinfo in tqdm(testdata.items()):

            for mid in uinfo['to_predict']:
                # calculate weights and store them in wl(weight list)
                wl = []
                for knownmid in uinfo['rated']:
                    w = self.cal_weight(mid, knownmid)
                    if w != 0:
                        wl.append([w, knownmid])

                # sort weights by absolute values in descending order
                swl = sorted(wl, key=lambda x: abs(x[0]), reverse=True)

                # predict
                rate = self.cal_rate(mid, swl, uinfo, k, sim)

                if round_:
                    rate = round(rate)
                    if rate < 1:
                        rate = 1
                    if rate > 5:
                        rate = 5
                res.append([uid, mid, rate])
        
        df = pd.DataFrame(sorted(res, key=lambda x: (x[0], x[1])), columns=['uid', 'mid', 'ratings'])
        return df
    
    def cal_rate(self, mid, swl, testuinfo, k, sim, print_=False):
        topwl = []
        toprl = []
        for mweight, knownmid in swl:
            # when we use adaptive k based on the ground similarity
            # if abs(uweight) < sim:
            #     break

            topwl.append(mweight)
            # use Pearson Correlation
            toprl.append(testuinfo['rated'][knownmid] - testuinfo['avg'])

            # when we use fixed k
            if len(topwl) >= k:
               break

        # if no similar one
        if len(topwl) == 0:
            if mid in self.mdict:
                rate = self.mdict[mid]['avg']
            else:
                rate = 3
        else:
            # use Pearson Correlation
            rate = (self.inner_product(topwl, toprl) / sum([abs(n) for n in topwl])) + testuinfo['avg']
        
        if print_:
            print(mid)
            print(topwl, toprl, rate)

        return rate

    
    def cal_weight(self, predmid, knownmid):
        if predmid not in self.mdict or knownmid not in self.mdict:
            return 0

        intersect = []
        for uid in self.mdict[knownmid]['rated']:
            if uid in self.mdict[predmid]['rated']:
                intersect.append(uid)
        
        if len(intersect) == 0:
            return 0
        
        knownrate = []
        predrate = []
        for uid in intersect:
            knownrate.append(self.mdict[knownmid]['rated'][uid] - self.udict[uid]['avg'])
            predrate.append(self.mdict[predmid]['rated'][uid] - self.udict[uid]['avg'])
        
        # smoothing, using self.smooth_para
        inp = self.inner_product(knownrate, predrate)
        if inp >= 0:
            knownrate.append(self.smooth_para)
            predrate.append(self.smooth_para)
        else:
            knownrate.append(-self.smooth_para)
            predrate.append(-self.smooth_para)
            
        weight = self.cosine(knownrate, predrate)
        return weight
    
    
    # calculate the cosine similarity of two array of rates
    def cosine(self, v1, v2):
        inp = self.inner_product(v1, v2)
        v1_size = math.sqrt(sum(r ** 2 for r in v1))
        v2_size = math.sqrt(sum(r ** 2 for r in v2))
        if 0 in (v1_size, v2_size):
            return 0
        return inp / (v1_size * v2_size)


    # calculate the inner product of two array of rates
    # the sign of the result shows whether they are positive related or negative related
    def inner_product(self, v1, v2):
        return sum(r1 * r2 for r1, r2 in zip(v1, v2))