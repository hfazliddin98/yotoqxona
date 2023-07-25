# server {
#     listen                  443 ssl http2;
#     listen                  [::]:443 ssl http2;
#     server_name             example.com;
#     set                     $base /var/www/example.com;

#     # SSL
#     ssl_certificate         /etc/letsencrypt/live/example.com/fullchain.pem;
#     ssl_certificate_key     /etc/letsencrypt/live/example.com/privkey.pem;
#     ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

#     # security
#     include                 nginxconfig.io/security.conf;

#     # logging
#     access_log              /var/log/nginx/access.log combined buffer=512k flush=1m;
#     error_log               /var/log/nginx/error.log warn;

#     location / {
#         include nginxconfig.io/python_uwsgi.conf;
#     }

#     # Django media
#     location /media/ {
#         alias $base/media/;
#     }

#     # Django static
#     location /static/ {
#         alias $base/static/;
#     }

#     # additional config
#     include nginxconfig.io/general.conf;
# }

# # subdomains redirect
# server {
#     listen                  443 ssl http2;
#     listen                  [::]:443 ssl http2;
#     server_name             *.example.com;

#     # SSL
#     ssl_certificate         /etc/letsencrypt/live/example.com/fullchain.pem;
#     ssl_certificate_key     /etc/letsencrypt/live/example.com/privkey.pem;
#     ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
#     return                  301 https://example.com$request_uri;
# }

# # HTTP redirect
# server {
#     listen      80;
#     listen      [::]:80;
#     server_name .example.com;
#     include     nginxconfig.io/letsencrypt.conf;

#     location / {
#         return 301 https://example.com$request_uri;
#     }
# }