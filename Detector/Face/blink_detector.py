from face_landmarks import draw_marks
import time

right_eye = [[37, 41], [38, 40]]
d_right = [0] * 2
left_eye = [[43, 47], [44, 46]]
d_left = [0] * 2
first_interval = time.time() + 10
second_interval = time.time() + 15


def blink_detector(img, shape):
    cnt_right = 0
    cnt_left = 0
    draw_marks(img, shape[36:48])
    if d_right[0] != 0 and time.time() > second_interval:
        for i, (p1, p2) in enumerate(right_eye):
            if d_right[i] - 2 > shape[p2][1] - shape[p1][1]:
                cnt_right += 1
        for i, (p1, p2) in enumerate(left_eye):
            if d_left[i] - 2 > shape[p2][1] - shape[p1][1]:
                cnt_left += 1
        if cnt_right > 1 and cnt_left > 1:
            print("Blinked")
            return True

    if d_right[0] == 0 and time.time() > first_interval:
        for z in range(100):
            for i, (p1, p2) in enumerate(right_eye):
                d_right[i] += shape[p2][1] - shape[p1][1]
            for i, (p1, p2) in enumerate(left_eye):
                d_left[i] += shape[p2][1] - shape[p1][1]
        d_right[:] = [x / 100 for x in d_right]
        d_left[:] = [x / 100 for x in d_left]
        print("Blink please")
