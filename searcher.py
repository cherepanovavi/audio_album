class Searcher:
    def __init__(self, audio_album):
        self.titles = {}
        self.audio_album =audio_album
        self.add_titles()

    def update(self):
        self.titles = {}
        self.add_titles()

    def add_titles(self):
        self.add_group_to_titles(self.audio_album.songs_titles)
        self.add_group_to_titles(self.audio_album.artist_titles)
        self.add_group_to_titles(self.audio_album.album_titles)
        self.add_group_to_titles(self.audio_album.genres_titles)
        self.add_group_to_titles(self.audio_album.playlists_titles)

    def add_group_to_titles(self, group_titles):
        for title in group_titles.keys():
            l_title = title.lower()
            if l_title not in self.titles.keys():
                self.titles[l_title] = []
            self.titles[l_title].append(group_titles[title])

    def search(self, request):
        result = []
        if request in self.titles.keys():
            result += self.titles[request]
        for title in self.titles:
            if title.find(request) != -1:
                result += self.titles[title]
        return result

    def get_search_results(self, request):
        results = self.search(request)
        return [('{}: {}'.format(type(r).__name__, r.title), r) for r in results]
