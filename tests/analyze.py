import json
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np

with open('../daemon/output.json', 'r') as src:
    raw_data = json.loads(src.read())

#print(raw_data)
sorted_by_host = {}
hosts = []
for i in range(len(raw_data)):
    record = raw_data[i]
    if record['host'] not in sorted_by_host.keys():
        hosts.append(record['host'])
        sorted_by_host[record['host']] = {}
        sorted_by_host[record['host']]['task_waiting_time'] = []
        sorted_by_host[record['host']]['task_time'] = []
        sorted_by_host[record['host']]['modelname'] = []
        sorted_by_host[record['host']]['avg_waiting'] = 0
        sorted_by_host[record['host']]['avg_task'] = 0
    
    sorted_by_host[record['host']]['task_waiting_time'].append(record['task_waiting_time'])
    sorted_by_host[record['host']]['task_time'].append(record['task_time'])
    sorted_by_host[record['host']]['modelname'].append(record['modelname'])
    sorted_by_host[record['host']]['avg_waiting'] += record['task_waiting_time']
    sorted_by_host[record['host']]['avg_task'] += record['task_time']


"""
More marker: https://matplotlib.org/api/markers_api.html#module-matplotlib.markers
"""
colors = ['bs', 'g^', 'rx']
total_task = 0
total_waiting = 0
total_length = 0
i = 0
while i < len(hosts):
    print('[Round {}]'.format(i%3))
    """ draw """
    fig = plt.figure()
    suptitle = ''
    ax = fig.add_subplot(1, 2, 1)
    bx = fig.add_subplot(1, 2, 2)

    j = i
    k = 0
    while k < 3 and j < len(hosts):
        host_data = sorted_by_host[hosts[j]]
        host_data['length'] = len(host_data['task_time'])

        total_task += host_data['avg_task']
        total_waiting += host_data['avg_waiting']
        total_length += host_data['length']

        host_data['avg_task'] /= host_data['length']
        host_data['avg_waiting'] /= host_data['length']
        print('[{}] avg waiting: {:.5f} avg_task: {:.5f}'.format(
                    hosts[j], host_data['avg_waiting'], host_data['avg_task']))
        
        ax.plot(host_data['task_waiting_time'], colors[k], label=hosts[j])
        bx.plot(host_data['task_time'], colors[k], label=hosts[j])
        suptitle += '[{}]: {:.5f}s, {:.5f}s '.format(
            hosts[j], host_data['avg_waiting'], host_data['avg_task'])
        j += 1
        k += 1
    

    plt.suptitle(suptitle)
    plt.legend(loc='right')
    plt.show()
    i += 1

total_task /= total_length
total_waiting /= total_length
print('Total length:', total_length)
print('Total waiting: {:.5f} {:.5f}'.format(total_waiting, total_task))
