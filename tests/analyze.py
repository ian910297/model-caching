import json
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np

with open('../daemon/output.json', 'r') as src:
    raw_data = json.loads(src.read())

#print(raw_data)
sorted_by_host = {}
waiting_data = []
task_data = []
waiting_data.append([])
task_data.append([])
avg_waiting = []
avg_task = []
for i in range(len(raw_data)):
    record = raw_data[i]
    if record['host'] not in sorted_by_host.keys():
        sorted_by_host[record['host']] = {}
        sorted_by_host[record['host']]['task_waiting_time'] = []
        sorted_by_host[record['host']]['task_time'] = []
        sorted_by_host[record['host']]['modelname'] = []
    
    sorted_by_host[record['host']]['task_waiting_time'].append(record['task_waiting_time'])
    sorted_by_host[record['host']]['task_time'].append(record['task_time'])
    sorted_by_host[record['host']]['modelname'].append(record['modelname'])
    
    waiting_data[0].append(record['task_waiting_time'])
    task_data[0].append(record['task_time'])


result = {}

color = [[1, 0, 0], [0, 0, 1]]
total_waiting = 0
total_task = 0
for key in sorted_by_host.keys():
    result[key] = {}
    host_data = sorted_by_host[key]
    average_task_waiting_time = 0
    average_task_time = 0
    for i in range(len(host_data['task_waiting_time'])):
        average_task_waiting_time += float(host_data['task_waiting_time'][i])
        average_task_time += float(host_data['task_time'][i])
    
    print(average_task_waiting_time / len(host_data['task_waiting_time']))
    print(average_task_time / len(host_data['task_waiting_time']))
    total_waiting += average_task_waiting_time
    total_task += average_task_time
    avg_waiting.append(average_task_waiting_time / len(host_data['task_waiting_time']))
    avg_task.append(average_task_time / len(host_data['task_waiting_time']))
    waiting_data.append(np.array(host_data['task_waiting_time']))
    task_data.append(host_data['task_time'])

print(len(waiting_data[0]))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(waiting_data[0], 'r--', label='total')
ax.plot(waiting_data[1], 'bs', label='node')
ax.plot(waiting_data[2], 'g^', label='pc')
ax.legend(loc='right')

plt.suptitle('node: {x1:.5f}s  pc: {x2:.5f}s  total: {x3:.5f}s'.format(
    x1=avg_waiting[0], x2=avg_waiting[1], x3=total_waiting / len(raw_data)))
plt.show()


