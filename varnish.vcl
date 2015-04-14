vcl 4.0;


acl local {
    "localhost";
    "192.168.1.0"/24;
}

backend default {
    .host = "127.0.0.1";
    .port = "8000";
}

sub vcl_recv {
    unset req.http.Accept-Encoding;
    unset req.http.User-Agent;


    if (req.url ~ "/blog/") {

        // Emulate pjax request for partial view
        if (req.esi_level > 0) {
            set req.http.x-pjax = 1;
        }

        // Check user authentication
        if ((req.http.Cookie ~ "WGAI=") || (req.http.Cookie ~ "hlauth=")) {
            set req.http.x-is-auth = regsub(req.http.Cookie,"^.*?hlauth=([^;]*);*.*$" , "\1");
        } else {
            set req.http.x-is-auth = 0;
        }

        // Session
        if (req.http.Cookie ~ "sessionid") {
            set req.http.x-sessionid = regsub(req.http.Cookie,"^.*?sessionid=([^;]*);*.*$" , "\1");
        }
        // CSRF
        if (req.http.Cookie ~ "csrftoken") {
            set req.http.x-sessionid = regsub(req.http.Cookie,"^.*?csrftoken=([^;]*);*.*$" , "\1");
        }

        // Language
        if (req.http.Cookie ~ "hlang=") {
            set req.http.x-lang = regsub(req.http.Cookie,"^.*?hlang=([^;]*);*.*$" , "\1");
        } else {
            if (req.http.Accept-Language) {
                set req.http.x-lang = req.http.Accept-Language;
            } else {
                set req.http.x-lang = "en";
            }
        }

        // Purge cache by url
        if (req.method == "PURGE") {
            if (client.ip ~ local) {
                return(purge);
            } else {
                return(synth(403, "Forbidden."));
            }
        }

        unset req.http.cookie;

        // Ban cache by pattern
        if (req.method == "BAN") {
            if (!client.ip ~ local) {
                return(synth(403, "Forbidden."));
            }
            ban("obj.http.x-url ~ " + req.url); # req.url is a regex
            return(synth(200, "Ban added"));
        }

        // Cleaning
        if (req.http.Cookie == "") {
            unset req.http.Cookie;
        }
    }



}

sub vcl_hash {
    hash_data(req.url);
    hash_data(req.http.X-IS-AUTH);
    hash_data(req.http.X-PJAX);
    hash_data(req.http.X-LANG);

//    return (lookup);
}

sub vcl_backend_response {
    set beresp.http.x-url = bereq.url;

    // Allow esi includes for pages
    set beresp.do_esi = true;

    // If no cache
    if (beresp.ttl <= 0s) {
        set beresp.ttl = 2s;
    }

    // Set small cache for 403, 404, 5xx responses
    if (beresp.status == 403 || beresp.status == 404 || beresp.status >= 500) {
    	set beresp.ttl = 3s;
    }

}

sub vcl_deliver {
	unset resp.http.x-url;
}