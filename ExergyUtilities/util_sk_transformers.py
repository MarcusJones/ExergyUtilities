import sklearn as sk
import pandas as pd

class TransformerLog():
    @property
    def log(self):
        return "Transformer: {}".format(type(self).__name__)

#%% 
#===============================================================================
# WordCounter
#===============================================================================
class WordCounter(sk.base.BaseEstimator, sk.base.TransformerMixin,TransformerLog):
    """
    """
    def __init__(self, col_name, new_col_name):
        self.col_name = col_name
        self.new_col_name = new_col_name
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, df, y=None):
        df[self.new_col_name] = df[self.col_name].apply(lambda x: len(x.split(" ")) )
        print(self.log)
        return df

# Debug:
#df = X_train
#col_name = 'question_text'
#new_col_name = "no_of_words_in_question"
#word_counter = WordCounter(col_name,new_col_name)
#word_counter.transform(df)

#===============================================================================
# TimeProperty
#===============================================================================
class TimeProperty(sk.base.BaseEstimator, sk.base.TransformerMixin,TransformerLog):
    """
    """
    def __init__(self, time_col_name, new_col_name,time_property):
        self.time_col_name = time_col_name
        self.new_col_name = new_col_name
        self.time_property = time_property
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, df, y=None):
        original_shape=df.shape
        if self.time_property == 'hour':
            df[self.new_col_name] = df[self.time_col_name].dt.hour
        elif self.time_property == 'month':
            df[self.new_col_name] = df[self.time_col_name].dt.month
        elif self.time_property == 'dayofweek':
            df[self.new_col_name] = df[self.time_col_name].dayofweek
        else:
            raise
        print("Transformer:", type(self).__name__, original_shape, "->", df.shape,vars(self))
        return df

    
# Debug:
#df = X_train
#time_col_name = 'question_utc'
#new_col_name = 'question_hour'
#time_property = 'hour'
#time_col_name = 'question_utc'
#new_col_name = 'question_month'
#time_property = 'month'
#time_adder = TimeProperty(time_col_name,new_col_name,time_property)
#res=time_adder.transform(df)
#        

#===============================================================================
# AnswerDelay
#===============================================================================

class AnswerDelay(sk.base.BaseEstimator, sk.base.TransformerMixin,TransformerLog):
    """
    """
    def __init__(self, new_col_name,divisor=1):
        self.new_col_name = new_col_name
        self.divisor = divisor
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, df, y=None):
        df[self.new_col_name] = df['answer_utc']- df['question_utc']
        df[self.new_col_name] = df[self.new_col_name].dt.seconds/self.divisor
        print(self.log)
        return df
           
    
# Debug:
#df = X_train
#new_col_name = 'answer_delay_seconds'
#answer_delay_adder = AnswerDelay(new_col_name)
#res=answer_delay_adder.transform(df)
#       

#===============================================================================
# ValueCounter
#===============================================================================
class ValueCounter(sk.base.BaseEstimator, sk.base.TransformerMixin,TransformerLog):
    """
    """
    def __init__(self, col_name):
        self.col_name = col_name
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, df, y=None):
        # Count the number of unique entries in a column
        # reset_index() is used to maintain the DataFrame for merging
        selected_df_col = df[self.col_name].value_counts().reset_index()
        # Create a new name for this column
        selected_df_col.columns = [self.col_name, self.col_name +'_counts']
        print(self.log)
        return pd.merge(selected_df_col, df, on=self.col_name)


#===============================================================================
# ConvertToDatetime
#===============================================================================
class ConvertToDatetime(sk.base.BaseEstimator, sk.base.TransformerMixin,TransformerLog):
    """
    """
    def __init__(self, time_col_name, unit='s'):
        self.time_col_name = time_col_name
        self.unit = unit
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, df, y=None):
        df[self.time_col_name] = pd.to_datetime(df[self.time_col_name], unit=self.unit)
        print("Transformer:", type(self).__name__, "converted", self.time_col_name, "to dt")
        return df