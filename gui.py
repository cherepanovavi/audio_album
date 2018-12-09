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
        tab1 = SongTab(nb, my_audio_album.songs, player)
        tab1.SetSize(600, 600)
        tab2 = ArtistTab(nb, player, my_audio_album.artists)
        tab3 = HalfSplittedTab(nb, my_audio_album.albums, player, "Choose an album to listen")
        tab4 = HalfSplittedTab(nb, my_audio_album.genres, player, "Choose a genre to listen")
        tab5 = PlaylistTab(nb, my_audio_album.playlists, player, "Choose a playlist to listen", my_audio_album)

        nb.AddPage(tab1, "Songs")
        nb.AddPage(tab2, "Artists")
        nb.AddPage(tab3, "Albums")
        nb.AddPage(tab4, "Genres")
        nb.AddPage(tab5, "Playlists")
        splitter.SplitHorizontally(p,  player)
        splitter.SetSashGravity(0.8)

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


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
