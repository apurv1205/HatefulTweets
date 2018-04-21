import gensim
from data_handler import get_data
from my_tokenizer import glove_tokenize

model = gensim.models.KeyedVectors.load_word2vec_format("glove_embeddings/glove.twitter.27B.200d.txt",binary=True)
print('Finished loading original model %.2f min' % ((time.time()-start)/60))
print('word2vec: %d' % len(model.vocab))

indices_to_delete = []
j = 0
st= set()
tweets = get_data()
X, Y = [], []
tweet_return = []
for tweet in tweets:
    _emb = 0
    words = glove_tokenize(tweet['text'].lower())
    for w in words:
        st.update(w)

for i,w in enumerate(model.index2word):
    l = w.strip().lower()
    found = False
    if l in st:
        found = True
    if found:
        model.vocab[w].index = j
        j += 1
    else:
        del model.vocab[w]
        indices_to_delete.append(i)

model.syn0 = np.delete(model.syn0, indices_to_delete, axis=0)
print('slim: %d' % len(model.vocab))

model.save_word2vec_format("slim.txt", binary=True)
del model

start = time.time()
model = word2vec.Word2Vec.load_word2vec_format("slim.txt", binary=True)
print('Finished loading slim model %.1f sec' % ((time.time()-start)))