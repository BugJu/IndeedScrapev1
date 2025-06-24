def create_bar_chart(data_dict):
    data_dict = dict(sorted(data_dict.items(), key=lambda item: item[1], reverse=True))
    print(data_dict)
