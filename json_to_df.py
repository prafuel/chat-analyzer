import json
import pandas as pd


f = open("hinglish-stopword.txt","r")
stopwords = [word.split("\n")[0] for word in f.readlines()]

# helper functions
# from nltk import word_tokenize
from string import punctuation
# from nltk.stem import PorterStemmer
from collections import Counter

# ps = PorterStemmer()

class JSON2DF :
    def __init__(self, data:str) -> None:
        self.data = json.loads(data)

    def converter(self) -> pd.DataFrame:
        msg = self.data
        
        sender_name = []
        sender_content = []
        for m in msg['messages']:
            
            if "content" in m.keys():
                sender_name.append(m['sender_name'].split(" ")[0])
                if "sent an attachment." in m['content'] :
                    sender_content.append("reel")
                else:
                    sender_content.append(m['content'])
            else :
                sender_name.append(m['sender_name'].split(" ")[0])
                sender_content.append("media")
        
        df_dict = {
            "users": sender_name,
            "msgs" : sender_content,
        }

        df = pd.DataFrame(df_dict)
        df['word_count'] = df['msgs'].apply(self.word_count)
        return df
    
    def word_count(self,text : str):
        if "reel" not in text and "media" not in text:
            return len(text.split(" "))
        else:
            return 0

    def total_users(self):
        msg = self.data
        total_users = [user['name'].split(" ")[0] for user in msg['participants']]
        return total_users
    
    def most_common_words(self, df: pd.DataFrame, count:int=20):
        y = []
        for text in df['msgs']:
            text = text.lower()
            for word in text.split(" "):
                if str.isalnum(word) and word not in punctuation and word not in stopwords:
                    y.append(word)

        counter = Counter(y)
        return pd.DataFrame(counter.most_common(count), columns=['words','count'])
    