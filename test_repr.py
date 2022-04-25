#!/usr/bin/python3
import matplotlib.pyplot as plt

n = list(range(50))
u1 = [1.0]
u2 = [1.0]
u3 = [1.0]
u4 = [1.0]
u5 = [1.0]
u6 = [1.0]
u7 = [1.0]
u8 = [1.0]
u9 = [1.0]
for i in range(1, 50):
    u1.append(u1[i-1]*0.1)
    u2.append(u2[i-1]*0.2)
    u3.append(u3[i-1]*0.3)
    u4.append(u4[i-1]*0.4)
    u5.append(u5[i-1]*0.5)
    u6.append(u6[i-1]*0.6)
    u7.append(u7[i-1]*0.7)
    u8.append(u8[i-1]*0.8)
    u9.append(u9[i-1]*0.9)

plt.plot(n, u1)
plt.plot(n, u2)
plt.plot(n, u3)
plt.plot(n, u4)
plt.plot(n, u5)
plt.plot(n, u6)
plt.plot(n, u7)
plt.plot(n, u8)
plt.plot(n, u9)
plt.show()
