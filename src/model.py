import tensorflow as tf

def build(vocab_size, input_length, output_size):
  model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 100, input_length=input_length),

    tf.keras.layers.Conv1D(filters=16, kernel_size=8, activation='relu'),
    tf.keras.layers.MaxPooling1D(pool_size=2),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.ReLU(),

    tf.keras.layers.Dense(output_size, activation='softmax'),
  ])

  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model
