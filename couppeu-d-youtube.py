#!/usr/bin/env python

#
# Try to fetch an album info from a youtube file, and then
# cut it up in mp3s using discogs api

# semi standard debian stuff (I guess)
import json
import sys
import urllib
import urlparse
import distutils.spawn
import getopt

# funky stuff
import oauth2 as oauth
# pip install oauth2

def usage():
  print "usage"
  print "  couppeu-d-youtube --url=youtube.url"

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["url="])
  except getopt.GetoptError as err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

  youtube_dl = distutils.spawn.find_executable('youtube-dl')

  if (youtube_dl == ""): 
    print "you need to install youtube-dl for this to work ; sudo apt-get install youtube-dl\n"
    sys.exit(3)
  url = ''
  while opts: 
    opt = opts.pop()
    if opt[0] == '--url':
      url = opt[1]

  if url == '': 
    usage() 
    sys.exit(2)

  # Your consumer key and consumer secret generated by discogs when an application is created
  # and registered . See http://www.discogs.com/settings/developers . These credentials
  # are assigned by application and remain static for the lifetime of your discogs application.
  # the consumer details below were generated for the 'discogs-oauth-example' application.
  consumer_key = 'sueGFeWiFjFfFHOQgObA'
  consumer_secret = 'ZFjKiCGmwFaseztBbTYDCMbunVHrePae'

  # The following oauth end-points are defined by discogs.com staff. These static endpoints
  # are called at various stages of oauth handshaking.
  request_token_url = 'https://api.discogs.com/oauth/request_token'
  authorize_url = 'https://www.discogs.com/oauth/authorize'
  access_token_url = 'https://api.discogs.com/oauth/access_token'

  # A user-agent is required with Discogs API requests. Be sure to make your user-agent
  # unique, or you may get a bad response.
  user_agent = 'logiciel-de-marde/66.6'

main()
