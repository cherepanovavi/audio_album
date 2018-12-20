import wx
import os
import wx.media
import audio_album
from audio_player import PlayerTab
from tabs_and_panels import HalfSplittedTab, SongTab, PlaylistTab
from artist_tab import ArtistTab
from searcher import Searcher
from audio_objects import Song, Album, Artist, Playlist, Genre

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class MainFrame(wx.Frame):
    def __init__(self, my_audio_album):
        wx.Frame.__init__(self, None)
        self.audio_album = my_audio_album
        splitter = wx.SplitterWindow(self)
        p = wx.Panel(splitter)
        self.nb = wx.Notebook(p)

        self.player = PlayerTab(splitter, my_audio_album)
        self.song_tab = SongTab(self.nb, my_audio_album.songs, self.player)
        self.song_tab.SetSize(600, 600)
        self.artist_tab = ArtistTab(self.nb, self.player, my_audio_album.artists)
        self.albums_tab = HalfSplittedTab(self.nb, my_audio_album.albums, self.player, "Choose an album to listen")
        self.genres_tab = HalfSplittedTab(self.nb, my_audio_album.genres, self.player, "Choose a genre to listen")
        self.playlist_tab = PlaylistTab(self.nb, my_audio_album.playlists, self.player, "Choose a playlist to listen", my_audio_album)

        self.nb.AddPage(self.song_tab, "Songs")
        self.nb.AddPage(self.artist_tab, "Artists")
        self.nb.AddPage(self.albums_tab, "Albums")
        self.nb.AddPage(self.genres_tab, "Genres")
        self.nb.AddPage(self.playlist_tab, "Playlists")
        splitter.SplitHorizontally(p, self.player)
        splitter.SetSashGravity(0.8)

        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        tb = wx.ToolBar(self, -1)
        self.ToolBar = tb
        self.searcher = Searcher(my_audio_album)
        self.search = wx.SearchCtrl(tb, style=wx.TE_PROCESS_ENTER)
        tb.Bind(wx.EVT_TEXT_ENTER, self.on_search)
        tb.AddControl(self.search)
        img = wx.Bitmap(os.path.join(bitmapDir, "update.png"))
        tb.AddTool(23, 'update', img)
        tb.Bind(wx.EVT_TOOL, self.update)
        tb.Realize()

    def update(self, event):
        self.searcher.update()
        self.update_tab(self.song_tab, self.audio_album.songs)
        self.update_tab(self.artist_tab, self.audio_album.artists)
        self.update_tab(self.albums_tab, self.audio_album.albums)
        self.update_tab(self.genres_tab, self.audio_album.genres)
        self.update_tab(self.playlist_tab, self.audio_album.playlists)

    def on_search(self, event):
        i = -1
        search_request = self.search.GetValue()
        results = self.searcher.get_search_results(search_request.lower())
        ch = wx.SingleChoiceDialog(self, 'Found for request: {}'.format(search_request), 'Search result', [r[0] for r in results])
        if ch.ShowModal() == wx.ID_OK:
            i = ch.GetSelection()
        ch.Destroy()
        if i != -1:
            self.open_search_result(results[i][1])

    def open_search_result(self, au_object):
        t = type(au_object)
        if t == Song:
            self.nb.SetSelection(0)
            for button in self.song_tab.panel.buttons:
                if au_object.id == button.Id:
                    self.focus(0, button)
                    break
            self.player.change_now_playing(self.audio_album.songs)
            self.player.set_idx(self.audio_album.songs.index(au_object))
        elif t == Album:
            self.focus(2, self.albums_tab.panel.buttons[self.audio_album.albums.index(au_object)])
        elif t == Artist:
            self.focus(1, self.artist_tab.panel.buttons[self.audio_album.artists.index(au_object)])
        elif t == Playlist:
            self.focus(4, self.playlist_tab.panel.buttons[self.audio_album.playlists.index(au_object)])
        elif t == Genre:
            self.focus(3, self.genres_tab.panel.buttons[self.audio_album.genres.index(au_object)])

    def focus(self, page, focus_button):
        self.nb.SetSelection(page)
        focus_button.SetFocus()

    @staticmethod
    def update_tab(tab, objects_list):
        tab.panel.delete_buttons()
        tab.panel.add_buttons(objects_list)


def main():
    app = wx.App()
    dir_selector = wx.DirSelector("Choose a folder to search audio files")
    try:
        my_audio_album = audio_album.AudioAlbum(dir_selector)
    except ValueError:
        wx.MessageBox("Directory is not selected. Application would be closed.", 'Error', wx.OK | wx.ICON_ERROR)
        app.Destroy()
    else:
        fr = MainFrame(my_audio_album)
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(os.path.join(bitmapDir, "icon.png")))
        fr.SetIcon(icon)
        fr.SetSize(600, 600)
        fr.Show()
        app.MainLoop()


if __name__ == "__main__":
    main()
