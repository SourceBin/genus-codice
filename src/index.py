import re
import model
import dataset
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import sklearn.model_selection as sk

data = dataset.load()

d = []
chunk_size = 2048

for i in data:
  for chunk in range(0, len(i[0]), chunk_size):
    snippet = i[0][chunk:chunk + chunk_size]
    snippet = re.sub(r'(\w+)', r' \1 ', snippet)
    snippet = snippet.lower()

    d.append({ 'snippet': snippet, 'language': i[1] })

df = pd.DataFrame(d, columns = ['snippet', 'language'])

snippet_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='\n\t')
snippet_tokenizer.fit_on_texts(df['snippet'])
snippet_tensor = snippet_tokenizer.texts_to_sequences(df['snippet'])

max_length = max([len(s.split()) for s in df['snippet']])
snippet_tensor = tf.keras.preprocessing.sequence.pad_sequences(snippet_tensor, maxlen=max_length, padding='post')

vocab_size = len(snippet_tokenizer.word_index) + 1

model = model.build(vocab_size=vocab_size, input_length=max_length, output_size=len(set(df['language'])))
model.summary()

x_train, x_test, y_train, y_test = sk.train_test_split(snippet_tensor, df['language'], test_size=0.2)

y_train = pd.get_dummies(y_train)
y_test = pd.get_dummies(y_test)

categorical_labels = tf.keras.utils.to_categorical(y_train, num_classes=None)

history = model.fit(x_train, y_train, batch_size=64, epochs=10, validation_data=(x_test, y_test))

fig, axs = plt.subplots(2)

# Plot training and validation accuracy values
axs[0].plot(history.history['accuracy'])
axs[0].plot(history.history['val_accuracy'])
axs[0].set_title('Model accuracy')
axs[0].set_xlabel('Epoch')
axs[0].set_ylabel('Accuracy')
axs[0].legend(['Train', 'Test'], loc='upper left')

# Plot training and validation loss values
axs[1].plot(history.history['loss'])
axs[1].plot(history.history['val_loss'])
axs[1].set_title('Model loss')
axs[1].set_xlabel('Epoch')
axs[1].set_ylabel('Loss')
axs[1].legend(['Train', 'Test'], loc='upper left')

plt.show()
