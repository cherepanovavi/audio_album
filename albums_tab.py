import wx
from song_tab import SongPanel


class AlbumsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(200, 600), style=wx.BORDER_SUNKEN)
        self.parent = parent
        self.albums_list = None
        self.buttons = []
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        t = wx.StaticText(self, -1, "Choose an album to listen")
        self.sizer.Add(t)
        self.SetSizer(self.sizer)

    def add_buttons(self, albums_list):
        self.albums_list = albums_list
        i = 0
        for album in albums_list:
            alb_button = wx.Button(self, i, label=album.title, size=(200, 25),
                                   pos=(0, (i+1)*25), style=wx.BU_LEFT)
            self.buttons.append(alb_button)
            self.sizer.Add(alb_button)
            alb_button.Bind(wx.EVT_BUTTON, self.on_alb_button)
            i += 1

    def delete_buttons(self):
        for button in self.buttons:
            print(button)
            button.Destroy()
        self.buttons = []

    def on_alb_button(self, event):
        self.parent.song_panel.delete_buttons()
        self.parent.song_panel.add_buttons(self.albums_list[event.Id].songs)


class AlbumTab(wx.SplitterWindow):
    def __init__(self, parent, albums_list, player):
        wx.SplitterWindow.__init__(self, parent)
        self.album_panel = AlbumsPanel(self)
        self.album_panel.add_buttons(albums_list)
        # panel.SetSize(300, 1000)
        self.song_panel = SongPanel(self, player)
        self.album_panel.SetBackgroundColour("Light Blue")
        self.SplitVertically(self.album_panel, self.song_panel)
        self.SetSashGravity(0.5)
