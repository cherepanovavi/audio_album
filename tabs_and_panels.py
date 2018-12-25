import wx
from wx.lib.scrolledpanel import ScrolledPanel
from audio_objects import Song
from menus import get_playlist_songs, get_playlist_title


class Panel(wx.Panel):
    def __init__(self, parent, text):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)
        self.parent = parent
        self.objects_list = None
        self.buttons = []
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        t = wx.StaticText(self, -1, text)
        self.sizer.Add(t)
        self.SetSizer(self.sizer)

    def add_buttons(self, objects_list):
        self.objects_list = objects_list
        i = 0
        for au_obj in objects_list:
            obj_id = i
            if type(au_obj) == Song:
                obj_id = au_obj.id
            button = wx.Button(self, obj_id, label=au_obj.title, size=(200, 25), style=wx.BU_LEFT)
            self.buttons.append(button)
            self.sizer.Add(button)
            button.Bind(wx.EVT_BUTTON, self.on_button)
            i += 1
        self.Layout()

    def delete_buttons(self):
        button: wx.Button
        for button in self.buttons:
            button.Destroy()
        self.buttons = []
        self.objects_list = None

    def on_button(self, event):
        self.parent.song_panel.delete_buttons()
        self.parent.song_panel.add_buttons(self.objects_list[event.Id].songs)


class SongPanel(ScrolledPanel):
    def __init__(self, parent, player, text="Choose a song to listen"):
        ScrolledPanel.__init__(self, parent, style=wx.BORDER_SUNKEN)
        self.parent = parent
        self.objects_list = None
        self.buttons = []
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        t = wx.StaticText(self, -1, text)
        self.sizer.Add(t)
        self.SetSizer(self.sizer)
        self.SetupScrolling()
        self.player = player

    def on_button(self, event):
        self.player.change_now_playing(self.objects_list)
        self.player.on_song(event)

    def add_buttons(self, objects_list):
        self.objects_list = objects_list
        for au_obj in objects_list:
            obj_id = au_obj.id
            button = wx.Button(self, obj_id, label=au_obj.title, size=(200, 25), style=wx.BU_LEFT)
            self.buttons.append(button)
            self.sizer.Add(button)
            button.Bind(wx.EVT_BUTTON, self.on_button)
            button.Bind(wx.EVT_RIGHT_DOWN, self.show_menu)
        self.Layout()

    def delete_buttons(self):
        button: wx.Button
        for button in self.buttons:
            button.Destroy()
        self.buttons = []
        self.objects_list = None

    def show_menu(self, event):
        menu = self.player.audio_album.songs_id[event.Id].menu()
        self.PopupMenu(menu, self.ScreenToClient(wx.GetMousePosition()))


class SongTab(SongPanel):
    def __init__(self, parent, song_list, player):
        SongPanel.__init__(self, parent, player)
        # self.panel = SongPanel(self, player)
        self.panel = self
        self.panel.add_buttons(song_list)


class HalfSplittedTab(wx.SplitterWindow):
    def __init__(self, parent, objects_list, player, text):
        wx.SplitterWindow.__init__(self, parent)
        self.panel = Panel(self, text)
        self.panel.add_buttons(objects_list)
        self.song_panel = SongPanel(self, player)
        self.SplitVertically(self.panel, self.song_panel)
        self.SetSashGravity(0.5)


class PlaylistTab(HalfSplittedTab):
    def __init__(self, parent, objects_list, player, text, au_album):
        wx.SplitterWindow.__init__(self, parent)
        self.panel = PlaylistPanel(self, text, au_album)
        self.panel.add_buttons(objects_list)
        self.song_panel = SongPanel(self, player)
        self.SplitVertically(self.panel, self.song_panel)
        self.SetSashGravity(0.5)
        self.audio_album = au_album
        button = wx.Button(self.panel, size=(100, 40), label="Create a playlist")
        button.SetBackgroundColour('light blue')
        button.Bind(wx.EVT_BUTTON, self.create_playlist)
        self.panel.sizer.Add(button)

    def create_playlist(self, event):
        title = get_playlist_title()
        playlist = self.audio_album.add_playlist(title)
        songs = get_playlist_songs(self.audio_album)
        self.audio_album.add_songs_to_playlist(songs, playlist)
        self.panel.delete_buttons()
        self.panel.add_buttons(self.audio_album.playlists)


class PlaylistPanel(Panel):
    def __init__(self, parent, text, au_album):
        Panel.__init__(self, parent, text)
        self.audio_album = au_album

    def add_buttons(self, objects_list):
        super().add_buttons(objects_list)
        for btn in self.buttons:
            btn.Bind(wx.EVT_RIGHT_DOWN, self.show_menu)

    def show_menu(self, event):
        menu = self.objects_list[event.Id].menu(self.audio_album)
        self.PopupMenu(menu, self.ScreenToClient(wx.GetMousePosition()))

