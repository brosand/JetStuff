from PIL import Image

img = Image.open('stitched_filters_4x4.png')
imgOut = Image.new(mode='RGB',size=(20*img.size[0],20*img.size[1]))

print img.size[0]
print img.size[1]
tmpArray = []
for a in range(img.size[0]):
    if (a % 10 == 0):
        print a
    for b in range(img.size[1]):
        for c in range((a*20),((a+1)*20)):
            for d in range((b*20),((b+1)*20)):

                imgOut.putpixel((c,d), img.getpixel((a,b)))



# w,h = len(data[0],data[1])
# a = np.zeros((h,w,3),dtype=np.uint8)
# for a in range(w):
#     for b in range(h):
#         a[a][b]=data[a][b]
# imgOut =Image.fromarray(a,'RGB')
imgOut.save('expanded.png')