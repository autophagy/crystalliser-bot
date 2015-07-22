import sys
import Image
import tweepy
import requests
from StringIO import StringIO
import pickle

#Twice the actual chunk size so we can downscale for anti-aliasing
chunkSize = 20

def crystallise(image):

    #trim the image down to the chunksize
    w,h = image.size
    newW = (w-(w%(chunkSize/2)))
    newH = (h-(h%(chunkSize/2)))
    image = image.crop((0,0,newW,newH))

    w,h = image.size

    image = image.resize((w*2,h*2), Image.ANTIALIAS)
    pixelMap = image.load()

    for x in range(0,w*2,chunkSize):
        for y in range(0,h*2,chunkSize):
            drawTopHalf(x,y,pixelMap)
            drawBottomHalf(x,y,pixelMap)

    image = image.resize((w,h), Image.ANTIALIAS)
    return image

def drawTopHalf(xOrigin, yOrigin, pixelMap):
    rgb = [0,0,0]
    counter = 0
    for y in range(0,chunkSize-1,4):
        for x in range(0,(chunkSize - 1 - y) - (y % 2),4):
            pixel = pixelMap[xOrigin+x,yOrigin+y]
            rgb = [sum(val) for val in zip(rgb,pixel)]
            counter+= 1

    averageChunkRGB = [val / counter for val in rgb]

    #Change all the pixels in the group to this colour
    for y in range(chunkSize-1):
        for x in range((chunkSize - 1 - y) - (y % 2)):
            pixelMap[xOrigin+x,yOrigin+y] = tuple(averageChunkRGB)

def drawBottomHalf(xOrigin, yOrigin, pixelMap):
    rgb = [0,0,0]
    counter = 0
    for y in range(1,chunkSize,4):
        for x in range(((chunkSize - 1 - y) + (y+1)%2),chunkSize,4):
            pixel = pixelMap[xOrigin+x,yOrigin+y]
            rgb = [sum(val) for val in zip(rgb,pixel)]
            counter += 1

    averageChunkRGB = [val / counter for val in rgb]

    #Change all pixels in the group to this colour
    for y in range(1,chunkSize):
        for x in range(((chunkSize - 1 - y) + (y+1)%2),chunkSize):
            pixelMap[xOrigin+x,yOrigin+y] = tuple(averageChunkRGB)


## Twitter API stuff

def getAPI(consumerKey, consumerSecret, accessKey, accessSecret):
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessKey, accessSecret)
    api = tweepy.API(auth)
    return api

def replyToMentions(api, sinceID):
    mentions = api.mentions_timeline(since_id=sinceID)

    #Pickle the first mention as the new sinceID
    pickle.dump(mentions[0].id_str, open("sinceID.p", "wb"))

    for mention in mentions:
        tweetID = mention.id_str
        media = mention.entities.get("media",[{}])[0]
        user = mention.user.screen_name

        ##First download the Image
        resp = requests.get(media["media_url"])
        image = Image.open(StringIO(resp.content))

        #crystallise it
        image = crystallise(image)

        #Save it
        image.save('output.png')

        #Tweet it back at the user
        api.update_with_media('output.png',status='@' + user,in_reply_to_status_id=tweetID)

api = getAPI(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
sinceID = pickle.load(open("sinceID.p", "rb"))
replyToMentions(api, sinceID)
