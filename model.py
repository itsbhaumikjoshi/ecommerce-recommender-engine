
from keras.layers import Concatenate, Dense, Dropout, Embedding, Flatten, Input
from keras.models import Model

def get_embeddings(input, input_dim, output_dim, input_length, name):
  embedding = Embedding(input_dim=input_dim, output_dim=output_dim, input_length=input_length, name=name)(input)
  flatten = Flatten()(embedding)
  return flatten

def build_model(total_unique_sessions: int, total_unique_products: int):
  session_input = Input(shape=(1,), name="session_input")
  product_input = Input(shape=(1,), name="product_input")

  concatenation = Concatenate(name="concatenation")([
      get_embeddings(session_input, total_unique_sessions, 5, input_length=(1,), name="session_embedding"),
      get_embeddings(product_input, total_unique_products, 5, input_length=(1,), name="product_embedding"),
  ])

  hidden_1 = Dense(64, activation="relu", name="hidden_1")(concatenation)
  dropout_1 = Dropout(0.5)(hidden_1)
  hidden_2 = Dense(64, activation="relu", name="hidden_2")(dropout_1)
  dropout_2 = Dropout(0.5)(hidden_2)
  output = Dense(2, activation="softmax", name="output")(hidden_2)

  model = Model(inputs=[session_input, product_input], outputs=output)

  model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

  return model
