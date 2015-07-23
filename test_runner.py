import os
import sys
import unittest

if __name__ == '__main__':
    sys.path.insert(0, os.path.expanduser('~/google_appengine'))

    import dev_appserver
    dev_appserver.fix_sys_path()

    try:
        import appengine_config
        (appengine_config)
    except ImportError:
        print "Note: unable to import appengine_config."

    # Discover and run tests.
    suite = unittest.loader.TestLoader().discover('./tests')
    unittest.TextTestRunner(verbosity=2).run(suite)
