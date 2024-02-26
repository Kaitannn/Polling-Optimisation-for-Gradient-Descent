# -*- coding: utf-8 -*-
"""OrdinaryNeuralNetwork.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15F61di-MsI5V6Zzu-YdmYZ7naE3toxz2
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from warnings import filterwarnings
import os
import sys

import tkinter as tk
from   tkinter import filedialog as fd

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

#suppress warnings
filterwarnings('ignore')

def createGUI():
    btn1       = None
    inputFile  = ""
    win  = tk.Tk()
    #----------------------------------------------------------------------------------------------
    def threadQuit():
        win.destroy()
        sys.exit(0)
    #----------------------------------------------------------------------------------------------
    def threadContinue():
        win.destroy()
    #----------------------------------------------------------------------------------------------
    def btnCallBack1():
        global inputFile
        filetypes = (
                        ('csv file', '*.csv'),
                    )
        inputFile = fd.askopenfilename(
                                        title='Select .csv input file to convert',
                                        initialdir='/',
                                        filetypes=filetypes
                                     )
        if inputFile != '':
            if not btn2 is None:
                label2.config(state=tk.NORMAL)
                btn2.config(state=tk.NORMAL)
    #----------------------------------------------------------------------------------------------
    def btnCallBack2():        
        threadContinue()
    #----------------------------------------------------------------------------------------------         
    win.protocol("WM_DELETE_WINDOW", threadQuit )
    win.title('Ordinary Neural Network')
    win.resizable( 0, 0 )
    win.geometry('340x170')
    #----------------------------------------------------------------------------------------------
    label1 = tk.Label( win, text="(1) Select .csv input file: " , height=4 )
    label1.place(x=15,y=0)
    #----------------------------------------------------------------------------------------------
    label2 = tk.Label( win, text="Designed by Tan Ren Kai \n University of Newcastle upon Tyne \n Agency for Science, Technology and Research \n (National Metrology Centre)" , height=4 )
    label2.place(x=50,y=100)
    #----------------------------------------------------------------------------------------------
    btn1 = tk.Button(win, text ="Select Input", command = btnCallBack1 )
    btn1.place(x=250,y=20)
    #----------------------------------------------------------------------------------------------
    btn2 = tk.Button(win, text ="Continue", command = btnCallBack2 )
    btn2.place(x=145,y=70)
    btn2.config(state=tk.DISABLED)
    #----------------------------------------------------------------------------------------------
    win.eval("tk::PlaceWindow . center")
    return inputFile, win

inputFile, win = createGUI()
win.mainloop()

raw_data = pd.read_csv(inputFile) # MNIST Database. Has 42,000 training data with pixel resolution of 784 pixels
raw_data = raw_data.sample(frac = 1) # Shuffle the 42,000 examples to be used for training/testing. Used for fairness.
raw_data = raw_data.reset_index(drop=True)
m = len(raw_data) # m is 42,000: 42,000 examples
n = len(raw_data.columns) # n is 785: 785 pixels (technically should be 784 because 1 column reserved for label)
processed_data = np.array(raw_data) # Converted into array format

processed_data_train = processed_data[1000:m].T # Transposes a random 41,000 examples. X-axis is now 785 and Y-axis is 41,000
label_array_train = processed_data_train[0] # Print(label_array_train.shape) - this is the array of the labels of the 41,000 examples. For example, is this picture 5, 6, 7, etc.?
X_Y_axis_train = processed_data_train[1:n] # Print(X_Y_axis_train.shape) - this is the array of pixels (x-axis) and examples (y-axis)
X_Y_axis_train = X_Y_axis_train / 255. # Grayscale normalisation, https://stackoverflow.com/questions/55859716/does-normalizing-images-by-dividing-by-255-leak-information-between-train-and-te

processed_data_test = processed_data[0:1000].T
label_array_test = processed_data_test[0]
X_Y_axis_test = processed_data_test[1:n]
X_Y_axis_test = X_Y_axis_test / 255. # Grayscale normalisation. Reduces Grayscale from 0-255 to 0-1.

def calculate_absolute_error(dZ2, history_toggle):
    sum_of_errors = 0
    if history_toggle == 1:
        for i in range(0, 10-1):
            for j in range(0, 41000-1):
                if (dZ2[i][j] > 0):
                    sum_of_errors = sum_of_errors + dZ2[i][j]
    return sum_of_errors

def initial_WB_randomisation():
    # Weights and biases must also have negative representation - https://towardsdatascience.com/whats-the-role-of-weights-and-bias-in-a-neural-network-4cf7e9888a0f
    W1 = np.random.random_sample(size =(10, 784)) - 0.5 # Initial randomised weights and biases activation function for every layer. Runs once. Creates a 10 x 784 matrix
    b1 = np.random.random_sample(size =(10, 1)) - 0.5 # Creates a 10 x 1 matrix
    W2 = np.random.random_sample(size =(10, 10)) - 0.5 # Creates a 10 x 10 matrix
    b2 = np.random.random_sample(size =(10, 1)) - 0.5 # Creates a 10 x 1 matrix
    return W1, b1, W2, b2

def sigmoid(x):
    return 1.0/(1.0+np.exp(-x))

def sigmoid_deriv(x):
    return sigmoid(x)*(1-sigmoid(x))

def softmax(Z):
    A = np.exp(Z) / sum(np.exp(Z))
    return A

def forward_propagation(W1, b1, W2, b2, X_Y_axis_train):
    Z1 = W1.dot(X_Y_axis_train) + b1 # https://stats.stackexchange.com/questions/291680/can-any-one-explain-why-dot-product-is-used-in-neural-network-and-what-is-the-in
    # https://machinelearningmastery.com/gentle-introduction-vectors-machine-learning/#:~:text=The%20dot%20product%20is%20the,symbol%20used%20to%20denote%20it.&text=The%20operation%20can%20be%20used,weighted%20sum%20of%20a%20vector.
    A1 = sigmoid(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2) # The softmax function is used as the activation function in the output layer of neural network models that predict a multinomial probability distribution
    # print(Z2.shape)
    return Z1, A1, A2

def one_hot_representation(label_array_train):
    one_hot = np.zeros((label_array_train.size, label_array_train.max() + 1)) # Sets the correct answer as 1.
    one_hot[np.arange(label_array_train.size), label_array_train] = 1
    one_hot = one_hot.T
    return one_hot

def backward_propagation(Z1, A1, A2, W2, X_Y_axis_train, label_array_train, history_toggle):
    one_hot = one_hot_representation(label_array_train)
    dZ2 = A2 - one_hot # probability minus correct answer, correct answer represented by negative number
    dW2 = 1 / m * dZ2.dot(A1.T) # https://python.plainenglish.io/neural-network-backward-propagation-and-parameters-update-cf88ebcab512
    # https://towardsdatascience.com/backpropagation-made-easy-e90a4d5ede55
    db2 = 1 / m * np.sum(dZ2, 1)
    dZ1 = W2.T.dot(dZ2) * sigmoid_deriv(Z1)
    dW1 = 1 / m * dZ1.dot(X_Y_axis_train.T)
    db1 = 1 / m * np.sum(dZ1, 1)
    sum_of_errors = calculate_absolute_error(dZ2, history_toggle)
    return dW1, db1, dW2, db2, sum_of_errors

def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * np.reshape(db1, (10,1))
    W2 = W2 - alpha * dW2
    b2 = b2 - alpha * np.reshape(db2, (10,1))
    return W1, b1, W2, b2

def get_predictions(A2):
    return np.argmax(A2, 0) # sets most likely answer to 1, and others to 0.

def get_accuracy(predictions, Y):
    print(predictions, Y)
    return np.sum(predictions == Y) / Y.size

def make_predictions(X, W1, b1, W2, b2):
    _, _, A2 = forward_propagation(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions

def test_prediction(index, W1, b1, W2, b2):
    current_image = X_Y_axis_test[:, index, None]
    prediction = make_predictions(X_Y_axis_test[:, index, None], W1, b1, W2, b2)
    label = label_array_test[index]
    print("Prediction: ", prediction)
    print("Label: ", label)

    current_image = current_image.reshape((28, 28)) * 255
    plt.gray()
    plt.imshow(current_image, interpolation='nearest')
    plt.show()

def main_script(alpha, epochs, history_toggle):
    history = []
    W1, b1, W2, b2 = initial_WB_randomisation()
    for i in range(epochs):
        Z1, A1, A2 = forward_propagation(W1, b1, W2, b2, X_Y_axis_train)
        dW1, db1, dW2, db2, sum_of_errors = backward_propagation(Z1, A1, A2, W2, X_Y_axis_train, label_array_train, history_toggle)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
        if history_toggle == 1:
            history.append(sum_of_errors)
        if i % 10 == 0:
            print("Iteration: ", i)
            predictions = get_predictions(A2)
            print(get_accuracy(predictions, label_array_train))

    for i in range (3):
        test_prediction(i, W1, b1, W2, b2)

    if history_toggle == 1:
        plt.plot(history)
        plt.title('Artificial Neural Network, Epochs:100')
        plt.ylabel('Absolute Difference Error')
        plt.xlabel('Training Iteration')
        plt.show()

if __name__ == "__main__":
    history_toggle = 1
    alpha = 0.5
    epochs = 100

    main_script(alpha, epochs, history_toggle)