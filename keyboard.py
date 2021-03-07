import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from pynput.keyboard import Key, Controller
import os
import sys

# If set True log all events (Too dangerous for privacy)
debug=True


# Remove user theme
#os.environ["GTK_THEME"] = "Adwaita"
# define css
screen = Gdk.Screen.get_default()
css = """
box {
border-width: 0px;
}
button {
    font-size: """+str(screen.get_height()/52)+"""px;
    font-family: monospace;
}
button:hover {
    background: #004c8c;
    color: #FFF;
}
#key_enabled {
    color: #FFF;
    background: #8e0000;
}
#key_lock {
    color: #FFF;
    background: #008e00;
}

"""

# Css provider
gtk_provider = Gtk.CssProvider()
gtk_context = Gtk.StyleContext()
gtk_context.add_provider_for_screen(
    screen, gtk_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
gtk_provider.load_from_data(css.encode("UTF-8"))
keyboard = Controller()

# layout creation
layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
layout2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
wlayout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
wlayout.pack_start(layout, 1, True, True)
wlayout.pack_end(layout2, 0, True, False)
hb = Gtk.HeaderBar()

# Window create
w = Gtk.Window()
w.add(wlayout)
w.set_titlebar(hb)
w.set_accept_focus(False)
w.set_keep_above(True)
w.set_resizable(False)
w.set_deletable(False)


# define static variables
l = []  # row array
l2 = []  # row array (left)
trf = ["+1234567890/-", "fgğıodrnhpqw", "uieaütkmlyşx", "<jövcçzsb.,", ""]
trq = ["\"1234567890*-", "qwertyuıopğü", "asdfghjklşi,", "<zxcvbnmöç.", ""]
trm = ["\"1234567890*-", "qwertyuiop", "asdfghjkl,", "<zxcvbnm.", ""]
trfm = ["+1234567890/-", "fgodrnhpqw", "uieatkmlyx", "<jvczsb.,", ""]
aqvoid = ["+1234567890/-", "aqvoidfınlmk", "ğcsergpyjhşx", "<tbuzçwöü.,", ""]

ru=["ё1234567890-=","йцукенгшщзхъ","фывапролджэ\\","~ячсмитьбю.",""]
us= ["`1234567890-=","qwertyuiop[]","asdfghjkl;'\\","~zxcvbnm,./",""]
single_keys = [] 
big = False

if  "trq" in sys.argv:
    kbd = trq
    os.system("setxkbmap tr")
elif  "trm" in sys.argv:
    kbd = trm
    os.system("setxkbmap tr")
elif  "trfm" in sys.argv:
    kbd = trfm
    os.system("setxkbmap tr f")
elif  "aqvoid" in sys.argv:
    kbd = aqvoid
    os.system("setxkbmap tr f")
elif "us" in sys.argv:
    kbd=us
    os.system("setxkbmap us")
elif "ru" in sys.argv:
    kbd=ru
    os.system("setxkbmap ru")
else:
    kbd = trf
    os.system("setxkbmap tr f")

# alt key fixes (xfce lxde cinnamon)
alt_enabled = False
alt_lock = False
alt = Gtk.Button(label="alt")


def alt_toggle(widget):
    global alt_enabled
    global alt_lock
    if debug:
        print("Alt-enable:"+str(alt_enabled))
        print("Alt-lock:"+str(alt_lock))
    if not alt_enabled:
        alt_enabled = True
    elif not alt_lock:
        alt_lock = True
    else:
        alt_enabled = False
        alt_lock = False
    if not alt_enabled:
        widget.set_name("key_disabled")
    elif alt_lock:
        widget.set_name("key_lock")
    else:
        widget.set_name("key_enabled")


alt.connect("clicked", alt_toggle)


# mode & mode_show buttons
mode=Gtk.Button(label="⚙")
mode_show=Gtk.Button(label="⚙")
def mode_click(widget):
    layout2.hide()
    mode_show.show()
    w.set_size_request(0,0)
    if debug:
        print("UI minimized")
def mode_show_click(widget):
    layout2.show()
    mode_show.hide()
    if debug:
        print("UI maximized")
    w.set_size_request(0,0)
mode.connect("clicked",mode_click)
mode_show.connect("clicked",mode_show_click)

class key:
    def __init__(self, n, m=None, toggle=False, flat=True):
        if not m:
            m = n
        self.key = n
        self.label = m
        self.flat = flat
        self.button = Gtk.Button(label=m)
        self.active = False
        self.lock = False
        if not toggle:
            self.button.connect("pressed", self.press)
            self.button.connect("released", self.release)
        else:
            self.button.connect("clicked", self.toggle)
        if toggle:
            single_keys.append(self)
        self.button.set_name("key_disabled")

    def press(self, widget):
        global alt_enabled
        self.button.set_name("key_enabled")
        if self.lock:
            self.button.set_name("key_lock")
        if big and self.flat:
            keyboard.press(Key.shift)
        if alt_enabled or alt_lock:
            keyboard.press(Key.alt)
        if self.key:
            keyboard.press(self.key)
        if debug:
            print("Press:"+str(self.key))

    def release(self, widget):
        global alt_enabled
        if not self.lock:
            self.active = False
            self.button.set_name("key_disabled")
            if self.key:
                keyboard.release(self.key)
        if debug:
            print("Release:"+str(self.key))
        if self not in single_keys:
            for key in single_keys:
                if not key.lock and key.active:
                    key.release(self.key)
            if not alt_lock:
                alt_enabled = False
                alt.set_name("key_disabled")
            keyboard.release(Key.alt)

    def toggle(self, widget):
        if not self.active:
            self.active = True
        elif not self.lock:
            self.lock = True
        else:
            self.active = False
            self.lock = False
        if self.active or self.lock:
            self.press(widget)
        else:
            self.release(widget)
        if debug:
            print("Toggle-active:"+str(self.active)+":"+str(self.key))
            print("Toggle-lock:"+str(self.lock)+":"+str(self.key))

def capslock_toggle(widget):
    global big
    if big:
        widget.set_name("key_disabled")
    else:
        widget.set_name("key_lock")
    big = not big


for j in [0,1,2,3,4]:
    ll = Gtk.Box()
    l.append(ll)
    layout.pack_start(ll, 1, True, True)


hb.add(key(Key.esc, "esc").button)
hl = Gtk.Box()
hb.set_custom_title(hl)
hl.add(key(Key.f1, "f1").button)
hl.add(key(Key.f2, "f2").button)
hl.add(key(Key.f3, "f3").button)
hl.add(key(Key.f4, "f4").button)
hl.add(Gtk.Label(label="      "))
hl.add(key(Key.f5, "f5").button)
hl.add(key(Key.f6, "f6").button)
hl.add(key(Key.f7, "f7").button)
hl.add(key(Key.f8, "f8").button)
hl.add(Gtk.Label(label="      "))
hl.add(key(Key.f9, "f9").button)
hl.add(key(Key.f10, "f10").button)
hl.add(key(Key.f11, "f11").button)
hl.add(key(Key.f12, "f12").button)
exit = Gtk.Button(label="✖")
exit.connect("clicked", Gtk.main_quit)
hb.pack_end(exit)
hb.pack_end(mode_show)


l[1].pack_start(key(Key.tab, "Tab").button, 0, False, False)
capslock = Gtk.Button(label="Caps")
capslock.connect("clicked", capslock_toggle)
capslock.set_name("key_disabled")
l[2].pack_start(capslock, 0, False, False)
l[3].pack_start(key(Key.shift, "  ⇧  ", True).button, 0, False, False)
l[4].pack_start(key(Key.ctrl, "ctrl", True).button, 0, False, False)
l[4].pack_start(key(Key.cmd, "❖").button, 0, False, True)
l[4].pack_start(alt, 0, False, False)
l[4].pack_start(key(Key.space, " ").button, 1, True, True)
l[4].pack_start(key(Key.alt_gr, "altgr", True).button, 0, False, False)
l[4].pack_start(key(Key.cmd, "❖").button, 0, False, False)
l[4].pack_start(key(Key.ctrl, "ctrl", True).button, 0, False, False)

for j in kbd:
    for i in j:
        l[kbd.index(j)].pack_start(
            key(i," {} ".format(i),flat=i.isalpha()).button, 1, True, True)

l[0].pack_start(key(Key.backspace, "     ⟸     ").button, 0, False, False)
l[1].pack_start(key(Key.delete, "delete").button, 0, False, False)
l[2].pack_start(key(Key.enter, "  ⏎  ").button, 0, False, False)
l[3].pack_start(key(Key.shift, "   ⇧   ", True).button, 0, False, False)

for j in [0,1,2,3,4]:
    ll = Gtk.Box()
    ll.set_homogeneous(True)
    l2.append(ll)
    layout2.pack_start(ll, 1, True, True)


l2[0].pack_start(key(Key.media_volume_down, "🔈").button, 1, True, True)
l2[0].pack_start(key(Key.media_volume_mute, "🔇").button, 1, True, True)
l2[0].pack_start(key(Key.media_volume_up, "🔊").button, 1, True, True)

l2[1].pack_start(key(Key.page_up, "pgup").button, 1, True, True)
l2[1].pack_start(key(Key.up, "↑").button, 1, True, True)
l2[1].pack_start(key(Key.page_down, "pgdwn").button, 1, True, True)
l2[2].pack_start(key(Key.left, "←").button, 1, True, True)
l2[2].pack_start(key(Key.enter, "⏎").button, 0, True, True)
l2[2].pack_start(key(Key.right, "→").button, 1, True, True)
l2[3].pack_start(key(Key.home, "home").button, 1, True, True)
l2[3].pack_start(key(Key.down, "↓").button, 1, True, True)
l2[3].pack_start(key(Key.end, "end").button, 1, True, True)
l2[4].pack_start(key(Key.insert, "insert").button, 1, True, True)
l2[4].pack_start(mode, 1, True, True)
l2[4].pack_start(key(Key.print_screen, "sysrq").button, 1, True, True)


w.show_all()
mode_click(None)
Gtk.main()
