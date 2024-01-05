import matplotlib.pyplot as plt
from IPython import display


plt.ion()

def plot(length):

    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Finding...')
    plt.xlabel('Trial')
    plt.ylabel('Length')
    plt.plot(length)
    plt.ylim(ymin=0)
    plt.text(len(length)-1, length[-1], str(length[-1]))
    plt.show(block=False)
    plt.pause(.1)