def Get_Playlist_Songs(data):
    my_list = []
    for i in data:
        my_list.append(i.s.name)
    return my_list

def Get_Song_Playlist(data):
    my_list = []
    for i in data:
        my_list.append(i.p.name)
    return my_list