import matplotlib.pyplot as plt
import panda_connect as pdct

# plt.plot(pdct.array_chennai_temp, marker="o")
# plt.plot(pdct.array_madurai_temp, marker='o')
# plt.ylabel('Temperature')
# plt.grid()
#plt.show()

plt.bar(pdct.df_chennai['id'],pdct.array_chennai_temp,color='blue',width=0.2)
plt.grid()
plt.show()
