import numpy as np
from sklearn.datasets import load_iris

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def deriv_sigmoid(x):
  fx = sigmoid(x)
  return fx * (1 - fx)

def mse_perdida(y_true, y_pred):
  return ((y_true - y_pred) ** 2).mean()

class redNeuronal:

  def __init__(self):
    # Pesos
    self.p1 = np.random.normal()
    self.p2 = np.random.normal()
    self.p3 = np.random.normal()
    self.p4 = np.random.normal()
    self.p5 = np.random.normal()
    self.p6 = np.random.normal()

    # Bias
    self.b1 = np.random.normal()
    self.b2 = np.random.normal()
    self.b3 = np.random.normal()

  def retroalimentacion(self, x):
    neurona1 = sigmoid(self.p1 * x[0] + self.p2 * x[1] + self.b1)
    neurona2 = sigmoid(self.p3 * x[0] + self.p4 * x[1] + self.b2)
    neurona3 = sigmoid(self.p5 * neurona1 + self.p6 * neurona2 + self.b3)
    return neurona3

  def train(self, datos, y_trues):
    tasa_aprendizaje = 0.1
    epocas = 1000

    for epoca in range(epocas):
	
      for x, y_true in zip(data, y_trues):
        sum_neurona1 = self.p1 * x[0] + self.p2 * x[1] + self.b1
        neurona1 = sigmoid(sum_neurona1)

        sum_neurona2 = self.p3 * x[0] + self.p4 * x[1] + self.b2
        neurona2 = sigmoid(sum_neurona2)

        sum_neurona3 = self.p5 * neurona1 + self.p6 * neurona2 + self.b3
        neurona3 = sigmoid(sum_neurona3)
        y_pred = neurona3

        # derivada parcial
        d_L_d_ypred = -2 * (y_true - y_pred)

        # Neurona3
        d_ypred_d_p5 = neurona1 * deriv_sigmoid(sum_neurona1)
        d_ypred_d_p6 = neurona2 * deriv_sigmoid(sum_neurona1)
        d_ypred_d_b3 = deriv_sigmoid(sum_neurona3)

        d_ypred_d_neurona1 = self.p5 * deriv_sigmoid(sum_neurona3)
        d_ypred_d_neurona2 = self.p6 * deriv_sigmoid(sum_neurona3)

        # Neurona1
        d_neurona1_d_p1 = x[0] * deriv_sigmoid(sum_neurona1)
        d_neurona1_d_p2 = x[1] * deriv_sigmoid(sum_neurona1)
        d_neurona1_d_b1 = deriv_sigmoid(sum_neurona1)

        # Neurona2
        d_neurona2_d_p3 = x[0] * deriv_sigmoid(sum_neurona2)
        d_neurona2_d_p4 = x[1] * deriv_sigmoid(sum_neurona2)
        d_neurona2_d_b2 = deriv_sigmoid(sum_neurona2)

        # Actualizar
        # Neurona1
        self.p1 -= tasa_aprendizaje * d_L_d_ypred * d_ypred_d_neurona1 * d_neurona1_d_p1
        self.p2 -= tasa_aprendizaje * d_L_d_ypred * d_ypred_d_neurona1 * d_neurona1_d_p2
        self.b1 -= tasa_aprendizaje * d_L_d_ypred * d_ypred_d_neurona1 * d_neurona1_d_b1

        # Neurona2
        self.p3 -= tasa_aprendizaje * d_L_d_ypred * d_ypred_d_neurona2 * d_neurona2_d_p3
        self.p4 -= tasa_aprendizaje * d_L_d_ypred * d_ypred_d_neurona2 * d_neurona2_d_p4
        self.b2 -= tasa_aprendizaje * d_L_d_ypred * d_ypred_d_neurona2 * d_neurona2_d_b2

        # Neurona3
        self.p5 -= tasa_aprendizaje * d_L_d_ypred * d_ypred_d_p5
        self.p6 -= tasa_aprendizaje * d_L_d_ypred * d_ypred_d_p6
        self.b3 -= tasa_aprendizaje * d_L_d_ypred * d_ypred_d_b3

      # perdida por cada epoca
      if epoca % 10 == 0:
        y_preds = np.apply_along_axis(self.retroalimentacion, 1, data)
        perdida = mse_perdida(y_trues, y_preds)
        print("epoca %d perdida: %.3f" % (epoca, perdida))

iris = load_iris()
data = iris.data
y_trues = iris.target

#print(data)
mired = redNeuronal()
mired.train(data, y_trues) 

entradas = np.array([1.3, 1.6])
pesos = np.array([1.4, -0.66])
bias = np.array([0,0])

def prediccion(entradas_vector, pesos_vector, bias_vector):
    capa1 = np.dot(entradas_vector, pesos_vector) + bias_vector
    capa2 = sigmoid(capa1)
    return capa2
y_esp = prediccion(entradas, pesos, bias)
print("Resultado Esperado:", y_esp)