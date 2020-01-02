# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 0.8.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Python による日本語自然言語処理
# http://www.nltk.org/book-jp/ch12.html

# # Mecab
# Japanese lanaguage text segmentation library
#
# Official Documentation: https://taku910.github.io/mecab/

# ## Install packages

# - Install Mecab
# - Install Ipadic
# - Install mecab python

# +
# Install Mecab

# !brew install mecab

# +
# Ipadic is a dictionary used in the heart of mecab
# !brew install mecab-ipadic

# +
# Install a mecab library in Python

# !pip install --upgrade pip
# !pip install mecab-python3
# !pip install urllib3
# !pip install beautifulsoup4

# +
# Install NEologd - Neologism dictionary for MeCab
# doc: https://github.com/neologd/mecab-ipadic-neologd

# !git clone https://github.com/neologd/mecab-ipadic-neologd.git
# !cd ~/mecab-ipadic-neologd&&ls&&echo 'your-password' | sudo -S bin/install-mecab-ipadic-neologd -y
# -

# ## Useful configuration commands

#Check the location of mecab
!mecab-config --sysconfdir 
# mecabrc is a config file
!ls $(mecab-config --sysconfdir)

# +
#Check the location of dictionary
!mecab-config --dicdir 
#Look up what dictionary are installed
!ls $(mecab-config --dicdir) 
# Current dictionary
!mecab -D

# !cat $(mecab-config --sysconfdir)'/mecabrc'
# Change the dictionary from ipadic to neologd in the config file
# !sed -i -e 's/\/ipadic/\/mecab-ipadic-neologd/g' $(mecab-config --sysconfdir)'/mecabrc'
# Change the dictionary back to ipadic in the config file
# !sed -i -e 's/\/mecab-ipadic-neologd/\/ipadic/g' $(mecab-config --sysconfdir)'/mecabrc'
# -

# Import library
import MeCab
import urllib3
from bs4 import BeautifulSoup

# ## Simple Examples 

# - Python
# - Command line
# - Analysis Options: wakati and chasen

# Very first naive example
mecab = MeCab.Tagger() 
mecab.parse("すもももももももものうち").split()

# -O wakati just seperate the text into words
wakati = MeCab.Tagger("-O wakati") 
wakati.parse("すもももももももものうち").split()

# -O chasen provides details
chasen = MeCab.Tagger("-O chasen") 
chasen.parse("すもももももももものうち").split()

# + {"language": "bash"}
# # Naive coding
# mecab
# すもももももももものうち

# + {"language": "bash"}
# # Just seperation
# mecab -O wakati
# すもももももももものうち

# + {"language": "bash"}
# # Details
# mecab -O chasen
# すもももももももものうち

# + {"language": "bash"}
# # Pass a variable to stdin
# sample="生麦生米生卵"
# mecab <<< $sample 

# + {"language": "bash"}
# # # Using << is known as here-document structure
# # cat > input.txt <<EOF
# # 今日は良い天気ですね。
# # $(date +%T)にめっちゃ走ったのに、電車に間に合わなかった。
# # EOF
#
# # Take a file as input and generate another file as output
# mecab -O wakati -o output.txt input.txt
# cat output.txt
# -

# ## mecab-ipadic-NEologd

# - \- d option is the key to switch the dictionary just one time

# + {"language": "bash"}
# #Just ipadic
# # mecab -d /usr/local/lib/mecab/dic/ipadic <<<$sample
# # mecab-ipadic-NEologd
# sample="生麦生米生卵"
# mecab -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd <<<$sample
# -

# Python with just seperation
sample="生麦生米生卵"
wakati = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -O wakati')
wakati.parse(sample).split()

# ## mecab-ipadic vs mecab-ipadic-NEologd

# mecab-ipadic only
import MeCab
mecab = MeCab.Tagger()
mecab.parse("国会議員Youtuberの立花孝志がNHKとKaggleをぶっ壊す").split()

# mecab-ipadic-NEologd
neologd = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
neologd.parse("国会議員Youtuberの立花孝志がNHKとKaggleをぶっ壊す").split()

# +
neologd = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

text = '国会議員Youtuberの立花孝志がNHKとKaggleをぶっ壊す'
node = neologd.parseToNode(text)

while node:
    word=node.surface 
    feature =node.feature.split(',') # Use split to put each element in a list
    print(word)
    print(','.join(feature)) # Use join to put together every element of the list
    node = node.next

# +
# Extract only nouns
neologd = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
text = '国会議員Youtuberの立花孝志がNHKとKaggleをぶっ壊す'
node = neologd.parseToNode(text)

while node:
    word=node.surface 
    feature =node.feature.split(',') # Use split to put each element in a list
    if feature[0] == "名詞":
        print(word)
        print(','.join(feature)) # Use join to put together every element of the list
    node = node.next
# -

# ## Large text example

# Download Kokoro!
# !brew install wget
!wget -O kokoro.zip  https://www.aozora.gr.jp/cards/000148/files/773_ruby_5968.zip
!unzip -f kokoro.zip

# +
import re
title='kokoro'
bindata = open(title+'.txt', 'rb').read()
textdata = bindata.decode('shift_jis')

# 青空文庫のための固有処理
textdata = re.split(r'\-{5,}', textdata)[2]
textdata = re.split(r'底本：', textdata)[0]
textdata = textdata.strip()

# 人によっては以下のパスは異なるので確認してね
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
mecab.parse('')  # バグ対処
results = []
lines = textdata.split("\r\n")
for line in lines:
    r = []
    # 学習に使わない表現の削除処理
    s = line
    s = s.replace("|", "")
    s = re.sub(r'《.+?》', "", s)
    s = re.sub(r'［.+?］', '', s)
    # Mecab
    node = mecab.parseToNode(s)
    while node:
        # 単語を取得
        if node.feature.split(",")[6] == '*':
            word = node.surface
        else:
            word = node.feature.split(",")[6]

        # 品詞を取得
        part = node.feature.split(",")[0]

        if part in ["名詞", "形容詞", "動詞", "記号"]:
            r.append(word)
        node = node.next
    rl = (" ".join(r)).strip()
    results.append(rl)

# write to a file
w_file = title+"_result.txt"
with open(w_file, 'w', encoding='utf-8') as wf:
    wf.write("\n".join(results))
# -

import pandas as pd
kokoro_pd = pd.read_csv(title+'.txt' ,header=None, encoding="SHIFT-JIS")
# Name a column as texts 
kokoro_pd.columns = ['texts']

# Find main texts
# Find the header ending row
start_index = kokoro_pd[kokoro_pd['texts'].str.contains(r'\-{5,}', regex=True)].index[1]+1
# Find the footer beginning row
end_index = kokoro_pd[kokoro_pd['texts'].str.contains(r'底本：', regex=True)].index[0]
kokoro_main_pd=kokoro_pd.iloc[start_index:end_index]
kokoro_main_pd.head()

# +
# Clean out all rubi and comments

# Drop all rubi
kokoro_main_pd.loc[:,'texts']=kokoro_main_pd.loc[:,'texts'].str.replace(r'《.+?》', "", regex=True)
# Drop all comments
kokoro_main_pd.loc[:,'texts']=kokoro_main_pd.loc[:,'texts'].str.replace(r'［.+?］', "", regex=True)
# Drop zenkaku
kokoro_main_pd.loc[:,'texts']=kokoro_main_pd.loc[:,'texts'].str.replace(r'\u3000', " ", regex=True)
# Strip space
kokoro_main_pd.loc[:,'texts']=kokoro_main_pd.loc[:,'texts'].str.strip()
# Verify that there is no empty string
# kokoro_main_pd.loc[:,'texts'].str.find("").any()
# Reset index
kokoro_main_pd.reset_index(drop=True, inplace=True)

kokoro_main_pd.head(20)

# +
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
mecab.parse('') # To avoid a bug

kokoro_main_pd.loc[:,'mecab']=kokoro_main_pd.loc[:,'texts'].apply(lambda x: mecab.parse(x).split())
kokoro_main_pd.loc[:,'wakati']=kokoro_main_pd.loc[:,'texts'].apply(lambda x: mecab.parse(x).split()[:-1:2])
kokoro_main_pd.loc[:,'syntax']=kokoro_main_pd.loc[:,'texts'].apply(lambda x: mecab.parse(x).split()[1::2])
kokoro_main_pd.head(10)

# +
# Use CountVectorizer
# Doc: https://qiita.com/chamao/items/7edaba62b120a660657e
from sklearn.feature_extraction.text import CountVectorizer
count_vectorizer = CountVectorizer(token_pattern=u'(?u)\\b\\w+\\b')

feature_vectors = count_vectorizer.fit_transform(kokoro_main_pd.loc[:,'wakati'].apply(lambda x: ' '.join(x)))
vocabulary = count_vectorizer.get_feature_names()
vocabulary[0:10]

# -

# ## Add words into dictionary

# + {"language": "bash"}
# # Look up dictionary folder 
# cd $(mecab-config --dicdir)
# pwd
#
# # Make a user dictionary in a CSV format
# cd $(mecab-config --dicdir )
# mkdir -p userdic
# cd userdic
# cat > add.csv << EOF
# ITトレンド,,,20,名詞,一般,*,*,*,*,ITトレンド,アイティートレンド,アイティートレンド
# EOF
# #Check the result
# cat add.csv
#
# # Complile the file to the dictionary
# $(mecab-config --libexecdir)/mecab-dict-index \
# -d /usr/local/lib/mecab/dic/ipadic \
# -u /usr/local/lib/mecab/dic/userdic/add.dic \
# -f utf-8 \
# -t utf-8 \
# add.csv
# + {"language": "bash"}
# original_userdic_path='\;\s*userdic.*$'
# new_userdic_path='userdic=\/usr\/local\/lib\/mecab\/dic\/userdic\/add.dic'
# sed -i -e "s/$original_userdic_path/$new_userdic_path/g" $(mecab-config --sysconfdir)'/mecabrc'
# # Multiple dictionaries can be specified like the below
# # userdic = /home/foo/bar/human.dic,/home/foo/bar/manga.dic
#
# # Show mecabrc
# cat $(mecab-config --sysconfdir)'/mecabrc'
# -


# Command line
!echo "ITトレンド" | mecab

# +
# Python

# Default
# neologd = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -O wakati' )
# neologd.parse("2020年のITトレンド").split()

neologd = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -u /usr/local/lib/mecab/dic/userdic/add.dic -O wakati')
neologd.parse("2020年のITトレンド").split()
# -


# # Wordnet in Japanese
# Official Doc: http://compling.hss.ntu.edu.sg/wnja/

# + {"language": "bash"}
# # Japanese Wordnet and English WordNet in an sqlite3 database
# mkdir -p wordnet&&cd $_
# wget http://compling.hss.ntu.edu.sg/wnja/data/1.1/wnjpn.db.gz
# gunzip -f wnjpn.db.gz
# -

import sqlite3
conn = sqlite3.connect("wordnet/wnjpn.db")

# Check tables
tables_df=pd.read_sql_query("select name from sqlite_master where type='table' ", conn)
tables_df

# ## Word Table

# +
# Check columns in word
    
word_table_df=pd.read_sql_query("PRAGMA TABLE_INFO(word)", conn)
word_table_df
# -

# Words in Japanese
words_df=pd.read_sql_query("select * from word where lang='jpn'", conn)
words_df.head()

# How many words in the DB?
word_counts_df=pd.read_sql_query("select count(*) from word", conn)
word_counts_df

# ## Sense Table

# Check columns in sense
sense_table_df=pd.read_sql_query("PRAGMA TABLE_INFO(sense)", conn)
sense_table_df

# Sense in Japanese
sense_df=pd.read_sql_query("select * from sense where lang='jpn' order by synset", conn)
sense_df.head(10)

# +
# Extract words which have the same concept
sense_synset1_df=pd.read_sql_query("select * from word where wordid in (select wordid from sense where synset = '00001740-n') and lang='jpn' ", conn)
sense_synset1_df.head(10)


# Another example    
# sense_synset2_df=pd.read_sql_query("select * from word where wordid in (select wordid from sense where synset='00002621-r') and lang='jpn' ", conn)
# sense_synset2_df.head(10)
# -

# ## Synset Table

# Check columns in synset
synset_table_df=pd.read_sql_query("PRAGMA TABLE_INFO(synset) ", conn)
synset_table_df.head(10)


# Synset examples    
synset_table_df=pd.read_sql_query("select * from synset order by synset", conn)
synset_table_df.head(10)

# +
# Extract the concept name of '00001740-v'

synset_example_df=pd.read_sql_query("select * from synset WHERE synset='00001740-v' ", conn)
synset_example_df.head(10)
# -

# ## Synset Definition

# Synset Def examples    
synset_def_df=pd.read_sql_query("select * from synset_def WHERE lang='jpn'", conn)
synset_def_df.head(10)

# # Synonym Finder

# https://qiita.com/pocket_kyoto/items/1e5d464b693a8b44eda5
# 特定の単語を入力とした時に、類義語を検索する関数
# Better to use try/except syntax? https://www.dreamincode.net/forums/topic/87732-tryexcept-vs-ifelse/
def SearchSimilarWords(word):

    # 問い合わせしたい単語がWordnetに存在するか確認する
    cur = conn.execute("select wordid from word where lemma='%s'" % word)
    word_id = 99999999  #temp 
    for row in cur:
        word_id = row[0]

    # Wordnetに存在する語であるかの判定
    if word_id==99999999:
        print("「%s」は、Wordnetに存在しない単語です。" % word)
        return
    else:
        print("【「%s」の類似語を出力します】\n" % word)

    # 入力された単語を含む概念を検索する
    cur = conn.execute("select synset from sense where wordid='%s'" % word_id)
    synsets = []
    for row in cur:
        synsets.append(row[0])

    # 概念に含まれる単語を検索して画面出力する
    no = 1
    for synset in synsets:
        cur1 = conn.execute("select name from synset where synset='%s'" % synset)
        for row1 in cur1:
            print("%sつめの概念 : %s" %(no, row1[0]))
        cur2 = conn.execute("select def from synset_def where (synset='%s' and lang='jpn')" % synset)
        sub_no = 1
        for row2 in cur2:
            print("意味%s : %s" %(sub_no, row2[0]))
            sub_no += 1
        cur3 = conn.execute("select wordid from sense where (synset='%s' and wordid!=%s)" % (synset,word_id))
        sub_no = 1
        for row3 in cur3:
            target_word_id = row3[0]
            cur3_1 = conn.execute("select lemma from word where wordid=%s" % target_word_id)
            for row3_1 in cur3_1:
                print("類義語%s : %s" % (sub_no, row3_1[0]))
                sub_no += 1
        print("\n")
        no += 1

# Example
SearchSimilarWords("ネコ")

# Synset links (Taxonomy)
# Ref: https://www.cs.cmu.edu/~hideki/software/jawjaw/index-en.html
synlink_df=pd.read_sql_query("select * from synlink", conn)
synlink_df.head(10)


# 07125096-n (hyponymy)and 07128527-n (hypernymy)
relation_example1_df=pd.read_sql_query("select * from word where wordid in (select wordid from sense where synset = '07125096-n')", conn)
relation_example1_df.head(20)


relation_example2_df=pd.read_sql_query("select * from word where wordid in (select wordid from sense where synset = '07128527-n')", conn)
relation_example2_df.head(10)

# 4. countvectorizer
# 5. word2vec
