# download training data and test data
mkdir data data/results
cd data
wget https://www.cse.scu.edu/~yfang/coen272/train.txt
wget https://www.cse.scu.edu/~yfang/coen272/test5.txt
wget https://www.cse.scu.edu/~yfang/coen272/test10.txt
wget https://www.cse.scu.edu/~yfang/coen272/test20.txt
# return to root
cd ../

# process data
python -m process_data.preprocess

# Run different algorithms

# Basic user-based cosine similarity method
# MAE 0.788581513708751
python cf_bas_cos.py

# Basic user-based Pearson correlation method
# MAE 0.769783286816615
python cf_bas_pc.py

# User-based Pearson correlation method with IUF
# MAE 0.770563125923494
python cf_iuf_pc.py

# User-based Pearson correlation method with IUF and case amplification
# MAE 0.77318995238877
python cf_adv_pc.py

# Item-based method based on adjusted cosine similarity
# 0.813454276801839
python cf_item.py

# Weighted slope one method
# MAE 0.763913971433262
python weighted_slope_one.py

# Combining modules
# MAE 0.740929239862092
python comb_modules.py

# For the bi-polar slope one method, I wrote a different process data program
# To run bi-polar slope one method, please run the following codes
# python -m process_data.preprocess_bipolar
# python bipolar_slope_one.py
# MAE 0.793999343293384