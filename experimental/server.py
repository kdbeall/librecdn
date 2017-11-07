from flask import Flask, request, send_from_directory
import libtorrent as lt
import sys
import time

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path="")

@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("js", path)


#@app.route("/")
#def hello():
#    return "Hello!"

@app.route("/")
def download():
    ses = lt.session()
    ses.listen_on(6881, 6891)
    info = lt.torrent_info('wiki.torrent')
    h = ses.add_torrent({'ti': info, 'save_path': './js'})
    print 'starting', h.name()

    while not h.is_seed():
        s = h.status()
    	state_str = [
        	'queued',
        	'checking',
        	'downloading metadata',
        	'downloading',
        	'finished',
        	'seeding',
        	'allocating',
        	'checking fastresume',
        	]
    	print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' \
        % (s.progress * 100, s.download_rate / 1000, s.upload_rate
           / 1000, s.num_peers, state_str[s.state]),
    	sys.stdout.flush()

    time.sleep(1)

    print h.name(), 'complete'

if __name__ == "__main__":
    app.run()
