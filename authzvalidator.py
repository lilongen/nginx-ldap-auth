
import yaml
import re
import os
import pprint

class AuthzValidator():
    def __init__(self):
        def getYamlFile():
            return os.path.dirname(os.path.realpath(__file__)) + '/nla.groups.yaml'

        with open(getYamlFile()) as f: 
            info = yaml.load(f)
        redelimeter = re.compile(r'\s*,\s*')

        userGroups = {}
        nlaGroups = {}

        for group, userList in info['group'].items():
            userGroups[group] = re.split(redelimeter, userList.strip())
        
        for group, guList in info['x-ldap-group'].items():
            node = nlaGroups[group] = {}
            node['g'] = []
            node['u'] = []
            for item in guList:
                item = item.strip()
                # g;super, data
                # u;lile, wangjd, luoyw, baosy, liukl, tangzx, maocy, wangxt, jingwz
                node[item[0:1]] += re.split(redelimeter, item[2:])

        self.userGroups = userGroups
        self.nlaGroups = nlaGroups


    def __str__(self):
        pp = pprint.PrettyPrinter(indent=4)
        return 'usergroups: %s \n\nnlaGroups: %s\n' % (pp.pformat(self.userGroups), pp.pformat(self.nlaGroups))


    def valid(self, group, user):
        if group == '':
            return True
        if user in self.userGroups['super']:
            return True
        if not group in self.nlaGroups:
            return False
        if user in self.nlaGroups[group]['u']:
            return True
        for g in self.nlaGroups[group]['g']:
            if user in self.userGroups[g]:
                return True
        return False


if __name__ == '__main__':
    validGroups = ['datav.tagging', 'datav.skyeye', 'datav.dashboard']
    invalidGroups = ['invalid.tagging', 'invalid.skyeye', '']
    users = ['lile', 'jenkins']
    
    def getTestset(groups, users):
        testset = []
        for g in groups:
            for u in users:
                testset.append((g, u))
        return testset

    authzvalidator = AuthzValidator()
    print(str(authzvalidator))
    print("do validating test ... ")
    for g, u in getTestset(validGroups + invalidGroups, users):
        print('valid({}, {}) : {}'.format(g, u, authzvalidator.valid(g, u)))

