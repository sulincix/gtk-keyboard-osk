
const St = imports.gi.St;
const Main = imports.ui.main;
const Keyboard = imports.ui.keyboard.Keyboard;
const Gio = imports.gi.Gio;
const GLib = imports.gi.GLib;


let showBackup
let hideBackup

function init() {
    
}

function enable() {
    showBackup = Keyboard.prototype['show']
    Keyboard.prototype['_show'] = function(monitor) {
         GLib.spawn_command_line_async( "osk", null ); // Start command
    }

    hideBackup = Keyboard.prototype['hide']
    Keyboard.prototype['_hide'] = function() {
         GLib.spawn_command_line_async( "killall osk", null ); // Start command
    }

}

function disable() {
    Keyboard.prototype['show'] = showBackup
    Keyboard.prototype['hide'] = hideBackup
}
