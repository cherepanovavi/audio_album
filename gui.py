import wx
import os
import wx.media
import audio_album
from audio_player import PlayerTab
from tabs_and_panels import HalfSplittedTab, SongTab, PlaylistTab
from artist_tab import ArtistTab

my_audio_album = None
dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        splitter = wx.SplitterWindow(self)
        p = wx.Panel(splitter)
        nb = wx.Notebook(p)

        player = PlayerTab(splitter, my_audio_album)
        self.song_tab = SongTab(nb, my_audio_album.songs, player)
        self.song_tab.SetSize(600, 600)
        self.artist_tab = ArtistTab(nb, player, my_audio_album.artists)
        self.albums_tab = HalfSplittedTab(nb, my_audio_album.albums, player, "Choose an album to listen")
        self.genres_tab = HalfSplittedTab(nb, my_audio_album.genres, player, "Choose a genre to listen")
        self.playlist_tab = PlaylistTab(nb, my_audio_album.playlists, player, "Choose a playlist to listen", my_audio_album)

        nb.AddPage(self.song_tab, "Songs")
        nb.AddPage(self.artist_tab, "Artists")
        nb.AddPage(self.albums_tab, "Albums")
        nb.AddPage(self.genres_tab, "Genres")
        nb.AddPage(self.playlist_tab, "Playlists")
        splitter.SplitHorizontally(p, player)
        splitter.SetSashGravity(0.8)

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        mb = wx.MenuBar()
        m = wx.Menu()
        s = 'Update {} tab'
        labels = ['Update everything', s.format('songs'), s.format('artists'), s.format('albums'), s.format('genres'),
             s.format('playlists')]
        handlers = [self.update, lambda e: self.update_tab(self.song_tab, my_audio_album.songs),
                    lambda e: self.update_tab(self.artist_tab, my_audio_album.artists),
                    lambda e: self.update_tab(self.albums_tab, my_audio_album.albums),
                    lambda e: self.update_tab(self.genres_tab, my_audio_album.genres),
                    lambda e: self.update_tab(self.playlist_tab, my_audio_album.playlists)]
        for i in range(0, 6):
            item = m.Append(-1, labels[i])
            self.Bind(wx.EVT_MENU, handlers[i], item)
        mb.Append(m, 'Update')
        self.SetMenuBar(mb)

    def update(self, event):
        self.update_tab(self.song_tab, my_audio_album.songs)
        self.update_tab(self.artist_tab, my_audio_album.artists)
        self.update_tab(self.albums_tab, my_audio_album.albums)
        self.update_tab(self.genres_tab, my_audio_album.genres)
        self.update_tab(self.playlist_tab, my_audio_album.playlists)

    def update_tab(self, tab, objects_list):
        tab.panel.delete_buttons()
        tab.panel.add_buttons(objects_list)


if __name__ == "__main__":
    app = wx.App()
    dir_selector = wx.DirSelector("Choose a folder to search audio files")
    try:
        my_audio_album = audio_album.AudioAlbum(dir_selector)
    except ValueError:
        wx.MessageBox("Directory is not selected. Application would be closed.", 'Error', wx.OK | wx.ICON_ERROR)
        app.Destroy()
    else:
        fr = MainFrame()
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(os.path.join(bitmapDir, "icon.png")))
        fr.SetIcon(icon)
        fr.SetSize(600, 600)
        fr.Show()
        app.MainLoop()
