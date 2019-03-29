import numpy as np
from tqdm import tqdm
import data
from recommenders.recommender_base import RecommenderBase


scores_impressions = [32.24, 10.63, 7.53, 6.01, 5.1,  4.13, 3.63, 3.17,
                      2.86, 2.597, 2.33, 2.148, 1.96, 1.8, 1.669, 1.58,
                      1.43, 1.32, 1.25, 1.166, 1.115, 1.055, 1.019, 1.007, 1.14]

class OrderedImpressionRecommender(RecommenderBase):
    """
    It recommends all impressions for each session ordered by
    how they are shown in Trivago during the clickout
    """
    def __init__(self, mode, cluster='no_cluster'):

        name = 'Ordered Impressions recommender'
        super(OrderedImpressionRecommender, self).__init__(mode, cluster, name)

        self.mode = mode



    def fit(self):
        """
        Create list of tuples for recommendations ordering them by impressions
        """

        df_test = data.test_df(self.mode)

        df_test_target = df_test[df_test["action_type"] == "clickout item"]

        df_test_target = df_test_target.replace(r'', np.nan, regex=True)

        df_test_target = df_test_target[~df_test_target.reference.notnull()]

        df_test_target = df_test_target.set_index("session_id")

        #Initializing list of recs
        recs_tuples = []
        for i in tqdm(df_test_target.index):
            impressions = df_test_target.at[i, "impressions"]
            impressions = list(map(int, impressions.split('|')))
            recs_tuples.append((i, impressions))

        self.recs_batch = recs_tuples


    def recommend_batch(self):
        return self.recs_batch

    def get_scores_batch(self):
        recs_batch = self.recommend_batch()

        recs_scores_batch = []
        print("{}: getting the model scores".format(self.name))
        for tuple in recs_batch:
            recs_scores_batch.append((tuple[0], tuple[1], scores_impressions[:len(tuple[1])]))

        return recs_scores_batch