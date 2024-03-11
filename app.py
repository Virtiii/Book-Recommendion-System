# from flask import Flask,render_template,request
# import pickle
# import numpy as np

# book_df=pickle.load(open('book.pkl','rb'))
# pt=pickle.load(open('pt.pkl','rb'))
# similarity_score=pickle.load(open('similarity_score.pkl','rb'))

# pt1=pickle.load(open('pt1.pkl','rb'))
# similarity_score1=pickle.load(open('similarity_score1.pkl','rb'))

# pt2=pickle.load(open('pt2.pkl','rb'))
# similarity_score2=pickle.load(open('similarity_score2.pkl','rb'))

# app=Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html',
#                            book_name=list(book_df['title'].values),
#                            author=list(book_df['authors'].values),
#                            image=list(book_df['thumbnail'].values),
#                            description=list(book_df['description'].values),
#                            pages=list(book_df['num_pages'].values),
#                            rating=list(book_df['average_rating'].values)
#                            )

# @app.route('/recommend')
# def recommend_bk():
#     return render_template('recommend.html')


# def recommend_same_author(user_input):
#     index=np.where(pt1.index==user_input)[0][0]
#     similar=sorted(list(enumerate(similarity_score1[index])),key=lambda x:x[1],reverse=True)[1:5]
#     data=[]
#     for i in similar:
#         item=[]
#         temp_df=book_df[book_df['title']==pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('title')['title'].values))
#         item.extend(list(temp_df.drop_duplicates('title')['authors'].values))
#         item.extend(list(temp_df.drop_duplicates('title')['thumbnail'].values))
#         item.extend(list(temp_df.drop_duplicates('title')['num_pages'].values))
#         item.extend(list(temp_df.drop_duplicates('title')['average_rating'].values))

#         data.append(item)
#     return data

# def recommend_same_category(user_input):
#     index=np.where(pt2.index==user_input)[0][0]
#     similar=sorted(list(enumerate(similarity_score2[index])),key=lambda x:x[1],reverse=True)[1:5]

#     data1=[]
#     for i in similar:
#         item=[]
#         temp1_df=book_df[book_df['title']==pt.index[i[0]]]
#         item.extend(list(temp1_df.drop_duplicates('title')['title'].values))
#         item.extend(list(temp1_df.drop_duplicates('title')['authors'].values))
#         item.extend(list(temp1_df.drop_duplicates('title')['thumbnail'].values))
#         item.extend(list(temp1_df.drop_duplicates('title')['num_pages'].values))
#         item.extend(list(temp1_df.drop_duplicates('title')['average_rating'].values))

#         data1.append(item)
#     return data1

# def recommend_both(user_input):
#     data_author=recommend_same_author(user_input)
#     data_category=recommend_same_category(user_input)
#     data2=data_author+data_category
#     return data2


# @app.route('/recommend_books' , methods=['POST'])
# def recommend_books():
#     user_input = request.form.get('user_input')
#     recommend_option = request.form.get('recommend_option')
#     data=[]
#     if recommend_option == 'same_author':
#         data = recommend_same_author(user_input)
#     elif recommend_option == 'same_category':
#         data = recommend_same_category(user_input)
#     elif recommend_option == 'both':
#         data = recommend_both(user_input)
#     else:
#         data = []
   
#     print(data)
#     return render_template('recommend.html',data=data)


# if __name__=='__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the data
book_df = pickle.load(open('book.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
pt1 = pickle.load(open('pt1.pkl', 'rb'))
similarity_score1 = pickle.load(open('similarity_score1.pkl', 'rb'))
pt2 = pickle.load(open('pt2.pkl', 'rb'))
similarity_score2 = pickle.load(open('similarity_score2.pkl', 'rb'))
pt3 = pickle.load(open('pt3.pkl', 'rb'))
similarity_score3 = pickle.load(open('similarity_score3.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(book_df['title'].values),
                           author=list(book_df['authors'].values),
                           image=list(book_df['thumbnail'].values),
                           description=list(book_df['description'].values),
                           pages=list(book_df['num_pages']),
                           rating=list(book_df['average_rating'].values))



@app.route('/recommend')
def recommend_bk():
    return render_template('recommend.html')



def recommend_same_author(user_input):
    index = np.where(pt1.index == user_input)[0][0]
    similar = sorted(list(enumerate(similarity_score1[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar:
        temp_df = book_df[book_df['title'] == pt1.index[i[0]]]
        item = (temp_df['title'].values[0], temp_df['authors'].values[0], temp_df['thumbnail'].values[0],temp_df['num_pages'].values[0], temp_df['average_rating'].values[0])
        data.append(item)
    return data



def recommend_same_category(user_input):
    index = np.where(pt2.index == user_input)[0][0]
    similar = sorted(list(enumerate(similarity_score2[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar:
        temp_df = book_df[book_df['title'] == pt2.index[i[0]]]
        item = (temp_df['title'].values[0], temp_df['authors'].values[0], temp_df['thumbnail'].values[0],temp_df['num_pages'].values[0], temp_df['average_rating'].values[0])
        data.append(item)
    return data



def recommend_both(user_input):
    data_author = recommend_same_author(user_input)
    data_category = recommend_same_category(user_input)
    data = data_author + data_category
    return data


def recommend_general(book_name):
    index=np.where(pt3.index==book_name)[0][0]
    similar=sorted(list(enumerate(similarity_score3[index])),key=lambda x:x[1],reverse=True)[1:5]

    data=[]
    for i in similar:
        item=[]
        temp_df=book_df[book_df['title']==pt3.index[i[0]]]
        item = (temp_df['title'].values[0], temp_df['authors'].values[0], temp_df['thumbnail'].values[0],temp_df['num_pages'].values[0], temp_df['average_rating'].values[0])
        data.append(item)

    return data


@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')
    recommend_option = request.form.get('recommend_option')
    data = []
    if recommend_option == 'same_author':
        data = recommend_same_author(user_input)
    elif recommend_option == 'same_category':
        data = recommend_same_category(user_input)
    elif recommend_option == 'both':
        data = recommend_both(user_input)
    elif recommend_option == 'general':
        data = recommend_general(user_input)
    else:
        pass
   
    print(data)
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
