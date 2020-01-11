import os

while True:
    image_buffer_directory = 'imageBuffer/'

    recent_1 = []
    recent_2 = []

    images = os.listdir(image_buffer_directory)

    for i in range(len(images)):
        
        f = image_buffer_directory + images[i]
        time = os.path.getmtime(f)

        if i == 0:
            recent_1 = [f, time]
        elif i == 1:
            recent_2 = [f, time]
        else:
            replace = min([recent_1, recent_2], key=lambda x: x[1])
            if replace[1] < time:
                replace[0] = f
                replace[1] = time

    print(recent_1, recent_2)
