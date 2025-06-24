import numpy as np
import matplotlib.pyplot as plt
def create_bar_chart(data_dict):
    sorted_dict = dict(sorted(data_dict.items(), key=lambda x: x[1],reverse=True))
    languages_names = [language for language in sorted_dict.keys()]
    languages_count = [language for language in sorted_dict.values()]
    languages_names = languages_names[:8]
    languages_count = languages_count[:8]
    plt.bar(languages_names, languages_count)
    plt.show()
