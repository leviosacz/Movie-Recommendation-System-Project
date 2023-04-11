# Movie Recommendation System Report



## Algorithms

I implemented eight algorithms for this project, including:

1. Basic user-based cosine similarity method;
2. Basic user-based Pearson correlation method;
3. User-based Pearson correlation method with inverse user frequency (IUF);
4. User-based Pearson correlation method with inverse user frequency and case amplification;
5. Item-based collaborative filtering algorithm based on adjusted cosine similarity;
6. Weighted slope one method;
7. Bi-polar slope one method;
8. Module combination approach.



## MAE of results

The table below displays the mean absolute error (MAE) for the results obtained from these algorithms.

| Algorithm                                                    | Overall MAE       |
| ------------------------------------------------------------ | ----------------- |
| Basic user-based cosine similarity method                    | 0.788581513708751 |
| Basic user-based Pearson correlation method                  | 0.769783286816615 |
| User-based Pearson correlation method with inverse user frequency (IUF) | 0.770563125923494 |
| User-based Pearson correlation method with IUF and case amplification | 0.77318995238877  |
| Item-based method based on adjusted cosine similarity        | 0.813454276801839 |
| Weighted slope one method                                    | 0.763913971433262 |
| Bi-polar slope one method                                    | 0.793999343293384 |
| Module combination approach                                  | 0.740929239862092 |



## Result Discussion

### Cosine similarity method

The result of the basic user-based cosine similarity method is actually not bad, although it can be affected by some factors:

1. When the recommendation system is unable to find a similar user to predict the user's rating for a particular movie, one possible approach is to use the movie's average rating as a substitute. Alternatively, the system could use the user's average rating across all movies, or a default value such as 3, to make the prediction.

   In all of my algorithms, I used the movie's average rating as a baseline estimate for predicting user ratings. And if there is no other ratings for the movie, I used a default value of 3.

2. We have two options for selecting the number of nearest neighbors to consider when making recommendations: we can either set k to a fixed value, or we can use a similarity threshold to include all users whose similarity with the test user exceeds the threshold.

   I found that using a similarity threshold produced better results than using a fixed k value in my cosine similarity algorithm.



### Pearson correlation method

Although the Pearson correlation method produced slightly better results than the cosine similarity method, I had to add a smoothing parameter to achieve these results. Without smoothing, the Pearson correlation method performs worse than the cosine similarity method.

To calculate the similarity between a training user and a testing user, I created two lists containing the difference between each movie rating and the user's average rating. If the inner product of the two lists is not negative, a smoothing parameter is added to both lists; otherwise, a negative smoothing parameter is added. This approach helped to avoid situations where all rating differences were zero and improved the overall similarity scores. I came up with this approach after considering situations where all rating differences are zero. This situation implies that both users rated the movies as average, which suggests a level of similarity between them that should be considered in the algorithm.

Although I implemented inverse user frequency (IUF), it did not improve the results. One possible reason could be the size of the data, but I am also considering another reason. IUF assumes that movies rated by many users are not as important, but this overlooks cases where a user rates a popular movie with a rare rating, which should be considered important.

Additionally, the use of case amplification did not yield satisfactory outcomes. It is possible that this is because the dataset was not substantial enough to generate noteworthy distinctions in user similarity scores.

Moreover, using a fixed value of k yielded better results compared to using a similarity threshold in the Pearson correlation approach.



### Item-based method based on adjusted cosine similarity

In my experiment, the item-based method produced the worst results in terms of recommendation accuracy among the eight implemented algorithms. This may be mainly due to the high sparsity of the user-item rating matrix, where most of the entries are empty or missing. Specifically, the number of movies in the dataset far exceeds the number of users, which makes it difficult to accurately calculate the similarity between movies. As a result, the item-based method may not capture the underlying relationships between items and may generate less accurate recommendations.

Moreover, the item-based method was observed to be slower than the user-based methods in the experiment, which may be partly due to the large number of movies in the dataset. However, it should be noted that the item-based method's computational efficiency is generally higher than the user-based methods in scenarios where the dataset contains a relatively low number of items. Therefore, while the item-based method may not be the best choice for highly sparse datasets, it can be a practical and efficient option in scenarios where the dataset contains a limited number of items.



### Slope One Method

The slope one method and the item-based method share a common approach, which is to concentrate on the similarity between movies. However, they differ in their use of ratings; the slope one method uses the difference between ratings instead of the raw ratings. Compared to other single algorithms, the slope one method yields superior results. Moreover, the weighted slope one method produces slightly better outcomes than the bi-polar slope one method.



### Module combination approach

When modules are combined, the resulting output typically shows improved performance compared to using each module in isolation. One possible explanation for this phenomenon is that when errors are present in one module, they tend to be in a different direction than the errors in another module. By combining these modules, the errors tend to cancel each other out, resulting in smaller overall errors and more accurate predictions.

The weights I used for methods are: basic cosine = 0.22, basic pearson correlation = 0.22, item-based = 0.2, weighted slope one = 0.36.



## Program usage instructions

The `run.sh` file contains all the necessary commands to run the program, and it can be executed by running `sh run.sh`. The resulting files will be saved in the `data/results` folder and named after their respective `.py` files. However, please note that for the bi-polar slope one method, a separate preprocessing step is required. To obtain the bi-polar slope one results, execute the following commands: `python -m process_data.preprocess_bipolar`, followed by `python bipolar_slope_one.py`.

The table below illustrates the correspondence between methods, programs, and result files.

| Method                                                     | Program               | Result Files                           |
| ---------------------------------------------------------- | --------------------- | -------------------------------------- |
| Cosine similarity method                                   | cf_bas_cos.py         | result(5/10/20)_cf_bas_cos.txt         |
| Pearson correlation method                                 | cf_bas_pc.py          | result(5/10/20)_cf_bas_pc.txt          |
| Pearson correlation method with IUF                        | cf_iuf_pc.py          | result(5/10/20)_cf_iuf_pc.txt          |
| Pearson correlation method with IUF and case amplification | cf_adv_pc.py          | result(5/10/20)_cf_adv_pc.txt          |
| Item-based method                                          | cf_item.py            | result(5/10/20)_cf_item.txt            |
| Weighted slope one method                                  | weighted_slope_one.py | result(5/10/20)_weighted_slope_one.txt |
| Module combination approach                                | comb_modules.py       | result(5/10/20)_comb_modules.txt       |
| Bi-polar slope one method                                  | bipolar_slope_one.py  | result(5/10/20)_bipolar_slope_one.txt  |



## References

Daniel Lemire, Anna Maclachlan, Slope One Predictors for Online Rating-Based Collaborative Filtering, In SIAM Data Mining (SDM) Conference.