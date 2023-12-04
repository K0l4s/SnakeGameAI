import os
import pandas as pd

class ranks:
    def __init__(self,score):
        self.score = score

    def high_score(self,score):
        file_path = 'ranks.xlsx'

        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=['High score'])
            df.to_excel(file_path, index=False)

        try:
            df = pd.read_excel(file_path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['High score'])
        
        if self.score > 0:
            if not df['High score'].isin([self.score]).any():
                new_row = pd.DataFrame({'High score': [self.score]})
                df = pd.concat([new_row, df], ignore_index=True)

                df = df.sort_values(by='High score', ascending=False).reset_index(drop=True)

        df = df.iloc[:10]
        df.to_excel(file_path, index=False)
        return df.head(10)
    
