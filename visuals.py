import matplotlib.pyplot as plt

def plot_paths(disciplined, emotional, index):
    fig, ax = plt.subplots()
    ax.plot(index, disciplined, label='Disciplina (buy & hold)')
    ax.plot(index, emotional, label='Comportamento reativo')
    ax.set_ylabel('Valor normalizado')
    ax.set_xlabel('Data')
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig
