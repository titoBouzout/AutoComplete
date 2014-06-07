# coding=utf8
import sublime_plugin
import sublime

from time import time as time

debug = False

class AllAutocomplete(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        start_time = time()

        words = set()

        # current view
        words.update(view.extract_completions(prefix, locations[0]) if len(locations) else view.extract_completions(prefix))

        # all views
        [v for window in sublime.windows() for v in window.views() if (v.buffer_id() != view.buffer_id() and time() - start_time < 0.040 and words.update(v.extract_completions(prefix)))]

        if debug and words:
            print(words)
            print(str(time() - start_time) + '\twords: '+str(len(words)))

        return [(w, ) for w in words]

AllAutocomplete.words = {} # for future caching.. of closed views