# Twitter In Disasters

**IRMiDiS FIRE 2018:**

For task1:

Run files in this order - 
make.py
make_test.py (test file json too big to be uploaded)
doc_freq_calc.py
tfidf.py
final_pos_words.py
final_neg_words.py
classify.py

For task 2:

Run files in this order -
save_news.py
store_pos.py
index_fire.java (twice, one for the headlines folder and once for the factual tweeets folder)
match_articles.java

**Incident detection:**

1. Run query.py to get ranked list of keywords for each kind of incident and form queries as in queries.txt.
2. Run pre_for_lucene.py to form test folder.
3. Run index.py followed by classify.py. 

**Tweet classification into modified categories:**

1. Run make_data with test and train json files corresponding to each of the 6 events (earthquake, typhoon, shooting, bombing, flood, fire)  to create data files.
2. Run precomp.py.
3. Run classify.py
