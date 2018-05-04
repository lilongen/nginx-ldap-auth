        location /login {
            proxy_pass http://backend/login;
            # Login service returns a redirect to the original URI
            # and sets the cookie for the ldap-auth daemon
            proxy_set_header X-Target $request_uri;
        }
