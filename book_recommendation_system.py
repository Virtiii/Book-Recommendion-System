#!/usr/bin/env python
# coding: utf-8

# In[63]:


import numpy as np
import pandas as pd
import pickle


# In[24]:


books=pd.read_csv('data.csv')


# In[25]:


books.head()


# In[26]:


books.isnull().sum()


# In[27]:


data_types_all = books.dtypes
print("Data types of all columns:")
print(data_types_all)


# In[28]:


books.duplicated().sum()


# In[29]:


# rating_df=books.groupby('title').count()['average_rating'].reset_index()
# rating_df        


# In[30]:


# books['Rating'] = pd.to_numeric(books['Rating'], errors='coerce')
# books['Rating'].fillna(0, inplace=True)
# avg_rating_df = books.groupby('Book')['Rating'].mean().reset_index()
# avg_rating_df.rename(columns={'Rating': 'avg-rating'}, inplace=True)
# avg_rating_df


# In[31]:


# pop_df=rating_df.merge(books,on='title')
# pop_df.sort_values('ratings_count_x',ascending=False) 
# pop_df  


# In[32]:


books = books.dropna(subset=['average_rating'])
books.tail(5)


# In[33]:


books['average_rating'] = pd.to_numeric(books['average_rating'])
books_new = books.sort_values('average_rating', ascending=False)


# In[34]:


books_new = books_new.drop_duplicates('title')
col=['title','subtitle','authors','categories','thumbnail','description','published_year','average_rating','num_pages','ratings_count']
books_new[col]


# In[35]:


books_new = books_new.rename_axis('UserID').reset_index()
books_new.reset_index(drop=True)
books_new.index+=1


# In[36]:


books_new.head() 


# In[37]:


books_new['ratings_count'] = pd.to_numeric(books['ratings_count'])


# In[38]:


# x=books_new.groupby('title').count()['ratings_count']>50
# users=x[x].index


# In[39]:


# filtered_rating=books_new[books_new['title'].isin(users)]
# filtered_rating.head()


# In[40]:


# rating =books_new.groupby('title').count()['ratings_count']>threshold
# rating


# In[41]:


threshold = 50
filtered_rating = books_new[(books_new['ratings_count'] > threshold) & (books_new['average_rating'] > 3)]
filtered_rating.head()


# In[61]:


books_new['thumbnail'][1]


# In[43]:


import langdetect

# Function to detect language with fallback to English if detection fails
def detect_language(text):
    try:
        return langdetect.detect(text)
    except langdetect.lang_detect_exception.LangDetectException:
        return 'en'  # Fallback to English if detection fails

# Assuming your DataFrame is named 'df' and the column containing text is 'text'
languages = filtered_rating['title'].apply(detect_language)

# Create a Series to count language occurrences
lang_counts = languages.value_counts()

# Print the most common languages (you can adjust the limit)
print(lang_counts)


# In[44]:


# import pandas as pd
# from googletrans import Translator

# # Assuming your DataFrame is 'df' and the column with text is 'column_name'
# translator = Translator()

# def translate_to_english(text):
#     try:
#         return translator.translate(text, dest='en').text
#     except Exception as e:
#         # Handle translation errors, e.g., text length exceeding limits
#         return "Translation failed"

# filtered_rating['title'] = filtered_rating['title'].apply(translate_to_english)


# In[45]:


pt=filtered_rating.pivot_table(index='title',columns=['authors','categories'],values='average_rating')
pt1=filtered_rating.pivot_table(index='title',columns='authors',values='average_rating')
pt2=filtered_rating.pivot_table(index='title',columns='categories',values='average_rating')


# In[46]:


pt.fillna(0,inplace=True)
pt1.fillna(0,inplace=True)
pt2.fillna(0,inplace=True)


# In[47]:


from sklearn.metrics.pairwise import cosine_similarity


# In[48]:


score=cosine_similarity(pt)
score1=cosine_similarity(pt1)
score2=cosine_similarity(pt2)


# In[49]:


score.shape


# In[50]:


score


# In[51]:


# def recommend(book_name):
#     index=np.where(pt.index==book_name)[0][0]
#     similar=sorted(list(enumerate(score[index])),key=lambda x:x[1],reverse=True)[:20]

#     for i in similar:
#         print(pt.index[i[0]])


# In[71]:


def recommend1(book_name):
    index=np.where(pt1.index==book_name)[0][0]
    similar=sorted(list(enumerate(score1[index])),key=lambda x:x[1],reverse=True)[:20]

    data=[]
    for i in similar:
        item=[]
        temp_df=books_new[books_new['title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['authors'].values))
        item.extend(list(temp_df.drop_duplicates('title')['thumbnail'].values))
        item.extend(list(temp_df.drop_duplicates('title')['num_pages'].values))
        item.extend(list(temp_df.drop_duplicates('title')['average_rating'].values))

        data.append(item)

    return data        


# In[72]:


recommend1('The Wee Free Men')


# In[73]:


def recommend2(book_name):
    index=np.where(pt2.index==book_name)[0][0]
    similar=sorted(list(enumerate(score2[index])),key=lambda x:x[1],reverse=True)[:20]

    data1=[]
    for i in similar:
        item=[]
        temp1_df=books_new[books_new['title']==pt.index[i[0]]]
        item.extend(list(temp1_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp1_df.drop_duplicates('title')['authors'].values))
        item.extend(list(temp1_df.drop_duplicates('title')['thumbnail'].values))
        item.extend(list(temp1_df.drop_duplicates('title')['num_pages'].values))
        item.extend(list(temp1_df.drop_duplicates('title')['average_rating'].values))

        data1.append(item)

    return data1


# In[74]:


recommend2('The Wee Free Men')


# In[80]:


def recommend(book_name):
    return recommend1(book_name)
    return recommend2(book_name)


# In[81]:


recommend('The Wee Free Men')


# In[82]:


pickle.dump(books_new,open('book.pkl','wb'))
pickle.dump(pt,open('pt.pkl','wb'))
pickle.dump(score,open('similarity_score.pkl','wb'))


# In[ ]:




