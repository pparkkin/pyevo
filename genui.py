
import threading
import wx
from evoimage import EvoImage

class EvoImageThread(threading.Thread):
    def __init__(self, imagefile):
        threading.Thread.__init__(self)

        self.evoimage = EvoImage(imagefile, self.newimage)

    def run(self):
        self.evoimage.run()

    def newimage(self, dna):
        evt = ImageEvent(dna)
        wx.PostEvent(wx.GetApp().frame, evt)

IMAGE_EVT_TYPE = 123

class ImageEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)

        self.SetEventType(IMAGE_EVT_TYPE)
        self.data = data

class MainFrame(wx.Frame):
    def __init__(self, target, parent=None, id=wx.ID_ANY, title='GEN'):
        wx.Frame.__init__(self, parent, id, title)

        self.Show()

        self._panel = wx.Panel(self, wx.ID_ANY)

        self.Connect(wx.ID_ANY, wx.ID_ANY,
                IMAGE_EVT_TYPE, self.on_img)

        # start evoimage thread
        print 'starting evo thread'
        self.evo = EvoImageThread(target)
        self.evo.start()

    def on_img(self, evt):
        prev = self._panel.GetChildren()
        for p in prev:
            p.Destroy()
        dna = evt.data
        dna.print_info()
        print '=='
        width, height = dna._image.size
        image = wx.EmptyImage(width, height)
        image.SetData(dna._image.convert('RGB').tostring())
        bm = image.ConvertToBitmap()
        sbm = wx.StaticBitmap(self._panel, wx.ID_ANY, bm)

class EvoUI(wx.App):
    def set_image(self, img):
        self.target = img

    def start(self):
        self.frame = MainFrame(self.target)

        self.SetTopWindow(self.frame)


if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1:
        main_app = EvoUI()
        main_app.set_image(argv[1])
        main_app.start()
        main_app.MainLoop()

