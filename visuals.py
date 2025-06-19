import matplotlib.pyplot as plt

def plot_paths(disciplined, emotional, index):
    fig, ax = plt.subplots()
    ax.plot(index, disciplined, label="Disciplina")
    ax.plot(index, emotional, label="Reativo")
    ax.set_ylabel("Valor normalizado")
    ax.legend()
    ax.grid(alpha=0.3)
    return fig
