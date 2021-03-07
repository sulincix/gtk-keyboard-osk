from gi.repository import Gtk, Gdk
from pynput.keyboard import Key, Controller
import os
import sys
# Remove user theme
os.environ["GTK_THEME"] = "Adwaita-dark"
# define css
css = """
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

#key_enabled {
    
}
.text-button *{
    font-size: 150%;
    border-width: 0;
    font-family: monospace;
}
"""

# Css provider
screen = Gdk.Screen.get_default()
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
single_keys = []
big = False

kbd = []
if len(sys.argv) < 2:
    kbd=trf
elif sys.argv[1] == "trq":
    kbd = trq
elif sys.argv[1] == "trf":
    kbd = trf

# alt key fixes (xfce lxde cinnamon)
alt_enabled = False
alt_lock = False
alt = Gtk.Button("alt")


def alt_toggle(widget):
    global alt_enabled
    global alt_lock
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


class key:
    def __init__(self, n, m=None, toggle=False, flat=True):
        if not m:
            m = n
        self.key = n
        self.label = m
        self.flat = flat
        self.button = Gtk.Button(m)
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

        if self not in single_keys:
            for key in single_keys:
                if not key.lock:
                    key.release(None)
            if not alt_lock:
                alt_enabled = False
                alt.set_name("key_disabled")
            keyboard.release(Key.alt)

    def release(self, widget):
        self.active = False
        self.button.set_name("key_disabled")
        if self.key:
            keyboard.release(self.key)

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


def capslock_toggle(widget):
    global big
    if big:
        widget.set_name("key_disabled")
    else:
        widget.set_name("key_lock")
    big = not big


for j in kbd:
    ll = Gtk.Box()
    l.append(ll)
    layout.pack_start(ll, 1, True, True)

for j in kbd:
    ll = Gtk.Box()
    ll.set_homogeneous(True)
    l2.append(ll)
    layout2.pack_start(ll, 1, True, True)


hb.add(key(Key.esc, "esc").button)
hl = Gtk.Box()
hb.set_custom_title(hl)
hl.add(key(Key.f1, "f1").button)
hl.add(key(Key.f2, "f2").button)
hl.add(key(Key.f3, "f3").button)
hl.add(key(Key.f4, "f4").button)
hl.add(Gtk.Label("      "))
hl.add(key(Key.f5, "f5").button)
hl.add(key(Key.f6, "f6").button)
hl.add(key(Key.f7, "f7").button)
hl.add(key(Key.f8, "f8").button)
hl.add(Gtk.Label("      "))
hl.add(key(Key.f9, "f9").button)
hl.add(key(Key.f10, "f10").button)
hl.add(key(Key.f11, "f11").button)
hl.add(key(Key.f12, "f12").button)
exit = Gtk.Button("✖")
exit.connect("clicked", Gtk.main_quit)
hb.pack_end(exit)


l[1].pack_start(key(Key.tab, "Tab").button, 0, False, False)
capslock = Gtk.Button("Caps")
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
            key(i, flat=i.isalpha()).button, 1, True, True)

l[0].pack_start(key(Key.backspace, " ⟸ ").button, 0, False, False)
l[1].pack_start(key(Key.delete, " ⌫ ").button, 0, False, False)
l[2].pack_start(key(Key.enter, "  ⏎  ").button, 0, False, False)
l[3].pack_start(key(Key.shift, "  ⇧  ", True).button, 0, False, False)


l2[0].pack_start(key(Key.home, "home").button, 1, True, True)
l2[0].pack_start(key(Key.end, "end").button, 1, True, True)
l2[1].pack_start(key(Key.page_up, "pgup").button, 1, True, True)
l2[1].pack_start(key(Key.page_down, "pgdwn").button, 1, True, True)
l2[2].pack_start(key(Key.insert, "insert").button, 1, True, True)
l2[2].pack_start(key(Key.print_screen, "sysrq").button, 1, True, True)
l2[3].pack_start(Gtk.Label(" "), 1, True, True)
l2[3].pack_start(key(Key.up, "↑").button, 1, True, True)
l2[3].pack_start(Gtk.Label(" "), 1, True, True)
l2[4].pack_start(key(Key.left, "←").button, 1, True, True)
l2[4].pack_start(key(Key.down, "↓").button, 1, True, True)
l2[4].pack_start(key(Key.right, "→").button, 1, True, True)
w.show_all()
Gtk.main()
