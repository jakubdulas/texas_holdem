import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Input

"""
input
[
    my_card_1,
    my_card_2,

    money_to_call,
    money,

    cards on table:
        c1,
        c2,
        c3,
        c4,
        c5
]
"""

def build_model():
    input_layer = Input(shape=(9, ))

    x = Dense(16, activation="relu")(input_layer)
    x = Dense(32, activation="relu")(x)
    x = Dense(64, activation="relu")(x)
    x = Dense(128, activation="relu")(x)
    x = Dense(128, activation="relu")(x)
    x = Dense(256, activation="relu")(x)
    x = Dense(512, activation="relu")(x)
    x = Dense(512, activation="relu")(x)
    x = Dense(256, activation="relu")(x)
    x = Dense(128, activation="relu")(x)
    x = Dense(128, activation="relu")(x)
    x = Dense(64, activation="relu")(x)
    x = Dense(32, activation="relu")(x)
    x = Dense(16, activation="relu")(x)
    x = Dense(4, activation="softmax")(x)

    return Model(inputs=input_layer, outputs=x)


if __name__ == "__main__":
    input_data = [
        42, 6, # my cards
        10, 100, # money to call, money
        34, 3, 23, 46, 12 # card on the table
    ]

    model = build_model()
    
    model.compile(loss="categorical_crossentropy", optimizer='adam')
    model.summary()

    pred = model.predict([input_data])

    print(pred)
    