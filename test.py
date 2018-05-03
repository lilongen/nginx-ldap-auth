#!/bin/sh
''''which python2 >/dev/null && exec python2 "$0" "$@" # '''
''''which python  >/dev/null && exec python  "$0" "$@" # '''

# Copyright (C) 2014-2015 Nginx, Inc.
#import nginx-ldap-auth-daemon-with.group.support
import yaml
import re
import pprint
import sys

class UserValidator():
    def __init__(self):
        self.groups = {}
        with open("./nginx.ldap.auth.groups.yaml") as f:
            groupInfo = yaml.load(f)

        pattern = re.compile(r"\s{2,}")
        for group, userLists in groupInfo.items():
            if not self.groups.has_key(group):
                self.groups[group] = [];
                
            for group2, userList in userLists.items():
                userList = userList.strip()
                userList = re.sub(pattern, " ", userList)
                self.groups[group] += userList.split(" ")

    
    def valid(self, group, user):
        return self.groups.has_key(group) and user in self.groups[group] 


if __name__ == '__main__':
    group = sys.argv[1]
    name = sys.argv[2]
    validator = UserValidator()
    pprint.pprint(validator.groups)
    ret = validator.valid(group,name)
    print(ret)