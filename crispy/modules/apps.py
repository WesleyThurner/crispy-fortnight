import logging
import shlex

from crispy.lib.module import *
from crispy.lib.fprint import *

logger = logging.getLogger(__name__)

__class_name__ = "AppsModule"
class AppsModule(CrispyModule):
    """ Enum applications on a remote machine. """

    # can be: 'Darwin', 'Linux', 'Windows', 'Android'
    compatible_systems = ['Darwin', 'Linux']

    def run(self, args):
        logger.debug("run(args) was called")

        if (self.is_compatible()):
            print "\nInstalled applications:\n==================="

            try:
                if self.client.is_darwin():
                    apps = self.client.conn.modules['os'].listdir('/Applications')
                    for app in apps:
                        if app.endswith(".app"):
                            try:
                                pl = self.client.conn.modules['plistlib'].readPlist('/Applications/' + app + '/Contents/Info.plist')
                                print app[:-4] + " " + pl["CFBundleShortVersionString"]
                            except:
                                print app[:-4] + " [No version in plist]"
                elif self.client.is_unix():
                    # Only gathers applications isntalled by a package manager
                    # for additional package managers, add additional comand in package_managers
                    package_managers = ['dpkg --get-selections', 'yum list installed']
                    for a in package_managers:
                        try:
                            #shlex splits string to ensure compatibility with check_output
                            command = shlex.split(a)
                            attempt_unix_apps = self.client.conn.modules['subprocess'].check_output(command)
                            print attempt_unix_apps
                        except OSError:
                            continue
                success("Done.")
            except KeyboardInterrupt:
                logger.info("Caught Ctrl-C")
            except Exception as e:
                logger.error(e)
                error(e)
        else:
            error("Current OS's supported: {}".format(', '.join(self.compatible_systems)))
