import math
import matplotlib.pyplot as plt


def xt(t):
  return 20 * math.cos(2 * math.pi * t)

Ts = 1.0 / 12

y = [xt(Ts * i) for i in range(120)]
y2 = [xt(Ts * i) * xt(Ts * i) for i in range(120)]

plt.subplot(211)
plt.title("y = x(t)")
plt.xlabel("t")
plt.ylabel("y")
plt.plot(y)

plt.subplot(212)
plt.title("z = x^2(t)")
plt.xlabel("t")
plt.ylabel("z")
plt.plot(y2)

plt.show()
