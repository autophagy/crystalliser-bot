import Image

#Twice the actual chunk size so we can downscale for anti-aliasing
chunkSize = 20

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

image = Image.open('input.jpg')
w,h = image.size

image = image.resize((w*2,h*2), Image.ANTIALIAS)
pixelMap = image.load()

for x in range(0,w*2,chunkSize):
    for y in range(0,h*2,chunkSize):
        drawTopHalf(x,y,pixelMap)
        drawBottomHalf(x,y,pixelMap)

image = image.resize((w,h), Image.ANTIALIAS)
image.save('output.png')
