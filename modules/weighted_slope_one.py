from tqdm import tqdm
import pandas as pd

class WeightedSlopeOne:

    def __init__(self, udict: dict, mdict: dict):
        self.udict = udict
        self.mdict = mdict
    
    def cf(self, testdata: dict, round_=True):
        res = []

        for uid, uinfo in tqdm(testdata.items()):

            for mid in uinfo['to_predict']:
                if mid in self.mdict:
                    rate = self.cal_rate(mid, uinfo)
                else:
                    rate = uinfo['avg']

                if round_:
                    rate = round(rate)
                    if rate < 1:
                        rate = 1
                    if rate > 5:
                        rate = 5
                res.append([uid, mid, rate])
        
        df = pd.DataFrame(sorted(res, key=lambda x: (x[0], x[1])), columns=['uid', 'mid', 'ratings'])
        return df
    
    def cal_rate(self, mid, uinfo):
        devs = []
        cards = []
        rates = []
        for knownmid in uinfo['rated']:
            if knownmid in self.mdict[mid]['dev']:
                devs.append(self.mdict[mid]['dev'][knownmid])
                cards.append(self.mdict[mid]['dev_len'][knownmid])
                rates.append(uinfo['rated'][knownmid])
        
        if len(devs) == 0:
            return self.mdict[mid]['avg']
        
        total = sum((dev + rate) * card for dev, card, rate in zip(devs, cards, rates))
        return total / sum(cards)