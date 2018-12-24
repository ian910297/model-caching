import matplotlib.pyplot as plt
import json
import glob
import numpy as np

files = glob.glob('*.json')

for i in range(len(files)):
    with open(files[i], 'r') as f:
        content = json.loads(f.read())

    filesizes = list(content.keys())
    j = 0
    while j < len(filesizes):
        fig = plt.figure()
        plt.suptitle(files[i])
        k = 0
        while k<2 and j+k<len(filesizes):
            filesize = filesizes[j+k]
            data = content[filesize]
            storage = list(data.keys())
            y_pos = np.arange(len(storage))
            times = [data[storage[m]]['times'] for m in range(len(storage))]
        
            ax = fig.add_subplot(1, 2, k+1)
            ax.barh(y_pos, times, align='center', color='green')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(storage)
            ax.invert_yaxis()
            ax.set_xlabel('Times')
            ax.set_title('{} KB'.format(filesize))
            
            k += 1
        j += k

        plt.show()


