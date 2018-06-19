
import yaml
import re
import os
import pprint

class AuthzValidator():
    def __init__(self):
        def getYamlFile():
            return os.path.dirname(os.path.realpath(__file__)) + '/nginx.ldap.auth.groups.yaml'

        with open(getYamlFile()) as f:
            info = yaml.load(f)
        redelimeter = re.compile(r',\s*')

        userGroups = {}
        xldapGroups = {}

        for group, userList in info['group'].items():
            userGroups[group] = re.split(redelimeter, userList.strip())
        
        for group, guList in info['x-ldap-group'].items():
            node = xldapGroups[group] = {}
            node['g'] = []
            node['u'] = []
            for item in guList:
                item = item.strip()
                # g;super, data
                # u;lile, wangjd, luoyw, baosy, liukl, tangzx, maocy, wangxt, jingwz
                node[item[0:1]] += re.split(redelimeter, item[2:])

        self.userGroups = userGroups
        self.xldapGroups = xldapGroups

    def __str__(self):
        pp = pprint.PrettyPrinter(indent=4)
        return 'usergroups: %s \n\nxldapgroups: %s\n' % (pp.pformat(self.userGroups), pp.pformat(self.xldapGroups))


    def valid(self, group, user):
        if group == '':
            return True
        if not group in self.xldapGroups:
            return False
        if user in self.xldapGroups[group]['u']:
            return True
        for g in self.xldapGroups[group]['g']:
            if user in self.userGroups[g]:
                return True
        return False


if __name__ == '__main__':
    authzvalidator = AuthzValidator()
    print(str(authzvalidator))
    test_set = (('datav.tagging', 'lile'), ('datav.tagging', 'jenkins'), ('', 'lile'), ('', 'jenkins'))
    print("do validating test ... ")
    for gn in test_set:
        print('. validate {}: {}'.format(str(gn), authzvalidator.valid(gn[0], gn[1])))

