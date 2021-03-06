# -*- coding: utf-8 -*-
"""Linear_Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zz_BwhW35bn8YS0FXlFomFzKvkxOmpN7

# Programming Assignment 2: Linear Regression

## Instructions

- The aim of this assignment is to give you a hands-on with a real-life machine learning application.
- Use separate training, and testing data as discussed in class.
- You can only use Python programming language and Jupyter Notebooks.
- There are three parts of this assignment. In parts 1 & 2, you can only use **numpy, scipy, pandas, matplotlib and are not allowed to use NLTK, scikit-learn or any other machine learning toolkit**. However, you have to use **scikit-learn** in part 3.
- Carefully read the submission instructions, plagiarism and late days policy below.
- Deadline to submit this assignment is: **Friday, 30th October 2020**.

## Submission Instructions

Submit your code both as notebook file (.ipynb) and python script (.py) on LMS. The name of both files should be your roll number. If you don’t know how to save .ipynb as .py [see this](https://i.stack.imgur.com/L1rQH.png). **Failing to submit any one of them will result in the reduction of marks**.

## Plagiarism Policy

The code MUST be done independently. Any plagiarism or cheating of work from others or the internet will be immediately referred to the DC. If you are confused about what constitutes plagiarism, it is YOUR responsibility to consult with the instructor or the TA in a timely manner. No “after the fact” negotiations will be possible. The only way to guarantee that you do not lose marks is “DO NOT LOOK AT ANYONE ELSE'S CODE NOR DISCUSS IT WITH THEM”.

## Late Days Policy

The deadline of the assignment is final. However, in order to accommodate all the 11th hour issues there is a late submission policy i.e. you can submit your assignment within 3 days after the deadline with 25% deduction each day.


## Introduction

In this exercise, you will implement linear regression and get to see it work on data. After completing this assignment, you will know:
- How to implement linear regression from scratch.
- How to estimate linear regression parameters using gradient descent.
- How to make predictions on new data using learned parameters.

Let's start with the necessary imports.
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot
import matplotlib.pyplot as plt
# %matplotlib inline

"""## 1. Linear Regression with one variable

Linear regression assumes a linear relationship between the input variables (X) and the single output variable (Y). More specifically, that output (Y) can be calculated from a linear combination of the input variables (X). When there is a single input variable, the method is referred to as a simple linear regression.

Now you will implement simple linear regression to predict profits for a food truck. Suppose you are the CEO of a restaurant franchise and are considering different cities for opening a new outlet. The chain already has trucks in various cities and you have data for profits and populations from the cities. You would like to use this data to help you select which city to expand to next.

### 1.1 Load the dataset

The file `Data/ex1data1.txt` contains the dataset for our linear regression problem. The first column is the population of a city (in 10,000s) and the second column is the profit of a food truck in that city (in $10,000s). A negative value for profit indicates a loss. 

We provide you with the code needed to load this data. The dataset is loaded from the data file into the variables `X` and `Y`.
"""

from google.colab import drive
drive.mount('/content/drive')

# data = np.loadtxt(os.path.join('Data', 'ex1data.txt'), delimiter=',')
data = np.loadtxt('/content/drive/My Drive/Machine Learning Fall 2020/Data/ex1data.txt', delimiter=',')
X, Y = data[:, 0], data[:, 1]

"""### 1.2 Plot the dataset
Before starting on any task, it is often useful to understand the data by visualizing it. For this dataset, you can use a scatter plot to visualize the data, since it has only two properties to plot (profit and population). Execute the next cell to visualize the data.
"""

pyplot.plot(X, Y, 'ro', ms=10, mec='k')
pyplot.ylabel('Profit in $10,000')
pyplot.xlabel('Population of City in 10,000s')

"""### 1.3 Learn the parameters
In this part, you will fit the linear regression parameters $\theta$ to the food truck dataset using gradient descent.

The objective of linear regression is to minimize the cost function

$$ J(\theta) = \frac{1}{2m} \sum_{i=1}^m \left( h_{\theta}(x^{(i)}) - y^{(i)}\right)^2 ------ (i)$$ 

where the hypothesis $h_\theta(x)$ is given by the linear model
$$ h_\theta(x) = \theta_0 + \theta_1 x ------ (ii)$$

The parameters of your model are the $\theta_j$ values. These are
the values you will adjust to minimize cost $J(\theta)$. One way to do this is to
use the batch gradient descent algorithm. In batch gradient descent, each
iteration performs the update

$$ \theta_0 = \theta_0 - \alpha \frac{1}{m} \sum_{i=1}^m \left( h_\theta(x^{(i)}) - y^{(i)}\right) ------ (iii)$$

$$ \theta_1 = \theta_1 - \alpha \frac{1}{m} \sum_{i=1}^m \left( h_\theta(x^{(i)}) - y^{(i)}\right)x^{(i)} ------ (iv)$$

With each step of gradient descent, your parameters $\theta_j$ come closer to the optimal values that will achieve the lowest cost J($\theta$).

Let's start by implementing the hypothesis $h_\theta(x)$.
"""

### GRADED FUNCTION ###
def predict(x, theta0, theta1):
    '''
    Calculates the hypothesis for any input sample `x` given the parameters `theta`.
    
    Arguments
    ---------
    x : float
        The input sample.
    
    theta0 : float
        The parameter for the regression function.
        
    theta1 : float
        The parameter for the regression function.
    
    Returns
    -------
    h_x : float
        The hypothesis for input sample.
    
    Hint(s)
    -------
    Compute equation (ii).
    '''
    # You need to return the following variable(s) correctly
    h_x = 0.0
    
    ### START CODE HERE ### (≈ 1 line of code)
    h_x = theta0 + theta1*(x)
    
    ### END CODE HERE ###
    
    return h_x

"""Execute the next cell to verify your implementation."""

h_x = predict(x=2, theta0=1.0, theta1=1.0)
print('With x = 2, theta0 = 1.0, theta1 = 1.0\nPredicted Hypothesis h(x) = %.2f' % h_x)
print("Expected hypothesis h(x) = 3.00\n")

"""As you perform gradient descent to learn minimize the cost function  $J(\theta)$, it is helpful to monitor the convergence by computing the cost. In this section, you will implement a function to calculate  $J(\theta)$ so you can check the convergence of your gradient descent implementation."""

### GRADED FUNCTION ###
def computeCost(X, Y, theta0, theta1):
    '''
    Computes cost for linear regression. Computes the cost of using `theta` as the
    parameter for linear regression to fit the data points in `X` and `Y`.
    
    Arguments
    ---------
    X : array
        The input dataset of shape (m, ), where m is the number of training examples.
    
    Y : array
        The values of the function at each data point. This is a vector of
        shape (m, ), where m is the number of training examples.
    
    theta0 : float
        The parameter for the regression function.
        
    theta1 : float
        The parameter for the regression function.
    
    Returns
    -------
    J : float
        The value of the regression cost function.
    
    Hint(s)
    -------
    Compute equation (i).
    '''
    # initialize some useful values
    m = Y.size  # number of training examples
    
    # You need to return the following variable(s) correctly
    J = 0
        
    ### START CODE HERE ### (≈ 3-4 lines of code)
    temp = 0
    for i in range(m):
      hx = predict(X[i],theta0,theta1)
      value = hx - Y[i]
      temp  = temp + value**2
    J = (1/(2*m))*temp
        
    
    
    ### END CODE HERE ###
    
    return J

"""Execute the next cell to verify your implementation."""

J = computeCost(X, Y, theta0=1.0, theta1=1.0)
print('With theta0 = 1.0, theta1 = 1.0\nPredicted cost J = %.2f' % J)
print("Expected cost J = 10.27\n")

"""Next, you will complete a function which implements gradient descent. The loop structure has been written for you, and you only need to supply the updates to parameters $\theta_j$  within each iteration (epoch). 

The starter code for the function `gradientDescent` calls `computeCost` on every iteration and saves the cost to a `python` list. Assuming you have implemented `gradientDescent` and `computeCost` correctly, your value of $J(\theta)$ should never increase, and should converge to a steady value by the end of the algorithm.
"""

### GRADED FUNCTION ###
def gradientDescent(X, Y, alpha, n_epoch):
    """
    Performs gradient descent to learn `theta`. Updates `theta` by taking `n_epoch`
    gradient steps with learning rate `alpha`.
    
    Arguments
    ---------
    X : array
        The input dataset of shape (m, ), where m is the number of training examples.
    
    Y : array
        The values of the function at each data point. This is a vector of
        shape (m, ), where m is the number of training examples.
    
    alpha : float
        The learning rate.
    
    n_epoch : int
        The number of iterations for gradient descent. 
    
    Returns
    -------
    theta0 : float
        The parameter for the regression function.
        
    theta1 : float
        The parameter for the regression function.
    
    J : list
        A python list for the values of the cost function after each iteration.
    
    Hint(s)
    -------
    Compute equation (iii) and (iv).

    While debugging, it can be useful to print out the values of 
    the cost function (computeCost) here.
    """
    # initialize some useful values
    m = Y.size  # number of training examples
    J = list()  # list to store cost
    
    # You need to return the following variables correctly
    theta0 = 0.0
    theta1 = 0.0
    
    for epoch in range(n_epoch):

        ### START CODE HERE ### (≈ 5-10 lines of code)
      temp_0 = 0
      for i in range(m):
        hx = predict(X[i],theta0,theta1)
        value = hx - Y[i]
        temp_0  = temp_0 + value
      
      temp0 = theta0 - alpha*(1/m)*temp_0
      temp_1 = 0
      for i in range(m):
        hx = predict(X[i],theta0,theta1)
        value = (hx - Y[i])*X[i]
        temp_1 = temp_1 + value
      temp1 = theta1 - alpha*(1/m)*temp_1
      theta0 = temp0
      theta1 = temp1  
        
        
        
        
        
        ### END CODE HERE ###

      J.append(computeCost(X, Y, theta0, theta1))
    return theta0, theta1, J

"""Execute the next cell to verify your implementation."""

n_epoch = 1500
alpha = 0.01

theta0, theta1, J = gradientDescent(X ,Y, alpha, n_epoch)
print('Predicted theta0 = %.4f, theta1 = %.4f, cost = %.4f' % (theta0, theta1, J[-1]))
print('Expected theta0 = -3.6303, theta1 = 1.1664, cost = 4.4834')

"""### 1.4 Plot the linear fit

Use your learned parameters $\theta_j$ to plot the linear fit.
"""

h_x = list()
for x in X:
    h_x.append(predict(x, theta0, theta1))
pyplot.plot(X, Y, 'ro', ms=10, mec='k')
pyplot.ylabel('Profit in $10,000')
pyplot.xlabel('Population of City in 10,000s')
pyplot.plot(X, h_x, '-')
pyplot.legend(['Training data', 'Linear regression'])

"""### 1.5 Make predictions

Use your learned parameters $\theta_j$ to make food truck profit predictions in areas with population of 40,000 and 65,000.
"""

print('For population = 40,000, predicted profit = $%.2f' % (predict(4, theta0, theta1)*10000))
print('For population = 65,000, predicted profit = $%.2f' % (predict(6.5, theta0, theta1)*10000))

"""## 2. Multivariate Linear Regression

Now, you will implement multivariate linear regression (from scratch) to predict the the median price of homes in a Boston suburb during the mid-1970s. To do this, you are given with the dataset that has 404 examples in the train set and 102 examples in test set. Each example has 13 input variables (features) and one output variable (price in $10,000s). Below is the description of input variables:

- Per capita crime rate.
- The proportion of residential land zoned for lots over 25,000 square feet.
- The proportion of non-retail business acres per town.
- Charles River dummy variable (= 1 if tract bounds river; 0 otherwise).
- Nitric oxides concentration (parts per 10 million).
- The average number of rooms per dwelling.
- The proportion of owner-occupied units built before 1940.
- Weighted distances to five Boston employment centers.
- Index of accessibility to radial highways.
- Full-value property-tax rate per $10,000.
- Pupil-teacher ratio by town.
- 1000 * (Bk - 0.63) ** 2 where Bk is the proportion of Black people by town.
- Percentage lower status of the population.

Each one of these input features is stored using a different scale. Some features are represented by a proportion between 0 and 1, other features are ranges between 1 and 12, some are ranges between 0 and 100, and so on. This is often the case with real-world data, and understanding how to explore and clean such data is an important skill to develop.

A common way to normalize features that use different scales and ranges is:

- Subtract the mean value of each feature from the dataset.
- After subtracting the mean, additionally scale (divide) the feature values by their respective standard deviations.

Note: We only use examples of the train set to estimate the mean and standard deviation.

You have to follow exactly the same steps as above i.e. implement hypothesis, cost function and gradient descent for multivariate linear regression to learn parameters $\theta$ using train set. Finally, report the cost (error) using your learned parameters $\theta$ on test set. Expected Mean Square Error on this dataset is 11.5 - 12.5 approximately. 

We provide you with the code needed to load this dataset. The dataset is loaded from the data files into the variables `train_X`, `train_Y`, `test_X` and `test_Y`.
"""

# train_X = np.loadtxt(os.path.join('Data', 'ex2traindata.txt'))
# train_Y = np.loadtxt(os.path.join('Data', 'ex2trainlabels.txt'))
# test_X = np.loadtxt(os.path.join('Data', 'ex2testdata.txt'))
# test_Y = np.loadtxt(os.path.join('Data', 'ex2testlabels.txt'))

train_X = np.loadtxt('/content/drive/My Drive/Machine Learning Fall 2020/Data/ex2traindata.txt')
train_Y = np.loadtxt('/content/drive/My Drive/Machine Learning Fall 2020/Data/ex2trainlabels.txt')
test_X = np.loadtxt('/content/drive/My Drive/Machine Learning Fall 2020/Data/ex2testdata.txt')
test_Y = np.loadtxt('/content/drive/My Drive/Machine Learning Fall 2020/Data/ex2testlabels.txt')

def normalization(column):
  mean = column.mean()
  st_dev = column.std()
  column = (column - mean)/st_dev

  return column,mean,st_dev

def updating_data(dt):
  df = pd.DataFrame(data = dt)
  mean_list =[]
  stdev_list = []
  for i in range(len(df.columns)):
    df[i],mean,stdev = normalization(df[i])
    mean_list.append(mean)
    stdev_list.append(stdev)
  return np.asarray(df),mean_list,stdev_list

def updating_test(dt,mean_list,stdev_list):
  df = pd.DataFrame(data = dt)
  for i in range(len(df.columns)):
    df[i] = ((df[i]-mean_list[i]))/stdev_list[i]
    
  return np.asarray(df)

train_X,X_mean,X_stdev = updating_data(train_X)
test_X = updating_test(test_X,X_mean,X_stdev)

def predict_hx(data,list_theta):
  X_0 = 1
  try:
    for ls in data:
      ls.insert(0,X_0)
  except:
    data.insert(0,X_0)
  # X = X_0 + X
  list_theta = np.transpose(np.array(list_theta))
  hx = list_theta*data
  hx_final = []
  try:
    hx.shape[1]
    for h_x in hx:
      h_x = h_x.sum()
      hx_final.append(h_x)
  except:
    hx_final.append(hx.sum())
  


  return hx_final

def costftn(X,Y,theta_list):
  m = Y.size  # number of training examples
  J = 0
      
  temp = 0
  for i in range(m):
    hx = predict_hx(list(X[i]),theta_list)
    hx = hx[0]
    value = hx - Y[i]
    temp  = temp + value**2
  J = (1/(2*m))*temp

  return J

thetas = np.zeros(len(train_X[0])+1)
J = costftn(train_X,train_Y,thetas)
J

def MVgradientDescent(X,Y,alpha,n_epoch):
  m = Y.size  
  J = list()  
  thetas = np.zeros(len(X[0])+1)
  for epoch in range(n_epoch):
    temp_thetas = []
    temp_0 = 0
    for i in range(m):
      hx = predict_hx(list(X[i]),thetas)
      hx = hx[0]
      value = hx - Y[i]
      temp_0  = temp_0 + value
    
    temp0 = thetas[0] - alpha*(1/m)*temp_0
    temp_thetas.append(temp0)
    temp_1 = 0
    for j in range(1,len(thetas)):
      for i in range(m):
        hx = predict_hx(list(X[i]),thetas)
        hx = hx[0]
        value = (hx - Y[i])*X[i][j-1]
        temp_1 = temp_1 + value
      temp_1 = thetas[j] - alpha*(1/m)*temp_1
      temp_thetas.append(temp_1)

    
    for i in range(0,len(thetas)):
      thetas[i] = temp_thetas[i]
     

    J.append(costftn(X, Y, thetas))
    # if (epoch % 100 == 0):
    #   print('Cost at Epoch ', epoch,' ',J[-1])

  return thetas, J

n_epoch = 1500
alpha = 0.01

thetas, J = MVgradientDescent(train_X,train_Y,alpha=0.01,n_epoch = 1500)
# print('Value of thetas', thetas)
print('Value of Cost ftn', J[-1])

# thetas
MSE = costftn(test_X,test_Y,thetas)
MSE

''' Start your code of part 2 from here, add the new code cells as per your requirement. '''

"""## 3. Regularized Linear Regression

Now, you'll use the [scikit-learn](https://scikit-learn.org/stable/index.html) to implement [Linear Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html), [Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge), [Lasso](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html#sklearn.linear_model.Lasso), [Elastic Net](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html#sklearn.linear_model.ElasticNet) and apply them to Boston house pricing dataset (provided in part 2). Try out different values of regularization coefficient (known as alpha in scikit-learn) and use the [Mean Squared Error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html) to report loss with each regression. Finally, plot the regularization coefficients alpha (x-axis) with learned parameters $\theta$ (y-axis) for Ridge and Lasso. Please read [this blog](https://scienceloft.com/technical/understanding-lasso-and-ridge-regression/) to get better understanding of the desired plots.
"""

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error

Lreg = LinearRegression().fit(train_X, train_Y)
lreg_pred = Lreg.predict(test_X)
lreg_mse = mean_squared_error(test_Y, lreg_pred)
print('MSE of Linear Regression: ', lreg_mse)

def Ridge_Reg(val):
  rid = Ridge(alpha=val).fit(train_X,train_Y)
  rid_pred = rid.predict(test_X)
  rid_mse = mean_squared_error(test_Y, rid_pred)
  # rid.coef_

  return rid_mse, rid.coef_

def Lasso_Reg(val):
  las = Lasso(alpha=val).fit(train_X,train_Y)
  las_pred = las.predict(test_X)
  las_mse = mean_squared_error(test_Y, las_pred)
  

  return las_mse,las.coef_

def Elastic_Reg(val):
  Elastic = ElasticNet(alpha=val).fit(train_X,train_Y)
  Elastic_pred = Elastic.predict(test_X)
  Elastic_mse = mean_squared_error(test_Y, Elastic_pred)


  return Elastic_mse

max_alphas = 100
alpha_range = np.logspace(-5, 10, max_alphas)
ridge_coeff = []
lasso_coeff =[]
mse_rid = []
mse_lasso =[]
mse_elastic = []
print('"MSE RESULTS" \nMSE of Linear Regression: ', lreg_mse)
for i in alpha_range:
  rid_mse, rid_coef_ = Ridge_Reg(i)
  mse_rid.append(rid_mse)
  las_mse,las_coef_ = Lasso_Reg(i)
  mse_lasso.append(las_mse)
  Elastic_mse = Elastic_Reg(i)
  mse_elastic.append(Elastic_mse)
  # print(las_coef_)
  # break
  ridge_coeff.append(rid_coef_)
  lasso_coeff.append(las_coef_)

  # print('\n--------------------\nFor alpha = ',i)
  # print('MSE Ridge Regression: ',rid_mse)
  # print('MSE Lasso Regression: ',las_mse)
  # print('MSE Elastic Net Regression: ',Elastic_mse)

mse_table = pd.DataFrame()
mse_table['Alphas'] = alpha_range
mse_table['MSE Ridge'] = mse_rid
mse_table['MSE Lasso'] = mse_lasso
mse_table['MSE ELastic Net'] = mse_elastic

mse_table

ridge_thetas = pd.DataFrame(columns=['Alpha Value','Theta0','Theta1','Theta2','Theta3','Theta4','Theta5','Theta6','Theta7','Theta8','Theta9','Theta10','Theta11','Theta12'])
ridge_thetas['Alpha Value'] = alpha_range
for i in range(len(ridge_coeff)):
  for j in range(0,13):
    ridge_thetas['Theta'+str(j)][i] = ridge_coeff[i][j]
  

ridge_thetas.head()

lasso_thetas = pd.DataFrame(columns=['Alpha Value','Theta0','Theta1','Theta2','Theta3','Theta4','Theta5','Theta6','Theta7','Theta8','Theta9','Theta10','Theta11','Theta12'])
lasso_thetas['Alpha Value'] = alpha_range
for i in range(len(lasso_coeff)):
  for j in range(0,13):
    lasso_thetas['Theta'+str(j)][i] = lasso_coeff[i][j]
  

lasso_thetas.head()

plt.figure(figsize=(20,10))
ax = plt.gca()

ax.plot(alpha_range, ridge_coeff)
ax.set_xscale('log')
plt.xlabel('Log Lambda')
plt.ylabel('Coefficients')
plt.title('Ridge Regression coefficients vs Log Lambda')
plt.legend(ridge_thetas.columns[1:])
plt.show()

plt.figure(figsize=(20,10))
ax = plt.gca()

ax.plot(alpha_range, lasso_coeff)
ax.set_xscale('log')
plt.xlabel('Log Lambda')
plt.ylabel('Coefficient')
plt.title('Lasso Regression coefficients vs Log Lambda')
plt.legend(lasso_thetas.columns[1:])
plt.show()

# rid = Ridge(alpha=1.0).fit(train_X,train_Y)
# rid_pred = rid.predict(test_X)
# rid_mse = mean_squared_error(test_Y, rid_pred)
# rid.coef_

# lreg_mse

''' Start your code of part 3 from here, add the new code cells as per your requirement. '''

