import wx
import os


class AlbumCover(wx.Frame):
    def __init__(self, song):
        wx.Frame.__init__(self, None)
        f = open('temp.jpeg', 'wb')
        f.write(song.image_data)
        # stream = wx.InputStream()
        f.close()
        png = wx.Bitmap('temp.jpeg', wx.BITMAP_TYPE_JPEG)
        wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
        os.remove('temp.jpeg')
