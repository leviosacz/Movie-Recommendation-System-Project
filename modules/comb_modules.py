from modules.weighted_slope_one import WeightedSlopeOne
from modules.cf_adv_pc import CFAdvPC
from modules.cf_bas_cos import CFBasicCos
from modules.cf_bas_pc import CFBasicPC
from modules.cf_item import CFItem

from tqdm import tqdm
import pandas as pd

class CombModules:

    def __init__(self, udict: dict, mdict: dict):
        self.udict = udict
        self.mdict = mdict

        self.use_rounded = False

        self.w_bas_cos = 0.22
        self.w_bas_pc = 0.22
        self.w_adv_pc = 0
        self.w_item = 0.2

        sub_sum = self.w_bas_cos + self.w_bas_pc + self.w_adv_pc + self.w_item
        if sub_sum > 1:
            print('Wrong Weights for Combing Modules!')

        self.w_slope_one = 1 - sub_sum
    
    def cf(self, testdata: dict):
        # if use_rounded == True, we use predicted ratings rounded to [1, 5] to calculate combined ratings
        # else, we use predicted ratings that haven't been rounded (floating point numbers and can be out of range [1, 5])
        bc = CFBasicCos(self.udict, self.mdict).cf(testdata, round_=self.use_rounded).values.tolist()
        bp = CFBasicPC(self.udict, self.mdict).cf(testdata, round_=self.use_rounded).values.tolist()
        ap = CFAdvPC(self.udict, self.mdict).cf(testdata, round_=self.use_rounded).values.tolist()
        it = CFItem(self.udict, self.mdict).cf(testdata, round_=self.use_rounded).values.tolist()
        so = WeightedSlopeOne(self.udict, self.mdict).cf(testdata, round_=self.use_rounded).values.tolist()


        res = so
        for i in tqdm(range(len(so))):
            rating = (self.w_bas_cos * bc[i][2] + self.w_bas_pc * bp[i][2] + self.w_adv_pc * ap[i][2]
                      + self.w_item * it[i][2] + self.w_slope_one * so[i][2])
            rating = round(rating)

            if not self.use_rounded:
                if rating < 1:
                    rating = 1
                if rating > 5:
                    rating = 5

            res[i][2] = rating
        
        df = pd.DataFrame(res, columns=['uid', 'mid', 'ratings'])
        return df