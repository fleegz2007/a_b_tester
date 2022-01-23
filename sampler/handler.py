from sampler.core.statistics import Statistics
from sampler.configuation import Connector


class Handler(Connector):
    def __init__(self):
        super().__init__()
        self.statistics = Statistics()


    def random_sampling(self, df_pop, df_sample):
        self.statistics.drop_duplicates(df_pop, df_sample)
        pop_size = len(df_pop)
        sample_size = len(df_sample)
        sample_data = self.statistics.random_numbers_pandas(df_pop, pop_size, sample_size)
        return sample_data


    def average_results():
        

