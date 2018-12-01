import wx


class SongPanel(wx.Panel):
    def __init__(self, parent, player):
        wx.Panel.__init__(self, parent, size=(300, 600), style=wx.BORDER_SUNKEN)
        self.buttons = []
        self.song_list = None
        self.player = player
        t = wx.StaticText(self, -1, "Choose a song to listen")
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(t)
        self.SetSizer(self.sizer)

    def add_buttons(self, song_list):
        i = 1
        self.song_list = song_list
        for song in song_list:
            label = str(song.number)+". "+song.title
            sb = wx.Button(self, song.id, label=label, size=(300, 25), pos=(0, i*25), style=wx.BU_LEFT)
            self.buttons.append(sb)
            sb.Bind(wx.EVT_BUTTON, self.on_song)
            self.sizer.Add(sb)
            i += 1

    def on_song(self, event):
        self.player.change_now_playing(self.song_list)
        self.player.on_song(event)

    def delete_buttons(self):
        for button in self.buttons:
            button.Destroy()
        self.buttons = []
        self.sizer.Layout()
        self.song_list = None


class SongTab(wx.SplitterWindow):
    def __init__(self, parent, song_list, player):
        wx.SplitterWindow.__init__(self, parent)
        panel = SongPanel(self, player)
        panel.add_buttons(song_list)


