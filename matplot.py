import matplotlib.pyplot as plt
import os

x = []
y = []
GLOBALPATH = "./pruebalive/data.txt"
print(os.path.isfile(GLOBALPATH))

for line in open(GLOBALPATH, 'r'):
    lines = [i for i in line.split()]
    print(lines)
    x.append(lines[0])
    y.append(int(lines[1]))
      
plt.title("Students Marks")
plt.xlabel('Roll Number')
plt.ylabel('Marks')
plt.yticks(y)
plt.plot(x, y, marker = 'o', c = 'g')
  
plt.show()
