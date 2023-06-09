FROM ubuntu:16.04

LABEL maintainer="armand@f5.com"

# Define NGINX versions for NGINX Plus and NGINX Plus modules
# Uncomment this block and the versioned nginxPackages in the main RUN
# instruction to install a specific release
# https://docs.nginx.com/nginx/releases/
ENV NGINX_VERSION 23        
# https://nginx.org/en/docs/njs/changes.html
ENV NJS_VERSION   0.5.2     
# https://plus-pkgs.nginx.com
ENV PKG_RELEASE   1~xenial  

# e.g '1234567890'
ARG API_KEY 
ENV ENV_API_KEY=$API_KEY

# e.g https://<fqdn>:8443/1.4
ARG CONTROLLER_URL
ENV ENV_CONTROLLER_URL=$CONTROLLER_URL

# e.g True or False
ARG STORE_UUID=False
ENV ENV_STORE_UUID=$STORE_UUID

# e.g Instance location already defined in Controller
ARG LOCATION
ENV ENV_LOCATION=$LOCATION

# Download certificate (nginx-repo.crt) and key (nginx-repo.key) from the customer portal (https://cs.nginx.com)
# and copy to the build context
COPY nginx-repo.* /etc/ssl/nginx/
COPY nginx-plus-api.conf /etc/nginx/conf.d/
COPY ./entrypoint.sh /

## Install Nginx Plus
# Download certificate and key from the customer portal https://account.f5.com/myf5
# and copy to the build context and set correct permissions
RUN mkdir -p /etc/ssl/nginx
COPY etc/ssl/nginx/nginx-repo.crt /etc/ssl/nginx/nginx-repo.crt
COPY etc/ssl/nginx/nginx-repo.key /etc/ssl/nginx/nginx-repo.key
RUN set -x \
    && chmod 644 /etc/ssl/nginx/* \
    # Create nginx user/group first, to be consistent throughout Docker variants
    && addgroup --system --gid 1001 nginx \
    && adduser --system --disabled-login --ingroup nginx --no-create-home --home /nonexistent --gecos "nginx user" --shell /bin/false --uid 1001 nginx \
    # Install prerequisite packages, vim for editing, then Install NGINX Plus
    && apt-get update && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get -qq -y install --no-install-recommends apt-transport-https lsb-release ca-certificates wget dnsutils gnupg vim-tiny apt-utils \
    # Install NGINX Plus from repo (https://cs.nginx.com/repo_setup)
    && wget http://nginx.org/keys/nginx_signing.key && apt-key add nginx_signing.key \
    && printf "deb https://plus-pkgs.nginx.com/ubuntu `lsb_release -cs` nginx-plus\n" | tee /etc/apt/sources.list.d/nginx-plus.list \
    && wget -P /etc/apt/apt.conf.d https://cs.nginx.com/static/files/90nginx \
    && apt-get update \
    #
    ## Install the latest release of NGINX Plus and/or NGINX Plus modules
    ## Optionally use versioned packages over defaults to specify a release
    # List available versions: 
    && apt-cache policy nginx-plus \
    ## Uncomment one:
    # && DEBIAN_FRONTEND=noninteractive apt-get -qq -y install --no-install-recommends nginx-plus \
    && DEBIAN_FRONTEND=noninteractive apt-get -qq -y install --no-install-recommends nginx-plus=${NGINX_VERSION}-${PKG_RELEASE} \
    #
    # NGINX Javascript module needed for APIM
    nginx-plus-module-njs  \
    #
    # Install Controller Agent
    && curl -k -sS -L ${CONTROLLER_URL}/install/controller/ > install.sh \
    && sed -i 's/^assume_yes=""/assume_yes="-y"/' install.sh \
    && sh ./install.sh -y \
    # Set permissions 
    && chown -R nginx:nginx /etc/nginx \
    # Forward request and error logs to docker log collector
    && ln -sf /dev/stdout /var/log/nginx-controller/agent.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log \
    # Raise the limits to successfully run benchmarks
    && ulimit -c -m -s -t unlimited \
    # Cleanup
    && apt-get remove --purge --auto-remove -y gnupg lsb-release apt-utils \  
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/nginx-plus.list \
    && rm -rf /etc/apt/apt.conf.d/90nginx \
    && rm -rf nginx_signing.key \
    # Remove the cert/keys from the image
    && rm /etc/ssl/nginx/nginx-repo.crt /etc/ssl/nginx/nginx-repo.key

# COPY /etc/nginx (Nginx configuration) directory
COPY etc/nginx /etc/nginx

# EXPOSE common ports, HTTP 80 and HTTPS 443
EXPOSE 80 443
STOPSIGNAL SIGTERM
ENTRYPOINT ["sh", "/entrypoint.sh"]