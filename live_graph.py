import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv


fig = plt.figure()
#creating a subplot 
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    data = open('data.csv','r').read()
    lines = data.split('\n')
    xs = []
    ys1 = []
    ys2 = []
   
    with open('data.csv') as f:
        rows = csv.reader(f, delimiter=',')
        for row in rows:
            xs.append(float(row[0]))
            ys1.append(float(row[1]))
            ys2.append(float(row[2]))


    ax1.clear()
    ax1.plot(xs, ys1)
    ax1.plot(xs, ys2)
    ax1.legend(["With Selfish Gene", "Without Selfish Gene"])

    plt.xlabel('Days')
    plt.ylabel('Population')
    plt.title('Days Vs. Population')	
	
    
ani = animation.FuncAnimation(fig, animate, interval=1000) 
plt.show()