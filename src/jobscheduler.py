import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Running job scheduler
def job_scheduler(self, filename, n, i, o):
    df = pd.read_csv('./jobs/' + filename + '.csv')
    df['duration'] += df['in']*i
    df['duration'] += df['out']*o
    df['begin'], df['end'], df['left'] = 0, 0, df['duration']

    time = 0
    memory = pd.DataFrame(columns = ['time', 'process', 'memory'])
    while not (df['left'] == 0).all():
        # Running n processes
        processes = df[(df['arrival'] <= time) & (df['left'] != 0)].head(n)
        processes.loc[processes['left'] == processes['duration'], 'begin'] = time
        processes['left'] -= 1
        processes.loc[processes['left'] == 0, 'end'] = time
        df = pd.concat([processes, df[~df.index.isin(processes.index)]])

        # Calculating used memory
        for index, row in processes.iterrows():
            for i in range(len(processes)):
                memory.loc[len(memory.index)] = [time + i, index, row['memory']]

        # Incrementing time
        time += max(1, len(processes))

    # Plotting processing
    df.sort_index(ascending = False, inplace = True)
    df['end'] -= df['begin']
    df.plot.barh(
        title = f'Evolução de execução - n = {n}',
        y = ['begin', 'end'],
        xlabel = 'Ciclos',
        ylabel = 'Processo',
        stacked = True,
        grid = True,
        linewidth = 0,
        legend = None,
        color = {
            'begin': matplotlib.colors.to_rgba('orange', 0),
            'end': matplotlib.colors.to_rgba('orange', 1)
        }
    )

    # Plotting memory
    memory.pivot_table(
        index = 'time',
        columns = 'process',
        values = 'memory'
    ).plot.area(
        title = f'Uso de memória - n = {n}',
        xlabel = 'Ciclos',
        ylabel = 'Memória',
        grid = True,
        linewidth = 0
    )
    plt.show()