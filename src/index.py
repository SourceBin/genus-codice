import model
import utils
import dataset
import pandas as pd
import tensorflow as tf
import sklearn.model_selection as sk

data = dataset.load()
print(data.groupby('lang').size())

print('Normalizing dataset')
rows = []
for i, row in data.iterrows():
  for chunk in utils.normalize_content(row['content']):
    rows.append({ 'content': chunk, 'lang': row['lang'] })

data = pd.DataFrame(rows)
print(data)
print(data.groupby('lang').size())

print('Tokenizing')
content_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='\n\t', num_words=1000)
content_tokenizer.fit_on_texts(data['content'])
content_tensor = content_tokenizer.texts_to_sequences(data['content'])

max_length = max([len(s.split()) for s in data['content']])
content_tensor = tf.keras.preprocessing.sequence.pad_sequences(content_tensor, maxlen=max_length, padding='post')

print('Building model')
vocab_size = len(content_tokenizer.word_index) + 1
model = model.build(vocab_size=vocab_size, input_length=max_length, output_size=len(set(data['lang'])))
model.summary()

print('Splitting dataset')
x_train, x_test, y_train, y_test = sk.train_test_split(content_tensor, data['lang'], test_size=0.2)

y_train = pd.get_dummies(y_train)
y_test = pd.get_dummies(y_test)

categorical_labels = tf.keras.utils.to_categorical(y_train, num_classes=None)

history = model.fit(x_train, y_train, batch_size=64, epochs=10, validation_data=(x_test, y_test))
