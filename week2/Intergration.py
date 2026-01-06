import numpy as np
import math

def Integration(fun, bounds=[-1, 1, -1, 1], samples=1000): #bounds=[x1, x2, y1, y2]
    rng = np.random.default_rng()
    x = rng.uniform(bounds[0], bounds[1], samples)
    y = rng.uniform(bounds[2], bounds[3], samples)

    lie_array = fun(x, y)
    box_area = (bounds[1] - bounds[0]) * (bounds[3] - bounds[2])

    return np.sum(lie_array == True) / samples * box_area

def circle(x, y):
    return x**2 + y**2 <= 1

def parabola(x, y):
    return y - x**2 <= 0

def gaussian(x, y):
    e_val = e()
    return y - e_val**(-x**2) <= 0

def e():
        samples = 1000000
        sample_i = np.random.default_rng().uniform(0, 1, size=(10, samples))
        matrix = sample_i[:-1, :]
        new_row = np.ones((1, samples))
        matrix = np.vstack((new_row, matrix))
        subtract = matrix - sample_i
        subtract= np.where(subtract < 0, 1, 0)
        args = np.argmax(subtract, axis=0)
        
        return np.mean(args) + 1



bounds = [-1, 1, -1, 1]
print(Integration(gaussian, bounds, 100000000))


######################################################################
# Below part was in diff file and the upload limit was only one file #
######################################################################

# import numpy as np
# import matplotlib.pyplot as plt
# import math

# class MonteCarlo_PI:
#     def __init__(self, n):
#         # print("Input the number sample points you want : ")
#         self.n = n

#     def pi(self):
#         x = np.random.rand(self.n, 1)*2 - 1
#         y = np.random.rand(self.n, 1)*2 - 1
#         x = x*x
#         y = y*y
#         count = np.sum(x + y < 1)
#         return 4 * count / self.n     

# class MonteCarlo_e:
#     def __init__(self, n):
#         self.n = n
#         self.inf = 10
    
#     # def __init__(self):
#     #     self.n = input(int("Input the number sample points you want : "))
#     #     self.inf = 1000
    
#     def e(self):
#         sample_i = np.random.default_rng().uniform(0, 1, size=(self.inf, self.n))
#         matrix = sample_i[:-1, :]
#         new_row = np.ones((1, self.n))
#         matrix = np.vstack((new_row, matrix))
#         subtract = matrix - sample_i
#         subtract= np.where(subtract < 0, 1, 0)
#         args = np.argmax(subtract, axis=0)
        
#         return np.mean(args) + 1


# a = 2
# b = 2
# xvalues = []
# value_of_pi = []
# error = []
# while a < 10e7:
#     find_pi = MonteCarlo_PI(a)
#     t_pi = find_pi.pi()
#     value_of_pi.append(t_pi)
#     xvalues.append(a)
#     error.append(abs(math.pi - t_pi) / math.pi * 100)
#     a *= 2

# fig, axes = plt.subplots(2,1)

# axes[0].plot(xvalues, value_of_pi, color='red')
# axes[0].set_xlabel("Number of Samples")
# axes[0].set_ylabel("Value of Pi")
# axes[0].set_title("Pi determination")

# axes[1].plot(xvalues, error, color='red')
# axes[1].set_xlabel("Number of Samples")
# axes[1].set_ylabel("Relative error")
# axes[1].set_title("Relative error analysis")

# plt.show()

# e = MonteCarlo_e(1000000)
# print(e.e())