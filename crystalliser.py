import Image

chunkSize = 10

def drawChunk(xOrigin, yOrigin, pixelMap):
    rgb = [0,0,0]
    counter = 0
    for x in range(xOrigin, xOrigin+chunkSize):
        for y in range(yOrigin, yOrigin+chunkSize):
            #Get average rgb value of pixel
            pixel = pixelMap[x,y]
            rgb = [sum(val) for val in zip(rgb,pixel)]
            counter+= 1

    averageChunkRGB = [val / counter for val in rgb]

    for x in range(xOrigin, xOrigin+chunkSize):
        for y in range(yOrigin, yOrigin+chunkSize):
            pixelMap[x,y] = tuple(averageChunkRGB)


image = Image.open('input.jpg')
pixelMap = image.load()


for x in range(0,image.size[0],chunkSize):
    for y in range(0,image.size[1],chunkSize):
        drawChunk(x,y,pixelMap)

image.save('output.png')
