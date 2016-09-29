# ref : http://egloos.zum.com/mcchae/v/11076302 [Accessed 2016 09 30]
import pprint


class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, _object, context, maxlevels, level):

        if isinstance(_object, unicode):
            return "'%s'" % _object.encode('utf8'), True, False
        elif isinstance(_object, str):
            _object = unicode(_object, 'utf8')
            return "'%s'" % _object.encode('utf8'), True, False

        return pprint.PrettyPrinter.format(self, _object, context, maxlevels, level)
