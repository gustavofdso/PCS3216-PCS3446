import pandas as pd
import matplotlib.pyplot as plt

# Running job scheduler
def job_scheduler(self, filename, n, i, o):
    df = pd.read_csv('./jobs/' + filename + '.csv')
    df['duration'] += df['in']*i
    df['duration'] += df['out']*o
    df['left'] = df['duration']

    time = 0
    df.sort_values('start', inplace = True)
    memory = pd.DataFrame(columns = ['time', 'process', 'memory'])
    while not (df['left'] == 0).all():
        # Running n processes
        processes = df[(df['start'] <= time) & (df['left'] != 0)].head(n)
        processes['left'] -= 1
        df = pd.concat([processes, df[~df.index.isin(processes.index)]])

        # Calculating used memory
        for index, row in processes.iterrows():
            for i in range(len(processes)):
                memory.loc[len(memory.index)] = [time + i, index, row['memory']]

        # Incrementing time
        time += max(1, len(processes))

    # Plotting memory graph
    memory = memory.pivot_table(index = 'time', columns = 'process', values = 'memory')
    memory.plot.area(stacked = True, title = 'Memória utilizada - n = {n}'.format(n = n), grid = True, linewidth = 0)
    plt.show()