#!/usr/bin/env python

#
# Try to fetch an album info from a youtube file, and then
# cut it up in mp3s using discogs api

# semi standard debian stuff (I guess)
import os
import json
import sys
import urllib
import urlparse
import distutils.spawn
import getopt
import subprocess
import pprint

# funky stuff
import oauth2 as oauth
# pip install oauth2

def usage():
  print "usage"
  print "  couppeu-d-youtube --url=youtube.url"

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["url=", "release="])
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
    if opt[0] == '--release':
      release = opt[1]

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
  
  # get the json info from the youtube page
  infos = json.loads(subprocess.check_output([youtube_dl, "-j", url]))
  # change asdf.mp4 => asdf.mp3
  filename = infos["_filename"][:-1] + "3"
  
  print(pprint.pformat(infos))
  
  # this is mostly for debugging, if the file is there don't redownload it for fun
  if (not os.path.isfile(filename)):
     print("downloading the mp3")
     # os.system(youtube_dl + " -x --audio-format mp3 " + url); 
 
  # great, we have a mp3 to cut up, let's check we can get from discogs

  consumer = oauth.Consumer(consumer_key, consumer_secret)
  client = oauth.Client(consumer)
 
  # pass in your consumer key and secret to the token request URL. Discogs returns
  # an ouath_request_token as well as an oauth request_token secret.
  #resp, content = client.request(request_token_url, 'POST', headers={'User-Agent': user_agent})

  # we terminate if the discogs api does not return an HTTP 200 OK. Something is
  # wrong.
  #if resp['status'] != '200':
  #  sys.exit('Invalid response {0}.'.format(resp['status']))

  #request_token = dict(urlparse.parse_qsl(content))

  #print ' == Request Token == '
  #print '    * oauth_token        = {0}'.format(request_token['oauth_token'])
  #print '    * oauth_token_secret = {0}'.format(request_token['oauth_token_secret'])
  #print

  # Authorize our newly received request_token against the discogs oauth endpoint.
  # Prompt your user to "accept" the terms of your application. The application
  # will act on behalf of their discogs.com account.
  # If the user accepts, discogs displays a key to the user that is used for
  # verification. The key is required in the 2nd phase of authentication.
  #print 'Please browse to the following URL {0}?oauth_token={1}'.format(
  #      authorize_url, request_token['oauth_token'])

  # Waiting for user input
  #accepted = 'n'
  #while accepted.lower() == 'n':
  #  print
  #  accepted = raw_input('Have you authorized me at {0}?oauth_token={1} [y/n] :'.format(
  #     authorize_url, request_token['oauth_token']))

  # request the verification token from the user.
  #oauth_verifier = raw_input('Verification code :')

  # Generate objects that pass the verification key with the oauth token and oauth
  # secret to the discogs access_token_url
  #token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
  #token.set_verifier(oauth_verifier)
  #client = oauth.Client(consumer, token)

  #resp, content = client.request(access_token_url, 'POST', headers={'User-Agent': user_agent})

  # if verification is successful, the discogs oauth API will return an access token
  # and access token secret. This is the final authentication phase. You should persist
  # the oauth_token and the oauth_token_secret to disk, database or some
  # other local store. All further requests to the discogs.com API that require authentication
  # and must be made with these access_tokens.
  access_token = {}
  access_token['oauth_token'] = 'boaRmBPPrxIEDNCVYpiHlprPqOQRpZfQcMfmUsjF'
  access_token['oauth_token_secret'] = 'xvYHcLTpmwaodSryKzYgfbdZwMtEemuLKfhaEqNP'

  # We're now able to fetch an image using the application consumer key and secret,
  # along with the verified oauth token and oauth token for this user.
  token = oauth.Token(key=access_token['oauth_token'],
          secret=access_token['oauth_token_secret'])
  client = oauth.Client(consumer, token)

  # With an active auth token, we're able to reuse the client object and request 
  # additional discogs authenticated endpoints, such as database search.
  print(infos["fulltitle"])
  resp, content = client.request('https://api.discogs.com/releases/' + release,
        headers={'User-Agent': user_agent})

  if resp['status'] != '200':
    sys.exit('Invalid API response {0}.'.format(resp['status']))


  releases = json.loads(content)
  print(pprint.pformat(releases))
  #for release in releases['results']:
  #  print '\n\t== discogs-id {id} =='.format(id=release['id'])
  #  print u'\tTitle\t: {title}'.format(title=release.get('title', 'Unknown'))
  #  print u'\tYear\t: {year}'.format(year=release.get('year', 'Unknown'))
  #  print u'\tLabels\t: {label}'.format(label=', '.join(release.get('label',
  #               ['Unknown'])))
  #  print u'\tCat No\t: {catno}'.format(catno=release.get('catno', 'Unknown'))
  #  print u'\tFormats\t: {fmt}'.format(fmt=', '.join(release.get('format',
  #               ['Unknown']))) 

    
    # https://www.youtube.com/watch?v=CrRFSuuvkmc

main()
