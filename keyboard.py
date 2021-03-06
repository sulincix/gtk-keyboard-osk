#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from pynput.keyboard import Key, Controller
import os
import sys
import fcntl
import subprocess
fh=0
#https://stackoverflow.com/questions/380870/make-sure-only-a-single-instance-of-a-program-is-running
def run_once():
    global fh
    fh=open(os.path.realpath(__file__),'r')
    try:
        fcntl.flock(fh,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except:
        print("Process already running.")
        os._exit(0)

run_once()
def get_output(cmd):
    p = subprocess.Popen(["sh", "-c", cmd], stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.decode("utf-8")

# If set True log all events (Too dangerous for privacy)
debug=("--debug" in sys.argv)
theming=("--no-theme" not in sys.argv)
scale=1


# define css
screen = Gdk.Screen.get_default()
# Window create
w = Gtk.Window(Gtk.WindowPosition.CENTER_ALWAYS)

css = """
button, label, entry {
    font-size: """+str(screen.get_height()*scale/62)+"""px;
    font-family: monospace;
}
button {
    padding: """+str(screen.get_height()*scale/300)+"""px;
    margin: """+str(screen.get_height()*scale/355)+"""px;
    min-height: """+str(screen.get_height()*scale/40)+"""px;
    min-width: """+str(screen.get_height()*scale/40)+"""px;
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
if theming:
    # Remove user theme
    os.environ["GTK_THEME"] = "Adwaita-dark"
    w.set_opacity(0.9)
    css+="""
    * {
        color: #fff;
        border-width: 0px;
    }
    box, headerbar, window {
        background: #000;
    }
    button {
        background: #333;
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

w.set_opacity(0.9)
if "--no-move" not in sys.argv:
    hb = Gtk.HeaderBar()
    w.set_titlebar(hb)
    w.add(wlayout)
    w.set_resizable(False)
else:
    wl = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    wl2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    w.add(wl2)
    hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    w.set_decorated(False)
    w.move(0,screen.get_height()*0.70)
    wl.pack_start(hb,0,True,False)
    wl.pack_start(wlayout,1,True,False)
    wl2.pack_start(Gtk.Label(),1,True,False)
    wl2.pack_start(Gtk.Label(),1,True,False)
    wl2.pack_start(Gtk.Label(),1,True,False)
    wl2.pack_start(wl,1,True,False)
    wl2.pack_end(Gtk.Label(),1,True,False)
    wl2.pack_end(Gtk.Label(),1,True,False)
    wl2.pack_end(Gtk.Label(),1,True,False)
    w.resize(screen.get_width(),screen.get_height()*0.30)
w.set_accept_focus(False)
w.set_keep_above(True)
w.set_deletable(False)
w.set_skip_taskbar_hint(True)
w.set_skip_pager_hint(True)


# define static variables
l = []  # row array
l2 = []  # row array (left)
trf = ["+1234567890/-", "fg????odrnhpqw", "uiea??tkmly??x", "<j??vc??zsb.,", ""]
trq = ["\"1234567890*-", "qwertyu??op????", "asdfghjkl??i,", "<zxcvbnm????.", ""]
aqvoid = ["+1234567890/-", "aqvoidf??nlmk", "??csergpyjh??x", "<tbuz??w????.,", ""]

ru=["??1234567890-=","????????????????????????","??????????????????????\\","~??????????????????.",""]
us= ["`1234567890-=","qwertyuiop[]","asdfghjkl;'\\","~zxcvbnm,./",""]
single_keys = [] 
big = False

lang=get_output("setxkbmap -query | grep layout").split(":")[-1].strip().split(",")[0]
variant=get_output("setxkbmap -query | grep variant").split(":")[-1].strip().split(",")[0]
kb=lang+variant

if "aqvoid" in sys.argv:
    kbd = aqvoid
elif  kb == "trf":
    kbd = trf
elif kb == "us":
    kbd = us
elif kb == "ru":
    kbd = ru
else:
    kbd = trq

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
mode=Gtk.Button(label=" ??? ")
mode_show=Gtk.Button(label=" ??? ")
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


hl = Gtk.Box()
if "--no-move" in sys.argv:
    hl.pack_start(key(Key.esc, "esc").button, 1,True,False)
    hb.pack_start(hl, 1,True,False)
    hl.pack_start(Gtk.Label(label="      "),1,True,False)
    
hl.pack_start(key(Key.f1, "f1").button,1,True,False)
hl.pack_start(key(Key.f2, "f2").button,1,True,False)
hl.pack_start(key(Key.f3, "f3").button,1,True,False)
hl.pack_start(key(Key.f4, "f4").button,1,True,False)
hl.pack_start(Gtk.Label(label="      "),1,True,False)
hl.pack_start(key(Key.f5, "f5").button,1,True,False)
hl.pack_start(key(Key.f6, "f6").button,1,True,False)
hl.pack_start(key(Key.f7, "f7").button,1,True,False)
hl.pack_start(key(Key.f8, "f8").button,1,True,False)
hl.pack_start(Gtk.Label(label="      "),1,True,False)
hl.pack_start(key(Key.f9, "f9").button,1,True,False)
hl.pack_start(key(Key.f10, "f10").button,1,True,False)
hl.pack_start(key(Key.f11, "f11").button,1,True,False)
hl.pack_start(key(Key.f12, "f12").button,1,True,False)

if "--no-exit" not in sys.argv:
    exit = Gtk.Button(label="???")
    exit.connect("clicked", Gtk.main_quit)
else:
    exit = Gtk.Label()
    
if "--no-move" not in sys.argv:
    hb.pack_start(key(Key.esc, "esc").button)
    hb.set_custom_title(hl)
    hb.pack_end(exit)
    hb.pack_end(mode_show)
else:
    hl.pack_start(Gtk.Label(label="      "),1,True,False)
    hl.pack_end(exit, 1,True,False)
    hl.pack_end(mode_show, 1,True,False)

l[1].pack_start(key(Key.tab, "Tab").button, 0, False, False)
capslock = Gtk.Button(label="Caps")
capslock.connect("clicked", capslock_toggle)
capslock.set_name("key_disabled")
l[2].pack_start(capslock, 0, False, False)
l[3].pack_start(key(Key.shift, "  ???  ", True).button, 0, False, False)
l[4].pack_start(key(Key.ctrl, "ctrl", True).button, 0, False, False)
l[4].pack_start(key(Key.cmd, "???").button, 0, False, True)
l[4].pack_start(alt, 0, False, False)
l[4].pack_start(key(Key.space, " ").button, 1, True, True)
l[4].pack_start(key(Key.alt_gr, "altgr", True).button, 0, False, False)
l[4].pack_start(key(Key.cmd, "???").button, 0, False, False)
l[4].pack_start(key(Key.ctrl, "ctrl", True).button, 0, False, False)

for j in kbd:
    for i in j:
        l[kbd.index(j)].pack_start(
            key(i," {} ".format(i),flat=i.isalpha()).button, 1, True, True)

l[0].pack_start(key(Key.backspace, "     ???     ").button, 0, False, False)
l[1].pack_start(key(Key.delete, "delete").button, 0, False, False)
l[2].pack_start(key(Key.enter, "  ???  ").button, 0, False, False)
l[3].pack_start(key(Key.shift, "   ???   ", True).button, 0, False, False)

for j in [0,1,2,3,4]:
    ll = Gtk.Box()
    ll.set_homogeneous(True)
    l2.append(ll)
    layout2.pack_start(ll, 1, True, True)


l2[0].pack_start(key(Key.media_volume_down, "V-").button, 1, True, True)
l2[0].pack_start(key(Key.media_volume_mute, "V0").button, 1, True, True)
l2[0].pack_start(key(Key.media_volume_up, "V+").button, 1, True, True)

l2[1].pack_start(key(Key.page_up, "pgup").button, 1, True, True)
l2[1].pack_start(key(Key.up, "???").button, 1, True, True)
l2[1].pack_start(key(Key.page_down, "pgdwn").button, 1, True, True)
l2[2].pack_start(key(Key.left, "???").button, 1, True, True)
l2[2].pack_start(key(Key.enter, "???").button, 0, True, True)
l2[2].pack_start(key(Key.right, "???").button, 1, True, True)
l2[3].pack_start(key(Key.home, "home").button, 1, True, True)
l2[3].pack_start(key(Key.down, "???").button, 1, True, True)
l2[3].pack_start(key(Key.end, "end").button, 1, True, True)
l2[4].pack_start(key(Key.insert, "insert").button, 1, True, True)
l2[4].pack_start(mode, 1, True, True)
l2[4].pack_start(key(Key.print_screen, "sysrq").button, 1, True, True)


w.show_all()
mode_click(None)
Gtk.main()
