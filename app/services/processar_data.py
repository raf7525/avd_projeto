import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'notebooks'))
from tratamento import tratando_linhas_nulas

class ProcessarData:
    @staticmethod
    def clean_null_rows(data_list):
        df = pd.DataFrame(data_list)
        return tratando_linhas_nulas(df).to_dict('records')