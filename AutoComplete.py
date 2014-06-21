# coding=utf8
import sublime_plugin
import sublime

from time import time as time

debug = False

class AutoComplete(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):

        if is_exclude(view, locations):
            return ([], 0)

        start_time = time()

        words = set()

        # current view
        words.update(view.extract_completions(prefix, locations[0]) if len(locations) else view.extract_completions(prefix))

        # all views
        [v for window in sublime.windows() for v in window.views() if (v.buffer_id() != view.buffer_id() and time() - start_time < 0.040 and words.update(v.extract_completions(prefix)))]

        if debug and words:
            print(words)
            print(str(time() - start_time) + '\twords: '+str(len(words)))
        return ([(w, ) for w in words], 0)

AutoComplete.words = {} # for future caching.. of closed views

def is_exclude(view, locations = None):
    return (view.file_name() and should_exclude(view.file_name())) or should_exclude(view.settings().get('syntax')) or ( locations and len(locations) and should_exclude(view.scope_name(locations[0])))

def should_exclude(string):
    return len([1 for exclusion in Pref.excluded_files_folders_syntaxes_scopes if exclusion in string.lower()])

Pref = {}
s = {}

class Pref():
    def load(self):
        if debug:
            print('-----------------')
        Pref.excluded_files_folders_syntaxes_scopes = [string.strip().lower() for string in s.get('excluded_files_folders_syntaxes_scopes', []) if string]

def plugin_loaded():
    global Pref, s
    s = sublime.load_settings('AutoComplete.sublime-settings')
    Pref = Pref()
    Pref.load()
    s.clear_on_change('reload')
    s.add_on_change('reload', lambda:Pref.load())