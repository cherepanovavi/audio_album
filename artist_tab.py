import wx
from tabs_and_panels import Panel, SongPanel
from wx.lib.splitter import MultiSplitterWindow


class ArtistPanel(wx.Panel):
    def __init__(self, parent, player, artists_list):
        self.parent = parent
        self.player = player
        self.artists_list = artists_list
        self.fr = None
        self.selected_artist = None
        wx.Panel.__init__(self, parent, size=(200, 600), style=wx.BORDER_SUNKEN)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        t = wx.StaticText(self, -1, "Choose an artist to listen")
        self.sizer.Add(t)
        i = 0
        for artist in self.artists_list:
            label = artist.title
            b = wx.Button(self, i, label=label, size=(200, 25), style=wx.BU_LEFT)
            self.sizer.Add(b)
            b.Bind(wx.EVT_BUTTON, self.on_artist)
            i += 1
        self.SetSizer(self.sizer)

    def on_artist(self, event):
        self.selected_artist = self.artists_list[event.Id]
        self.fr = ArtistMessage(self)
        self.fr.SetSize(400, 80)
        self.fr.SetPosition((300, 200))
        self.fr.Show()

    def on_button(self, event):
        i = event.Id
        self.fr.Destroy()
        self.parent.song_panel.delete_buttons()
        self.parent.album_panel.delete_buttons()
        if i == 1:
            self.parent.song_panel.add_buttons(self.selected_artist.songs)
        else:
            self.parent.album_panel.add_buttons(self.selected_artist.albums)


class ArtistTab(MultiSplitterWindow):
    def __init__(self, parent, player, artists_list):
        MultiSplitterWindow.__init__(self, parent)
        self.artist_panel = ArtistPanel(self, player, artists_list)
        self.album_panel = Panel(self, "Choose an album to listen")
        self.song_panel = SongPanel(self, player)
        self.AppendWindow(self.artist_panel)
        self.AppendWindow(self.album_panel)
        self.AppendWindow(self.song_panel)
        self.SetSashPosition(0, 200)
        self.SetSashPosition(1, 200)
        self.SetSashPosition(2, 200)


class ArtistMessage(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None)
        p = wx.Panel(self, size=(400, 80), pos=(0, 0))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        button1 = wx.Button(p, 1, size=(150, 80), pos=(0, 0), label="Show all artist's songs")
        button2 = wx.Button(p, 2, size=(250, 80), pos=(200, 0), label="Show artist's song grouped by albums")
        button1.Bind(wx.EVT_BUTTON, parent.on_button)
        button2.Bind(wx.EVT_BUTTON, parent.on_button)
        sizer.Add(button1)
        sizer.Add(button2)
        p.SetSizer(sizer)
