from tqdm import tqdm
import math
import pandas as pd

class CFBasicCos:

    def __init__(self, udict: dict, mdict: dict):
        self.udict = udict
        self.mdict = mdict
    
    def cf(self, testdata: dict, round_=True, k=60, sim=0.78):
        res = []

        for uid, uinfo in tqdm(testdata.items()):
            # calculate weights and store them in wl(weight list)
            wl = []
            for trainuid, trainuinfo in self.udict.items():
                w = self.cal_weight(trainuinfo, uinfo)
                if w != 0:
                    wl.append([w, trainuid])
            # sort weights by absolute values in descending order
            swl = sorted(wl, key=lambda x: abs(x[0]), reverse=True)

            # predict
            for mid in uinfo['to_predict']:
                rate = self.cal_rate(mid, swl, k, sim)

                if round_:
                    rate = round(rate)
                    if rate < 1:
                        rate = 1
                    if rate > 5:
                        rate = 5
                res.append([uid, mid, rate])
        
        df = pd.DataFrame(sorted(res, key=lambda x: (x[0], x[1])), columns=['uid', 'mid', 'ratings'])
        return df
    
    def cal_rate(self, mid, swl, k, sim, print_=False):
        topwl = []
        toprl = []
        for uweight, trainuid in swl:
            if not mid in self.udict[trainuid]['rated']:
                continue

            # if we use adaptive k based on the ground similarity
            if abs(uweight) < sim:
                break

            topwl.append(uweight)
            toprl.append(self.udict[trainuid]['rated'][mid])

            # if we use fixed k
            # if len(topwl) >= k:
            #    break

        # if no similar one
        if len(topwl) == 0:
            if mid in self.mdict:
                rate = self.mdict[mid]['avg']
            else:
                rate = 3
        else:
            rate = self.inner_product(topwl, toprl) / sum([abs(n) for n in topwl])
        
        if print_:
            print(mid)
            print(topwl, toprl, rate)

        return rate

    
    def cal_weight(self, trainuinfo, testuinfo):
        intersect = []
        for mid in testuinfo['rated']:
            if mid in trainuinfo['rated']:
                intersect.append(mid)
        
        if len(intersect) == 0:
            return 0
        
        trainrate = []
        testrate = []
        for mid in intersect:
            trainrate.append(trainuinfo['rated'][mid])
            testrate.append(testuinfo['rated'][mid])
        weight = self.cosine(trainrate, testrate)
        return weight
    
    
    # calculate the cosine similarity of two array of rates
    def cosine(self, v1, v2):
        inp = self.inner_product(v1, v2)
        v1_size = math.sqrt(sum(n ** 2 for n in v1))
        v2_size = math.sqrt(sum(n ** 2 for n in v2))
        return inp / (v1_size * v2_size)


    # calculate the inner product of two array of rates
    # the sign of the result shows whether they are positive related or negative related
    def inner_product(self, v1, v2):
        res = 0
        for n1, n2 in zip(v1, v2):
            res += n1 * n2
        return res