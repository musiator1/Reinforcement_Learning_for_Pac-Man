import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    x_values_mean = list(range(0, len(mean_scores) * 20, 20))  # Ustawianie wartości x dla mean_scores co 10 jednostek
    plt.plot(scores, label='Scores')  # Wykres dla scores z normalnymi wartościami x
    if mean_scores:  # Sprawdź, czy mean_scores nie jest pustą listą
        plt.plot(x_values_mean, mean_scores, label='Mean Scores from 20 previous games')
    plt.ylim(0, 188)  # Ustaw stałą skalę osi Y od 0 do 188
    if scores:
        plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    if mean_scores:
        plt.text(x_values_mean[-1], mean_scores[-1], str(mean_scores[-1]))
    plt.legend()
    plt.show(block=False)
    plt.pause(.1)
