import pandas as pd
import tensorflow as tf

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

SHUFFLE_BUFFER = 500
BATCH_SIZE = 2

filepath = "Data/traindataBTC.csv"
column_names = ['Date', 'Open', 'High', 'Low', 'Adj Close', 'Close', 'Volume'
                , 'rs', 'rsi' ,'pul', 'momentum']

df = pd.read_csv(filepath)
print(df.head())

target = df.pop('Close')

numeric_feature_names = ['Open', 'High', 'Low', 'Adj Close', 'Volume', 'rs', 'rsi', 'pul', 'momentum']
numeric_features = df[numeric_feature_names]
numeric_features.head()

tf.convert_to_tensor(numeric_features)

normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(numeric_features)

normalizer(numeric_features.iloc[:3])

def get_basic_model():
  model = tf.keras.Sequential([
    normalizer,
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1)
  ])

  model.compile(optimizer='adam',
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=['accuracy'])
  return model

model = get_basic_model()
model.fit(numeric_features, target, epochs=50, batch_size=BATCH_SIZE)